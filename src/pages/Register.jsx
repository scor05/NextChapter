import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (username && email && password) {
      try {
        await axios.post("http://localhost:8000/api/register", {
          nombre: username,
          correo: email,
          contraseña: password
        });
        alert("Registro exitoso");
        navigate("/login");
      } catch (error) {
        alert("Error al registrar: " + error.response?.data?.detail);
      }
    } else {
      alert("Llena todos los campos");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form onSubmit={handleSubmit} className="bg-white p-6 rounded shadow-md w-80">
        <h2 className="text-xl font-bold mb-4 text-center">Registro</h2>
        <input
          type="text"
          placeholder="Usuario"
          className="border p-2 w-full mb-3"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="email"
          placeholder="Correo"
          className="border p-2 w-full mb-3"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Contraseña"
          className="border p-2 w-full mb-3"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="bg-blue-900 text-white w-full py-2 rounded">
          Registrarse
        </button>
      </form>
    </div>
  );
}