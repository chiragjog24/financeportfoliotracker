import { useState, FormEvent } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function ForgotPassword() {
  const { forgotPassword, confirmForgotPassword, isLoading, error } = useAuth()
  const [formError, setFormError] = useState<string | null>(null)
  const [username, setUsername] = useState('')
  const [codeSent, setCodeSent] = useState(false)
  const [confirmationCode, setConfirmationCode] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const handleRequestReset = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setFormError(null)

    try {
      await forgotPassword({ username })
      setCodeSent(true)
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
        username,
        confirmationCode,
        newPassword,
      })
      // Redirect to sign in after successful reset
      window.location.href = '/signin'
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'Failed to reset password')
    }
  }

  if (codeSent) {
    return (
      <div className="container mx-auto py-10 flex items-center justify-center min-h-screen">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Reset Password</CardTitle>
            <CardDescription>
              Enter the confirmation code sent to your email and your new password
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
                <Label htmlFor="code">Confirmation Code</Label>
                <Input
                  id="code"
                  type="text"
                  placeholder="Enter 6-digit code"
                  value={confirmationCode}
                  onChange={(e) => setConfirmationCode(e.target.value)}
                  required
                  disabled={isLoading}
                />
              </div>
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
            Enter your username or email to receive a password reset code
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
              <Label htmlFor="username">Username or Email</Label>
              <Input
                id="username"
                type="text"
                placeholder="username@example.com"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? 'Sending code...' : 'Send Reset Code'}
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
