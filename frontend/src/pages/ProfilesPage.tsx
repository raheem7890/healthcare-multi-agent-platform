import { FormEvent, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { createProfile, deleteProfile, listProfiles } from '../api/profiles'
import type { ProfileType } from '../types'

export function ProfilesPage() {
  const client = useQueryClient()
  const { data = [], isLoading } = useQuery({ queryKey: ['profiles'], queryFn: listProfiles })
  const [type, setType] = useState<ProfileType>('adult')
  const [name, setName] = useState('')
  const [dob, setDob] = useState('')
  const [dueDate, setDueDate] = useState('')
  const [consent, setConsent] = useState(false)
  const create = useMutation({ mutationFn: createProfile, onSuccess: () => client.invalidateQueries({ queryKey: ['profiles'] }) })
  const remove = useMutation({ mutationFn: deleteProfile, onSuccess: () => client.invalidateQueries({ queryKey: ['profiles'] }) })

  async function submit(event: FormEvent) {
    event.preventDefault()
    await create.mutateAsync({
      profile_type: type,
      display_name: name,
      date_of_birth: dob || undefined,
      pregnancy_due_date: type === 'maternity' && dueDate ? dueDate : undefined,
      relationship_to_user: ['baby', 'child'].includes(type) ? 'guardian' : 'self',
      memory_consent: consent,
    })
    setName(''); setDob(''); setDueDate(''); setConsent(false)
  }

  return (
    <div className="page">
      <header className="page-header"><div><span className="eyebrow">Household</span><h1>Care profiles</h1>
        <p>Use separate profiles so guidance and appointments stay attached to the right person.</p></div></header>
      <div className="two-column">
        <section className="panel"><h2>Your profiles</h2>
          {isLoading ? <p>Loading…</p> : data.length === 0 ? <p className="muted">No profiles yet.</p> : (
            <div className="stack">{data.map((profile) => (
              <article className="list-card" key={profile.id}><div><strong>{profile.display_name}</strong>
                <span>{profile.profile_type} · memory {profile.memory_consent ? 'allowed' : 'off'}</span></div>
                <button className="text-button danger" onClick={() => window.confirm('Delete this profile?') && remove.mutate(profile.id)}>Delete</button>
              </article>
            ))}</div>
          )}
        </section>
        <form className="panel form-stack" onSubmit={submit}><h2>Add a profile</h2>
          <label className="field"><span>Profile type</span><select value={type} onChange={(e) => setType(e.target.value as ProfileType)}>
            <option value="adult">Adult</option><option value="baby">Baby</option><option value="child">Child</option><option value="maternity">Maternity</option>
          </select></label>
          <label className="field"><span>Name</span><input value={name} onChange={(e) => setName(e.target.value)} required maxLength={255} /></label>
          <label className="field"><span>Date of birth</span><input type="date" value={dob} onChange={(e) => setDob(e.target.value)} /></label>
          {type === 'maternity' && <label className="field"><span>Estimated due date</span><input type="date" value={dueDate} onChange={(e) => setDueDate(e.target.value)} /></label>}
          <label className="check-field"><input type="checkbox" checked={consent} onChange={(e) => setConsent(e.target.checked)} />
            <span>Allow useful conversation summaries to be saved for future visits.</span></label>
          {create.error && <p className="form-error">{create.error.message}</p>}
          <button className="button primary" disabled={create.isPending}>{create.isPending ? 'Creating…' : 'Create profile'}</button>
        </form>
      </div>
    </div>
  )
}
