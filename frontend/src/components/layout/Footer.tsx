export default function Footer() {
  return (
    <footer className="border-t mt-auto">
      <div className="container mx-auto py-6 px-4">
        <p className="text-center text-sm text-muted-foreground">
          © {new Date().getFullYear()} Finance Portfolio Tracker. All rights reserved.
        </p>
      </div>
    </footer>
  )
}
