import { apiRequest } from './client'
import type { Profile, ProfileType } from '../types'

export interface ProfileInput {
  profile_type: ProfileType
  display_name: string
  relationship_to_user?: string
  date_of_birth?: string
  pregnancy_due_date?: string
  medical_notes?: string
  memory_consent: boolean
}

export const listProfiles = () => apiRequest<Profile[]>('/v1/profiles')
export const createProfile = (payload: ProfileInput) =>
  apiRequest<Profile>('/v1/profiles', { method: 'POST', body: JSON.stringify(payload) })
export const deleteProfile = (id: string) =>
  apiRequest<void>(`/v1/profiles/${id}`, { method: 'DELETE' })

