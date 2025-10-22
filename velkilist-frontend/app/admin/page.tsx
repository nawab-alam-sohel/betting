import { get } from '@/lib/api'

export default async function AdminHome() {
  let summary: any = {}
  try { summary = await get('/api/admin/dashboard/summary/') } catch {}
  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Admin Dashboard</h1>
      <pre className="text-sm text-slate-300 bg-slate-900 border border-slate-800 rounded p-4 overflow-auto">{JSON.stringify(summary, null, 2)}</pre>
    </div>
  )
}
