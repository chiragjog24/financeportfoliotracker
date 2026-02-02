import { useState, FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function ForgotPassword() {
  const navigate = useNavigate()
  const { forgotPassword, confirmForgotPassword, isLoading, error } = useAuth()
  const [formError, setFormError] = useState<string | null>(null)
  const [email, setEmail] = useState('')
  const [tokenReceived, setTokenReceived] = useState(false)
  const [resetToken, setResetToken] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const handleRequestReset = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setFormError(null)

    try {
      const result = await forgotPassword({ email })
      // In development, the token is returned directly
      if (result.token) {
        setResetToken(result.token)
        setTokenReceived(true)
      } else {
        setFormError('Reset token not received. Check your email or contact support.')
      }
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'Failed to send reset code')
    }
  }

  const handleConfirmReset = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setFormError(null)

    if (newPassword !== confirmPassword) {
      setFormError('Passwords do not match')
      return
    }

    if (newPassword.length < 8) {
      setFormError('Password must be at least 8 characters long')
      return
    }

    try {
      await confirmForgotPassword({
        token: resetToken,
        new_password: newPassword,
      })
      navigate('/signin', { state: { message: 'Password reset successfully. Please sign in.' } })
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'Failed to reset password')
    }
  }

  if (tokenReceived) {
    return (
      <div className="container mx-auto py-10 flex items-center justify-center min-h-screen">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Reset Password</CardTitle>
            <CardDescription>
              Enter your new password below
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleConfirmReset} className="space-y-4">
              {(error || formError) && (
                <div className="p-3 text-sm text-destructive bg-destructive/10 rounded-md">
                  {error || formError}
                </div>
              )}
              <div className="space-y-2">
                <Label htmlFor="newPassword">New Password</Label>
                <Input
                  id="newPassword"
                  type="password"
                  placeholder="••••••••"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  required
                  disabled={isLoading}
                  minLength={8}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="confirmPassword">Confirm New Password</Label>
                <Input
                  id="confirmPassword"
                  type="password"
                  placeholder="••••••••"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                  disabled={isLoading}
                  minLength={8}
                />
              </div>
              <Button type="submit" className="w-full" disabled={isLoading}>
                {isLoading ? 'Resetting password...' : 'Reset Password'}
              </Button>
              <div className="text-center text-sm">
                <Link to="/signin" className="text-primary hover:underline">
                  Back to sign in
                </Link>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container mx-auto py-10 flex items-center justify-center min-h-screen">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Forgot Password</CardTitle>
          <CardDescription>
            Enter your email to receive a password reset token
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleRequestReset} className="space-y-4">
            {(error || formError) && (
              <div className="p-3 text-sm text-destructive bg-destructive/10 rounded-md">
                {error || formError}
              </div>
            )}
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="user@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? 'Sending token...' : 'Send Reset Token'}
            </Button>
            <div className="text-center text-sm">
              <Link to="/signin" className="text-primary hover:underline">
                Back to sign in
              </Link>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
