import { NextResponse } from 'next/server'

export async function GET() {
  try {
    const apiBase = process.env.INTERNAL_API_BASE_URL || process.env.NEXT_PUBLIC_API_BASE_URL
    const res = apiBase ? await fetch(`${apiBase}/api/cms/settings/`, { cache: 'no-store' }) : null
    const data = res && res.ok ? await res.json() : null
    const robots = (data?.robots_txt || '').trim()
    if (robots) {
      return new NextResponse(robots, { headers: { 'Content-Type': 'text/plain' } })
    }
  } catch {}
  // default allow all
  const fallback = `User-agent: *\nAllow: /\n`
  return new NextResponse(fallback, { headers: { 'Content-Type': 'text/plain' } })
}
