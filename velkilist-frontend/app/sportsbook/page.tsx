// @ts-nocheck
"use client"

import React, { useEffect, useMemo, useState } from 'react'
import { demoUpcomingSports, type DemoSportGame } from '@/lib/demoData'
import OddsTable from '@/components/sportsbook/OddsTable'
import LeagueFilter from '@/components/sportsbook/LeagueFilter'
import BetSlip, { type BetSelection } from '@/components/sportsbook/BetSlip'
import type { Match, OutcomeKey, OddsTriple } from '@/components/sportsbook/MatchCard'
import { placeBet } from '@/services/betsService'
import { listGames } from '@/services/sportsbookService'

function oddsFromId(id: number | string): OddsTriple {
  const n = typeof id === 'number' ? id : parseInt(String(id).replace(/\D/g, ''), 10) || 7
  const base = 1.4 + ((n % 10) / 20) // 1.4..1.9
  const home = +(base + ((n % 3) * 0.12)).toFixed(2)
  const draw = +(1.0 + base * 0.6).toFixed(2)
  const away = +(base + (((n + 1) % 3) * 0.12)).toFixed(2)
  return { HOME: home, DRAW: draw, AWAY: away }
}

export default function SportsbookHome({ searchParams }: { searchParams?: Record<string, string> }) {
  const initialStatus = searchParams?.status === 'live' ? 'live' : 'scheduled'
  const [status, setStatus] = useState<'scheduled' | 'live'>(initialStatus)
  const [apiGames, setApiGames] = useState<DemoSportGame[] | null>(null)

  useEffect(() => {
    let mounted = true
    ;(async () => {
      try {
        const data = await listGames({ status })
        if (mounted && Array.isArray(data) && data.length) {
          // try to map to DemoSportGame shape, fallback if keys are different
          const mapped: DemoSportGame[] = data.map((g: any) => ({
            id: g.id ?? g.match_id ?? g.slug ?? Math.random(),
            home_team_name: g.home_team_name ?? g.home_team ?? g.home ?? 'Home',
            away_team_name: g.away_team_name ?? g.away_team ?? g.away ?? 'Away',
            start_time: g.start_time ?? g.start ?? new Date().toISOString(),
            league_name: g.league_name ?? g.league ?? g.tournament ?? 'League',
            status: (g.status === 'live' || g.is_live) ? 'live' : 'scheduled',
          }))
          setApiGames(mapped)
        } else {
          setApiGames(null)
        }
      } catch {
        setApiGames(null)
      }
    })()
    return () => { mounted = false }
  }, [status])

  const allGames = useMemo(() => (apiGames && apiGames.length ? apiGames : demoUpcomingSports(status as any)), [apiGames, status])
  const leagues = useMemo(() => Array.from(new Set(allGames.map(g => g.league_name || 'League'))), [allGames])
  const [league, setLeague] = useState<string | undefined>(undefined)

  const rows = useMemo(() => {
    const games = league ? allGames.filter(g => (g.league_name || 'League') === league) : allGames
    return games.map(g => ({
      match: {
        id: g.id,
        league: g.league_name || 'League',
        home: g.home_team_name,
        away: g.away_team_name,
        start: g.start_time,
        status: g.status || status,
      } as Match,
      odds: oddsFromId(g.id),
    }))
  }, [allGames, league, status])

  const [selections, setSelections] = useState<BetSelection[]>([])

  function handlePick(match: Match, key: OutcomeKey, price: number) {
    const label = key === 'HOME' ? match.home : key === 'AWAY' ? match.away : 'Draw'
    const selId = `${match.id}:${key}`
    setSelections(prev => {
      // toggle if already selected
      const exists = prev.find(s => s.id === selId)
      if (exists) return prev.filter(s => s.id !== selId)
      // remove other outcomes of same match
      const filtered = prev.filter(s => s.matchId !== match.id)
      return [
        ...filtered,
        { id: selId, matchId: match.id, eventLabel: `${match.home} vs ${match.away}`, market: '1x2', outcome: label, price },
      ]
    })
  }

  const rowsWithSelection = rows.map(r => ({
    ...r,
    selected: (selections.find(s => String(s.matchId) === String(r.match.id))?.outcome === r.match.home ? 'HOME'
      : selections.find(s => String(s.matchId) === String(r.match.id))?.outcome === 'Draw' ? 'DRAW'
      : selections.find(s => String(s.matchId) === String(r.match.id))?.outcome === r.match.away ? 'AWAY'
      : null)
  }))

  async function handlePlaceBet(stake: number, sels: BetSelection[]) {
    await placeBet({ stake, selections: sels.map(s => ({ matchId: s.matchId, market: s.market, outcome: s.outcome, price: s.price })) })
    setSelections([])
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <div className="lg:col-span-2">
        <div className="mb-4">
          <LeagueFilter leagues={leagues} value={league} onChange={setLeague} status={status} onStatusChange={setStatus} />
        </div>
        <OddsTable rows={rowsWithSelection} onPick={handlePick} />
        {rows.length === 0 && (
          <div className="text-slate-400 mt-6">No games found.</div>
        )}
      </div>

      <div className="lg:col-span-1">
        <BetSlip selections={selections} onRemove={(id) => setSelections(prev => prev.filter(s => s.id !== id))} onClear={() => setSelections([])} onPlaceBet={handlePlaceBet} />
      </div>
    </div>
  )
}
