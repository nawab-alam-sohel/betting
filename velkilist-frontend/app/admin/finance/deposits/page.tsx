// @ts-nocheck
'use client'
import React, { useEffect, useState } from 'react'
import { listDeposits, getDepositsSummary } from '@/services/adminFinanceService'

const depositTabs = [
  { key: 'all', label: 'All' },
  { key: 'pending', label: 'Pending' },
  { key: 'approved', label: 'Approved' },
  { key: 'successful', label: 'Successful' },
  { key: 'rejected', label: 'Rejected' },
  { key: 'initiated', label: 'Initiated' },
]

export default function DepositsPage() {
  const [active, setActive] = useState('all')
  const [data, setData] = useState({ count: 0, page: 1, page_size: 25, results: [] })
  const [summary, setSummary] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  const load = async (status = active, page = 1) => {
    setLoading(true)
    try {
      const [list, sum] = await Promise.all([
        listDeposits({ status, page, page_size: data.page_size }),
        getDepositsSummary(),
      ])
      setData(list)
      setSummary(sum)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load('all', 1) }, [])

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Deposits</h1>

      <div className="flex flex-wrap gap-2">
        {depositTabs.map(t => (
          <button
            key={t.key}
            onClick={() => { setActive(t.key); load(t.key, 1) }}
            className={`px-3 py-1 rounded-full border text-sm ${active === t.key ? 'bg-blue-600 border-blue-600 text-white' : 'border-slate-700 text-slate-200 hover:bg-slate-800'}`}
            >
            {t.label}
            {summary && (
              <span className="ml-2 text-xs opacity-80">
                ({
                  t.key === 'all' ? summary.all :
                  t.key === 'pending' ? summary.pending :
                  t.key === 'approved' ? summary.approved :
                  t.key === 'successful' ? summary.successful :
                  t.key === 'rejected' ? summary.rejected :
                  t.key === 'initiated' ? summary.initiated : 0
                })
              </span>
            )}
          </button>
        ))}
      </div>

      <div className="rounded-xl border border-slate-800 bg-slate-900 overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="border-b border-slate-800 text-slate-400">
            <tr>
              <th className="text-left p-3">ID</th>
              <th className="text-left p-3">User</th>
              <th className="text-left p-3">Provider</th>
              <th className="text-left p-3">Amount</th>
              <th className="text-left p-3">Currency</th>
              <th className="text-left p-3">Status</th>
              <th className="text-left p-3">Created</th>
              <th className="text-left p-3">Reference</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td className="p-3" colSpan={8}>Loading…</td></tr>
            ) : data.results.length === 0 ? (
              <tr><td className="p-3" colSpan={8}>No records</td></tr>
            ) : (
              data.results.map((r: any) => (
                <tr key={r.id} className="border-t border-slate-800 hover:bg-slate-800/50">
                  <td className="p-3">{r.id}</td>
                  <td className="p-3">{r.user}</td>
                  <td className="p-3">{r.provider}</td>
                  <td className="p-3">{(r.amount_cents/100).toFixed(2)}</td>
                  <td className="p-3">{r.currency}</td>
                  <td className="p-3 capitalize">{r.status}</td>
                  <td className="p-3">{new Date(r.created_at).toLocaleString()}</td>
                  <td className="p-3">{r.reference || '-'}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <Pagination
        page={data.page}
        pageSize={data.page_size}
        total={data.count}
        onPage={(p) => load(active, p)}
      />
    </div>
  )
}

function Pagination({ page, pageSize, total, onPage }) {
  const pages = Math.max(1, Math.ceil(total / pageSize))
  return (
    <div className="flex items-center gap-2 text-sm">
      <button disabled={page<=1} onClick={() => onPage(page-1)} className="px-2 py-1 rounded border border-slate-700 disabled:opacity-50">Prev</button>
      <div className="text-slate-400">Page {page} / {pages}</div>
      <button disabled={page>=pages} onClick={() => onPage(page+1)} className="px-2 py-1 rounded border border-slate-700 disabled:opacity-50">Next</button>
    </div>
  )
}
