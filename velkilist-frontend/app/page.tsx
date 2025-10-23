import dynamic from 'next/dynamic'
import LiveTVSection from '@/components/home/LiveTVSection'
import SportsSection from '@/components/home/SportsSection'
type Game = {
  id: number
  home_team_name: string
  away_team_name: string
  start_time: string
  league_name?: string
}

function apiBase() {
  // Use internal base for server-side in Docker; fallback to public
  return process.env.INTERNAL_API_BASE_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
}

async function getUpcoming(): Promise<Game[]> {
  const res = await fetch(`${apiBase()}/api/sports/games/upcoming/`, { next: { revalidate: 30 } })
  if (!res.ok) return []
  return res.json()
}

export default async function HomePage() {
  const games = await getUpcoming()
  return (
    <div>
      <LiveTVSection />
      <SportsSection />
      <h1 className="text-2xl font-semibold">Upcoming games</h1>
      <p className="text-slate-400 text-sm">Powered by your Django backend at {apiBase()}</p>
      <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {games.map(g => (
          <div key={g.id} className="rounded-lg border border-slate-800 bg-slate-900 p-4">
            <div className="text-sm text-slate-400">{g.league_name || 'League'}</div>
            <div className="mt-1 text-lg">{g.home_team_name} vs {g.away_team_name}</div>
            <div className="mt-2 text-slate-400 text-sm">{new Date(g.start_time).toLocaleString()}</div>
          </div>
        ))}
        {games.length === 0 && (
          <div className="text-slate-400">No upcoming games found. Seed data or connect a provider.</div>
        )}
      </div>
    </div>
  )
}
