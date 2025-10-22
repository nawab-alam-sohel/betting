import { api } from '@/app/api/client'

async function getMarkets(id: string) {
  return api(`/api/sports/markets/?game=${id}`)
}

export default async function MatchDetail({ params }: { params: { matchId: string } }) {
  const markets = await getMarkets(params.matchId)
  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Match #{params.matchId}</h1>
      <pre className="text-sm text-slate-300 bg-slate-900 border border-slate-800 rounded p-4 overflow-auto">{JSON.stringify(markets, null, 2)}</pre>
    </div>
  )
}
