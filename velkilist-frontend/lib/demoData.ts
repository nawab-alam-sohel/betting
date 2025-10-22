export type DemoSportGame = {
  id: string | number
  home_team_name: string
  away_team_name: string
  start_time: string
  league_name?: string
  status?: 'scheduled' | 'live' | 'finished'
}

export function demoUpcomingSports(status: 'scheduled' | 'live' = 'scheduled'): DemoSportGame[] {
  const now = Date.now()
  const base = [
    { id: 101, league_name: 'La Liga', home_team_name: 'Barcelona', away_team_name: 'Sevilla', start_time: new Date(now + 60*60*1000).toISOString(), status: 'scheduled' as const },
    { id: 102, league_name: 'Premier League', home_team_name: 'Liverpool', away_team_name: 'Arsenal', start_time: new Date(now + 2*60*60*1000).toISOString(), status: 'scheduled' as const },
    { id: 103, league_name: 'Serie A', home_team_name: 'Inter', away_team_name: 'Juventus', start_time: new Date(now + 3*60*60*1000).toISOString(), status: 'scheduled' as const },
    { id: 201, league_name: 'UCL', home_team_name: 'Real Madrid', away_team_name: 'PSG', start_time: new Date(now - 10*60*1000).toISOString(), status: 'live' as const },
    { id: 202, league_name: 'Bundesliga', home_team_name: 'Bayern', away_team_name: 'Dortmund', start_time: new Date(now - 30*60*1000).toISOString(), status: 'live' as const },
  ]
  return base.filter(g => g.status === status)
}

export type DemoCasinoGame = {
  id: number
  name: string
  provider: string
  category: string
  image: string
  isNew?: boolean
}

export function demoCasinoCategories(): string[] {
  return ['Popular', 'Live', 'Slots', 'Table', 'Jackpot']
}

export function demoCasinoGames(category?: string): DemoCasinoGame[] {
  const games: DemoCasinoGame[] = Array.from({ length: 12 }).map((_, i) => ({
    id: i + 1,
    name: `Game ${i + 1}`,
    provider: ['Pragmatic Play', 'Evolution', 'NetEnt'][i % 3],
    category: ['Popular', 'Live', 'Slots', 'Table'][i % 4],
    image: `https://placehold.co/400x240/0b1220/ffffff?text=Game+${i + 1}`,
    isNew: i % 5 === 0,
  }))
  if (!category) return games
  return games.filter(g => g.category === category)
}
