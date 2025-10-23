import { get } from '@/lib/api'

export default async function AgentsPage() {
  // Assuming an endpoint for agents exists later; fallback to placeholder
  let agents: any[] = []
  try { agents = await get('/api/agents/') } catch {}
  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Agents</h1>
      <pre className="text-sm text-slate-300 bg-slate-900 border border-slate-800 rounded p-4 overflow-auto">{JSON.stringify(agents, null, 2)}</pre>
    </div>
  )
}
