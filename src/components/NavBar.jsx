import { Link } from 'react-router-dom'
import { useState } from "react";

export default function Navbar({ usuario, setUsuario }) {
  const [dropdownVisible, setDropdownVisible] = useState(false);

  return (
    <nav className="bg-blue-900 text-white p-4 flex justify-between items-center shadow">
      <h1 className="text-lg font-bold">
        <Link to="/">NextChapter</Link>
      </h1>
      <ul className="flex gap-4 items-center">
        <li>
          <Link to="/buscar" className="hover:underline">
            Buscar
          </Link>
        </li>
        <li>
          <Link to="/favoritos" className="hover:underline">
            Favoritos
          </Link>
        </li>
        <li>
          <Link to="/" className="hover:underline">
            Descubrir
          </Link>
        </li>
        <li className="relative">
          <button
            className="hover:underline"
            onClick={() => setDropdownVisible(!dropdownVisible)}
          >
            {usuario?.nombre ?? "Usuario"}
          </button>
          {dropdownVisible && (
            <div className="absolute right-0 mt-2 w-48 bg-white border rounded shadow z-10 text-gray-800">
              <p className="px-4 py-2 text-sm border-b">
                Conectado como: <strong>{usuario.nombre}</strong>
              </p>
              <button
                onClick={() => {
                  setDropdownVisible(false);
                  setUsuario(null);
                }}
                className="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
              >
                Cerrar sesión
              </button>
            </div>
          )}
        </li>
      </ul>
    </nav>
  );
}
