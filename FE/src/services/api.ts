/**
 * API Service Configuration for ChamaNexus Frontend
 */

import axios from 'axios';

// ============================================================================
// Configuration
// ============================================================================

// API base URL (can be overridden by environment variable)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';

// CSRF token management
let csrfToken: string | null = null;

// ============================================================================
// CSRF Token Utilities
// ============================================================================

/**
 * Extract CSRF token from cookies
 */
const getCsrfTokenFromCookies = (): string | null => {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.substring(0, name.length + 1) === (name + '=')) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }
  return null;
};

/**
 * Fetch CSRF token from server
 */
const fetchCsrfToken = async (): Promise<string | null> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/csrf-token/`, {
      withCredentials: true,
    });
    
    if (response.data && response.data.csrfToken) {
      csrfToken = response.data.csrfToken;
      return csrfToken;
    }
    return null;
  } catch (error) {
    console.error('CSRF token fetch failed:', error);
    return null;
  }
};

// ============================================================================
// Axios Instance Configuration
// ============================================================================

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  async (config) => {
    // Skip CSRF for GET requests and CSRF token endpoint itself
    const isGetRequest = config.method?.toLowerCase() === 'get';
    const isCsrfEndpoint = config.url?.includes('csrf-token');
    
    if (!isGetRequest && !isCsrfEndpoint) {
      let token = getCsrfTokenFromCookies();
      
      // If no CSRF token in cookies, fetch one
      if (!token) {
        token = await fetchCsrfToken();
      }
      
      if (token) {
        config.headers = config.headers || {};
        config.headers['X-CSRFToken'] = token;
      }
    }
    
    // Add authentication token if available
    const authToken = localStorage.getItem('auth_token');
    if (authToken) {
      config.headers = config.headers || {};
      config.headers['Authorization'] = `Token ${authToken}`;
    }
    
    return config;
  },
  (error) => {
    console.error('Request interceptor error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle CSRF token errors (403)
    if (error.response?.status === 403) {
      console.error('CSRF Error:', error.response.data);
      
      // Try to get new CSRF token
      fetchCsrfToken().then(() => {
        console.log('CSRF token refreshed after 403 error');
      });
    }
    
    // Handle authentication errors (401)
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      
      // Redirect to login page if not already there
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login';
      }
    }
    
    // Log error details
    console.error('API Error:', {
      status: error.response?.status,
      data: error.response?.data,
      url: error.config?.url,
      method: error.config?.method,
    });
    
    return Promise.reject(error);
  }
);

// Export individual HTTP methods
export const apiGet = (url: string, config?: any) => api.get(url, config);
export const apiPost = (url: string, data?: any, config?: any) => api.post(url, data, config);
export const apiPut = (url: string, data?: any, config?: any) => api.put(url, data, config);
export const apiPatch = (url: string, data?: any, config?: any) => api.patch(url, data, config);
export const apiDelete = (url: string, config?: any) => api.delete(url, config);

// Export the raw instance
export { api };

export default api;
