import axios from "axios";
import { useEffect, useState } from "react";

export default function BookCard({ book, usuario, setUsuario }) {
  const [isFavorite, setIsFavorite] = useState(false);

  useEffect(() => {
    if (usuario?.favoritos?.includes(book.titulo)) {
      setIsFavorite(true);
    } else {
      setIsFavorite(false);
    }
  }, [usuario, book.titulo]);

  const toggleFavorite = async () => {
    if (!usuario) return;

    const nuevosFavoritos = isFavorite
      ? usuario.favoritos.filter((titulo) => titulo !== book.titulo)
      : [...usuario.favoritos, book.titulo];

    try {
      await axios.put("http://localhost:8000/api/modificar_usuario", {
        id: usuario.id,
        nombre: usuario.nombre,
        correo: usuario.correo,
        contraseña: null,
        favoritos: nuevosFavoritos
      }, {
        headers: {
          "Content-Type": "application/json"
        }
      });

      setUsuario({ ...usuario, favoritos: nuevosFavoritos });
      setIsFavorite(!isFavorite);
    } catch (error) {
      console.error("Error actualizando favoritos:", error);
    }
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow text-center relative">
      {/* Estrellita arriba a la derecha */}
      <button
        onClick={toggleFavorite}
        className={`absolute top-2 right-2 text-2xl transition ${
          isFavorite ? "text-yellow-500" : "text-gray-300"
        } hover:scale-110`}
        title={isFavorite ? "Eliminar de favoritos" : "Agregar a favoritos"}
      >
        ★
      </button>
      {/* Detalles del libro */}
      <h3 className="text-lg font-semibold mb-1">{book.titulo}</h3>
      <p className="text-sm text-gray-600 mb-1">
        <strong>Autores:</strong> {book.autores.join(", ")}
      </p>
      <p className="text-sm text-gray-600 mb-1">
        <strong>Géneros:</strong> {book.generos.join(", ")}
      </p>
    </div>
  );
}
