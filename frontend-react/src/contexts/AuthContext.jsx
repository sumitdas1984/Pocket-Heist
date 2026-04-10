import { createContext, useContext, useState, useEffect } from 'react';
import * as authService from '../services/auth';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize auth state from localStorage on mount
  useEffect(() => {
    const storedToken = authService.getToken();
    const storedUser = authService.getUser();

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(storedUser);
    }

    setIsLoading(false);
  }, []);

  /**
   * Login user
   */
  const login = async (username, password) => {
    const result = await authService.login(username, password);

    if (result.success) {
      setToken(result.data.token);
      setUser(result.data.user);
      return { success: true };
    }

    return { success: false, error: result.error };
  };

  /**
   * Register new user
   */
  const register = async (username, password) => {
    const result = await authService.register(username, password);
    return result;
  };

  /**
   * Logout user
   */
  const logout = () => {
    authService.logout();
    setToken(null);
    setUser(null);
  };

  /**
   * Check if user is authenticated
   */
  const isAuthenticated = () => {
    return !!token && !!user;
  };

  const value = {
    user,
    token,
    isLoading,
    isAuthenticated: isAuthenticated(),
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

/**
 * Custom hook to use auth context
 */
export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }

  return context;
};

export default AuthContext;
