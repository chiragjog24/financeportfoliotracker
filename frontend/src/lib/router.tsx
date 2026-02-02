import { createBrowserRouter } from 'react-router-dom'
import Layout from '@/components/layout/Layout'
import { ProtectedRoute } from '@/components/auth/ProtectedRoute'
import Home from '@/pages/Home'
import About from '@/pages/About'
import SignIn from '@/pages/SignIn'
import SignUp from '@/pages/SignUp'
import ForgotPassword from '@/pages/ForgotPassword'
import NotFound from '@/pages/NotFound'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        index: true,
        element: (
          <ProtectedRoute>
            <Home />
          </ProtectedRoute>
        ),
      },
      {
        path: 'about',
        element: (
          <ProtectedRoute>
            <About />
          </ProtectedRoute>
        ),
      },
    ],
  },
  {
    path: '/signin',
    element: (
      <ProtectedRoute requireAuth={false}>
        <SignIn />
      </ProtectedRoute>
    ),
  },
  {
    path: '/signup',
    element: (
      <ProtectedRoute requireAuth={false}>
        <SignUp />
      </ProtectedRoute>
    ),
  },
  {
    path: '/forgot-password',
    element: (
      <ProtectedRoute requireAuth={false}>
        <ForgotPassword />
      </ProtectedRoute>
    ),
  },
  {
    path: '*',
    element: <NotFound />,
  },
])
