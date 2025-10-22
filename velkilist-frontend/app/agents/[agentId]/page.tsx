import { get } from '@/lib/api'

export default async function AgentDetail({ params }: { params: { agentId: string } }) {
  let detail: any = {}
  try { detail = await get(`/api/agents/${params.agentId}/`) } catch {}
  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Agent #{params.agentId}</h1>
      <pre className="text-sm text-slate-300 bg-slate-900 border border-slate-800 rounded p-4 overflow-auto">{JSON.stringify(detail, null, 2)}</pre>
    </div>
  )
}
