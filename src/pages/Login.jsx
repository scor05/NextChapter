import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Login({ onLogin }) {
  const [correo, setCorreo] = useState("");
  const [contraseña, setContraseña] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await axios.post("http://localhost:8000/api/login", {
        correo,
        contraseña
      });
      const usuario = response.data.usuario;
      onLogin(usuario);
      navigate("/"); 
    } catch (error) {
      alert("Login fallido: " + error.response?.data?.detail);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-12 p-6 bg-white shadow rounded">
      <h2 className="text-xl font-bold mb-4">Iniciar Sesión</h2>
      <input
        className="w-full border px-3 py-2 mb-4 rounded"
        placeholder="Correo electrónico"
        value={correo}
        onChange={(e) => setCorreo(e.target.value)}
      />
      <input
        className="w-full border px-3 py-2 mb-4 rounded"
        type="password"
        placeholder="Contraseña"
        value={contraseña}
        onChange={(e) => setContraseña(e.target.value)}
      />
      <button
        className="bg-blue-900 text-white w-full py-2 rounded"
        onClick={handleLogin}
      >
        Entrar
      </button>
      <p className="text-sm text-center mt-4 text-gray-600">
        ¿No tienes cuenta? <a className="text-blue-700 underline" href="/register">Regístrate</a>
      </p>
    </div>
  );
}