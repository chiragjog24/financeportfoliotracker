export interface User {
  sub: string
  email?: string
  full_name?: string
}

export interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

export interface SignInInput {
  email: string
  password: string
}

export interface SignUpInput {
  email: string
  password: string
  full_name?: string
}

export interface RefreshTokenInput {
  refresh_token: string
}

export interface PasswordResetRequestInput {
  email: string
}

export interface PasswordResetConfirmInput {
  token: string
  new_password: string
}

export interface ApiResponse<T = unknown> {
  data?: T
  error?: string
  message?: string
}

export interface ApiError {
  message: string
  status?: number
  details?: unknown
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}
