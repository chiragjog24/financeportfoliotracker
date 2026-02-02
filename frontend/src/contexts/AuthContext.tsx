import React, { createContext, useContext, useEffect, useState, useCallback } from 'react'
import { authService } from '@/services/auth'
import type {
  SignInInput,
  SignUpInput,
  PasswordResetRequestInput,
  PasswordResetConfirmInput,
  RefreshTokenInput,
  User,
  AuthState,
} from '@/types/auth'

interface AuthContextType extends AuthState {
  signIn: (input: SignInInput) => Promise<void>
  signUp: (input: SignUpInput) => Promise<void>
  signOut: () => Promise<void>
  forgotPassword: (input: PasswordResetRequestInput) => Promise<void>
  confirmForgotPassword: (input: PasswordResetConfirmInput) => Promise<void>
  refreshAuth: () => Promise<void>
  getAccessToken: () => string | null
  refreshAccessToken: () => Promise<string | null>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refreshAuth = useCallback(async () => {
    try {
      setIsLoading(true)
      setError(null)
      
      const accessToken = authService.getAccessToken()
      if (!accessToken) {
        setUser(null)
        setIsAuthenticated(false)
        return
      }

      // Try to get current user
      try {
        const currentUser = await authService.getCurrentUser()
        setUser(currentUser)
        setIsAuthenticated(true)
      } catch (err) {
        // Token might be expired, try to refresh
        const refreshToken = authService.getRefreshToken()
        if (refreshToken) {
          try {
            const tokens = await authService.refreshToken({ refresh_token: refreshToken })
            authService.setTokens(tokens.access_token, tokens.refresh_token)
            const currentUser = await authService.getCurrentUser()
            setUser(currentUser)
            setIsAuthenticated(true)
          } catch {
            // Refresh failed, clear tokens
            authService.clearTokens()
            setUser(null)
            setIsAuthenticated(false)
          }
        } else {
          authService.clearTokens()
          setUser(null)
          setIsAuthenticated(false)
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to refresh authentication')
      setUser(null)
      setIsAuthenticated(false)
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    refreshAuth()
  }, [refreshAuth])

  const signIn = async (input: SignInInput) => {
    try {
      setIsLoading(true)
      setError(null)
      const tokens = await authService.login(input)
      authService.setTokens(tokens.access_token, tokens.refresh_token)
      await refreshAuth()
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Sign in failed'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const signUp = async (input: SignUpInput) => {
    try {
      setIsLoading(true)
      setError(null)
      const tokens = await authService.register(input)
      authService.setTokens(tokens.access_token, tokens.refresh_token)
      await refreshAuth()
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Sign up failed'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const signOut = async () => {
    try {
      setIsLoading(true)
      setError(null)
      authService.clearTokens()
      setUser(null)
      setIsAuthenticated(false)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Sign out failed'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const forgotPassword = async (input: PasswordResetRequestInput) => {
    try {
      setIsLoading(true)
      setError(null)
      await authService.requestPasswordReset(input)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Password reset failed'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const confirmForgotPassword = async (input: PasswordResetConfirmInput) => {
    try {
      setIsLoading(true)
      setError(null)
      await authService.confirmPasswordReset(input)
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Password confirmation failed'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const getAccessToken = (): string | null => {
    return authService.getAccessToken()
  }

  const refreshAccessToken = async (): Promise<string | null> => {
    try {
      const refreshToken = authService.getRefreshToken()
      if (!refreshToken) {
        return null
      }

      const tokens = await authService.refreshToken({ refresh_token: refreshToken })
      authService.setTokens(tokens.access_token, tokens.refresh_token)
      return tokens.access_token
    } catch {
      authService.clearTokens()
      setUser(null)
      setIsAuthenticated(false)
      return null
    }
  }

  const value: AuthContextType = {
    user,
    isAuthenticated,
    isLoading,
    error,
    signIn,
    signUp,
    signOut,
    forgotPassword,
    confirmForgotPassword,
    refreshAuth,
    getAccessToken,
    refreshAccessToken,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
