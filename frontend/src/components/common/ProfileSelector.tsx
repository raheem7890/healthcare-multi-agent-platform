import { useQuery } from '@tanstack/react-query'
import { listProfiles } from '../../api/profiles'

interface Props {
  value: string | null
  onChange: (id: string | null) => void
  required?: boolean
}

export function ProfileSelector({ value, onChange, required = false }: Props) {
  const { data = [], isLoading } = useQuery({ queryKey: ['profiles'], queryFn: listProfiles })
  return (
    <label className="field">
      <span>Patient profile</span>
      <select
        value={value ?? ''}
        onChange={(event) => onChange(event.target.value || null)}
        required={required}
        disabled={isLoading}
      >
        <option value="">{required ? 'Choose a profile' : 'No profile selected'}</option>
        {data.map((profile) => (
          <option key={profile.id} value={profile.id}>
            {profile.display_name} · {profile.profile_type}
          </option>
        ))}
      </select>
    </label>
  )
}

