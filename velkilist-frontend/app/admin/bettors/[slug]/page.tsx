// @ts-nocheck
export default function BettorsPlaceholder({ params }: { params: { slug: string } }) {
  const title = (params.slug || '').split('-').map(s=>s[0]?.toUpperCase()+s.slice(1)).join(' ')
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
      <div className="text-lg font-semibold">{title || 'Bettors'}</div>
      <div className="text-sm text-slate-400 mt-1">This section will list bettors filtered by: {params.slug}.</div>
    </div>
  )
}
