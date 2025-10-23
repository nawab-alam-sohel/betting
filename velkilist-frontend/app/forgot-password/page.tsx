// @ts-nocheck
'use client'

import { useState } from 'react'
import AuthLayout from '@/app/components/AuthLayout'
import { isValidEmail } from '@/lib/validators'

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [status, setStatus] = useState<'idle'|'loading'|'sent'|'error'>('idle')
  const [message, setMessage] = useState<string>('')
  const [captcha, setCaptcha] = useState(false)

  async function onSubmit(e: any) {
    e.preventDefault()
    setStatus('loading')
    setMessage('')
    try {
      if (!isValidEmail(email)) {
        throw new Error('Please enter a valid email address')
      }
      const base = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
      const res = await fetch(`${base}/api/users/password/reset/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      })
      if (!res.ok) throw new Error(await res.text())
      setStatus('sent')
      setMessage('If that email exists, a reset link has been sent.')
    } catch (err: any) {
      setStatus('error')
      setMessage(err?.message || 'Failed to send reset link')
    }
  }

  return (
    <AuthLayout title="Account recovery">
      <form onSubmit={onSubmit} className="space-y-4">
        <p className="text-sm text-slate-600">Enter your email and we'll send you a password reset link.</p>
        <div>
          <label className="block text-sm text-slate-700 mb-1">Email<span className="text-red-500"> *</span></label>
          <input type="email" value={email} onChange={(e)=>setEmail(e.target.value)} required placeholder="you@example.com" className="w-full rounded border border-slate-300 bg-white px-3 py-2" />
        </div>
        {/* reCAPTCHA demo */}
        <label className="flex items-center gap-3 text-sm text-slate-700 rounded border border-slate-300 bg-slate-50 p-3">
          <input type="checkbox" className="h-4 w-4" checked={captcha} onChange={(e)=>setCaptcha(e.target.checked)} />
          I'm not a robot (demo)
          <span className="ml-auto inline-flex items-center justify-center rounded bg-slate-200 px-2 py-1 text-xs text-slate-700">reCAPTCHA</span>
        </label>
        {message && (
          <div className={
            'text-sm ' +
            (status === 'sent' ? 'text-emerald-600' : status === 'error' ? 'text-red-600' : 'text-slate-600')
          }>{message}</div>
        )}
        <button type="submit" disabled={status==='loading'} className="w-full bg-indigo-600 hover:bg-indigo-500 disabled:opacity-60 text-white font-medium rounded px-3 py-2.5">
          {status==='loading' ? 'Sending…' : 'Send reset link'}
        </button>
        <div className="text-sm text-slate-700 text-center">
          Remembered your password? <a href="/login" className="text-indigo-600 hover:underline">Login</a>
        </div>
      </form>
    </AuthLayout>
  )
}
 
