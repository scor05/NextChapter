export default function Favoritos() {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h2 className="text-2xl font-bold mb-4">Mis Favoritos</h2>
      <p className="text-gray-600 mb-4">Aquí aparecerán los libros que marcaste como favoritos.</p>

      {/* Primera fila de libros */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 mb-8">
        {["A", "B", "C"].map((letra) => (
          <div key={letra} className="bg-white p-4 rounded-lg shadow text-center">
            <div className="h-40 w-full bg-orange-400 rounded mb-2 text-white flex items-center justify-center font-bold">
              PORTADA
            </div>
            <h3 className="font-semibold">Nombre Libro {letra}</h3>
            <p className="text-sm text-gray-600">Autor · Género · Año</p>
            <button className="mt-2 bg-red-600 text-white px-4 py-2 rounded">Eliminar</button>
          </div>
        ))}
      </div>

      {/* Segunda fila de libros */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 mb-8">
        {["D", "E", "F"].map((letra) => (
          <div key={letra} className="bg-white p-4 rounded-lg shadow text-center">
            <div className="h-40 w-full bg-orange-400 rounded mb-2 text-white flex items-center justify-center font-bold">
              PORTADA
            </div>
            <h3 className="font-semibold">Nombre Libro {letra}</h3>
            <p className="text-sm text-gray-600">Autor · Género · Año</p>
            <button className="mt-2 bg-red-600 text-white px-4 py-2 rounded">Eliminar</button>
          </div>
        ))}
      </div>

      <p className="text-gray-600">¡Agrega libros a tus favoritos desde la página de búsqueda!</p>
    </div>
  );
}
