import api from './api';

/**
 * Authentication Service
 * Handles user registration, login, logout, and token management
 */

/**
 * Register a new user
 * @param {string} username - Username (operative codename)
 * @param {string} password - Password (min 8 characters)
 * @returns {Promise<Object>} User data
 */
export const register = async (username, password) => {
  try {
    const response = await api.post('/auth/register', {
      username,
      password,
    });
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Registration failed',
    };
  }
};

/**
 * Login user and store JWT token
 * @param {string} username - Username
 * @param {string} password - Password
 * @returns {Promise<Object>} Login result with token
 */
export const login = async (username, password) => {
  try {
    const response = await api.post('/auth/login', null, {
      params: { username, password },
    });

    const { access_token, token_type } = response.data;

    // Store token in localStorage
    localStorage.setItem('jwt_token', access_token);

    // Store user info
    localStorage.setItem('user', JSON.stringify({ username }));

    return {
      success: true,
      data: {
        token: access_token,
        tokenType: token_type,
        user: { username },
      },
    };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Invalid credentials',
    };
  }
};

/**
 * Logout user and clear stored data
 */
export const logout = () => {
  localStorage.removeItem('jwt_token');
  localStorage.removeItem('user');
  window.location.href = '/login';
};

/**
 * Get stored JWT token
 * @returns {string|null} JWT token or null
 */
export const getToken = () => {
  return localStorage.getItem('jwt_token');
};

/**
 * Get stored user data
 * @returns {Object|null} User object or null
 */
export const getUser = () => {
  const userStr = localStorage.getItem('user');
  if (!userStr) return null;

  try {
    return JSON.parse(userStr);
  } catch {
    return null;
  }
};

/**
 * Check if user is authenticated
 * @returns {boolean} True if user has valid token
 */
export const isAuthenticated = () => {
  const token = getToken();
  return !!token;
};

export default {
  register,
  login,
  logout,
  getToken,
  getUser,
  isAuthenticated,
};
