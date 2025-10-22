"use client"

import React, { createContext, useContext, useMemo, useRef, useState, useEffect } from 'react'

export type LiveMatch = {
  matchId: string
  teamA: string
  teamB: string
  oddsA: number
  oddsB: number
  score: string
  possession: number // % for teamA, teamB = 100 - possession
  shotsA: number
  shotsB: number
  minute: number
  isLive: boolean
}

type LiveDataContextType = {
  matches: LiveMatch[]
  getMatch: (id: string) => LiveMatch | undefined
}

const LiveDataContext = createContext<LiveDataContextType | undefined>(undefined)

function randomDelta(min: number, max: number) {
  return Math.random() * (max - min) + min
}

const INITIAL_MATCHES: LiveMatch[] = [
  {
    matchId: 'm1', teamA: 'Barcelona', teamB: 'Real Madrid',
    oddsA: 1.75, oddsB: 2.05, score: '2 – 1', possession: 62,
    shotsA: 9, shotsB: 7, minute: 58, isLive: true,
  },
  {
    matchId: 'm2', teamA: 'Liverpool', teamB: 'Man City',
    oddsA: 2.10, oddsB: 1.90, score: '0 – 0', possession: 48,
    shotsA: 5, shotsB: 6, minute: 23, isLive: true,
  },
  {
    matchId: 'm3', teamA: 'PSG', teamB: 'Marseille',
    oddsA: 1.60, oddsB: 2.30, score: '—', possession: 50,
    shotsA: 0, shotsB: 0, minute: 0, isLive: false,
  },
]

export function LiveDataProvider({ children }: { children: React.ReactNode }) {
  const [matches, setMatches] = useState<LiveMatch[]>(INITIAL_MATCHES)

  // Simulate live odds updates every 3s
  useEffect(() => {
    const oddsTimer = setInterval(() => {
      setMatches(prev => prev.map(m => {
        if (!m.isLive) return m
        let oddsA = Math.max(1.1, Math.min(4.5, m.oddsA + (Math.random() > 0.5 ? randomDelta(0.01, 0.08) : -randomDelta(0.01, 0.08))))
        let oddsB = Math.max(1.1, Math.min(4.5, m.oddsB + (Math.random() > 0.5 ? randomDelta(0.01, 0.08) : -randomDelta(0.01, 0.08))))
        // small coupling to score: if oddsA drops a lot, maybe teamA scored
        let score = m.score
        if (Math.random() < 0.02) {
          // random goal event
          const [aStr, bStr] = (m.score === '—' ? '0 – 0' : m.score).split(' – ')
          let a = parseInt(aStr, 10), b = parseInt(bStr, 10)
          if (Math.random() > 0.5) a++; else b++
          score = `${a} – ${b}`
        }
        return { ...m, oddsA, oddsB, score }
      }))
    }, 3000)
    return () => clearInterval(oddsTimer)
  }, [])

  // Simulate stats updates every 5s
  useEffect(() => {
    const statsTimer = setInterval(() => {
      setMatches(prev => prev.map(m => {
        if (!m.isLive) return m
        const swing = Math.floor(randomDelta(-3, 3))
        let possession = Math.max(35, Math.min(65, m.possession + swing))
        const shotsA = m.shotsA + (Math.random() < 0.3 ? 1 : 0)
        const shotsB = m.shotsB + (Math.random() < 0.25 ? 1 : 0)
        const minute = Math.min(95, m.minute + 1)
        return { ...m, possession, shotsA, shotsB, minute }
      }))
    }, 5000)
    return () => clearInterval(statsTimer)
  }, [])

  const value = useMemo(() => ({
    matches,
    getMatch: (id: string) => matches.find(m => m.matchId === id),
  }), [matches])

  return (
    <LiveDataContext.Provider value={value}>{children}</LiveDataContext.Provider>
  )
}

export function useLiveData() {
  const ctx = useContext(LiveDataContext)
  if (!ctx) throw new Error('useLiveData must be used within LiveDataProvider')
  return ctx
}
