import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

interface ProtectedRouteProps {
  children: React.ReactNode
  requireAuth?: boolean
}

export function ProtectedRoute({ children, requireAuth = true }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading } = useAuth()
  const location = useLocation()

  if (isLoading) {
    return (
      <div className="container mx-auto py-10 flex items-center justify-center min-h-screen">
        <Card>
          <CardHeader>
            <CardTitle>Loading...</CardTitle>
            <CardDescription>Checking authentication status</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="animate-pulse">Please wait...</div>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (requireAuth && !isAuthenticated) {
    // Redirect to sign in page with return URL
    return <Navigate to="/signin" state={{ from: location }} replace />
  }

  if (!requireAuth && isAuthenticated) {
    // Redirect authenticated users away from auth pages
    const from = (location.state as { from?: Location })?.from
    return <Navigate to={from?.pathname || '/'} replace />
  }

  return <>{children}</>
}
