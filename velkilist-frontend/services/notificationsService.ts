import axiosInstance from '@/lib/axiosInstance'

export async function getUnreadCount(): Promise<{ ok: boolean; count: number; message?: string }>{
  try {
    const res = await axiosInstance.get('/api/notifications/unread_count/')
    if (typeof res.data?.count === 'number') return { ok: true, count: res.data.count }
    // fallback: try list endpoint and count unread
    const list = await axiosInstance.get('/api/notifications/')
    const items = Array.isArray(list.data) ? list.data : []
    const count = items.filter((n: any) => !n.read).length
    return { ok: true, count }
  } catch (e: any) {
    return { ok: false, count: 0, message: e?.message || 'notifications unavailable' }
  }
}
