import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Resume from './pages/Resume'
import Analysis from './pages/Analysis'

function ProtectedRoute({ children }) {
  const { isLoggedIn } = useAuth()
  return isLoggedIn ? children : <Navigate to='/login' replace />
}

export default function App() {
  return (
    <Routes>
      <Route path='/login'     element={<Login />} />
      <Route path='/register'  element={<Register />} />
      <Route path='/dashboard' element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path='/resume'    element={<ProtectedRoute><Resume /></ProtectedRoute>} />
      <Route path='/analysis'  element={<ProtectedRoute><Analysis /></ProtectedRoute>} />
      <Route path='*'          element={<Navigate to='/login' replace />} />
    </Routes>
  )
}
