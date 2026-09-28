import { NavLink, Outlet } from 'react-router-dom'

const links = [
  ['/', 'Overview'],
  ['/chat', 'Care chat'],
  ['/appointments', 'Appointments'],
  ['/profiles', 'Profiles'],
  ['/memory', 'Memory'],
  ['/privacy', 'Privacy'],
]

export function AppShell() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">+</span>
          <div><strong>CareBridge</strong><small>Health assistant</small></div>
        </div>
        <nav aria-label="Primary navigation">
          {links.map(([to, label]) => (
            <NavLink key={to} to={to} end={to === '/'}>{label}</NavLink>
          ))}
        </nav>
        <div className="sidebar-note">For education and care navigation. Not a replacement for medical care.</div>
      </aside>
      <main className="main-content"><Outlet /></main>
    </div>
  )
}

