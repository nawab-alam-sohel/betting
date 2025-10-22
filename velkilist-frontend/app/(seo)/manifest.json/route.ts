export const runtime = 'edge'

export function GET() {
  const json = {
    name: 'VelkiList',
    short_name: 'Velki',
    start_url: '/',
    display: 'standalone',
    background_color: '#0b1220',
    theme_color: '#0B5FFF',
    icons: [
      { src: '/favicon.ico', sizes: 'any', type: 'image/x-icon' }
    ]
  }
  return new Response(JSON.stringify(json), { headers: { 'Content-Type': 'application/manifest+json' } })
}
