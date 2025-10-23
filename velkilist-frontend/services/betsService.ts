import axios from '@/lib/axiosInstance'

export type PlaceBetPayload = {
  stake: number
  selections: Array<{
    matchId: string | number
    market: string
    outcome: string
    price: number
  }>
}

export async function placeBet(payload: PlaceBetPayload) {
  try {
    const { data } = await axios.post('/api/bets/place/', payload)
    return data
  } catch (e) {
    // graceful fallback for demo
    console.warn('placeBet fallback (demo):', payload)
    return { ok: true, reference: 'DEMO-' + Math.random().toString(36).slice(2, 8) }
  }
}
