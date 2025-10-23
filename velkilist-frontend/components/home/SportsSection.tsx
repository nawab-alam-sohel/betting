// @ts-nocheck
"use client"

import { useMemo, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useLiveData } from '@/context/LiveDataContext'
import clsx from 'clsx'

export default function SportsSection() {
  const { matches } = useLiveData()
  const live = useMemo(() => matches.filter(m => m.isLive), [matches])
  if (live.length === 0) return null

  return (
    <section className="mt-8">
      <h2 className="text-xl font-semibold mb-3">Live Odds</h2>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {live.map(m => (
          <MatchCard key={m.matchId} {...m} />
        ))}
      </div>
    </section>
  )
}

function MatchCard({ teamA, teamB, oddsA, oddsB, score, isLive }: any) {
  return (
    <div className={clsx(
      "rounded-lg border p-4 bg-slate-900/70 border-slate-800",
      isLive && 'ring-1 ring-rose-500/50'
    )}>
      <div className="flex items-center justify-between">
        <div>
          <div className="text-sm text-slate-400">LIVE</div>
          <div className="text-lg font-medium">{teamA} vs {teamB}</div>
        </div>
        <div className="text-emerald-400 font-semibold">{score}</div>
      </div>
      <div className="mt-4 grid grid-cols-2 gap-3">
        <OddsPill label={teamA} value={oddsA} />
        <OddsPill label={teamB} value={oddsB} />
      </div>
    </div>
  )
}

function OddsPill({ label, value }: { label: string; value: number }) {
  const prev = useRef<number>(value)
  const dir = value > prev.current ? 'up' : value < prev.current ? 'down' : 'same'
  if (value !== prev.current) prev.current = value

  return (
    <motion.div
      key={value}
      initial={{ scale: 1 }}
      animate={{ scale: [1, 1.06, 1] }}
      transition={{ duration: 0.6 }}
      className={clsx(
        'rounded-lg px-3 py-2 text-center border bg-slate-800/80',
        dir === 'up' && 'border-emerald-500/60 shadow-[0_0_0_2px_rgba(16,185,129,0.25)]',
        dir === 'down' && 'border-rose-500/60 shadow-[0_0_0_2px_rgba(244,63,94,0.25)]'
      )}
    >
      <div className="text-xs text-slate-400 truncate">{label}</div>
      <div className={clsx('text-lg font-semibold', dir === 'up' ? 'text-emerald-400' : dir === 'down' ? 'text-rose-400' : 'text-slate-100')}>
        {value.toFixed(2)}
      </div>
    </motion.div>
  )
}
