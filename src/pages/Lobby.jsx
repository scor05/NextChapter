import axios from "axios";
import { useEffect, useState } from "react";
import BookCard from "../components/BookCard";

export default function Lobby({ usuario, setUsuario }) {
  const [libros, setLibros] = useState([]);

  useEffect(() => {
    const fetchRecomendaciones = async () => {
      try {
        const response = await axios.get("http://localhost:8000/api/recomendar", {
          params: { correo: usuario.correo }
        });
        setLibros(response.data);
      } catch (error) {
        console.error("Error al obtener recomendaciones:", error);
      }
    };

    if (usuario) {
      fetchRecomendaciones();
    }
  }, [usuario]);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-semibold mb-2">Con base a tus gustos:</h2>
      <p className="mb-6 text-gray-600">(Agrega tus favoritos para mejores recomendaciones)</p>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 mb-8">
        {libros.map((libro, index) => (
          <BookCard
            key={index}
            book={libro}
            usuario={usuario}
            setUsuario={setUsuario}
          />
        ))}
      </div>

      <h2 className="text-xl font-semibold mb-2">¿Deseas algo más específico?</h2>
      <div className="flex flex-wrap gap-4">
        <input className="border px-3 py-2 rounded" placeholder="Título" />
        <input className="border px-3 py-2 rounded" placeholder="Autor" />
        <input className="border px-3 py-2 rounded" placeholder="Género" />
        <button className="bg-blue-900 text-white px-4 py-2 rounded">Buscar</button>
      </div>
    </div>
  );
}
