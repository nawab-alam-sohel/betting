"use client"

import { useEffect, useMemo, useState } from 'react'
import { numbers } from '@/lib/whatsappNumbers'
import { motion } from 'framer-motion'

function shuffle<T>(arr: T[]): T[] {
  const a = arr.slice()
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

export default function WhatsAppButton() {
  const order = useMemo(() => shuffle(numbers), [])
  const [index, setIndex] = useState(0)

  useEffect(() => {
    const t = setInterval(() => setIndex(i => (i + 1) % order.length), 60000)
    return () => clearInterval(t)
  }, [order.length])

  const current = order[index]
  const href = `https://wa.me/${current.replace(/[^0-9]/g, '')}?text=${encodeURIComponent('Hello, I need support.')}`

  return (
    <motion.a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      aria-label="Contact us on WhatsApp"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="fixed bottom-5 right-5 z-40 h-14 w-14 rounded-full bg-[#00a6ff] text-white shadow-lg shadow-[#00a6ff]/50 ring-2 ring-[#00a6ff]/70 flex items-center justify-center"
      title={`Chat: ${current}`}
    >
      {/* Icon */}
      <svg viewBox="0 0 32 32" className="h-7 w-7 fill-white" aria-hidden>
        <path d="M19.11 17.04c-.33-.17-1.98-.98-2.29-1.1-.31-.11-.54-.17-.77.17-.23.33-.88 1.1-1.08 1.32-.2.22-.4.25-.73.08-.33-.17-1.4-.51-2.68-1.62-.99-.88-1.66-1.96-1.85-2.29-.19-.33-.02-.51.15-.68.16-.16.36-.42.54-.63.18-.21.24-.36.36-.6.12-.24.07-.45-.03-.63-.11-.17-.77-1.85-1.06-2.54-.28-.68-.57-.59-.77-.59-.2 0-.43-.02-.66-.02-.23 0-.61.09-.93.45-.33.36-1.22 1.19-1.22 2.9 0 1.7 1.25 3.34 1.43 3.57.18.24 2.46 3.77 5.97 5.13.83.36 1.47.58 1.97.74.83.27 1.58.23 2.17.14.66-.1 1.98-.81 2.26-1.6.28-.79.28-1.48.2-1.62-.07-.14-.27-.22-.6-.39z" />
        <path d="M27.1 4.9C24.2 2 20.3.5 16.2.5 7.9.5 1.2 7.2 1.2 15.5c0 2.6.7 5.2 2 7.4L1 31l8.3-2.2c2.1 1.2 4.6 1.8 7 1.8 8.3 0 15-6.7 15-15 0-4-1.6-7.8-4.5-10.7zm-10.9 24c-2.3 0-4.6-.6-6.6-1.7l-.5-.3-4.9 1.3 1.3-4.8-.3-.5C3 21.1 2.4 18.9 2.4 16.5c0-7.6 6.2-13.8 13.8-13.8 3.7 0 7.2 1.4 9.8 4.1 2.6 2.6 4.1 6.1 4.1 9.8 0 7.6-6.2 13.9-13.8 13.9z" />
      </svg>
    </motion.a>
  )
}
