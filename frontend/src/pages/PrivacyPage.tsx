export function PrivacyPage() {
  return (
    <div className="page narrow">
      <header className="page-header"><div><span className="eyebrow">Privacy & safety</span><h1>How your information is handled</h1></div></header>
      <section className="prose panel">
        <h2>Short-term conversation context</h2>
        <p>Recent messages are kept temporarily so the assistants can follow the current conversation. Production Redis sessions expire automatically.</p>
        <h2>Long-term memory</h2>
        <p>Useful summaries may be stored in the local SQLite database only for profiles where you have enabled memory consent. You can review and delete these from Saved memory.</p>
        <h2>Clinical limitations</h2>
        <p>The assistants provide education and care navigation. They do not diagnose, prescribe, or replace a licensed clinician. Emergency warning signs are routed to immediate-help guidance.</p>
        <h2>Appointments</h2>
        <p>No appointment is created, changed, or cancelled without an explicit confirmation.</p>
      </section>
    </div>
  )
}
