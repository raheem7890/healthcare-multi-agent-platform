export type ProfileType = 'adult' | 'baby' | 'child' | 'maternity'

export interface Profile {
  id: string
  profile_type: ProfileType
  display_name: string
  relationship_to_user: string | null
  date_of_birth: string | null
  pregnancy_due_date: string | null
  medical_notes: string | null
  memory_consent: boolean
  created_at: string
  updated_at: string
}

export interface ChatResponse {
  request_id: string
  session_id: string
  agent: 'general_care' | 'baby_care' | 'maternity_care' | 'booking' | 'emergency'
  urgency: 'routine' | 'soon' | 'urgent' | 'emergency'
  response: string
  recommended_action: string
  follow_up_questions: string[]
  appointment_handoff_available: boolean
  disclaimer: string | null
}

export interface AppointmentSlot {
  slot_id: string
  provider_id: string
  provider_name: string
  specialty: string
  starts_at: string
  location: string
}

export interface Appointment {
  id: string
  profile_id: string
  provider_id: string
  provider_name: string
  specialty: string
  scheduled_at: string
  status: string
  booking_reference: string
  created_at: string
}

export interface MemoryItem {
  id: string
  profile_id: string | null
  memory_type: string
  summary_text: string
  importance_score: number
  created_at: string
}
