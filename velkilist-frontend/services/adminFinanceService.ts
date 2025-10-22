import axios from '@/lib/axiosInstance'

export async function getDepositsSummary() {
  const { data } = await axios.get('/api/admin/dashboard/finance/deposits/summary/')
  return data
}

export async function listDeposits(params: { status?: string; page?: number; page_size?: number } = {}) {
  const { data } = await axios.get('/api/admin/dashboard/finance/deposits/', { params })
  return data as { count: number; page: number; page_size: number; results: any[] }
}

export async function getWithdrawalsSummary() {
  const { data } = await axios.get('/api/admin/dashboard/finance/withdrawals/summary/')
  return data
}

export async function listWithdrawals(params: { status?: string; page?: number; page_size?: number } = {}) {
  const { data } = await axios.get('/api/admin/dashboard/finance/withdrawals/', { params })
  return data as { count: number; page: number; page_size: number; results: any[] }
}
