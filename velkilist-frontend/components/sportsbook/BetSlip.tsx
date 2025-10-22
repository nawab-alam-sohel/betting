// @ts-nocheck
"use client"

import React, { useMemo, useState } from 'react'

export type BetSelection = {
  id: string
  matchId: string | number
  eventLabel: string // e.g., TeamA vs TeamB
  market: string // 1x2
  outcome: string // HOME/DRAW/AWAY or name
  price: number
}

export default function BetSlip({
  selections,
  onRemove,
  onClear,
  onPlaceBet,
}: {
  selections: BetSelection[]
  onRemove: (id: string) => void
  onClear: () => void
  onPlaceBet: (stake: number, selections: BetSelection[]) => Promise<void> | void
}) {
  const [stake, setStake] = useState<number>(100)
  const totalOdds = useMemo(() => selections.reduce((acc, s) => acc * s.price, 1), [selections])
  const possibleWin = useMemo(() => +(stake * totalOdds).toFixed(2), [stake, totalOdds])

  return (
    <aside className="rounded-xl border border-slate-800 bg-slate-900 p-4 sticky top-24 max-h-[80vh] overflow-auto">
      <div className="flex items-center justify-between">
        <h3 className="font-semibold">Bet Slip</h3>
        <button className="text-xs text-slate-400 hover:text-slate-200" onClick={onClear}>Clear</button>
      </div>

      <div className="mt-3 space-y-2">
        {selections.length === 0 && (
          <div className="text-slate-400 text-sm">No selections yet. Click odds to add.</div>
        )}
        {selections.map(s => (
          <div key={s.id} className="rounded-lg border border-slate-800 bg-slate-950 p-3">
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="text-xs text-slate-400">{s.market} • {s.outcome}</div>
                <div className="text-sm">{s.eventLabel}</div>
              </div>
              <div className="text-right">
                <div className="font-semibold tabular-nums">{s.price.toFixed(2)}</div>
                <button onClick={() => onRemove(s.id)} className="text-xs text-slate-400 hover:text-slate-200">Remove</button>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 space-y-2">
        <label className="text-xs text-slate-400">Stake</label>
        <input
          type="number"
          min={1}
          step={1}
          value={stake}
          onChange={e => setStake(parseFloat(e.target.value || '0'))}
          className="w-full rounded-md bg-slate-800 border border-slate-700 px-3 py-2"
        />
      </div>

      <div className="mt-3 rounded-lg bg-slate-950 border border-slate-800 p-3 text-sm">
        <div className="flex items-center justify-between"><span className="text-slate-400">Total odds</span><span className="tabular-nums font-semibold">{totalOdds.toFixed(2)}</span></div>
        <div className="flex items-center justify-between mt-1"><span className="text-slate-400">Potential win</span><span className="tabular-nums font-semibold text-emerald-400">{possibleWin.toFixed(2)}</span></div>
      </div>

      <button
        disabled={selections.length === 0}
        onClick={() => onPlaceBet(stake, selections)}
        className="mt-4 w-full rounded-md bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed text-white py-2 font-semibold"
      >
        Place bet
      </button>
    </aside>
  )
}
