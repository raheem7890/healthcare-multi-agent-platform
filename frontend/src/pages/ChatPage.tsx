import { FormEvent, useEffect, useRef, useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { sendChatMessage } from '../api/chat'
import { MessageBubble } from '../components/chat/MessageBubble'
import { ProfileSelector } from '../components/common/ProfileSelector'
import { useChatStore } from '../stores/chatStore'

export function ChatPage() {
  const [draft, setDraft] = useState('')
  const endRef = useRef<HTMLDivElement>(null)
  const { sessionId, selectedProfileId, setSelectedProfileId, messages, addMessage, reset } = useChatStore()
  const mutation = useMutation({ mutationFn: sendChatMessage })

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function submit(event: FormEvent) {
    event.preventDefault()
    const text = draft.trim()
    if (!text || mutation.isPending) return
    setDraft('')
    addMessage({ id: crypto.randomUUID(), role: 'user', text })
    try {
      const response = await mutation.mutateAsync({
        session_id: sessionId,
        profile_id: selectedProfileId,
        message: text,
      })
      addMessage({ id: response.request_id, role: 'assistant', text: response.response, response })
    } catch (error) {
      addMessage({
        id: crypto.randomUUID(),
        role: 'assistant',
        text: error instanceof Error ? error.message : 'The assistant is unavailable. Please try again.',
      })
    }
  }

  const latestQuestions = [...messages].reverse().find((message) => message.response)?.response?.follow_up_questions ?? []

  return (
    <div className="page chat-page">
      <header className="page-header compact">
        <div><span className="eyebrow">Care chat</span><h1>Talk with the right care assistant</h1></div>
        <button className="button secondary" onClick={reset}>New conversation</button>
      </header>
      <ProfileSelector value={selectedProfileId} onChange={setSelectedProfileId} />
      <section className="chat-panel" aria-live="polite">
        {messages.length === 0 && (
          <div className="empty-state"><div className="empty-icon">+</div><h2>Start with what’s concerning you</h2>
            <p>We’ll route your question to general, baby, maternity, or appointment support.</p></div>
        )}
        {messages.map((message) => <MessageBubble key={message.id} message={message} />)}
        {mutation.isPending && <div className="typing">Finding the right care path…</div>}
        <div ref={endRef} />
      </section>
      {latestQuestions.length > 0 && (
        <div className="suggestion-row">
          {latestQuestions.map((question) => <button key={question} onClick={() => setDraft(question)}>{question}</button>)}
        </div>
      )}
      <form className="composer" onSubmit={submit}>
        <label className="sr-only" htmlFor="chat-message">Message</label>
        <textarea id="chat-message" value={draft} onChange={(event) => setDraft(event.target.value)}
          placeholder="Describe your question or ask to book an appointment…" maxLength={4000} rows={2} />
        <button className="button primary" disabled={!draft.trim() || mutation.isPending}>Send</button>
      </form>
    </div>
  )
}
