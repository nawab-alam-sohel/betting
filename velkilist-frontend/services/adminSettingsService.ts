import axios from '@/lib/axiosInstance'

export async function getSportsProvider() {
  const { data } = await axios.get('/api/admin/dashboard/settings/providers/sports/')
  return data
}

export async function updateSportsProvider(payload: any) {
  const { data } = await axios.put('/api/admin/dashboard/settings/providers/sports/', payload)
  return data
}

export async function getCasinoProvider() {
  const { data } = await axios.get('/api/admin/dashboard/settings/providers/casino/')
  return data
}

export async function updateCasinoProvider(payload: any) {
  const { data } = await axios.put('/api/admin/dashboard/settings/providers/casino/', payload)
  return data
}
