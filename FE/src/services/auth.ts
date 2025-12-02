import api from './api';

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  phone_number?: string;
  is_verified: boolean;
  profile_picture?: string;
  created_at: string;
  last_login?: string;
}

export interface LoginResponse {
  message: string;
  user: User;
  token: string;
}

export interface RegisterData {
  email: string;
  first_name: string;
  last_name: string;
  password: string;
  password_confirm: string;
  phone_number?: string;
}

export const authService = {
  // Register new user
  async register(userData: RegisterData): Promise<LoginResponse> {
    const response = await api.post('/accounts/auth/register/', userData);
    
    if (response.data.token) {
      localStorage.setItem('auth_token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    
    return response.data;
  },

  // Login user
  async login(email: string, password: string): Promise<LoginResponse> {
    const response = await api.post('/accounts/auth/login/', { email, password });
    
    if (response.data.token) {
      localStorage.setItem('auth_token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    
    return response.data;
  },

  // Logout user
  async logout(): Promise<void> {
    try {
      const response = await api.post('/accounts/auth/logout/');
      // Get redirect URL from backend response if available
      const redirectUrl = response.data.redirect_url || '/';
      
      // Clear local storage
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      
      // Redirect to landing page (or URL from backend)
      window.location.href = redirectUrl;
    } catch (error) {
      console.error('Logout error:', error);
      // Even on error, clear storage and redirect to landing page
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      window.location.href = '/';
    }
  },

  // Get user profile
  async getProfile(): Promise<User> {
    const response = await api.get('/accounts/users/profile/');
    localStorage.setItem('user', JSON.stringify(response.data));
    return response.data;
  },

  // Change password
  async changePassword(
    oldPassword: string, 
    newPassword: string, 
    confirmPassword: string
  ): Promise<{ message: string; token?: string }> {
    const response = await api.put('/accounts/users/change-password/', {
      old_password: oldPassword,
      new_password: newPassword,
      confirm_password: confirmPassword,
    });
    
    if (response.data.token) {
      localStorage.setItem('auth_token', response.data.token);
    }
    
    return response.data;
  },

  // Request password reset
  async requestPasswordReset(email: string): Promise<{ message: string }> {
    const response = await api.post('/accounts/password-reset/', { email });
    return response.data;
  },

  // Confirm password reset
  async confirmPasswordReset(
    resetToken: string, 
    newPassword: string, 
    confirmPassword: string
  ): Promise<{ message: string }> {
    const response = await api.post('/accounts/password-reset/confirm/', {
      reset_token: resetToken,
      new_password: newPassword,
      confirm_password: confirmPassword,
    });
    return response.data;
  },

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!localStorage.getItem('auth_token');
  },

  // Get current user
  getCurrentUser(): User | null {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  // Get auth token
  getToken(): string | null {
    return localStorage.getItem('auth_token');
  },
};
