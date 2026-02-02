import React, { createContext, useContext, useEffect, useState, useCallback } from 'react'
import {
  signIn as amplifySignIn,
  signOut as amplifySignOut,
  signUp as amplifySignUp,
  confirmSignUp as amplifyConfirmSignUp,
  resetPassword as amplifyResetPassword,
  confirmResetPassword as amplifyConfirmResetPassword,
  getCurrentUser,
  fetchAuthSession,
} from 'aws-amplify/auth'
import type {
  SignInInput,
  SignUpInput,
  ConfirmSignUpInput,
  ForgotPasswordInput,
  ConfirmForgotPasswordInput,
  User,
  AuthState,
} from '@/types/auth'

interface AuthContextType extends AuthState {
  signIn: (input: SignInInput) => Promise<void>
  signUp: (input: SignUpInput) => Promise<void>
  confirmSignUp: (input: ConfirmSignUpInput) => Promise<void>
  signOut: () => Promise<void>
  forgotPassword: (input: ForgotPasswordInput) => Promise<void>
  confirmForgotPassword: (input: ConfirmForgotPasswordInput) => Promise<void>
  refreshAuth: () => Promise<void>
  getAccessToken: () => Promise<string | null>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const extractUserFromSession = useCallback(async (): Promise<User | null> => {
    try {
      const currentUser = await getCurrentUser()
      const session = await fetchAuthSession()
      
      if (session.tokens?.idToken) {
        const idToken = session.tokens.idToken
        const payload = idToken.payload as Record<string, unknown>
        
        return {
          sub: payload.sub as string,
          email: payload.email as string | undefined,
          username: payload['cognito:username'] as string | undefined,
          groups: (payload['cognito:groups'] as string[]) || [],
        }
      }
      return null
    } catch {
      return null
    }
  }, [])

  const refreshAuth = useCallback(async () => {
    try {
      setIsLoading(true)
      setError(null)
      const currentUser = await extractUserFromSession()
      
      if (currentUser) {
        setUser(currentUser)
        setIsAuthenticated(true)
      } else {
        setUser(null)
        setIsAuthenticated(false)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to refresh authentication')
      setUser(null)
      setIsAuthenticated(false)
    } finally {
      setIsLoading(false)
    }
  }, [extractUserFromSession])

  useEffect(() => {
    refreshAuth()
  }, [refreshAuth])

  const signIn = async (input: SignInInput) => {
    try {
      setIsLoading(true)
      setError(null)
      await amplifySignIn({ username: input.username, password: input.password })
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
      await amplifySignUp({
        username: input.username,
        password: input.password,
        options: {
          userAttributes: {
            email: input.email,
          },
        },
      })
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Sign up failed'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const confirmSignUp = async (input: ConfirmSignUpInput) => {
    try {
      setIsLoading(true)
      setError(null)
      await amplifyConfirmSignUp({
        username: input.username,
        confirmationCode: input.confirmationCode,
      })
      await refreshAuth()
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Confirmation failed'
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
      await amplifySignOut()
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

  const forgotPassword = async (input: ForgotPasswordInput) => {
    try {
      setIsLoading(true)
      setError(null)
      await amplifyResetPassword({ username: input.username })
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Password reset failed'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const confirmForgotPassword = async (input: ConfirmForgotPasswordInput) => {
    try {
      setIsLoading(true)
      setError(null)
      await amplifyConfirmResetPassword({
        username: input.username,
        confirmationCode: input.confirmationCode,
        newPassword: input.newPassword,
      })
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Password confirmation failed'
      setError(errorMessage)
      throw err
    } finally {
      setIsLoading(false)
    }
  }

  const getAccessToken = async (): Promise<string | null> => {
    try {
      const session = await fetchAuthSession()
      return session.tokens?.accessToken?.toString() || null
    } catch {
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
    confirmSignUp,
    signOut,
    forgotPassword,
    confirmForgotPassword,
    refreshAuth,
    getAccessToken,
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
