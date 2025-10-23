import axios from '@/lib/axiosInstance'

export async function listCategories() {
  const { data } = await axios.get('/api/sports/categories/')
  return data
}

export async function listGames(params?: Record<string, string>) {
  const query = new URLSearchParams(params || {}).toString()
  const { data } = await axios.get(`/api/sports/games/${query ? `?${query}` : ''}`)
  return data
}

export async function listMarkets(gameId: number | string) {
  const { data } = await axios.get(`/api/sports/markets/?game=${gameId}`)
  return data
}
