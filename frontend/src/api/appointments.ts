import { apiRequest } from './client'
import type { Appointment, AppointmentSlot } from '../types'

export interface SlotSearchInput {
  profile_id: string
  specialty: string
  date_from: string
  date_to: string
  location?: string
}

export const listAppointments = () => apiRequest<Appointment[]>('/v1/appointments')
export const searchSlots = (payload: SlotSearchInput) =>
  apiRequest<AppointmentSlot[]>('/v1/appointments/slots/search', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
export const createAppointment = (profileId: string, slot: AppointmentSlot) =>
  apiRequest<Appointment>('/v1/appointments', {
    method: 'POST',
    body: JSON.stringify({
      profile_id: profileId,
      slot_id: slot.slot_id,
      provider_id: slot.provider_id,
      provider_name: slot.provider_name,
      specialty: slot.specialty,
      scheduled_at: slot.starts_at,
      confirmed: true,
    }),
  })
export const cancelAppointment = (id: string) =>
  apiRequest<Appointment>(`/v1/appointments/${id}`, {
    method: 'DELETE',
    body: JSON.stringify({ confirmed: true }),
  })
export const rescheduleAppointment = (id: string, scheduledAt: string) =>
  apiRequest<Appointment>(`/v1/appointments/${id}`, {
    method: 'PATCH',
    body: JSON.stringify({
      slot_id: `manual-${scheduledAt}`,
      scheduled_at: scheduledAt,
      confirmed: true,
    }),
  })
