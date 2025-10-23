import axios from '@/lib/axiosInstance'

export async function getSiteSettings() {
  const { data } = await axios.get('/api/cms/settings/')
  return data
}

export async function updateSiteSettings(payload: any) {
  const { data } = await axios.put('/api/cms/settings/', payload)
  return data
}
