# Pocket Heist - Simple Cloud Deployment Plan

## Recommended Approach: Render.com (All-in-One)

**Why Render?**
- Free tier available for both frontend and backend
- Zero DevOps complexity
- Automatic HTTPS
- Built-in PostgreSQL database
- Easy GitHub integration

---

## Architecture Overview

```
User → Render Static Site (React) → Render Web Service (FastAPI) → Render PostgreSQL
        [CDN + HTTPS]                [Auto-scaling]                  [Managed DB]
```

---

## Required Changes

### 1. Database Migration (SQLite → PostgreSQL)

**Backend changes needed:**

```bash
# Add to backend/requirements.txt
psycopg2-binary==2.9.9
```

**Update `backend/database.py`:**
```python
import os
from sqlalchemy import create_engine

# Use PostgreSQL in production, SQLite in development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./heists.db"  # Fallback for local dev
)

# Render provides DATABASE_URL, but uses 'postgres://' which needs to be 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
```

### 2. Environment Variables

**Backend `.env` (for Render):**
```bash
DATABASE_URL=<provided-by-render>
SECRET_KEY=<generate-random-64-char-string>
ALLOWED_ORIGINS=https://your-app.onrender.com
```

**Frontend `.env.production`:**
```bash
VITE_API_BASE_URL=https://your-backend.onrender.com
```

---

## Deployment Steps

### Step 1: Prepare Repository

1. **Create `render.yaml` in project root:**

```yaml
services:
  # Backend API
  - type: web
    name: pocket-heist-api
    runtime: python
    buildCommand: "pip install -r backend/requirements.txt"
    startCommand: "uvicorn backend.main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: pocket-heist-db
          property: connectionString
      - key: ALLOWED_ORIGINS
        value: https://pocket-heist.onrender.com

  # Frontend Static Site
  - type: web
    name: pocket-heist-frontend
    runtime: static
    buildCommand: "cd frontend-react && npm install && npm run build"
    staticPublishPath: frontend-react/dist
    envVars:
      - key: VITE_API_BASE_URL
        value: https://pocket-heist-api.onrender.com

databases:
  - name: pocket-heist-db
    databaseName: pocket_heist
    user: pocket_heist_user
```

2. **Push to GitHub** (if not already done)

### Step 2: Deploy to Render

1. Go to [render.com](https://render.com) and sign up
2. Click **"New" → "Blueprint"**
3. Connect your GitHub repository
4. Select `render.yaml`
5. Click **"Apply"**

Render will automatically:
- Create PostgreSQL database
- Deploy backend API
- Build and deploy React frontend
- Set up HTTPS certificates

### Step 3: Initialize Database

After deployment, run migrations:

```bash
# SSH into Render backend service (from Render dashboard)
python -c "from backend.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

Or add this to `backend/main.py` startup:
```python
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
```

---

## Cost Estimation

### Option 1: Free Tier (Render)

| Service | Plan | Cost | Limitations |
|---------|------|------|-------------|
| Backend (Web Service) | Free | **$0/month** | Spins down after 15 min inactivity (cold starts ~30s) |
| Frontend (Static Site) | Free | **$0/month** | 100 GB bandwidth/month |
| PostgreSQL | Free | **$0/month** | 90-day expiration, 1 GB storage |
| **Total** | | **$0/month** | Good for MVP/testing |

**Limitations:**
- Backend sleeps after inactivity (first request takes 30s)
- Database expires after 90 days (must upgrade or re-create)
- Not suitable for production traffic

### Option 2: Paid Tier (Production-Ready)

| Service | Plan | Cost | Features |
|---------|------|------|----------|
| Backend | Starter | **$7/month** | Always on, 512 MB RAM, auto-scaling |
| Frontend | Free | **$0/month** | 100 GB bandwidth |
| PostgreSQL | Starter | **$7/month** | 1 GB storage, daily backups |
| **Total** | | **$14/month** | Production-ready |

**Benefits:**
- No cold starts (always-on backend)
- Persistent database with backups
- Custom domain support
- 99.9% uptime SLA

### Option 3: Scaled Production

| Service | Plan | Cost | Features |
|---------|------|------|----------|
| Backend | Pro | **$25/month** | 2 GB RAM, faster CPU, dedicated resources |
| Frontend | Free | **$0/month** | 100 GB bandwidth |
| PostgreSQL | Standard | **$20/month** | 10 GB storage, point-in-time recovery |
| **Total** | | **$45/month** | High-traffic production |

---

## Alternative: Railway.app

**Pros:**
- $5 free credit/month (good for hobbyist projects)
- Simpler UI than Render
- Better developer experience

**Cons:**
- No free tier after credits run out
- Slightly more expensive (~$10-15/month baseline)

**Quick setup:**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

---

## Alternative: Vercel + Render

**Frontend (Vercel):**
- Free tier: Unlimited bandwidth, automatic deployments
- Best-in-class frontend hosting

**Backend (Render):**
- Free or $7/month web service
- $7/month PostgreSQL

**Total:** $0-14/month

---

## Recommended Path

### For Testing/MVP:
**Render Free Tier** - $0/month
- Accept cold starts
- Re-create database every 90 days
- Validate product-market fit

### For Production:
**Render Paid Tier** - $14/month
- Always-on backend
- Persistent database with backups
- Custom domain (pocketheist.com)

### For Scale (1000+ users):
**Render Pro** - $45/month
- Dedicated resources
- Auto-scaling
- Advanced monitoring

---

## Post-Deployment Checklist

- [ ] Update CORS origins in `backend/main.py`
- [ ] Set strong `SECRET_KEY` (64+ random characters)
- [ ] Enable HTTPS-only (automatic on Render)
- [ ] Set up custom domain (optional)
- [ ] Configure database backups
- [ ] Add health check endpoint (`/health`)
- [ ] Set up monitoring/logging
- [ ] Test authentication flow end-to-end
- [ ] Verify deadline-based heist filtering works
- [ ] Load test with 100+ concurrent users

---

## Security Notes

1. **Never commit `.env` files** - use Render's environment variables
2. **Rotate SECRET_KEY** every 90 days
3. **Enable rate limiting** (add to FastAPI with `slowapi`)
4. **Use HTTPS-only** (automatic on Render)
5. **Sanitize user inputs** (already done via Pydantic)

---

## Rollback Plan

If deployment fails:
1. Keep local SQLite version running
2. Export users/heists from PostgreSQL
3. Revert to local development
4. Debug issues in staging environment

---

## Next Steps

1. **Add PostgreSQL support** (update `backend/database.py`)
2. **Add to `requirements.txt`:** `psycopg2-binary`
3. **Test locally with PostgreSQL:**
   ```bash
   docker run -e POSTGRES_PASSWORD=test -p 5432:5432 postgres
   DATABASE_URL=postgresql://postgres:test@localhost/heists uvicorn backend.main:app
   ```
4. **Push to GitHub**
5. **Deploy via Render Blueprint**
6. **Test end-to-end**

---

## Estimated Timeline

- **Code changes:** 30 minutes (database.py + requirements.txt)
- **Render setup:** 15 minutes (create account, connect repo)
- **Initial deployment:** 10 minutes (automatic)
- **Testing:** 30 minutes (E2E validation)

**Total:** ~90 minutes from start to production
