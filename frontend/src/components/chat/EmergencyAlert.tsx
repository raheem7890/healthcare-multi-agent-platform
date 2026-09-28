export function EmergencyAlert({ text }: { text: string }) {
  return (
    <div className="emergency-alert" role="alert">
      <strong>Get immediate help</strong>
      <p>{text}</p>
    </div>
  )
}

