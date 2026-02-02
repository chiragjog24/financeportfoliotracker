import { API_BASE_URL } from '@/utils/constants'
import type {
  User,
  SignInInput,
  SignUpInput,
  RefreshTokenInput,
  PasswordResetRequestInput,
  PasswordResetConfirmInput,
  TokenResponse,
} from '@/types/auth'

class AuthService {
  private baseUrl = `${API_BASE_URL}/auth`

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    })

    if (!response.ok) {
      let errorMessage = `Request failed with status ${response.status}`
      try {
        const errorData = await response.json()
        errorMessage = errorData.detail || errorData.message || errorMessage
      } catch {
        errorMessage = response.statusText || errorMessage
      }
      throw new Error(errorMessage)
    }

    return response.json()
  }

  async register(input: SignUpInput): Promise<TokenResponse> {
    return this.request<TokenResponse>('/register', {
      method: 'POST',
      body: JSON.stringify(input),
    })
  }

  async login(input: SignInInput): Promise<TokenResponse> {
    return this.request<TokenResponse>('/login', {
      method: 'POST',
      body: JSON.stringify(input),
    })
  }

  async refreshToken(input: RefreshTokenInput): Promise<TokenResponse> {
    return this.request<TokenResponse>('/refresh', {
      method: 'POST',
      body: JSON.stringify({ refresh_token: input.refresh_token }),
    })
  }

  async requestPasswordReset(
    input: PasswordResetRequestInput
  ): Promise<{ message: string; token?: string }> {
    return this.request<{ message: string; token?: string }>('/password-reset', {
      method: 'POST',
      body: JSON.stringify(input),
    })
  }

  async confirmPasswordReset(
    input: PasswordResetConfirmInput
  ): Promise<{ message: string }> {
    return this.request<{ message: string }>('/password-reset/confirm', {
      method: 'POST',
      body: JSON.stringify({
        token: input.token,
        new_password: input.new_password,
      }),
    })
  }

  async getCurrentUser(): Promise<User> {
    const token = this.getAccessToken()
    if (!token) {
      throw new Error('No access token available')
    }

    return this.request<User>('/me', {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
  }

  // Token storage helpers
  getAccessToken(): string | null {
    return localStorage.getItem('access_token')
  }

  getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token')
  }

  setTokens(accessToken: string, refreshToken: string): void {
    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', refreshToken)
  }

  clearTokens(): void {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }
}

export const authService = new AuthService()
