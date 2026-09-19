import { useAuth } from '../context/AuthContext'
import Icon from './Icon'

function initials(user) {
  if (!user) return '?'
  const value = `${user.first_name?.[0] || ''}${user.last_name?.[0] || ''}`
  return value.toUpperCase() || (user.email?.[0] || '?').toUpperCase()
}

export default function Topbar() {
  const { user, logout } = useAuth()
  return (
    <header className="topbar">
      <div>
        <h1>Dashboard</h1>
      </div>
      <div className="topbar-user">
        <span className="avatar">{initials(user)}</span>
        <div className="user-meta">
          <span className="user-name">{user?.full_name || user?.email}</span>
          <span className="user-role">{user?.role}</span>
        </div>
        <button className="logout-btn" onClick={logout} title="Sign out">
          <Icon name="logout" />
        </button>
      </div>
    </header>
  )
}
