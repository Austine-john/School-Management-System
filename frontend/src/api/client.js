import axios from 'axios'
import { clearTokens, getAccessToken, getRefreshToken, setTokens } from './auth'

// Shared axios instance pointed at the Django REST API (proxied in dev).
const client = axios.create({
  baseURL: '/api/v1',
})

// Attach the JWT access token to every request.
client.interceptors.request.use((config) => {
  const token = getAccessToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// On 401, try to refresh the access token once, then retry the original call.
client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const token = getAccessToken()

    if (error.response?.status === 401 && token && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = getRefreshToken()
      if (refreshToken) {
        try {
          const { data } = await axios.post('/api/v1/auth/refresh/', {
            refresh: refreshToken,
          })
          setTokens(data.access, data.refresh ?? refreshToken)
          originalRequest.headers.Authorization = `Bearer ${data.access}`
          return client(originalRequest)
        } catch {
          clearTokens()
        }
      }
      clearTokens()
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  },
)

export default client
