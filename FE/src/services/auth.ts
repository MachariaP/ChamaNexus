import api from './api';

export const authService = {
  async login(email: string, password: string) {
    const response = await api.post('/auth-token/', { email, password });
    const token = response.data.token;
    localStorage.setItem('auth_token', token);
    return response.data;
  },

  async logout() {
    localStorage.removeItem('auth_token');
    await api.post('/auth/logout/');
  },

  async getProfile() {
    const response = await api.get('/user/profile/');
    return response.data;
  },
};
