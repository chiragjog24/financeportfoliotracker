export interface User {
  sub: string
  email?: string
  username?: string
  groups?: string[]
}

export interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

export interface SignInInput {
  username: string
  password: string
}

export interface SignUpInput {
  username: string
  password: string
  email: string
}

export interface ConfirmSignUpInput {
  username: string
  confirmationCode: string
}

export interface ForgotPasswordInput {
  username: string
}

export interface ConfirmForgotPasswordInput {
  username: string
  confirmationCode: string
  newPassword: string
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
