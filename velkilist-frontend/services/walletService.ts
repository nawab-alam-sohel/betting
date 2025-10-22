import axios from '@/lib/axiosInstance'

export type Wallet = { balance_cents: number; reserved_balance_cents: number }
export type Transaction = { id: number; amount_cents: number; type: string; created_at: string }

export async function getWallet(): Promise<Wallet> {
  const { data } = await axios.get('/api/wallets/')
  return data
}

export async function deposit(amount: string): Promise<Wallet> {
  const { data } = await axios.post('/api/wallets/deposit/', { amount })
  return data
}

export async function transactions(): Promise<Transaction[]> {
  const { data } = await axios.get('/api/wallets/transactions/')
  return data
}
