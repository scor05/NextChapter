import React, { useState, useEffect } from "react";

export default function BookCard({ book }) {
  const [isFavorite, setIsFavorite] = useState(false);

  useEffect(() => {
    const stored = JSON.parse(localStorage.getItem("favoritos")) || [];
    setIsFavorite(stored.some((fav) => fav.id === book.id));
  }, [book.id]);

  const toggleFavorite = () => {
    const stored = JSON.parse(localStorage.getItem("favoritos")) || [];
    let updated;

    if (isFavorite) {
      updated = stored.filter((fav) => fav.id !== book.id);
    } else {
      updated = [...stored, book];
    }

    localStorage.setItem("favoritos", JSON.stringify(updated));
    setIsFavorite(!isFavorite);
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow text-center relative">
      {/* Estrellita arriba a la derecha */}
      <button
        onClick={toggleFavorite}
        className="absolute top-2 right-2 text-yellow-500 text-2xl hover:scale-110 transition"
        title={isFavorite ? "Eliminar de favoritos" : "Agregar a favoritos"}
      >
        {isFavorite ? "★" : "☆"}
      </button>

      {/* Imagen ficticia de portada */}
      <div className="h-40 w-full bg-orange-400 rounded mb-2 text-white flex items-center justify-center font-bold">
        PORTADA
      </div>

      {/* Detalles del libro */}
      <h3 className="font-semibold">{book.title}</h3>
      <p className="text-sm text-gray-600">
        {book.author} · {book.genre} · {book.year}
      </p>
    </div>
  );
}
