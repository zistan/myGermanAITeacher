export interface User {
  id: number;
  username: string;
  email: string;
  native_language: string;
  target_language: string;
  proficiency_level: string;
  created_at: string;
  last_login?: string;
  settings?: Record<string, any>;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  native_language?: string;
  target_language?: string;
  proficiency_level?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface LoginResponse extends AuthResponse {
  // Login returns just token, need to fetch user separately
}

export interface RegisterResponse extends User {
  // Register returns the user object directly
}

export interface TokenPayload {
  sub: string; // user ID as string
  exp: number;
}
