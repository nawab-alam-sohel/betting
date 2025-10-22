export const runtime = 'edge'

export function GET() {
  const body = `User-agent: *\nAllow: /\nSitemap: ${process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'}/sitemap.xml\n`
  return new Response(body, { headers: { 'Content-Type': 'text/plain' } })
}
