import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function About() {
  return (
    <div className="container mx-auto py-10">
      <Card>
        <CardHeader>
          <CardTitle>About</CardTitle>
          <CardDescription>
            Finance Portfolio Tracker Application
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            This application helps you track and manage your investment portfolio.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
