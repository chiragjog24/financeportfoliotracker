import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function NotFound() {
  return (
    <div className="container mx-auto py-10 flex items-center justify-center min-h-screen">
      <Card>
        <CardHeader>
          <CardTitle>404 - Page Not Found</CardTitle>
          <CardDescription>
            The page you're looking for doesn't exist.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Link to="/">
            <Button>Go Home</Button>
          </Link>
        </CardContent>
      </Card>
    </div>
  )
}
