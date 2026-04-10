import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ToastProvider } from './contexts/ToastContext';
import ProtectedRoute from './components/ProtectedRoute';
import DashboardLayout from './layouts/DashboardLayout';
import LandingPage from './pages/LandingPage';
import WarRoom from './pages/WarRoom';
import MyAssignments from './pages/MyAssignments';
import BlueprintStudio from './pages/BlueprintStudio';
import IntelArchive from './pages/IntelArchive';

function App() {
  return (
    <AuthProvider>
      <ToastProvider>
        <BrowserRouter>
          <Routes>
            {/* Public Route */}
            <Route path="/login" element={<LandingPage />} />

            {/* Protected Routes */}
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <DashboardLayout />
                </ProtectedRoute>
              }
            >
              {/* Redirect root to war-room */}
              <Route index element={<Navigate to="/war-room" replace />} />

              {/* Dashboard Pages */}
              <Route path="war-room" element={<WarRoom />} />
              <Route path="my-assignments" element={<MyAssignments />} />
              <Route path="create" element={<BlueprintStudio />} />
              <Route path="archive" element={<IntelArchive />} />
            </Route>

            {/* Catch all - redirect to root */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </ToastProvider>
    </AuthProvider>
  );
}

export default App;
