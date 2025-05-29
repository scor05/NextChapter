export default function Buscar() {
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Buscar Libros</h2>
      <div className="flex flex-wrap gap-4 mb-6">
        <input className="border px-3 py-2 rounded" placeholder="Título" />
        <input className="border px-3 py-2 rounded" placeholder="Autor" />
        <input className="border px-3 py-2 rounded" placeholder="Género" />
        <button className="bg-blue-900 text-white px-4 py-2 rounded">Buscar</button>
      </div>
      <div className="text-gray-600">Resultados de búsqueda aparecerán aquí.</div>
    </div>
  )
}
