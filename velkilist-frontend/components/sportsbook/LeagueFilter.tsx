// @ts-nocheck
"use client"

import React from 'react'

export default function LeagueFilter({
  leagues,
  value,
  onChange,
  status,
  onStatusChange,
}: {
  leagues: string[]
  value?: string
  onChange: (league?: string) => void
  status: 'scheduled' | 'live'
  onStatusChange: (s: 'scheduled' | 'live') => void
}) {
  return (
    <div className="flex flex-wrap items-center gap-2">
      <div className="flex items-center gap-1">
        <span className="text-xs text-slate-400">View:</span>
        <button
          className={`px-3 py-1.5 text-sm rounded-md border ${status==='scheduled' ? 'bg-slate-800 border-slate-700' : 'bg-slate-900 border-slate-800 hover:bg-slate-800'}`}
          onClick={() => onStatusChange('scheduled')}
        >Upcoming</button>
        <button
          className={`px-3 py-1.5 text-sm rounded-md border ${status==='live' ? 'bg-slate-800 border-slate-700' : 'bg-slate-900 border-slate-800 hover:bg-slate-800'}`}
          onClick={() => onStatusChange('live')}
        >Live</button>
      </div>
      <div className="h-4 w-px bg-slate-800 mx-1" />
      <div className="flex items-center gap-2 overflow-auto">
        <button
          onClick={() => onChange(undefined)}
          className={`px-3 py-1.5 text-sm rounded-full border ${!value ? 'bg-emerald-600 text-white border-emerald-500' : 'bg-slate-900 border-slate-800 hover:bg-slate-800'}`}
        >All</button>
        {leagues.map(l => (
          <button key={l}
            onClick={() => onChange(l)}
            className={`px-3 py-1.5 text-sm rounded-full border ${value===l ? 'bg-emerald-600 text-white border-emerald-500' : 'bg-slate-900 border-slate-800 hover:bg-slate-800 text-slate-100'}`}
          >{l}</button>
        ))}
      </div>
    </div>
  )
}
