// @ts-nocheck
"use client"

import React, { useMemo } from 'react'
import { MatchCard, type Match, type OutcomeKey, type OddsTriple } from './MatchCard'

export type OddsRow = {
  match: Match
  odds: OddsTriple
  selected?: OutcomeKey | null
}

export default function OddsTable({
  rows,
  onPick,
}: {
  rows: OddsRow[]
  onPick: (match: Match, key: OutcomeKey, price: number) => void
}) {
  const leagues = useMemo(() => {
    const set = new Set<string>()
    rows.forEach(r => r.match.league && set.add(r.match.league))
    return Array.from(set)
  }, [rows])

  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-2">
      {rows.map((r) => (
        <MatchCard
          key={r.match.id}
          match={r.match}
          odds={r.odds}
          selected={r.selected}
          onPick={onPick}
        />
      ))}
    </div>
  )
}
