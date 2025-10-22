// @ts-nocheck
"use client"

import React, { useEffect, useState } from 'react'
import { getSiteSettings, updateSiteSettings } from '@/services/cmsSettingsService'

export default function FrontendContentSettingsPage() {
  const [data, setData] = useState<any>({
    homepage_title: '',
    homepage_subtitle: '',
    custom_css: '',
  })
  const [saving, setSaving] = useState(false)
  const [toast, setToast] = useState<string|null>(null)

  useEffect(() => { (async()=>{ try { setData(await getSiteSettings()) } catch {} })() }, [])

  async function save() {
    setSaving(true)
    try {
      await updateSiteSettings({
        homepage_title: data.homepage_title,
        homepage_subtitle: data.homepage_subtitle,
        custom_css: data.custom_css,
      })
      setToast('Frontend content saved')
      setTimeout(()=>setToast(null), 2000)
    } finally { setSaving(false) }
  }

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-semibold">Manage Frontend Content</h1>
      {toast && <div className="rounded-md border border-emerald-700/40 bg-emerald-900/20 p-3 text-emerald-300 text-sm">{toast}</div>}

      <div className="rounded-xl border border-slate-800 bg-slate-900 p-4 grid gap-3">
        <div>
          <label className="text-xs text-slate-400">Homepage Title</label>
          <input value={data.homepage_title||''} onChange={e=>setData({...data, homepage_title:e.target.value})} className="w-full rounded-md bg-slate-800 border border-slate-700 px-3 py-2" />
        </div>
        <div>
          <label className="text-xs text-slate-400">Homepage Subtitle</label>
          <input value={data.homepage_subtitle||''} onChange={e=>setData({...data, homepage_subtitle:e.target.value})} className="w-full rounded-md bg-slate-800 border border-slate-700 px-3 py-2" />
        </div>
      </div>

      <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
        <div className="text-sm text-slate-400 mb-2">Custom CSS</div>
        <textarea value={data.custom_css||''} onChange={e=>setData({...data, custom_css:e.target.value})} rows={10} className="w-full rounded-md bg-slate-800 border border-slate-700 px-3 py-2 font-mono text-xs" placeholder={"/* Paste CSS that should apply globally */"} />
      </div>

      <div className="flex justify-end">
        <button disabled={saving} onClick={save} className="px-4 py-2 rounded-md bg-emerald-600 hover:bg-emerald-500 text-white disabled:opacity-50">{saving ? 'Saving…' : 'Save Changes'}</button>
      </div>
    </div>
  )
}
