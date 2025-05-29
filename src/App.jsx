import { useState } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import Navbar from './components/Navbar'
import Buscar from './pages/Buscar'
import Favoritos from './pages/Favoritos'
import Lobby from './pages/Lobby'
import Login from './pages/Login'
import Perfil from './pages/Perfil'
import Register from './pages/Register'

function App() {
  const [usuario, setUsuario] = useState(null);

  // Si NO está logueado, solo mostrar Login y Register
  if (!usuario) {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <Routes>
        <Route path="/login" element={<Login onLogin={(user) => setUsuario(user)} />} />
        <Route path="/register" element={<Register />} />
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </main>
  );
}


  // Si está logueado, mostrar el sitio completo
  return (
  <div className='min-h-screen bg-gray-50'>
    <Navbar usuario={usuario} setUsuario={setUsuario} />
    <Routes>
      <Route path="/" element={<Lobby />} />
      <Route path="/buscar" element={<Buscar />} />
      <Route path="/favoritos" element={<Favoritos />} />
      <Route path="/perfil" element={<Perfil />} />
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  </div>
);

}

export default App
