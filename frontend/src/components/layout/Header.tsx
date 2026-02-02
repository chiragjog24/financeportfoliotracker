import { Link, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/contexts/AuthContext'

export default function Header() {
  const { isAuthenticated, user, signOut, isLoading } = useAuth()
  const navigate = useNavigate()

  const handleSignOut = async () => {
    try {
      await signOut()
      navigate('/signin')
    } catch (error) {
      console.error('Sign out error:', error)
    }
  }

  return (
    <header className="border-b">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link to="/" className="flex items-center space-x-2">
          <span className="text-xl font-bold">Finance Portfolio Tracker</span>
        </Link>
        <nav className="flex items-center space-x-4">
          {isAuthenticated ? (
            <>
              <Link to="/">
                <Button variant="ghost">Home</Button>
              </Link>
              <Link to="/about">
                <Button variant="ghost">About</Button>
              </Link>
              <div className="flex items-center space-x-2">
                {user?.email && (
                  <span className="text-sm text-muted-foreground">{user.email}</span>
                )}
                <Button variant="outline" onClick={handleSignOut} disabled={isLoading}>
                  {isLoading ? 'Signing out...' : 'Sign Out'}
                </Button>
              </div>
            </>
          ) : (
            <>
              <Link to="/signin">
                <Button variant="ghost">Sign In</Button>
              </Link>
              <Link to="/signup">
                <Button>Sign Up</Button>
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  )
}
