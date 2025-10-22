import { NextResponse } from 'next/server'

const staticUrls = ['/', '/sportsbook', '/casino', '/wallet', '/support', '/login', '/register', '/admin/dashboard']

export async function GET() {
  const origin = process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'
  const now = new Date().toISOString()
  const items = staticUrls.map(u => `<url><loc>${origin}${u}</loc><lastmod>${now}</lastmod><changefreq>daily</changefreq><priority>0.7</priority></url>`).join('')
  const xml = `<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${items}</urlset>`
  return new NextResponse(xml, { headers: { 'Content-Type': 'application/xml' } })
}
