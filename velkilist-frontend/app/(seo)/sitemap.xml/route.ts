export const runtime = 'edge'

export function GET() {
  const base = process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'
  const urls = ['/', '/sportsbook', '/casino', '/login']
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map(u => `<url><loc>${base}${u}</loc></url>`).join('')}\n</urlset>`
  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } })
}
