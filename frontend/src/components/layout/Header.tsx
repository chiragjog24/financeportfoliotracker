import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'

export default function Header() {
  return (
    <header className="border-b">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link to="/" className="flex items-center space-x-2">
          <span className="text-xl font-bold">Finance Portfolio Tracker</span>
        </Link>
        <nav className="flex items-center space-x-4">
          <Link to="/">
            <Button variant="ghost">Home</Button>
          </Link>
          <Link to="/about">
            <Button variant="ghost">About</Button>
          </Link>
        </nav>
      </div>
    </header>
  )
}
