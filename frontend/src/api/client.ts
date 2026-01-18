import axios, { type AxiosError, type InternalAxiosRequestConfig } from 'axios';
import type { ApiError } from './types/common.types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add JWT token to requests
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<any>) => {
    if (error.response) {
      let errorMessage = 'An error occurred';

      // Handle different error response formats
      if (error.response.data) {
        const data = error.response.data;

        // Case 1: FastAPI validation error (422) - detail is an array
        if (Array.isArray(data.detail)) {
          const validationErrors = data.detail
            .map((err: any) => {
              const field = err.loc && err.loc.length > 1 ? err.loc[err.loc.length - 1] : 'field';
              return `${field}: ${err.msg}`;
            })
            .join(', ');
          errorMessage = validationErrors || 'Validation error';
        }
        // Case 2: Simple string detail
        else if (typeof data.detail === 'string') {
          errorMessage = data.detail;
        }
        // Case 3: Other error formats
        else if (data.message) {
          errorMessage = data.message;
        }
      }

      const apiError: ApiError = {
        detail: errorMessage,
        status_code: error.response.status,
      };

      // Handle 401 Unauthorized - token expired or invalid
      if (error.response.status === 401) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');

        // Redirect to login if not already there
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
      }

      return Promise.reject(apiError);
    } else if (error.request) {
      // Request was made but no response received
      const networkError: ApiError = {
        detail: 'Network error. Please check your connection.',
      };
      return Promise.reject(networkError);
    } else {
      // Something else happened
      const unknownError: ApiError = {
        detail: error.message || 'An unexpected error occurred',
      };
      return Promise.reject(unknownError);
    }
  }
);

export default apiClient;
