/**
 * API Service Configuration for ChamaNexus Frontend
 */

import axios from 'axios';

// ============================================================================
// Configuration
// ============================================================================

// API base URL - remove any trailing slash
const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1').replace(/\/$/, '');

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
  if (typeof document === 'undefined') return null;
  
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
    // Try the primary API v1 CSRF endpoint
    const response = await axios.get(`${API_BASE_URL}/csrf-token/`, {
      withCredentials: true,
    });
    
    if (response.data && response.data.csrfToken) {
      csrfToken = response.data.csrfToken;
      return csrfToken;
    }
    return null;
  } catch (error: any) {
    console.warn('CSRF token fetch from API endpoint failed, trying fallback:', error.message);
    
    // Fallback to root CSRF endpoint if API v1 endpoint fails
    try {
      const baseUrl = API_BASE_URL.replace(/\/api\/v1$/, '');
      const fallbackResponse = await axios.get(`${baseUrl}/csrf-token/`, {
        withCredentials: true,
      });
      
      if (fallbackResponse.data && fallbackResponse.data.csrfToken) {
        csrfToken = fallbackResponse.data.csrfToken;
        return csrfToken;
      }
      return null;
    } catch (fallbackError: any) {
      console.error('Fallback CSRF token fetch failed:', fallbackError.message);
      return null;
    }
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
    const isExemptEndpoint = [
      'login',
      'register',
      'password-reset',
      'api-token-auth'
    ].some(endpoint => config.url?.includes(endpoint));
    
    if (!isGetRequest && !isCsrfEndpoint && !isExemptEndpoint) {
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
    const originalRequest = error.config;
    
    // Handle CSRF token errors (403)
    if (error.response?.status === 403 && !originalRequest._retry) {
      console.warn('CSRF Error, refreshing token...');
      originalRequest._retry = true;
      
      // Try to get new CSRF token
      return fetchCsrfToken().then(() => {
        return api(originalRequest);
      }).catch(csrfError => {
        console.error('Failed to refresh CSRF token:', csrfError);
        return Promise.reject(error);
      });
    }
    
    // Handle authentication errors (401)
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      
      // Only redirect if not already on login page
      if (window.location.pathname !== '/login' && 
          window.location.pathname !== '/register') {
        window.location.href = '/login';
      }
    }
    
    // Log error details for debugging
    console.error('API Error:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      url: error.config?.url,
      method: error.config?.method,
    });
    
    return Promise.reject(error);
  }
);

// ============================================================================
// Helper Functions for Authentication
// ============================================================================

/**
 * Login helper function
 */
export const loginUser = async (email: string, password: string) => {
  try {
    const response = await api.post('/accounts/auth/login/', { email, password });
    
    if (response.data.token) {
      localStorage.setItem('auth_token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    
    // Fetch CSRF token after successful login
    await fetchCsrfToken();
    
    return response.data;
  } catch (error: any) {
    console.error('Login error:', error.response?.data || error.message);
    throw error;
  }
};

/**
 * Register helper function
 */
export const registerUser = async (userData: any) => {
  try {
    const response = await api.post('/accounts/auth/register/', userData);
    
    if (response.data.token) {
      localStorage.setItem('auth_token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    
    return response.data;
  } catch (error: any) {
    console.error('Registration error:', error.response?.data || error.message);
    throw error;
  }
};

/**
 * Logout helper function
 */
export const logoutUser = async () => {
  try {
    await api.post('/accounts/auth/logout/');
  } catch (error: any) {
    console.warn('Logout error:', error.message);
  } finally {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }
};

// ============================================================================
// Export HTTP methods
// ============================================================================

export const apiGet = (url: string, config?: any) => api.get(url, config);
export const apiPost = (url: string, data?: any, config?: any) => api.post(url, data, config);
export const apiPut = (url: string, data?: any, config?: any) => api.put(url, data, config);
export const apiPatch = (url: string, data?: any, config?: any) => api.patch(url, data, config);
export const apiDelete = (url: string, config?: any) => api.delete(url, config);

// Export the raw instance and auth helpers
// Note: Removed duplicate export statement that was causing build error
// export { api, loginUser, registerUser, logoutUser }; // ← REMOVE THIS LINE

export default api;
