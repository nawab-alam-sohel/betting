import axios from '@/lib/axiosInstance'

export async function login(username: string, password: string) {
  const { data } = await axios.post('/api/users/token/', { username, password })
  if (typeof window !== 'undefined') {
    localStorage.setItem('access_token', data.access)
    if (data.refresh) localStorage.setItem('refresh_token', data.refresh)
  }
  return data
}

export async function me() {
  const { data } = await axios.get('/api/users/me/')
  return data
}
