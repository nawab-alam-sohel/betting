// @ts-nocheck
'use client'

import { useState } from 'react'
import AuthLayout from '@/app/components/AuthLayout'
import { isValidEmail } from '@/lib/validators'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [remember, setRemember] = useState(false)
  const [captcha, setCaptcha] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    try {
      // If user typed an email-like value, validate it; otherwise allow usernames
      if (email.includes('@') && !isValidEmail(email)) {
        throw new Error('Please enter a valid email address')
      }
      const base = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
      const res = await fetch(`${base}/api/users/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: email, password })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data?.detail || 'Login failed')
      localStorage.setItem('access_token', data.access)
      if (data.refresh) localStorage.setItem('refresh_token', data.refresh)
      if (remember) localStorage.setItem('remember_me', '1'); else localStorage.removeItem('remember_me')
      window.location.href = '/'
    } catch (err: any) {
      setError(err.message || 'Something went wrong')
    }
  }

  return (
    <AuthLayout title="Login to your account">
      <form onSubmit={onSubmit} className="space-y-4">
        <div>
          <label className="block text-sm text-slate-700 mb-1">Username or Email<span className="text-red-500"> *</span></label>
          <input value={email} onChange={e => setEmail(e.target.value)} type="text" placeholder="username or you@example.com" className="w-full rounded border border-slate-300 bg-white px-3 py-2" required />
        </div>
        <div>
          <label className="block text-sm text-slate-700 mb-1">Password<span className="text-red-500"> *</span></label>
          <input value={password} onChange={e => setPassword(e.target.value)} type="password" placeholder="••••••••" className="w-full rounded border border-slate-300 bg-white px-3 py-2" required />
        </div>
        {/* reCAPTCHA demo */}
        <div className="flex items-center gap-3 rounded border border-slate-300 bg-slate-50 p-3">
          <input id="captcha" type="checkbox" className="h-4 w-4" checked={captcha} onChange={(e)=>setCaptcha(e.target.checked)} />
          <label htmlFor="captcha" className="text-sm text-slate-700">I'm not a robot (demo)</label>
          <span className="ml-auto inline-flex items-center justify-center rounded bg-slate-200 px-2 py-1 text-xs text-slate-700">reCAPTCHA</span>
        </div>
        <div className="flex items-center justify-between text-sm">
          <label className="inline-flex items-center gap-2 text-slate-700">
            <input type="checkbox" checked={remember} onChange={(e)=>setRemember(e.target.checked)} className="h-4 w-4" />
            Remember Me
          </label>
          <a href="/forgot-password" className="text-indigo-600 hover:underline">Forgot Password?</a>
        </div>
        {error && <div className="text-red-600 text-sm">{error}</div>}
        <button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded px-3 py-2.5">Login</button>
        <div className="text-sm text-slate-700 text-center">
          Don't have account? <a href="/register" className="text-indigo-600 hover:underline">Create account</a>
        </div>
      </form>
    </AuthLayout>
  )
}
