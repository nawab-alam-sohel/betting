// @ts-nocheck
'use client'
import React, { useEffect, useState } from 'react'
import { getDepositsSummary, getWithdrawalsSummary } from '@/services/adminFinanceService'

export default function FinanceOverviewPage() {
  const [deposits, setDeposits] = useState<any>(null)
  const [withdrawals, setWithdrawals] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let mounted = true
    Promise.all([getDepositsSummary(), getWithdrawalsSummary()])
      .then(([d, w]) => {
        if (!mounted) return
        setDeposits(d)
        setWithdrawals(w)
      })
      .catch(() => {})
      .finally(() => mounted && setLoading(false))
    return () => { mounted = false }
  }, [])

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Finance Overview</h1>
      {loading && <div className="text-slate-400">Loading…</div>}
      {!loading && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <section className="rounded-xl border border-slate-800 bg-slate-900 p-4">
            <h2 className="font-medium text-slate-200 mb-2">Deposits</h2>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <Stat label="All" value={deposits?.all} />
              <Stat label="Pending" value={deposits?.pending} />
              <Stat label="Approved" value={deposits?.approved} />
              <Stat label="Successful" value={deposits?.successful} />
              <Stat label="Rejected" value={deposits?.rejected} />
              <Stat label="Initiated" value={deposits?.initiated} />
            </div>
          </section>
          <section className="rounded-xl border border-slate-800 bg-slate-900 p-4">
            <h2 className="font-medium text-slate-200 mb-2">Withdrawals</h2>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <Stat label="All" value={withdrawals?.all} />
              <Stat label="Pending" value={withdrawals?.pending} />
              <Stat label="Approved" value={withdrawals?.approved} />
              <Stat label="Rejected" value={withdrawals?.rejected} />
            </div>
          </section>
        </div>
      )}
    </div>
  )
}

function Stat({ label, value }: { label: string, value: any }) {
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-950 p-3 flex items-center justify-between">
      <div className="text-slate-400">{label}</div>
      <div className="font-semibold">{value ?? 0}</div>
    </div>
  )
}
