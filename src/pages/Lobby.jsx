import React from "react";
import BookCard from "../components/BookCard";

const libros = [
  { id: "1", title: "Nombre Libro A", author: "Autor A", genre: "Ficción", year: "2020" },
  { id: "2", title: "Nombre Libro B", author: "Autor B", genre: "Misterio", year: "2021" },
  { id: "3", title: "Nombre Libro C", author: "Autor C", genre: "Romance", year: "2019" }
];

export default function Lobby() {
  return (
    <div className="p-6">
      <h2 className="text-2xl font-semibold mb-2">Con base a tus gustos:</h2>
      <p className="mb-6 text-gray-600">(Agrega tus favoritos para mejores recomendaciones)</p>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 mb-8">
        {libros.map((libro) => (
          <BookCard key={libro.id} book={libro} />
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
