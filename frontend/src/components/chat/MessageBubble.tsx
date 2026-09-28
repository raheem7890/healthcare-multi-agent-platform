import type { ChatMessage } from '../../stores/chatStore'
import { EmergencyAlert } from './EmergencyAlert'

export function MessageBubble({ message }: { message: ChatMessage }) {
  if (message.response?.urgency === 'emergency') {
    return <EmergencyAlert text={message.text} />
  }
  return (
    <article className={`message ${message.role}`}>
      <div className="message-meta">
        {message.role === 'user' ? 'You' : message.response?.agent.replaceAll('_', ' ') ?? 'Assistant'}
      </div>
      <p>{message.text}</p>
      {message.response && (
        <>
          <div className={`urgency ${message.response.urgency}`}>{message.response.urgency}</div>
          <p className="recommended"><strong>Next step:</strong> {message.response.recommended_action}</p>
          {message.response.disclaimer && <small>{message.response.disclaimer}</small>}
        </>
      )}
    </article>
  )
}

