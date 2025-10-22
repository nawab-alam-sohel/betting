// @ts-nocheck
"use client"

import React, { useEffect, useState } from 'react'
import { getSportsProvider, updateSportsProvider, getCasinoProvider, updateCasinoProvider } from '@/services/adminSettingsService'

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
      <div className="text-sm text-slate-400 mb-2">{title}</div>
      {children}
    </div>
  )
}

export default function ApiSettingsPage() {
  const [sports, setSports] = useState<any>({ key: 'default', name: 'Sports Provider', base_url: '', config: { api_key: '' }, active: true })
  const [casino, setCasino] = useState<any>({ key: 'generic', name: 'Casino Provider', base_url: '', config: { api_key: '' }, active: true })
  const [saving, setSaving] = useState(false)
  const [toast, setToast] = useState<string | null>(null)

  useEffect(() => {
    ;(async () => {
      try { setSports(await getSportsProvider()) } catch {}
      try { setCasino(await getCasinoProvider()) } catch {}
    })()
  }, [])

  async function saveAll() {
    setSaving(true)
    try {
      await updateSportsProvider(sports)
      await updateCasinoProvider(casino)
      setToast('Saved successfully')
      setTimeout(()=>setToast(null), 2000)
    } finally { setSaving(false) }
  }

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">API Settings</h1>
      {toast && <div className="rounded-md border border-emerald-700/40 bg-emerald-900/20 p-3 text-emerald-300 text-sm">{toast}</div>}

      <Section title="Sports Provider">
        <div className="grid gap-3 sm:grid-cols-2">
          <div>
            <label className="text-xs text-slate-400">Provider Key</label>
            <input value={sports.key} onChange={e=>setSports({...sports, key:e.target.value})} className="w-full rounded-md bg-slate-800 border border-slate-700 px-3 py-2" />
          </div>
          <div>
            <label className="text-xs text-slate-400">Display Name</label>
            <input value={sports.name} onChange={e=>setSports({...sports, name:e.target.value})} className="w-full rounded-md bg-slate-800 border border-slate-700 px-3 py-2" />
          </div>
          <div className="sm:col-span-2">
            <label className="text-xs text-slate-400">Base URL</label>
            <input value={sports.base_url} onChange={e=>setSports({...sports, base_url:e.target.value})} className="w-full rounded-md bg-slate-800 border border-slate-700 px-3 py-2" />
          </div>
          <div className="sm:col-span-2">
            <label className="text-xs text-slate-400">API Key / Token</label>
            <input type="password" value={sports.config?.api_key || ''} onChange={e=>setSports({...sports, config:{...(sports.config||{}), api_key:e.target.value}})} className="w-full rounded-md bg-slate-800 border border-slate-700 px-3 py-2" />
          </div>
          <label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={!!sports.active} onChange={e=>setSports({...sports, active:e.target.checked})} /> Active</label>
        </div>
      </Section>

      <Section title="Casino Provider">
        <div className="grid gap-3 sm:grid-cols-2">
          <div>
            <label className="text-xs text-slate-400">Provider Key</label>
            <input value={casino.key} onChange={e=>setCasino({...casino, key:e.target.value})} className="w-full rounded-md bg-slate-800 border border-slate-700 px-3 py-2" />
          </div>
          <div>
            <label className="text-xs text-slate-400">Display Name</label>
            <input value={casino.name} onChange={e=>setCasino({...casino, name:e.target.value})} className="w-full rounded-md bg-slate-800 border border-slate-700 px-3 py-2" />
          </div>
          <div className="sm:col-span-2">
            <label className="text-xs text-slate-400">Base URL</label>
            <input value={casino.base_url} onChange={e=>setCasino({...casino, base_url:e.target.value})} className="w-full rounded-md bg-slate-800 border border-slate-700 px-3 py-2" />
          </div>
          <div className="sm:col-span-2">
            <label className="text-xs text-slate-400">API Key / Token</label>
            <input type="password" value={casino.config?.api_key || ''} onChange={e=>setCasino({...casino, config:{...(casino.config||{}), api_key:e.target.value}})} className="w-full rounded-md bg-slate-800 border border-slate-700 px-3 py-2" />
          </div>
          <label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={!!casino.active} onChange={e=>setCasino({...casino, active:e.target.checked})} /> Active</label>
        </div>
      </Section>

      <div className="flex justify-end">
        <button disabled={saving} onClick={saveAll} className="px-4 py-2 rounded-md bg-emerald-600 hover:bg-emerald-500 text-white disabled:opacity-50">{saving ? 'Saving…' : 'Save Changes'}</button>
      </div>
    </div>
  )
}
