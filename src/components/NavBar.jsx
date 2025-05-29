import { Link } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="bg-blue-900 text-white px-6 py-4 flex justify-between items-center">
      <h1 className="text-xl font-bold">NextChapter</h1>
      <div className="space-x-4">
        <Link to="/">Inicio</Link>
        <Link to="/buscar">Buscar</Link>
        <Link to="/favoritos">Mis Favoritos</Link>
        <Link to="/descubrir">Descubrir</Link>
        <Link to="/perfil">Usuario</Link>
      </div>
    </nav>
  )
}
// Navbar.jsx
// Este componente Navbar es una barra de navegación simple que utiliza React Router para la navegación entre diferentes secciones de la aplicación.