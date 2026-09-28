import { apiRequest } from './client'
import type { MemoryItem } from '../types'

export const listMemory = () => apiRequest<MemoryItem[]>('/v1/memory')
export const deleteMemory = (id: string) =>
  apiRequest<void>(`/v1/memory/${id}`, { method: 'DELETE' })

