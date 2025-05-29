import { Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import Lobby from './pages/Lobby'
import Buscar from './pages/Buscar'
import Favoritos from './pages/Favoritos'
import Descubrir from './pages/Descubrir'
import Perfil from './pages/Perfil'
import Login from './pages/Login'
import Register from './pages/Register'
import { useState } from 'react'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  // Si NO está logueado, solo mostrar Login y Register
  if (!isLoggedIn) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
        <Routes>
          <Route path="/login" element={<Login onLogin={() => setIsLoggedIn(true)} />} />
          <Route path="/register" element={<Register />} />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </main>
    )
  }

  // Si está logueado, mostrar el sitio completo
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow p-4">
        <Routes>
          <Route path="/" element={<Lobby />} />
          <Route path="/buscar" element={<Buscar />} />
          <Route path="/favoritos" element={<Favoritos />} />
          <Route path="/descubrir" element={<Descubrir />} />
          <Route path="/perfil" element={<Perfil />} />
          <Route path="/login" element={<Navigate to="/" />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
