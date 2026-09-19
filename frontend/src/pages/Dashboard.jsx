import { useEffect, useState } from 'react'
import client from '../api/client'
import { useAuth } from '../context/AuthContext'
import Sidebar from '../components/Sidebar'
import Topbar from '../components/Topbar'
import StatCard from '../components/StatCard'

const STATS = [
  { key: 'students', label: 'Students', path: '/students/' },
  { key: 'teachers', label: 'Teachers', path: '/teachers/' },
  { key: 'classes', label: 'Classes', path: '/classes/' },
  { key: 'courses', label: 'Courses', path: '/courses/' },
]

export default function Dashboard() {
  const { user } = useAuth()
  const [counts, setCounts] = useState({})
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    Promise.all(STATS.map((s) => client.get(s.path)))
      .then((responses) => {
        if (!active) return
        const next = {}
        responses.forEach((res, i) => {
          next[STATS[i].key] = res.data.count
        })
        setCounts(next)
      })
      .catch(() => {
        if (active) setError('Could not load dashboard stats.')
      })
    return () => {
      active = false
    }
  }, [])

  return (
    <div className="app-shell">
      <Sidebar />
      <div className="app-main">
        <Topbar />
        <main className="content">
          <h2>Welcome back, {user?.first_name || user?.email}</h2>
          <p className="subtitle">Here's an overview of your school.</p>

          {error && <div className="alert-error">{error}</div>}

          <div className="stats-grid">
            {STATS.map((s) => (
              <StatCard key={s.key} label={s.label} value={counts[s.key]} />
            ))}
          </div>

          <div className="panel">
            <h3>Getting started</h3>
            <p>
              Manage students, teachers, classes, courses, attendance and grades
              from the sidebar. The remaining sections will be wired up as the
              pages are built.
            </p>
          </div>
        </main>
      </div>
    </div>
  )
}
