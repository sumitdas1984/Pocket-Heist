# Testing Guide - Task 24: Final E2E Testing

This guide will help you complete the final end-to-end testing of the Pocket Heist React frontend.

## Quick Start

### Step 1: Run Automated API Tests (Optional but Recommended)

This verifies the backend API is working before manual UI testing.

**On Windows (Git Bash or WSL):**
```bash
cd C:\Users\Sumit Das\experiments\Pocket-Heist\frontend-react
bash test-api.sh
```

**On Mac/Linux:**
```bash
cd ~/path/to/Pocket-Heist/frontend-react
chmod +x test-api.sh
./test-api.sh
```

Expected output: `✓ All API tests passed! Backend is ready for E2E testing.`

---

### Step 2: Start Both Servers

**Terminal 1 - Backend:**
```bash
cd C:\Users\Sumit Das\experiments\Pocket-Heist
uvicorn backend.main:app --reload
```
Wait for: `Uvicorn running on http://127.0.0.1:8000`

**Terminal 2 - React Frontend:**
```bash
cd C:\Users\Sumit Das\experiments\Pocket-Heist\frontend-react
npm run dev
```
Wait for: `Local: http://localhost:5173/`

---

### Step 3: Open E2E Test Checklist

Open the comprehensive test checklist:
```
C:\Users\Sumit Das\experiments\Pocket-Heist\frontend-react\E2E_TEST_CHECKLIST.md
```

Or view it in VS Code/your editor for easy reference.

---

### Step 4: Execute Manual Tests

Follow the checklist systematically:

1. **Test Suite 1: Authentication** (15 min)
   - Register, login, logout
   - Protected routes

2. **Test Suite 2: Heist Management** (25 min)
   - Create, view, search, abort heists
   - Archive functionality

3. **Test Suite 3: UI/UX Polish** (10 min)
   - Loading states, toasts, hover effects

4. **Test Suite 4: Responsive Design** (15 min)
   - Desktop, tablet, mobile views

5. **Test Suite 5: Cross-Browser** (15 min - optional)
   - Chrome/Edge, Firefox, Safari

6. **Test Suite 6: Edge Cases** (10 min)
   - Error handling, validation

---

## Testing Tips

### Browser DevTools Usage

**Open DevTools:** F12 or Right-click → Inspect

**Key Tabs:**
- **Console** - Check for errors (should be clean)
- **Network** - Monitor API calls
- **Application > Local Storage** - Verify JWT storage
- **Device Toolbar** - Test responsive design (Ctrl+Shift+M)

### What to Look For

✅ **Good Signs:**
- No console errors
- Toast notifications appear and dismiss
- Smooth animations
- Data loads correctly
- Forms submit and clear

❌ **Red Flags:**
- Console errors (especially TypeErrors, network errors)
- White screen / crash
- API calls fail (check CORS)
- No redirect after login
- Broken images/icons

---

## Quick Test (5 minutes)

If you're short on time, do this minimal test:

1. ✅ Register new user
2. ✅ Login
3. ✅ Create heist
4. ✅ View heist in War Room
5. ✅ Abort heist
6. ✅ Check archive
7. ✅ Logout
8. ✅ Verify protected route redirect

If all 8 pass → Core functionality works!

---

## Troubleshooting

### Backend Connection Issues

**Symptom:** API calls fail, CORS errors in console

**Fix:**
```bash
# Check backend is running
curl http://127.0.0.1:8000

# Should return: {"message":"Welcome to Pocket Heist API"}
```

If not running:
```bash
cd C:\Users\Sumit Das\experiments\Pocket-Heist
uvicorn backend.main:app --reload
```

---

### React App Not Loading

**Symptom:** Blank page, Vite error

**Fix:**
```bash
# Ensure dependencies installed
cd frontend-react
npm install

# Restart dev server
npm run dev
```

---

### Authentication Not Working

**Symptom:** Login succeeds but redirects to login again

**Fix:**
1. Open DevTools > Application > Local Storage
2. Check for `jwt_token` and `user` keys
3. If missing, check browser console for errors
4. Verify backend JWT secret is consistent

---

### Toast Notifications Not Appearing

**Symptom:** Actions complete but no toast feedback

**Fix:**
1. Check console for errors in ToastContext
2. Verify ToastProvider wraps App in App.jsx
3. Check toast container is rendering (should see `<div class="fixed top-4 right-4...">`)

---

## Checklist Progress Tracker

Mark these off as you complete each test suite:

- [ ] **Setup Complete** (Both servers running)
- [ ] **Suite 1: Authentication** (4 tests)
- [ ] **Suite 2: Heist Management** (9 tests)
- [ ] **Suite 3: UI/UX Polish** (4 tests)
- [ ] **Suite 4: Responsive Design** (3 tests)
- [ ] **Suite 5: Cross-Browser** (3 browsers)
- [ ] **Suite 6: Edge Cases** (5 tests)
- [ ] **Suite 7: Performance** (2 tests)

**Total Tests:** ~30 test cases

---

## Reporting Results

After testing, document:

### ✅ What Works
- List all passing features
- Note any exceptional performance

### ⚠️ Known Issues
- Document any bugs found
- Use bug template in E2E_TEST_CHECKLIST.md

### 📊 Browser Compatibility
- Chrome: ✅/❌
- Firefox: ✅/❌
- Safari: ✅/❌
- Edge: ✅/❌

---

## Task 24 Completion Criteria

Task 24 is **COMPLETE** when:

✅ All critical tests pass (see checklist)  
✅ No console errors on happy path  
✅ Authentication flow works  
✅ CRUD operations work (Create, Read, Abort)  
✅ Responsive design verified (mobile, desktop)  
✅ At least 2 browsers tested  

---

## Next Steps After Testing

Once Task 24 passes:

1. ✅ Mark Phase 2 as complete
2. 🚀 Ready for production deployment
3. 📝 Update project documentation
4. 🎉 Celebrate successful React migration!

---

**Good luck with testing! 🧪**

If you encounter issues, refer to:
- `E2E_TEST_CHECKLIST.md` for detailed test steps
- `README.md` for setup instructions
- `CLAUDE.md` for architecture guidance
