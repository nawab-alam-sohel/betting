"use client"

import React, { useEffect, useState } from 'react'
import { getWallet, deposit, transactions, type Wallet, type Transaction } from '@/services/walletService'

export default function WalletPage() {
  const [wallet, setWallet] = useState<Wallet | null>(null)
  const [txs, setTxs] = useState<Transaction[]>([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function load() {
    setLoading(true)
    setError(null)
    try {
      const [w, t] = await Promise.all([getWallet(), transactions()])
      setWallet(w)
      setTxs(t)
    } catch (e: any) {
      setError(e?.message || 'Failed to load wallet')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const fd = new FormData(e.currentTarget)
    const amount = String(fd.get('amount') || '')
    if (!amount) return
    setSubmitting(true)
    setError(null)
    try {
      await deposit(amount)
      await load()
      e.currentTarget.reset()
    } catch (e: any) {
      setError(e?.message || 'Deposit failed')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="grid gap-6 md:grid-cols-3">
      <div className="md:col-span-1 space-y-3">
        <div className="rounded border border-slate-800 bg-slate-900 p-4">
          <div className="text-sm text-slate-400">Available Balance</div>
          <div className="mt-1 text-2xl font-semibold">
            {loading ? '…' : wallet ? (wallet.balance_cents / 100).toFixed(2) : '—'}
          </div>
        </div>
        <form className="rounded border border-slate-800 bg-slate-900 p-4" onSubmit={onSubmit}>
          <div className="text-sm text-slate-400 mb-2">Deposit</div>
          <input
            name="amount"
            placeholder="Amount"
            className="w-full rounded bg-slate-950 border border-slate-800 px-3 py-2 mb-2"
          />
          <button
            disabled={submitting}
            className="w-full bg-brand-500 hover:bg-brand-400 disabled:opacity-60 text-white font-medium rounded px-3 py-2"
          >
            {submitting ? 'Processing…' : 'Deposit'}
          </button>
          {error && <div className="mt-2 text-xs text-red-400">{error}</div>}
        </form>
      </div>
      <div className="md:col-span-2 rounded border border-slate-800 bg-slate-900 p-4">
        <div className="text-sm text-slate-400 mb-3">Transactions</div>
        <div className="space-y-2">
          {txs.map((t) => (
            <div key={t.id} className="flex items-center justify-between text-sm">
              <div className="text-slate-300">{t.type}</div>
              <div className="text-slate-400">{(t.amount_cents / 100).toFixed(2)}</div>
              <div className="text-slate-500">{new Date(t.created_at).toLocaleString()}</div>
            </div>
          ))}
          {!loading && txs.length === 0 && <div className="text-slate-400">No transactions.</div>}
        </div>
      </div>
    </div>
  )
}
