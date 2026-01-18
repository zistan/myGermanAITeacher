import apiClient from '../client';
import type { LoginRequest, RegisterRequest, AuthResponse, User } from '../types/auth.types';

class AuthService {
  /**
   * POST /api/v1/auth/login
   * Authenticate user and receive JWT token
   */
  async login(credentials: LoginRequest): Promise<{ user: User }> {
    // Backend expects form data for OAuth2 password flow
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    // Step 1: Get the token
    const tokenResponse = await apiClient.post<AuthResponse>('/api/v1/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    // Store token
    localStorage.setItem('access_token', tokenResponse.data.access_token);

    // Step 2: Fetch user data with the token
    const user = await this.getCurrentUser();

    return { user };
  }

  /**
   * POST /api/v1/auth/register
   * Register a new user, then auto-login
   */
  async register(userData: RegisterRequest): Promise<{ user: User }> {
    // Step 1: Register the user (backend returns User object, no token)
    const registerResponse = await apiClient.post<User>('/api/v1/auth/register', userData);
    const user = registerResponse.data;

    // Step 2: Auto-login to get the token
    const formData = new URLSearchParams();
    formData.append('username', userData.username);
    formData.append('password', userData.password);

    const loginResponse = await apiClient.post<AuthResponse>('/api/v1/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    // Store token and user in localStorage
    localStorage.setItem('access_token', loginResponse.data.access_token);
    localStorage.setItem('user', JSON.stringify(user));

    return { user };
  }

  /**
   * GET /api/v1/auth/me
   * Get current authenticated user
   */
  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<User>('/api/v1/auth/me');
    localStorage.setItem('user', JSON.stringify(response.data));
    return response.data;
  }

  /**
   * Logout user - clear local storage
   */
  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  }

  /**
   * Get stored user from localStorage
   */
  getStoredUser(): User | null {
    const userStr = localStorage.getItem('user');
    if (!userStr) return null;
    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  }
}

export default new AuthService();
