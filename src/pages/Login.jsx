export default function Login({ onLogin }) {
  return (
    <div className="max-w-md mx-auto mt-12 p-6 bg-white shadow rounded">
      <h2 className="text-xl font-bold mb-4">Iniciar Sesión</h2>
      <input className="w-full border px-3 py-2 mb-4 rounded" placeholder="Correo electrónico" />
      <input className="w-full border px-3 py-2 mb-4 rounded" type="password" placeholder="Contraseña" />
      <button
        className="bg-blue-900 text-white w-full py-2 rounded"
        onClick={onLogin}
      >
        Entrar
      </button>
      <p className="text-sm text-center mt-4 text-gray-600">
        ¿No tienes cuenta? <a className="text-blue-700 underline" href="/register">Regístrate</a>
      </p>
    </div>
  )
}

