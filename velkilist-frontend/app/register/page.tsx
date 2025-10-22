// @ts-nocheck
'use client'

import { useState } from 'react'
import AuthLayout from '@/app/components/AuthLayout'
import { isValidEmail } from '@/lib/validators'

export default function RegisterPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [captcha, setCaptcha] = useState(false)

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    try {
      if (!isValidEmail(email)) {
        throw new Error('Please enter a valid email address')
      }
      const base = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
      const res = await fetch(`${base}/api/users/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      if (!res.ok) throw new Error(await res.text())
      setSuccess(true)
    } catch (err: any) {
      setError(err.message || 'Registration failed')
    }
  }

  return (
    <AuthLayout title="Create your account">
      <form onSubmit={onSubmit} className="space-y-4">
        <div>
          <label className="block text-sm text-slate-700 mb-1">Email<span className="text-red-500"> *</span></label>
          <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" placeholder="you@example.com" className="w-full rounded border border-slate-300 bg-white px-3 py-2" required />
        </div>
        <div>
          <label className="block text-sm text-slate-700 mb-1">Password<span className="text-red-500"> *</span></label>
          <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="••••••••" className="w-full rounded border border-slate-300 bg-white px-3 py-2" required />
        </div>
        {/* reCAPTCHA demo */}
        <label className="flex items-center gap-3 text-sm text-slate-700 rounded border border-slate-300 bg-slate-50 p-3">
          <input type="checkbox" className="h-4 w-4" checked={captcha} onChange={(e)=>setCaptcha(e.target.checked)} />
          I'm not a robot (demo)
          <span className="ml-auto inline-flex items-center justify-center rounded bg-slate-200 px-2 py-1 text-xs text-slate-700">reCAPTCHA</span>
        </label>
        {error && <div className="text-red-600 text-sm">{error}</div>}
        {success && <div className="text-emerald-600 text-sm">Account created. You can sign in now.</div>}
        <button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded px-3 py-2.5">Create account</button>
        <div className="text-sm text-slate-700 text-center">
          Already have an account? <a href="/login" className="text-indigo-600 hover:underline">Login</a>
        </div>
      </form>
    </AuthLayout>
  )
}
