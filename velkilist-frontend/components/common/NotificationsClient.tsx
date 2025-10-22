"use client"

import { useEffect, useState } from 'react'
import { getUnreadCount } from '@/services/notificationsService'

export default function NotificationsClient() {
  const [count, setCount] = useState<number>(0)
  const [available, setAvailable] = useState<boolean>(true)

  useEffect(() => {
    let mounted = true
    const tick = async () => {
      const res = await getUnreadCount()
      if (!mounted) return
      if (res.ok) {
        setAvailable(true)
        setCount(res.count)
      } else {
        // graceful: mark as unavailable but don't spam UI
        setAvailable(false)
      }
    }
    tick()
    const t = setInterval(tick, 30000)
    return () => { mounted = false; clearInterval(t) }
  }, [])

  if (!available && count === 0) return null

  return (
    <a href="/notifications" className="fixed top-4 right-4 z-40">
      <div className="relative">
        <div className="h-10 w-10 rounded-full bg-slate-800/80 border border-slate-700 backdrop-blur flex items-center justify-center text-slate-200">
          {/* bell icon */}
          <svg viewBox="0 0 24 24" className="h-5 w-5" fill="currentColor" aria-hidden>
            <path d="M12 22a2.5 2.5 0 0 0 2.5-2.5h-5A2.5 2.5 0 0 0 12 22z"/>
            <path d="M18 16v-5a6 6 0 1 0-12 0v5l-2 2v1h16v-1l-2-2z"/>
          </svg>
        </div>
        {count > 0 && (
          <span className="absolute -top-1 -right-1 min-w-5 h-5 px-1 rounded-full bg-rose-500 text-white text-xs font-bold flex items-center justify-center">{count}</span>
        )}
      </div>
    </a>
  )
}
