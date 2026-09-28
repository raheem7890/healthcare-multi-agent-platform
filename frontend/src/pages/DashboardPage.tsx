import { Link } from 'react-router-dom'

const cards = [
  ['General care', 'Health education and guidance for everyday concerns.', '/chat'],
  ['Baby care', 'Age-aware support for parents and guardians.', '/chat'],
  ['Maternity care', 'Pregnancy and postpartum education and navigation.', '/chat'],
  ['Appointments', 'Find, confirm, review, and cancel appointments.', '/appointments'],
]

export function DashboardPage() {
  return (
    <div className="page">
      <header className="page-header hero">
        <div><span className="eyebrow">Your care, coordinated</span><h1>How can we help today?</h1>
          <p>Choose a care path, ask a question, or arrange your next appointment.</p></div>
        <Link className="button primary" to="/chat">Start a conversation</Link>
      </header>
      <section className="card-grid" aria-label="Care options">
        {cards.map(([title, copy, to]) => (
          <Link className="feature-card" to={to} key={title}>
            <span className="feature-icon" aria-hidden="true">+</span>
            <h2>{title}</h2><p>{copy}</p><span className="card-link">Continue →</span>
          </Link>
        ))}
      </section>
      <div className="info-banner"><strong>Medical emergency?</strong> Contact your local emergency services now. Do not wait for a chat response.</div>
    </div>
  )
}

