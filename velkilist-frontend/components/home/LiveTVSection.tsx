// @ts-nocheck
"use client"

import { motion } from 'framer-motion'
import { useLiveData } from '@/context/LiveDataContext'

export default function LiveTVSection() {
  const { matches } = useLiveData()
  const primary = matches.find(m => m.isLive) || matches[0]
  if (!primary) return null

  return (
    <section className="mt-6">
      <div className="relative overflow-hidden rounded-xl border border-slate-800 bg-gradient-to-br from-slate-900 to-slate-800">
        {/* Video placeholder */}
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/images/support-demo.svg" alt="Live stream" className="w-full h-64 md:h-80 object-cover opacity-60" />

        {/* Glass overlay with live stats */}
        <motion.div
          initial={{ opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="absolute top-4 left-4 right-4 md:left-6 md:top-6 md:right-auto backdrop-blur bg-white/10 border border-white/20 text-white rounded-lg px-4 py-3"
        >
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <TeamBadge name={primary.teamA} />
              <span className="text-slate-100 font-semibold">{primary.teamA}</span>
              <span className="text-slate-400">vs</span>
              <span className="text-slate-100 font-semibold">{primary.teamB}</span>
              <TeamBadge name={primary.teamB} />
            </div>
            <div className="flex items-center gap-2">
              <span className="text-rose-400 text-xs font-semibold">● LIVE</span>
              <span className="text-slate-200 font-bold text-lg">{primary.score}</span>
              <span className="text-slate-300 text-sm">{primary.minute}'</span>
            </div>
          </div>

          {/* Possession bar */}
          <div className="mt-3">
            <div className="flex justify-between text-[11px] text-slate-200">
              <span>{primary.teamA}</span>
              <span>{primary.teamB}</span>
            </div>
            <div className="mt-1 h-2 rounded bg-white/10 overflow-hidden">
              <motion.div
                key={primary.possession}
                initial={{ width: 0 }}
                animate={{ width: `${primary.possession}%` }}
                transition={{ duration: 0.6 }}
                className="h-full bg-emerald-400/80"
              />
            </div>
            <div className="mt-1 text-[11px] text-slate-300">
              Possession: {primary.possession}% – {100 - primary.possession}%
            </div>
          </div>

          {/* Shots on goal */}
          <div className="mt-2 text-[12px] text-slate-200">
            Shots on goal: {primary.shotsA} – {primary.shotsB}
          </div>
        </motion.div>
      </div>
    </section>
  )
}

function TeamBadge({ name }: { name: string }) {
  const letter = name.charAt(0).toUpperCase()
  return (
    <div className="h-6 w-6 rounded-full bg-white/20 border border-white/30 flex items-center justify-center text-[11px] font-bold">
      {letter}
    </div>
  )
}
