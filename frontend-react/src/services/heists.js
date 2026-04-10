import api from './api';

/**
 * Heist Management Service
 * Handles all heist-related API calls
 */

/**
 * List all active heists (War Room)
 * @returns {Promise<Object>} List of active heists
 */
export const listActiveHeists = async () => {
  try {
    const response = await api.get('/heists');
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to fetch active heists',
      data: [],
    };
  }
};

/**
 * List heists created by current user (My Assignments)
 * @returns {Promise<Object>} List of user's heists
 */
export const listMyHeists = async () => {
  try {
    const response = await api.get('/heists/mine');
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to fetch your heists',
      data: [],
    };
  }
};

/**
 * List archived heists (Expired/Aborted)
 * @returns {Promise<Object>} List of archived heists
 */
export const listArchiveHeists = async () => {
  try {
    const response = await api.get('/heists/archive');
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to fetch archive',
      data: [],
    };
  }
};

/**
 * Get heist by ID
 * @param {number} id - Heist ID
 * @returns {Promise<Object>} Heist details
 */
export const getHeist = async (id) => {
  try {
    const response = await api.get(`/heists/${id}`);
    return { success: true, data: response.data };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Heist not found',
      data: null,
    };
  }
};

/**
 * Create a new heist
 * @param {Object} heistData - Heist data
 * @param {string} heistData.title - Mission name
 * @param {string} heistData.target - Target sector
 * @param {string} heistData.difficulty - Difficulty level
 * @param {string} heistData.assignee_username - Operative to assign
 * @param {string} heistData.deadline - ISO datetime string
 * @param {string} [heistData.description] - Optional mission details
 * @returns {Promise<Object>} Created heist
 */
export const createHeist = async (heistData) => {
  try {
    const response = await api.post('/heists', heistData);
    return { success: true, data: response.data };
  } catch (error) {
    // Handle validation errors (422)
    if (error.response?.status === 422) {
      const validationErrors = error.response.data?.detail;
      return {
        success: false,
        error: 'Blueprint incomplete. Fill all required fields.',
        validationErrors,
      };
    }

    return {
      success: false,
      error: error.response?.data?.detail || 'Failed to create heist',
    };
  }
};

/**
 * Abort a heist (creator only)
 * @param {number} id - Heist ID
 * @returns {Promise<Object>} Updated heist
 */
export const abortHeist = async (id) => {
  try {
    const response = await api.patch(`/heists/${id}/abort`);
    return { success: true, data: response.data };
  } catch (error) {
    // Handle specific error codes
    const status = error.response?.status;
    let errorMessage = 'Failed to abort heist';

    if (status === 403) {
      errorMessage = 'Only the creator can abort this mission';
    } else if (status === 404) {
      errorMessage = 'Heist not found';
    } else if (status === 409) {
      errorMessage = 'Heist is already expired or aborted';
    }

    return {
      success: false,
      error: error.response?.data?.detail || errorMessage,
    };
  }
};

export default {
  listActiveHeists,
  listMyHeists,
  listArchiveHeists,
  getHeist,
  createHeist,
  abortHeist,
};
