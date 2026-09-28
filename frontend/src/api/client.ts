const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
const DEV_USER_ID = import.meta.env.VITE_DEV_USER_ID ?? 'local-demo-user'

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
  }
}

export async function apiRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      'X-User-ID': DEV_USER_ID,
      ...init.headers,
    },
  })

  if (!response.ok) {
    const payload = await response.json().catch(() => ({ detail: 'Request failed' }))
    throw new ApiError(response.status, payload.detail ?? 'Request failed')
  }

  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}

