import { useEffect, useState } from "react";
import axios from "axios";
import BookCard from "../components/BookCard";
import qs from "qs";

export default function Favoritos({ usuario, setUsuario }) {
  const [libros, setLibros] = useState([]);

  useEffect(() => {
    const fetchFavoritos = async () => {
      try {
        const res = await axios.get("http://localhost:8000/api/libros_favoritos", {
          params: { titulos: usuario.favoritos },
          paramsSerializer: (params) =>
            qs.stringify(params, { arrayFormat: "repeat" })
        });
        setLibros(res.data);
      } catch (error) {
        console.error("Error al cargar favoritos:", error);
      }
    };

    if (usuario?.favoritos?.length > 0) {
      fetchFavoritos();
    }
  }, [usuario]);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h2 className="text-2xl font-bold mb-4">Mis Favoritos</h2>
      <p className="text-gray-600 mb-4">Aquí aparecerán los libros que marcaste como favoritos.</p>

      {libros.length === 0 ? (
        <p className="text-gray-500">No tienes libros en favoritos aún.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 mb-8">
          {libros.map((libro, i) => (
            <BookCard
              key={i}
              book={libro}
              usuario={usuario}
              setUsuario={setUsuario}
            />
          ))}
        </div>
      )}
    </div>
  );
}