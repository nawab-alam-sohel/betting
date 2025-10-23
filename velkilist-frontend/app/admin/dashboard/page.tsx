// @ts-nocheck
"use client"

import React, { useEffect, useMemo, useState } from 'react'
import { getAdminSummary, getAdminCharts } from '@/services/adminDashboardService'

function StatCard({ title, value, icon, color = 'emerald' }: { title: string; value: React.ReactNode; icon?: React.ReactNode; color?: 'emerald'|'sky'|'rose'|'violet'|'amber' }) {
  const colorMap: any = {
    emerald: 'border-emerald-700/40 bg-emerald-900/10 text-emerald-300',
    sky: 'border-sky-700/40 bg-sky-900/10 text-sky-300',
    rose: 'border-rose-700/40 bg-rose-900/10 text-rose-300',
    violet: 'border-violet-700/40 bg-violet-900/10 text-violet-300',
    amber: 'border-amber-700/40 bg-amber-900/10 text-amber-300',
  }
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
      <div className="flex items-center justify-between">
        <div className="text-sm text-slate-400">{title}</div>
        <div className={`h-8 w-8 rounded-md border grid place-items-center text-xs ${colorMap[color]}`}>{icon || '➔'}</div>
      </div>
      <div className="mt-2 text-2xl font-semibold tabular-nums">{value}</div>
    </div>
  )
}

function numberUSD(cents?: number) {
  const v = (cents || 0) / 100
  return v.toLocaleString(undefined, { style: 'currency', currency: 'USD', maximumFractionDigits: 2 })
}

function toDailySeries(list: any[]): { labels: string[]; values: number[] } {
  const labels = list.map(x => typeof x.day === 'string' ? x.day : (x.day || ''))
  const values = list.map(x => (x.total_cents || 0) / 100)
  return { labels, values }
}

function SimpleLineChart({ series, labels }: { series: Array<{label: string; values: number[]; color: string}>, labels: string[] }) {
  // very small SVG line chart
  const width = 520, height = 160, pad = 24
  const allValues = series.flatMap(s => s.values)
  const maxVal = Math.max(1, ...allValues)
  const pointsFor = (values: number[]) => {
    const n = Math.max(values.length, 2)
    return values.map((v, i) => {
      const x = pad + (i*(width-2*pad))/Math.max(n-1,1)
      const y = height - pad - (v/maxVal)*(height-2*pad)
      return `${x},${y}`
    }).join(' ')
  }
  return (
    <svg width="100%" height={height} viewBox={`0 0 ${width} ${height}`} className="overflow-visible">
      <rect x={0} y={0} width={width} height={height} className="fill-slate-950" rx={12} />
      {[0,0.25,0.5,0.75,1].map((t,i)=> (
        <line key={i} x1={pad} x2={width-pad} y1={height-pad - t*(height-2*pad)} y2={height-pad - t*(height-2*pad)} className="stroke-slate-800" strokeWidth={1} />
      ))}
      {series.map((s, idx) => (
        <polyline key={idx} points={pointsFor(s.values)} fill="none" stroke={s.color} strokeWidth={2} strokeLinejoin="round" strokeLinecap="round" />
      ))}
    </svg>
  )
}

function DonutChart({ parts }: { parts: Array<{label: string; value: number; color: string}> }) {
  const total = parts.reduce((a,b)=>a+b.value,0) || 1
  let acc = 0
  const stops = parts.map(p => {
    const start = (acc/total)*100; acc += p.value; const end = (acc/total)*100
    return `${p.color} ${start}% ${end}%`
  }).join(', ')
  return (
    <div className="flex items-center gap-3">
      <div className="h-36 w-36 rounded-full" style={{ background: `conic-gradient(${stops})` }} />
      <div className="text-sm space-y-1">
        {parts.map((p,i)=> (
          <div key={i} className="flex items-center gap-2"><span className="h-2 w-2 rounded-full" style={{background:p.color}} /> <span className="text-slate-300">{p.label}</span> <span className="tabular-nums text-slate-400">{p.value}</span></div>
        ))}
      </div>
    </div>
  )
}

const DEMO_SUMMARY = {
  users: { total_bettors: 4366, active_bettors: 4365, email_unverified: 0, mobile_unverified: 0 },
  games: { in_play: 6796, upcoming: 780, open_for_betting: 7584, not_open_for_betting: 0 },
  deposits: { total_cents: 154413000, pending: 125, rejected: 0, charge_cents: 152971 },
  withdrawals: { total_cents: 300000, pending: 123, rejected: 1, charge_cents: 2120 },
  bets: { pending: 91, won: 0, lost: 0, refunded: 0 },
  support: { pending_tickets: 27 },
  kyc: { pending: 0 },
  outcomes: { pending: 73 },
}

export default function AdminDashboardPage() {
  const [summary, setSummary] = useState<any | null>(null)
  const [charts, setCharts] = useState<any | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true
    ;(async () => {
      try {
        const s = await getAdminSummary()
        const c = await getAdminCharts()
        if (!mounted) return
        setSummary(s)
        setCharts(c)
      } catch (e: any) {
        // Fallback to demo if unauthorized or API not ready
        if (!mounted) return
        setSummary(DEMO_SUMMARY)
        setCharts({
          deposits_daily: Array.from({length:30}).map((_,i)=>({day:`D${i+1}`, total_cents: (1000 + (i%7)*300)*100 })),
          withdraws_daily: Array.from({length:30}).map((_,i)=>({day:`D${i+1}`, total_cents: (i%10===0?9000:500)*100 })),
          transactions_plus_daily: Array.from({length:30}).map((_,i)=>({day:`D${i+1}`, total_cents: (4000 + (i%5)*700)*100 })),
          transactions_minus_daily: Array.from({length:30}).map((_,i)=>({day:`D${i+1}`, total_cents: (i%3===0?3500:800)*100 })),
          login_by_browser: [{browser:'Chrome',count:68},{browser:'Safari',count:22},{browser:'Edge',count:8},{browser:'Other',count:2}],
          login_by_os: [{os_type:'Windows',count:60},{os_type:'Android',count:20},{os_type:'iOS',count:15},{os_type:'Linux',count:5}],
          login_by_country: [{location:'BD',count:50},{location:'IN',count:25},{location:'PK',count:15},{location:'Other',count:10}],
        })
        if (e?.response?.status === 403) setError('You are not authorized to view admin dashboard.')
      }
    })()
    return () => { mounted = false }
  }, [])

  const depositSeries = useMemo(() => {
    if (!charts) return null
    const d = toDailySeries(charts.deposits_daily || [])
    const w = toDailySeries(charts.withdraws_daily || [])
    return { labels: d.labels, series: [ { label: 'Deposited', values: d.values, color: '#22c55e' }, { label: 'Withdrawn', values: w.values, color: '#38bdf8' } ] }
  }, [charts])

  const txSeries = useMemo(() => {
    if (!charts) return null
    const p = toDailySeries(charts.transactions_plus_daily || [])
    const m = toDailySeries(charts.transactions_minus_daily || [])
    return { labels: p.labels, series: [ { label: 'Plus', values: p.values, color: '#22c55e' }, { label: 'Minus', values: m.values, color: '#f43f5e' } ] }
  }, [charts])

  const loginBrowserParts = useMemo(() => {
    if (!charts) return []
    const colors = ['#6366f1','#22c55e','#f59e0b','#ef4444','#0ea5e9','#84cc16','#a855f7']
    return (charts.login_by_browser || []).map((x:any,i:number)=>({label: x.browser || x.label || '—', value: x.count || 0, color: colors[i%colors.length]}))
  }, [charts])
  const loginOSParts = useMemo(() => {
    const colors = ['#22c55e','#0ea5e9','#a855f7','#f59e0b','#ef4444']
    return (charts?.login_by_os || []).map((x:any,i:number)=>({label: x.os_type || x.label || '—', value: x.count || 0, color: colors[i%colors.length]}))
  }, [charts])
  const loginCountryParts = useMemo(() => {
    const colors = ['#f59e0b','#ef4444','#22c55e','#0ea5e9','#a855f7']
    return (charts?.login_by_country || []).map((x:any,i:number)=>({label: x.location || x.label || '—', value: x.count || 0, color: colors[i%colors.length]}))
  }, [charts])

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Dashboard</h1>
        <div className="text-sm text-slate-400">Admin</div>
      </div>

      {!!error && (
        <div className="rounded-md border border-amber-700/40 bg-amber-900/20 p-3 text-amber-300 text-sm">{error}</div>
      )}

      {/* Top summary cards */}
      <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Total Bettors" value={summary?.users?.total_bettors ?? '—'} color="violet" />
        <StatCard title="Active Bettors" value={summary?.users?.active_bettors ?? '—'} color="emerald" />
        <StatCard title="Email Unverified" value={summary?.users?.email_unverified ?? '—'} color="rose" />
        <StatCard title="Mobile Unverified" value={summary?.users?.mobile_unverified ?? '—'} color="sky" />
      </div>

      <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
        <StatCard title="In Play Games" value={summary?.games?.in_play ?? '—'} />
        <StatCard title="Upcoming Games" value={summary?.games?.upcoming ?? '—'} />
        <StatCard title="Open For Betting" value={summary?.games?.open_for_betting ?? '—'} />
        <StatCard title="Not Open For Betting" value={summary?.games?.not_open_for_betting ?? '—'} />
      </div>

      <div className="grid gap-3 md:grid-cols-2">
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
          <div className="text-sm text-slate-400">Deposits</div>
          <div className="mt-1 grid grid-cols-2 gap-2">
            <div className="rounded-lg border border-slate-800 bg-slate-950 p-3 text-sm">
              <div className="text-slate-400">Total Deposited</div>
              <div className="text-lg font-semibold">{numberUSD(summary?.deposits?.total_cents)}</div>
            </div>
            <div className="rounded-lg border border-slate-800 bg-slate-950 p-3 text-sm">
              <div className="text-slate-400">Pending Deposits</div>
              <div className="text-lg font-semibold">{summary?.deposits?.pending ?? '—'}</div>
            </div>
          </div>
        </div>
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
          <div className="text-sm text-slate-400">Withdrawals</div>
          <div className="mt-1 grid grid-cols-2 gap-2">
            <div className="rounded-lg border border-slate-800 bg-slate-950 p-3 text-sm">
              <div className="text-slate-400">Total Withdrawn</div>
              <div className="text-lg font-semibold">{numberUSD(summary?.withdrawals?.total_cents)}</div>
            </div>
            <div className="rounded-lg border border-slate-800 bg-slate-950 p-3 text-sm">
              <div className="text-slate-400">Pending Withdrawals</div>
              <div className="text-lg font-semibold">{summary?.withdrawals?.pending ?? '—'}</div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Pending Bet" value={summary?.bets?.pending ?? '—'} />
        <StatCard title="Pending Support Tickets" value={summary?.support?.pending_tickets ?? '—'} />
        <StatCard title="Pending KYC Verifications" value={summary?.kyc?.pending ?? '—'} />
        <StatCard title="Pending Outcomes" value={summary?.outcomes?.pending ?? '—'} />
      </div>

      {/* Charts */}
      <div className="grid gap-3 lg:grid-cols-2">
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
          <div className="text-sm text-slate-400 mb-2">Deposit & Withdraw Report</div>
          {depositSeries ? <SimpleLineChart series={depositSeries.series} labels={depositSeries.labels} /> : <div className="h-40" />}
        </div>
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
          <div className="text-sm text-slate-400 mb-2">Transactions Report</div>
          {txSeries ? <SimpleLineChart series={txSeries.series} labels={txSeries.labels} /> : <div className="h-40" />}
        </div>
      </div>

      <div className="grid gap-3 lg:grid-cols-3">
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
          <div className="text-sm text-slate-400 mb-2">Login By Browser (Last 30 days)</div>
          <DonutChart parts={loginBrowserParts} />
        </div>
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
          <div className="text-sm text-slate-400 mb-2">Login By OS (Last 30 days)</div>
          <DonutChart parts={loginOSParts} />
        </div>
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
          <div className="text-sm text-slate-400 mb-2">Login By Country (Last 30 days)</div>
          <DonutChart parts={loginCountryParts} />
        </div>
      </div>
    </div>
  )
}
