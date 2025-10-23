import axios from '@/lib/axiosInstance'

export async function getAdminSummary() {
  const { data } = await axios.get('/api/admin/dashboard/summary/')
  return data
}

export async function getAdminCharts() {
  const { data } = await axios.get('/api/admin/dashboard/charts/')
  return data
}
