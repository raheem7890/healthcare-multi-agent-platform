import { FormEvent, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { cancelAppointment, createAppointment, listAppointments, rescheduleAppointment, searchSlots } from '../api/appointments'
import { ProfileSelector } from '../components/common/ProfileSelector'
import type { AppointmentSlot } from '../types'

function localDate(daysFromNow: number) {
  const date = new Date()
  date.setDate(date.getDate() + daysFromNow)
  return date.toISOString().slice(0, 10)
}

export function AppointmentsPage() {
  const client = useQueryClient()
  const [profileId, setProfileId] = useState<string | null>(null)
  const [specialty, setSpecialty] = useState('General Care')
  const [from, setFrom] = useState(localDate(1))
  const [to, setTo] = useState(localDate(7))
  const [slots, setSlots] = useState<AppointmentSlot[]>([])
  const appointments = useQuery({ queryKey: ['appointments'], queryFn: listAppointments })
  const search = useMutation({ mutationFn: searchSlots, onSuccess: setSlots })
  const book = useMutation({
    mutationFn: ({ profileId, slot }: { profileId: string; slot: AppointmentSlot }) => createAppointment(profileId, slot),
    onSuccess: () => { setSlots([]); client.invalidateQueries({ queryKey: ['appointments'] }) },
  })
  const cancel = useMutation({ mutationFn: cancelAppointment, onSuccess: () => client.invalidateQueries({ queryKey: ['appointments'] }) })
  const reschedule = useMutation({
    mutationFn: ({ id, scheduledAt }: { id: string; scheduledAt: string }) => rescheduleAppointment(id, scheduledAt),
    onSuccess: () => client.invalidateQueries({ queryKey: ['appointments'] }),
  })

  async function submit(event: FormEvent) {
    event.preventDefault()
    if (!profileId) return
    await search.mutateAsync({
      profile_id: profileId,
      specialty,
      date_from: new Date(`${from}T00:00:00`).toISOString(),
      date_to: new Date(`${to}T23:59:59`).toISOString(),
    })
  }

  function confirmBooking(slot: AppointmentSlot) {
    if (!profileId) return
    const when = new Date(slot.starts_at).toLocaleString()
    if (window.confirm(`Confirm ${slot.specialty} with ${slot.provider_name} on ${when}?`)) {
      book.mutate({ profileId, slot })
    }
  }

  function requestReschedule(id: string) {
    const value = window.prompt('Enter the new local date and time (YYYY-MM-DDTHH:mm)')
    if (!value) return
    const date = new Date(value)
    if (Number.isNaN(date.getTime())) {
      window.alert('Enter a valid date and time.')
      return
    }
    if (window.confirm(`Reschedule to ${date.toLocaleString()}?`)) {
      reschedule.mutate({ id, scheduledAt: date.toISOString() })
    }
  }

  return (
    <div className="page">
      <header className="page-header"><div><span className="eyebrow">Scheduling</span><h1>Appointments</h1>
        <p>Find a suitable time and confirm before anything is booked.</p></div></header>
      <div className="two-column appointments-layout">
        <form className="panel form-stack" onSubmit={submit}><h2>Find a time</h2>
          <ProfileSelector value={profileId} onChange={setProfileId} required />
          <label className="field"><span>Specialty</span><select value={specialty} onChange={(e) => setSpecialty(e.target.value)}>
            <option>General Care</option><option>Pediatrics</option><option>Maternity</option><option>Postpartum Care</option>
          </select></label>
          <div className="field-row"><label className="field"><span>From</span><input type="date" value={from} onChange={(e) => setFrom(e.target.value)} required /></label>
            <label className="field"><span>To</span><input type="date" value={to} onChange={(e) => setTo(e.target.value)} required /></label></div>
          {search.error && <p className="form-error">{search.error.message}</p>}
          <button className="button primary" disabled={!profileId || search.isPending}>{search.isPending ? 'Searching…' : 'Search availability'}</button>
        </form>
        <section className="panel"><h2>Available times</h2>
          {slots.length === 0 ? <p className="muted">Search to see appointment times.</p> : <div className="stack">
            {slots.map((slot) => <article className="slot-card" key={slot.slot_id}><div><strong>{new Date(slot.starts_at).toLocaleString()}</strong>
              <span>{slot.provider_name} · {slot.location}</span></div><button className="button small" onClick={() => confirmBooking(slot)}>Choose</button></article>)}
          </div>}
        </section>
      </div>
      <section className="panel section-gap"><h2>Your appointments</h2>
        {appointments.data?.length ? <div className="stack">{appointments.data.map((appointment) => (
          <article className="list-card" key={appointment.id}><div><strong>{appointment.specialty}</strong>
            <span>{new Date(appointment.scheduled_at).toLocaleString()} · {appointment.provider_name} · {appointment.status}</span></div>
            {appointment.status !== 'cancelled' && <div className="inline-actions"><button className="text-button" onClick={() => requestReschedule(appointment.id)}>Reschedule</button>
              <button className="text-button danger" onClick={() => window.confirm('Cancel this appointment?') && cancel.mutate(appointment.id)}>Cancel</button></div>}
          </article>
        ))}</div> : <p className="muted">No appointments yet.</p>}
      </section>
    </div>
  )
}
