// @ts-nocheck
'use client'

import { useState } from 'react'
import Image from 'next/image'
import { createSupportTicket } from '@/services/supportService'
import { isValidEmail } from '@/lib/validators'

export default function SupportPage() {
  const [form, setForm] = useState({ name: '', email: '', subject: '', message: '', captcha: false })
  const [submitting, setSubmitting] = useState(false)
  const [result, setResult] = useState<{ ok: boolean; msg: string } | null>(null)

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setSubmitting(true)
    setResult(null)
    // Basic email validation
    if (!isValidEmail(form.email)) {
      setResult({ ok: false, msg: 'Please enter a valid email address' })
      setSubmitting(false)
      return
    }
    const res = await createSupportTicket({
      name: form.name,
      email: form.email,
      subject: form.subject,
      message: form.message,
      captchaToken: form.captcha ? 'demo-ok' : undefined,
    })
    if (res.ok) setResult({ ok: true, msg: 'Ticket submitted successfully' })
    else setResult({ ok: false, msg: res.message || 'Failed to submit' })
    setSubmitting(false)
  }

  return (
    <div className="relative -mx-4 md:-mx-8 lg:-mx-16">
      {/* Background demo image */}
      <div className="absolute inset-0 -z-10">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src="/images/support-demo.svg" alt="Support background" className="h-full w-full object-cover" />
        <div className="absolute inset-0 bg-slate-900/40" />
      </div>

      <div className="container mx-auto px-4 md:px-8 lg:px-16 py-8 md:py-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
          {/* Left: Contact detail cards */}
          <div className="space-y-4">
            <ContactCard
              icon={
                <svg viewBox="0 0 24 24" className="h-6 w-6 text-white" fill="none" stroke="currentColor" strokeWidth="1.8">
                  <path d="M12 21s-7-4.35-7-10a7 7 0 1 1 14 0c0 5.65-7 10-7 10z" />
                  <circle cx="12" cy="11" r="2.5" />
                </svg>
              }
              title="Address Details"
              lines={["1520 North Kierland Bl.100 Old City"]}
            />
            <ContactCard
              icon={
                <svg viewBox="0 0 24 24" className="h-6 w-6 text-white" fill="none" stroke="currentColor" strokeWidth="1.8">
                  <path d="M22 16.92V21a1 1 0 0 1-1.09 1A19.86 19.86 0 0 1 3 5.09 1 1 0 0 1 4 4h4.09A1 1 0 0 1 9 4.91a12.44 12.44 0 0 0 6.59 6.59A1 1 0 0 1 16.09 12V16a1 1 0 0 1-.91 1H15" />
                </svg>
              }
              title="Contact No"
              lines={["0123 - 4567 - 890"]}
            />
            <ContactCard
              icon={
                <svg viewBox="0 0 24 24" className="h-6 w-6 text-white" fill="none" stroke="currentColor" strokeWidth="1.8">
                  <path d="M4 4h16v16H4z" />
                  <path d="m22 6-10 7L2 6" />
                </svg>
              }
              title="Email Details"
              lines={["support@mail.com"]}
            />
          </div>

          {/* Right: Form */}
          <div className="bg-white/95 backdrop-blur rounded-lg shadow-xl p-6 md:p-8">
            <h1 className="text-xl md:text-2xl font-semibold text-slate-900">Get In Touch</h1>
            <div className="h-0.5 w-12 bg-indigo-500 my-3" />
            <form onSubmit={onSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input label="Name" required value={form.name} onChange={(v)=>setForm({ ...form, name: v })} />
                <Input label="Email" type="email" required value={form.email} onChange={(v)=>setForm({ ...form, email: v })} />
              </div>
              <Input label="Subject" required value={form.subject} onChange={(v)=>setForm({ ...form, subject: v })} />
              <Textarea label="Message" rows={6} required value={form.message} onChange={(v)=>setForm({ ...form, message: v })} />

              {/* reCAPTCHA placeholder */}
              <label className="flex items-center gap-3 text-sm text-slate-700">
                <input type="checkbox" className="h-4 w-4" checked={form.captcha} onChange={(e)=>setForm({ ...form, captcha: e.target.checked })} />
                I'm not a robot (demo)
                <span className="ml-auto inline-flex items-center justify-center rounded bg-slate-200 px-2 py-1 text-xs text-slate-700">reCAPTCHA</span>
              </label>

              <button disabled={submitting} className="w-full rounded bg-indigo-600 hover:bg-indigo-500 disabled:opacity-60 text-white font-medium py-2.5">
                {submitting ? 'Sending…' : 'Send Message'}
              </button>
              {result && (
                <div className={"text-sm " + (result.ok ? 'text-green-600' : 'text-red-600')}>{result.msg}</div>
              )}
              <p className="text-xs text-slate-500">Note: Background image is a demo. Replace 
                <code className="mx-1">/public/images/support-demo.svg</code> with your real background later.
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

function ContactCard({ icon, title, lines }: { icon: React.ReactNode; title: string; lines: string[] }) {
  return (
    <div className="flex items-center gap-4 rounded-lg bg-white/10 backdrop-blur border border-white/20 p-4 text-white">
      <div className="flex h-10 w-10 items-center justify-center rounded-full bg-indigo-600 shadow-inner">
        {icon}
      </div>
      <div>
        <div className="text-sm opacity-90">{title}</div>
        {lines.map((l, i) => (
          <div key={i} className="text-sm md:text-[15px] opacity-80">{l}</div>
        ))}
      </div>
    </div>
  )
}

function Input({ label, value, onChange, type='text', required=false }: { label: string; value: string; onChange: (v: string)=>void; type?: string; required?: boolean }) {
  return (
    <label className="block text-sm">
      <span className="text-slate-700">{label}{required && <span className="text-red-500"> *</span>}</span>
      <input
        type={type}
        value={value}
        onChange={(e)=>onChange(e.target.value)}
        required={required}
        className="mt-1 w-full rounded border border-slate-300 bg-white px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500"
      />
    </label>
  )
}

function Textarea({ label, value, onChange, rows=4, required=false }: { label: string; value: string; onChange: (v: string)=>void; rows?: number; required?: boolean }) {
  return (
    <label className="block text-sm">
      <span className="text-slate-700">{label}{required && <span className="text-red-500"> *</span>}</span>
      <textarea
        value={value}
        onChange={(e)=>onChange(e.target.value)}
        required={required}
        rows={rows}
        className="mt-1 w-full rounded border border-slate-300 bg-white px-3 py-2 outline-none focus:ring-2 focus:ring-indigo-500"
      />
    </label>
  )
}
