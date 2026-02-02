import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function Home() {
  return (
    <div className="container mx-auto py-10">
      <Card>
        <CardHeader>
          <CardTitle>Finance Portfolio Tracker</CardTitle>
          <CardDescription>
            Welcome to your portfolio management dashboard
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            This is the home page. Your portfolio tracking features will be available here.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
