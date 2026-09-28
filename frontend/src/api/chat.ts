import { apiRequest } from './client'
import type { ChatResponse } from '../types'

export const sendChatMessage = (payload: {
  session_id: string
  profile_id: string | null
  message: string
}) => apiRequest<ChatResponse>('/v1/chat', { method: 'POST', body: JSON.stringify(payload) })

