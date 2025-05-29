import axios from 'axios';
import { useState } from 'react';
import BookCard from '../components/BookCard';

function Buscar({usuario, setUsuario}) {
  const [titulo, setTitulo] = useState('');
  const [autor, setAutor] = useState('');
  const [genero, setGenero] = useState('');
  const [resultados, setResultados] = useState([]);

  const handleBuscar = async () => {
    // Validación de campos vacíos
    if (!titulo && !autor && !genero) {
      alert("Debe de llenar por lo menos un campo");
      return;
    }

    try {
      setResultados([]);
      
      const params = {titulo, autor, genero};
      const response = await axios.get('http://localhost:8000/api/buscar', {
        params,
      });

      if (Array.isArray(response.data)) {
        if (response.data.length === 0) {
          alert("No se encontraron libros con los criterios de búsqueda");
        }
        setResultados(response.data);
        
      } else {
        console.error("La respuesta no es una lista:", response.data);
        alert("La respuesta del servidor no tiene el formato esperado");
        setResultados([]);
      }

    } catch (error) {
      console.error("Error al buscar libros:", error);
      alert(`Error al buscar: ${error.message}`);
      setResultados([]);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-start p-6 bg-white">
      <h1 className="text-3xl font-bold mb-6 text-center">Buscar Libros</h1>
      
      <div className="w-full max-w-xl grid grid-cols-1 gap-4 mb-4">
        <input
          type="text"
          placeholder="Título"
          value={titulo}
          onChange={(e) => setTitulo(e.target.value)}
          className="border border-gray-300 rounded p-2 w-full"
        />
        <input
          type="text"
          placeholder="Autor"
          value={autor}
          onChange={(e) => setAutor(e.target.value)}
          className="border border-gray-300 rounded p-2 w-full"
        />
        <input
          type="text"
          placeholder="Género"
          value={genero}
          onChange={(e) => setGenero(e.target.value)}
          className="border border-gray-300 rounded p-2 w-full"
        />
        <button
          onClick={handleBuscar}
          className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
        >
          Buscar
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-6xl">
        {resultados.map((libro, idx) => (
          <BookCard
            key={idx}
            book={libro}
            usuario={usuario}
            setUsuario={setUsuario}
          />
        ))}
      </div>
    </div>
  );

}

export default Buscar;
