// @ts-nocheck
"use client"

import React from 'react'
import { motion } from 'framer-motion'

export type Match = {
  id: number | string
  league?: string
  home: string
  away: string
  start: string // ISO string
  status?: 'scheduled' | 'live'
}

export type OutcomeKey = 'HOME' | 'DRAW' | 'AWAY'

export type OddsTriple = {
  HOME: number
  DRAW: number
  AWAY: number
}

export function MatchCard({
  match,
  odds,
  onPick,
  selected,
}: {
  match: Match
  odds: OddsTriple
  onPick: (match: Match, key: OutcomeKey, price: number) => void
  selected?: OutcomeKey | null
}) {
  const btn = (key: OutcomeKey, label: string) => {
    const active = selected === key
    const price = odds[key]
    return (
      <button
        key={key}
        onClick={() => onPick(match, key, price)}
        className={
          `flex-1 rounded-md px-3 py-2 text-sm font-semibold border transition
          ${active ? 'bg-emerald-600 text-white border-emerald-500' : 'bg-slate-800 text-slate-100 border-slate-700 hover:bg-slate-700'}`
        }
      >
        <div className="flex items-center justify-between gap-3">
          <span className="text-xs text-slate-300">{label}</span>
          <motion.span
            key={price}
            initial={{ scale: 0.95 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
            className="tabular-nums"
          >
            {price.toFixed(2)}
          </motion.span>
        </div>
      </button>
    )
  }

  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900 p-3">
      <div className="flex items-center justify-between">
        <div>
          <div className="text-xs text-slate-400">{match.league || 'League'}</div>
          <div className="text-sm mt-0.5 text-slate-200">{match.home} vs {match.away}</div>
        </div>
        <div className="text-xs text-slate-400">{new Date(match.start).toLocaleString()}</div>
      </div>
      <div className="mt-3 grid grid-cols-3 gap-2">
        {btn('HOME', match.home)}
        {btn('DRAW', 'Draw')}
        {btn('AWAY', match.away)}
      </div>
    </div>
  )
}
