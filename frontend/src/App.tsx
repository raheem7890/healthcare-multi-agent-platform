import { Navigate, Route, Routes } from 'react-router-dom'
import { AppShell } from './components/layout/AppShell'
import { AppointmentsPage } from './pages/AppointmentsPage'
import { ChatPage } from './pages/ChatPage'
import { DashboardPage } from './pages/DashboardPage'
import { MemoryPage } from './pages/MemoryPage'
import { PrivacyPage } from './pages/PrivacyPage'
import { ProfilesPage } from './pages/ProfilesPage'

export default function App() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route index element={<DashboardPage />} />
        <Route path="chat" element={<ChatPage />} />
        <Route path="appointments" element={<AppointmentsPage />} />
        <Route path="profiles" element={<ProfilesPage />} />
        <Route path="memory" element={<MemoryPage />} />
        <Route path="privacy" element={<PrivacyPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}

