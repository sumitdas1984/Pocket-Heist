# Pocket Heist - React Frontend

Production-ready React frontend for the Pocket Heist gamified task management application. Built with React 18, Vite, Tailwind CSS, and Axios.

## Features

- **Authentication** - JWT-based login/register with localStorage persistence
- **Heist Management** - Create, view, abort, and archive missions
- **Real-time Search** - Filter heists across all pages
- **Responsive Design** - Mobile-first UI with Tailwind breakpoints
- **Toast Notifications** - Non-blocking success/error messages
- **Skeleton Loaders** - Smooth loading states
- **Dark Theme** - Spy-themed UI with gold accents

## Tech Stack

- **React 18** - Component-based UI library
- **Vite** - Fast development server and build tool
- **React Router v6** - Client-side routing
- **Axios** - HTTP client with interceptors
- **Tailwind CSS v3.4** - Utility-first CSS framework
- **date-fns** - Date formatting and manipulation
- **Lucide React** - Icon library

## Prerequisites

- Node.js 18+ and npm
- Backend API running at `http://127.0.0.1:8000` (see main project README)

## Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Update `.env` if your backend runs on a different URL:
   ```
   VITE_API_BASE_URL=http://127.0.0.1:8000
   ```

## Development

1. **Start the backend API** (in separate terminal)
   ```bash
   # From project root
   uvicorn backend.main:app --reload
   ```

2. **Start the React dev server**
   ```bash
   npm run dev
   ```

3. **Open your browser**
   ```
   http://localhost:5173
   ```

The dev server features:
- Hot Module Replacement (HMR) - instant updates
- Fast Refresh - preserves component state
- Error overlay - helpful debugging

## Production Build

1. **Create optimized build**
   ```bash
   npm run build
   ```
   
   This generates a production-ready bundle in `dist/`:
   - Minified JavaScript and CSS
   - Tree-shaken dependencies
   - Optimized assets

2. **Test production build locally**
   ```bash
   npm run preview
   ```
   
   Opens at `http://localhost:4173`

3. **Deploy**
   - Upload `dist/` folder to your hosting service
   - Ensure backend CORS allows your production domain
   - Set `VITE_API_BASE_URL` to production backend URL

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── HeistCard.jsx           # Individual heist card
│   ├── HeistCardSkeleton.jsx   # Loading skeleton
│   ├── HeistDetailsModal.jsx   # Full heist details modal
│   ├── HeistGrid.jsx           # Responsive grid layout
│   ├── ProtectedRoute.jsx      # Auth guard for routes
│   └── Toast.jsx               # Toast notification
│
├── contexts/            # React Context providers
│   ├── AuthContext.jsx         # Authentication state
│   └── ToastContext.jsx        # Toast notifications
│
├── layouts/             # Page layouts
│   └── DashboardLayout.jsx     # Main dashboard with sidebar
│
├── pages/               # Route pages
│   ├── LandingPage.jsx         # Login/Register
│   ├── WarRoom.jsx             # Active heists
│   ├── MyAssignments.jsx       # User's created heists
│   ├── BlueprintStudio.jsx     # Create heist form
│   └── IntelArchive.jsx        # Archived heists
│
├── services/            # API client layer
│   ├── api.js                  # Axios instance
│   ├── auth.js                 # Auth endpoints
│   └── heists.js               # Heist endpoints
│
├── App.jsx              # Root component with routing
├── main.jsx             # React entry point
└── index.css            # Tailwind imports
```

## Routes

| Route             | Page              | Access    | Description                    |
|-------------------|-------------------|-----------|--------------------------------|
| `/login`          | LandingPage       | Public    | Login and registration         |
| `/war-room`       | WarRoom           | Protected | Active heists                  |
| `/my-assignments` | MyAssignments     | Protected | User's created heists          |
| `/create`         | BlueprintStudio   | Protected | Create new heist               |
| `/archive`        | IntelArchive      | Protected | Expired/aborted heists         |

## API Integration

The frontend communicates with the FastAPI backend via REST API:

**Base URL:** `http://127.0.0.1:8000` (configurable via `.env`)

**Authentication:**
- JWT tokens stored in `localStorage`
- Axios request interceptor auto-injects token
- Axios response interceptor handles 401 errors

**Endpoints Used:**
- `POST /auth/register` - Create new user
- `POST /auth/login` - Authenticate user
- `GET /heists` - List active heists
- `POST /heists` - Create new heist
- `GET /heists/mine` - List user's heists
- `GET /heists/archive` - List archived heists
- `PATCH /heists/{id}/abort` - Abort heist

## Environment Variables

| Variable              | Default                    | Description           |
|-----------------------|----------------------------|-----------------------|
| `VITE_API_BASE_URL`   | `http://127.0.0.1:8000`    | Backend API base URL  |

**Note:** All Vite environment variables must be prefixed with `VITE_` to be exposed to the client.

## Backend CORS Configuration

Ensure your backend (`backend/main.py`) includes the React dev server URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",
        # Add production domain here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Troubleshooting

**Issue:** API requests fail with CORS error
- **Fix:** Verify backend CORS includes `http://localhost:5173`

**Issue:** Authentication not persisting on refresh
- **Fix:** Check browser localStorage for `jwt_token` and `user` keys

**Issue:** Build errors with Tailwind
- **Fix:** Ensure `tailwindcss@^3.4.0` is installed (not v4)

**Issue:** Environment variables not working
- **Fix:** Restart dev server after changing `.env`, ensure `VITE_` prefix

## Scripts

| Command           | Description                          |
|-------------------|--------------------------------------|
| `npm run dev`     | Start development server (port 5173) |
| `npm run build`   | Create production build              |
| `npm run preview` | Preview production build (port 4173) |
| `npm run lint`    | Run ESLint                           |

## Design System

**Colors:**
- Background: `#0a0a0c` (dark-bg)
- Cards: `#111114` (dark-card)
- Accent: `#f59e0b` (gold)
- Borders: `#1e293b` (slate-800)

**Typography:**
- Font: Inter (system fallback)
- Headlines: Bold, tight tracking
- Labels: Uppercase, wide tracking

**Components:**
- Rounded corners: `rounded-xl` / `rounded-2xl`
- Shadows: Subtle with gold glow on hover
- Animations: Smooth transitions, fade-ins

## Contributing

When adding new features:
1. Follow existing component patterns
2. Use Tailwind utility classes (avoid custom CSS)
3. Implement loading states with skeletons
4. Add error handling with toast notifications
5. Test responsiveness at all breakpoints

## License

Part of the Pocket Heist project.
