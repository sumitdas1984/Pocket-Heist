# End-to-End Testing Checklist - Pocket Heist React Frontend

This checklist provides comprehensive manual testing steps to verify the React frontend works correctly end-to-end.

## Pre-Testing Setup

### 1. Start Backend Server
```bash
# Terminal 1 - From project root
cd C:\Users\Sumit Das\experiments\Pocket-Heist
uvicorn backend.main:app --reload
```
✅ Verify backend is running at: `http://127.0.0.1:8000`  
✅ Open API docs to confirm: `http://127.0.0.1:8000/docs`

### 2. Start React Frontend
```bash
# Terminal 2 - From frontend-react directory
cd C:\Users\Sumit Das\experiments\Pocket-Heist\frontend-react
npm run dev
```
✅ Verify React app is running at: `http://localhost:5173`

---

## Test Suite 1: Authentication Flow

### Test 1.1: User Registration
**Steps:**
1. Navigate to `http://localhost:5173`
2. Should redirect to `/login` (LandingPage)
3. Click "Apply for New Credentials" button at bottom
4. Fill in registration form:
   - Operative Codename: `test_agent_001`
   - Set Encryption Key: `SecurePass123`
   - Confirm Encryption Key: `SecurePass123`
5. Click "Register" button

**Expected Results:**
- ✅ Green success toast appears: "Account created! You can now authenticate."
- ✅ Form clears after 2 seconds
- ✅ Switches to login view automatically
- ✅ No errors in browser console

**If Failed:**
- Check backend logs for errors
- Verify CORS is configured correctly
- Check Network tab in browser DevTools

---

### Test 1.2: User Login
**Steps:**
1. On login screen, enter credentials:
   - Operative Codename: `test_agent_001`
   - Access Credentials: `SecurePass123`
2. Click "Establish Connection" button

**Expected Results:**
- ✅ Redirects to `/war-room` (War Room page)
- ✅ Sidebar shows username "test_agent_001"
- ✅ JWT token stored in localStorage (check DevTools > Application > Local Storage)
- ✅ Header shows "War Room" title
- ✅ Page displays empty state: "📭 No active heists. Time to plan a new mission!"

---

### Test 1.3: Protected Route Access
**Steps:**
1. While logged in, manually navigate to `/login` in address bar
2. Observe behavior

**Expected Results:**
- ✅ Should show login page (no automatic redirect since already logged in)
- ✅ Can navigate back to dashboard using browser back button

---

### Test 1.4: Logout
**Steps:**
1. Click "Logout" button in sidebar (bottom)
2. Confirm logout

**Expected Results:**
- ✅ Redirects to `/login`
- ✅ localStorage cleared (check DevTools)
- ✅ Attempting to navigate to `/war-room` redirects back to `/login`

---

## Test Suite 2: Heist Management

### Test 2.1: Create New Heist
**Steps:**
1. Login as `test_agent_001`
2. Navigate to "Blueprint Studio" from sidebar (or `/create`)
3. Fill in heist creation form:
   - Mission Name: `Operation Coffee Heist`
   - Target Sector: `Kitchen Pantry`
   - Difficulty: `Medium`
   - Assign Operative: `test_agent_001`
   - Intel Briefing: `Infiltrate the kitchen and secure the last bag of premium coffee beans before the morning rush.`
4. Click "Initialize Operation" button

**Expected Results:**
- ✅ Success toast appears: "Mission launched: Operation Coffee Heist"
- ✅ Form clears
- ✅ Redirects to War Room after 2 seconds
- ✅ New heist appears in War Room list

---

### Test 2.2: View Heist in War Room
**Steps:**
1. Navigate to "War Room" (should already be there)
2. Verify the created heist appears

**Expected Results:**
- ✅ Heist card displays:
  - Status badge: "ACTIVE" (green)
  - Title: "Operation Coffee Heist"
  - Target: "Kitchen Pantry"
  - Difficulty: "Medium"
  - Operative: "test_agent_001"
  - Time Remaining: "in about 3 hours"
  - ID badge (e.g., #0001)
- ✅ Abort button visible (since you're the creator)
- ✅ "View Intel" button clickable

---

### Test 2.3: View Heist Details Modal
**Steps:**
1. Click "View Intel" button on the heist card

**Expected Results:**
- ✅ Modal opens with backdrop blur
- ✅ Modal displays:
  - Status badge: "ACTIVE"
  - Difficulty badge: "MEDIUM"
  - Full title and ID
  - Intel Briefing section with description
  - Mission Details grid showing:
    - Target Sector
    - Assigned Operative
    - Mission Creator (highlighted in gold)
    - Created timestamp
  - Deadline section with countdown
  - "Abort Mission" button at bottom
- ✅ Click outside modal → closes
- ✅ Click X button → closes
- ✅ Pressing ESC key → closes (optional, test manually)

---

### Test 2.4: View in My Assignments
**Steps:**
1. Navigate to "My Assignments" from sidebar
2. Check if heist appears

**Expected Results:**
- ✅ Shows same heist card
- ✅ Status tabs show: All (1), Active (1), Expired (0), Aborted (0)
- ✅ Abort button visible
- ✅ Clicking "Active" tab filters correctly

---

### Test 2.5: Search Functionality
**Steps:**
1. In War Room, type "Coffee" in search bar
2. Press Enter or wait for debounce

**Expected Results:**
- ✅ Search indicator appears: "Searching: Coffee (1 result)"
- ✅ Heist card still visible
- ✅ Search for "Invalid" → shows "No heists found matching 'Invalid'."

**Test in My Assignments:**
- ✅ Same search behavior works

---

### Test 2.6: Abort Heist
**Steps:**
1. In War Room, click "Abort" button on heist card
2. Confirm in browser alert dialog

**Expected Results:**
- ✅ Confirmation dialog: "Are you sure you want to abort 'Operation Coffee Heist'?"
- ✅ Click OK
- ✅ Success toast: "Mission aborted successfully"
- ✅ Heist disappears from War Room
- ✅ Navigate to My Assignments → Status shows "Aborted"

---

### Test 2.7: Abort from Details Modal
**Steps:**
1. Create another heist (follow Test 2.1)
2. Open heist details modal
3. Click "Abort Mission" button at bottom
4. Confirm in dialog

**Expected Results:**
- ✅ Info toast: "Aborting mission..."
- ✅ Modal closes
- ✅ Success toast: "Mission aborted successfully"
- ✅ Heist updates to "Aborted" status

---

### Test 2.8: View in Archive
**Steps:**
1. Navigate to "Intel Archive" from sidebar
2. Check aborted heists appear

**Expected Results:**
- ✅ Both aborted heists appear
- ✅ Status tabs show: All (2), Expired (0), Aborted (2)
- ✅ No abort button (archive is read-only)
- ✅ Status badge shows "ABORTED" (rose color)
- ✅ Filter by "Aborted" tab works

---

### Test 2.9: Create Multiple Heists
**Steps:**
1. Create 3 more heists with different data:
   - **Heist 2:** Name: "Desk Swap", Target: "Marketing Floor", Difficulty: "Easy", Assignee: "agent_002"
   - **Heist 3:** Name: "Stapler Liberation", Target: "Supply Closet", Difficulty: "Hard", Assignee: "test_agent_001"
   - **Heist 4:** Name: "Phantom Printer", Target: "IT Department", Difficulty: "Legendary", Assignee: "agent_003"

**Expected Results:**
- ✅ All heists create successfully
- ✅ War Room shows 3 active heists (grid layout)
- ✅ My Assignments shows 5 total (3 active, 2 aborted)
- ✅ Different difficulty colors display correctly:
  - Easy: green
  - Medium: yellow
  - Hard: orange
  - Legendary: rose/red

---

## Test Suite 3: UI/UX Polish

### Test 3.1: Loading States
**Steps:**
1. Refresh War Room page
2. Observe loading behavior

**Expected Results:**
- ✅ Shows 3 skeleton loader cards with pulsing animation
- ✅ Skeletons match HeistCard structure
- ✅ Smooth transition to actual cards when loaded

---

### Test 3.2: Toast Notifications
**Steps:**
1. Test different toast types:
   - Create heist → success toast (green)
   - Try invalid login → error toast (rose)
   - Abort heist → success toast

**Expected Results:**
- ✅ Toast slides in from right
- ✅ Auto-dismisses after 3 seconds
- ✅ Can manually close with X button
- ✅ Multiple toasts stack vertically
- ✅ Correct icons: CheckCircle (success), AlertCircle (error)

---

### Test 3.3: Hover Effects
**Steps:**
1. Hover over various interactive elements

**Expected Results:**
- ✅ Heist cards: border glows gold on hover
- ✅ Buttons: smooth color transitions
- ✅ Sidebar items: background highlights on hover
- ✅ "View Intel" button: smooth transition

---

### Test 3.4: Empty States
**Steps:**
1. Check empty states in different views:
   - War Room with no active heists
   - My Assignments with filters that return no results
   - Intel Archive with no archived heists

**Expected Results:**
- ✅ Each shows appropriate emoji and message
- ✅ Messages are contextual (e.g., "No active heists" vs "No aborted heists")

---

## Test Suite 4: Responsive Design

### Test 4.1: Desktop View (1920x1080)
**Steps:**
1. Set browser window to desktop size
2. Navigate through all pages

**Expected Results:**
- ✅ Sidebar stays open
- ✅ Heist grid shows 3 columns (lg:grid-cols-3)
- ✅ Header search bar full width
- ✅ Modal fits comfortably with margins

---

### Test 4.2: Tablet View (768px)
**Steps:**
1. Resize browser to ~768px width (or use DevTools Device Toolbar)
2. Navigate through all pages

**Expected Results:**
- ✅ Heist grid shows 2 columns (md:grid-cols-2)
- ✅ Sidebar remains functional
- ✅ Forms stack properly in Blueprint Studio
- ✅ Modal scrollable if needed

---

### Test 4.3: Mobile View (375px)
**Steps:**
1. Resize browser to mobile size (375px) or use DevTools
2. Test all pages

**Expected Results:**
- ✅ Heist grid shows 1 column
- ✅ Sidebar adapts (may need to collapse, check design)
- ✅ Search bar responsive
- ✅ Forms single column
- ✅ Modal full screen on mobile
- ✅ Touch targets large enough (buttons, links)

---

## Test Suite 5: Cross-Browser Testing

### Test 5.1: Chrome/Edge (Chromium)
- ✅ Complete Test Suites 1-4
- ✅ No console errors
- ✅ All features work

### Test 5.2: Firefox
- ✅ Complete Test Suites 1-4
- ✅ Check CSS compatibility (especially animations)
- ✅ Verify backdrop-blur works

### Test 5.3: Safari (if available on Mac)
- ✅ Complete Test Suites 1-4
- ✅ Check webkit-specific issues
- ✅ Verify date formatting works correctly

---

## Test Suite 6: Edge Cases & Error Handling

### Test 6.1: Invalid Login
**Steps:**
1. Try logging in with wrong password

**Expected Results:**
- ✅ Error toast: "Authentication failed. Invalid credentials."
- ✅ Stays on login page
- ✅ No redirect

---

### Test 6.2: Duplicate Username Registration
**Steps:**
1. Try registering with existing username `test_agent_001`

**Expected Results:**
- ✅ Error toast: "Username already exists" or similar backend error
- ✅ Form stays filled
- ✅ No redirect

---

### Test 6.3: Form Validation
**Steps:**
1. In Blueprint Studio, try submitting empty form
2. Try password too short in registration

**Expected Results:**
- ✅ Validation prevents submission
- ✅ Error toast: "Blueprint incomplete. Fill all required fields."
- ✅ HTML5 validation highlights required fields

---

### Test 6.4: Backend Offline
**Steps:**
1. Stop backend server
2. Try creating a heist

**Expected Results:**
- ✅ Error toast with network error message
- ✅ App doesn't crash
- ✅ Retry button in error states works when backend restored

---

### Test 6.5: Token Expiry (24 hour test - optional)
**Steps:**
1. Login and wait 24 hours (or mock expired token in localStorage)

**Expected Results:**
- ✅ Next API call gets 401
- ✅ Axios interceptor catches it
- ✅ localStorage cleared
- ✅ Redirects to `/login`

---

## Test Suite 7: Performance

### Test 7.1: Page Load Speed
**Steps:**
1. Open DevTools > Network tab
2. Hard refresh War Room page

**Expected Results:**
- ✅ Initial load < 2 seconds
- ✅ CSS and JS bundles load quickly
- ✅ No render-blocking resources

---

### Test 7.2: Large Dataset
**Steps:**
1. Create 20+ heists
2. Test scrolling and filtering

**Expected Results:**
- ✅ Grid renders smoothly
- ✅ Search filters instantly
- ✅ No lag or jank

---

## Final Checklist Summary

### Critical Tests (Must Pass)
- [ ] User registration works
- [ ] User login works
- [ ] User logout works
- [ ] Create heist works
- [ ] View heist in War Room works
- [ ] View heist in My Assignments works
- [ ] Abort heist works
- [ ] Aborted heist appears in Archive
- [ ] Toast notifications appear
- [ ] Loading skeletons show
- [ ] Search/filter works
- [ ] Mobile responsive (1 column grid)

### Nice-to-Have Tests
- [ ] Desktop 3-column grid
- [ ] Tablet 2-column grid
- [ ] Cross-browser (Chrome, Firefox, Safari)
- [ ] Hover effects smooth
- [ ] Modal animations smooth
- [ ] Error handling graceful

---

## Bug Reporting Template

If you find issues, document them as:

**Bug Title:** [Short description]  
**Steps to Reproduce:**
1. Step 1
2. Step 2

**Expected Behavior:** What should happen  
**Actual Behavior:** What actually happened  
**Browser/OS:** Chrome 120 / Windows 11  
**Console Errors:** [Paste any errors]  
**Screenshots:** [If applicable]

---

## Post-Testing

Once all tests pass:
1. ✅ Mark Task 24 as complete
2. ✅ Document any known issues
3. ✅ Ready for production deployment!

---

**Happy Testing! 🎯**
