import axios from '@/lib/axiosInstance'

export type SupportTicketPayload = {
  name: string
  email: string
  subject: string
  message: string
  captchaToken?: string
}

export type SupportTicketResponse = {
  ok: boolean
  id?: number | string
  message?: string
}

export async function createSupportTicket(payload: SupportTicketPayload): Promise<SupportTicketResponse> {
  try {
    const { data } = await axios.post('/api/support/tickets/', payload)
    return { ok: true, ...data }
  } catch (err: any) {
    // Backend ticketing is not available yet in this project; surface a friendly message
    const status = err?.response?.status
    if (status === 404) {
      return {
        ok: false,
        message: 'Support ticket API is not enabled on the server yet. Please contact support@domain.com',
      }
    }
    return { ok: false, message: err?.response?.data?.detail || err?.message || 'Failed to submit ticket' }
  }
}
