// @ts-nocheck
"use client"

import { useEffect } from 'react'

export default function CustomCssInjector() {
  useEffect(() => {
    let el: HTMLStyleElement | null = null
    const run = async () => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || ''}/api/cms/settings/`)
        if (!res.ok) return
        const data = await res.json()
        const css = data?.custom_css?.trim()
        if (css) {
          el = document.createElement('style')
          el.setAttribute('data-custom-css', '1')
          el.innerHTML = css
          document.head.appendChild(el)
        }
      } catch {}
    }
    run()
    return () => { if (el && el.parentNode) el.parentNode.removeChild(el) }
  }, [])
  return null
}
