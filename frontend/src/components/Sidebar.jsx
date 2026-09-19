import { NavLink } from 'react-router-dom'
import Icon from './Icon'

// Only the dashboard is implemented in this scaffold; the rest are placeholders.
const NAV = [
  { to: '/dashboard', label: 'Dashboard', icon: 'dashboard', enabled: true },
  { to: '/students', label: 'Students', icon: 'students', enabled: false },
  { to: '/teachers', label: 'Teachers', icon: 'teachers', enabled: false },
  { to: '/classes', label: 'Classes', icon: 'classes', enabled: false },
  { to: '/courses', label: 'Courses', icon: 'courses', enabled: false },
  { to: '/attendance', label: 'Attendance', icon: 'attendance', enabled: false },
  { to: '/grades', label: 'Grades', icon: 'grades', enabled: false },
]

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-mark">SMS</div>
        <span>School MS</span>
      </div>

      <nav className="sidebar-nav">
        {NAV.map((item) =>
          item.enabled ? (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                isActive ? 'nav-item active' : 'nav-item'
              }
            >
              <Icon name={item.icon} />
              {item.label}
            </NavLink>
          ) : (
            <span key={item.to} className="nav-item disabled">
              <Icon name={item.icon} />
              {item.label}
              <span className="soon">soon</span>
            </span>
          ),
        )}
      </nav>

      <div className="sidebar-footer">v0.1 · React + Django</div>
    </aside>
  )
}
