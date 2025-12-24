import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Home from '@/pages/Home'
import Onboarding from '@/pages/Onboarding'
import History from '@/pages/History'
import Login from '@/pages/Login'
import Signup from '@/pages/Signup'
// import { Toaster } from "@/components/ui/toaster"

const queryClient = new QueryClient()

function App() {
  const isAuthenticated = !!localStorage.getItem('token');
  // detailed auth logic omitted for brevity, simpler check

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-background text-foreground antialiased font-sans">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/onboarding" element={isAuthenticated ? <Onboarding /> : <Navigate to="/login" />} />
            <Route path="/" element={isAuthenticated ? <Home /> : <Navigate to="/login" />} />
            <Route path="/history" element={isAuthenticated ? <History /> : <Navigate to="/login" />} />
          </Routes>
          {/* <Toaster /> */}
        </div>
      </Router>
    </QueryClientProvider>
  )
}

export default App
