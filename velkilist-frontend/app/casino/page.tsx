// @ts-nocheck
import Image from 'next/image'
import { demoCasinoCategories, demoCasinoGames } from '@/lib/demoData'

export default function CasinoPage({ searchParams }: { searchParams?: Record<string, string> }) {
  const category = searchParams?.category
  const categories = demoCasinoCategories()
  const games = demoCasinoGames(category)

  return (
    <section className="space-y-6">
      <div className="overflow-hidden rounded">
        <Image src="https://placehold.co/1200x220/0b1220/ffffff?text=Casino+Banner" alt="Casino banner" width={1200} height={220} />
      </div>

      <div className="grid md:grid-cols-4 gap-4">
        {/* Filters */}
        <aside className="md:col-span-1 space-y-3">
          <div className="bg-white/5 p-4 rounded border border-white/10">
            <div className="text-sm opacity-80 mb-2">Categories</div>
            <div className="flex flex-wrap gap-2">
              {categories.map((c) => (
                <a key={c} href={`/casino?category=${encodeURIComponent(c)}`} className="px-2 py-1 bg-white/10 rounded text-xs hover:bg-white/20">
                  {c}
                </a>
              ))}
            </div>
          </div>
          <div className="bg-white/5 p-4 rounded border border-white/10">
            <div className="text-sm opacity-80">A–Z</div>
            <div className="mt-2 flex flex-wrap gap-2">
              {'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').map(ch => (
                <span key={ch} className="px-2 py-1 bg-white/10 rounded text-xs">{ch}</span>
              ))}
            </div>
          </div>
        </aside>

        {/* Games grid */}
        <div className="md:col-span-3 grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {games.map((g) => (
            <a key={g.id} href={`/casino/game/${g.id}`} className="bg-white/5 p-2 rounded border border-white/10 hover:border-white/20">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={g.image} alt={g.name} className="w-full h-40 object-cover rounded" />
              <div className="mt-2 text-sm opacity-90">{g.name}</div>
              <div className="text-xs opacity-70">{g.provider} • {g.category}{g.isNew ? ' • New' : ''}</div>
            </a>
          ))}
          {games.length === 0 && (
            <div className="text-slate-400">No games found.</div>
          )}
        </div>
      </div>
    </section>
  )
}
