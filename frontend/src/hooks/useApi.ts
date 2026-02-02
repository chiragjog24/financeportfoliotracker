import { useState, useCallback } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { API_BASE_URL } from '@/utils/constants'
import type { ApiResponse, ApiError } from '@/types/auth'

interface UseApiOptions {
  skipAuth?: boolean
}

interface UseApiReturn<T> {
  data: T | null
  loading: boolean
  error: ApiError | null
  execute: (url: string, options?: RequestInit) => Promise<T | null>
  reset: () => void
}

export function useApi<T = unknown>(options: UseApiOptions = {}): UseApiReturn<T> {
  const { getAccessToken, isAuthenticated, refreshAuth } = useAuth()
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<ApiError | null>(null)

  const execute = useCallback(
    async (url: string, requestOptions: RequestInit = {}): Promise<T | null> => {
      try {
        setLoading(true)
        setError(null)

        // Get access token if authentication is required
        let token: string | null = null
        if (!options.skipAuth && isAuthenticated) {
          token = await getAccessToken()
          if (!token) {
            // Try to refresh auth if token is missing
            await refreshAuth()
            token = await getAccessToken()
          }
        }

        // Build headers
        const headers: HeadersInit = {
          'Content-Type': 'application/json',
          ...requestOptions.headers,
        }

        if (token && !options.skipAuth) {
          headers['Authorization'] = `Bearer ${token}`
        }

        // Make the request
        const response = await fetch(`${API_BASE_URL}${url}`, {
          ...requestOptions,
          headers,
        })

        // Handle non-OK responses
        if (!response.ok) {
          let errorMessage = `Request failed with status ${response.status}`
          let errorDetails: unknown = null

          try {
            const errorData = await response.json()
            errorMessage = errorData.message || errorData.detail || errorMessage
            errorDetails = errorData
          } catch {
            // If response is not JSON, use status text
            errorMessage = response.statusText || errorMessage
          }

          const apiError: ApiError = {
            message: errorMessage,
            status: response.status,
            details: errorDetails,
          }

          // Handle authentication errors
          if (response.status === 401) {
            // Token might be expired, try to refresh
            if (!options.skipAuth && isAuthenticated) {
              await refreshAuth()
              // Retry once after refresh
              const retryToken = await getAccessToken()
              if (retryToken) {
                headers['Authorization'] = `Bearer ${retryToken}`
                const retryResponse = await fetch(`${API_BASE_URL}${url}`, {
                  ...requestOptions,
                  headers,
                })
                if (retryResponse.ok) {
                  const retryData = await retryResponse.json()
                  setData(retryData)
                  return retryData
                }
              }
            }
          }

          setError(apiError)
          throw apiError
        }

        // Parse response
        const contentType = response.headers.get('content-type')
        let responseData: T

        if (contentType && contentType.includes('application/json')) {
          responseData = await response.json()
        } else {
          responseData = (await response.text()) as unknown as T
        }

        setData(responseData)
        return responseData
      } catch (err) {
        const apiError: ApiError =
          err instanceof Error && 'status' in err
            ? (err as ApiError)
            : {
                message: err instanceof Error ? err.message : 'An unknown error occurred',
              }
        setError(apiError)
        return null
      } finally {
        setLoading(false)
      }
    },
    [getAccessToken, isAuthenticated, refreshAuth, options.skipAuth]
  )

  const reset = useCallback(() => {
    setData(null)
    setError(null)
    setLoading(false)
  }, [])

  return { data, loading, error, execute, reset }
}
