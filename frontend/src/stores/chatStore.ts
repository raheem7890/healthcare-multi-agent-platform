import { create } from 'zustand'
import type { ChatResponse } from '../types'

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  text: string
  response?: ChatResponse
}

interface ChatState {
  sessionId: string
  selectedProfileId: string | null
  messages: ChatMessage[]
  setSelectedProfileId: (id: string | null) => void
  addMessage: (message: ChatMessage) => void
  reset: () => void
}

const newSessionId = () => `session-${crypto.randomUUID()}`

export const useChatStore = create<ChatState>((set) => ({
  sessionId: newSessionId(),
  selectedProfileId: null,
  messages: [],
  setSelectedProfileId: (selectedProfileId) => set({ selectedProfileId }),
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  reset: () => set({ sessionId: newSessionId(), messages: [] }),
}))
