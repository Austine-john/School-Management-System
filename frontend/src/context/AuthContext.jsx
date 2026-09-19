import { createContext, useContext, useEffect, useState } from 'react'
import client from '../api/client'
import { clearTokens, setTokens } from '../api/auth'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // Restore the session on first load (no redirect if there is no token).
  useEffect(() => {
    client
      .get('/auth/me/')
      .then((res) => setUser(res.data))
      .catch(() => setUser(null))
      .finally(() => setLoading(false))
  }, [])

  async function login(email, password) {
    const { data } = await client.post('/auth/login/', { email, password })
    setTokens(data.access, data.refresh)
    const me = await client.get('/auth/me/')
    setUser(me.data)
    return me.data
  }

  function logout() {
    clearTokens()
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
