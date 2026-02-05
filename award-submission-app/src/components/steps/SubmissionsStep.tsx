import { useState, useMemo } from 'react'
import {
  ClipboardList,
  Calendar,
  AlertTriangle,
  CheckCircle2,
  Clock,
  FileEdit,
  Eye,
  Send,
  Filter,
  ChevronDown,
  Plus,
  Trash2,
  Edit3
} from 'lucide-react'
import type { Submission, SubmissionStatus, SubmissionFilters } from '../../types'

interface SubmissionsStepProps {
  submissions: Submission[]
  onUpdateSubmission: (id: string, updates: Partial<Submission>) => void
  onDeleteSubmission: (id: string) => void
  onAddSubmission?: () => void
}

const STATUS_CONFIG: Record<SubmissionStatus, { label: string; color: string; icon: any; bgColor: string }> = {
  not_started: { label: 'Not Started', color: '#6b7280', icon: Clock, bgColor: 'rgba(107, 114, 128, 0.1)' },
  draft: { label: 'Draft', color: '#f59e0b', icon: FileEdit, bgColor: 'rgba(245, 158, 11, 0.1)' },
  in_review: { label: 'In Review', color: '#8b5cf6', icon: Eye, bgColor: 'rgba(139, 92, 246, 0.1)' },
  elt_approved: { label: 'ELT Approved', color: '#3b82f6', icon: CheckCircle2, bgColor: 'rgba(59, 130, 246, 0.1)' },
  client_approved: { label: 'Client Approved', color: '#22c55e', icon: CheckCircle2, bgColor: 'rgba(34, 197, 94, 0.1)' },
  submitted: { label: 'Submitted', color: '#10b981', icon: Send, bgColor: 'rgba(16, 185, 129, 0.1)' }
}

const STATUS_ORDER: SubmissionStatus[] = ['not_started', 'draft', 'in_review', 'elt_approved', 'client_approved', 'submitted']

function getDaysUntil(deadline: string): number {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const deadlineDate = new Date(deadline)
  deadlineDate.setHours(0, 0, 0, 0)
  return Math.ceil((deadlineDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24))
}

function getUrgencyLevel(days: number): 'critical' | 'soon' | 'comfortable' {
  if (days <= 7) return 'critical'
  if (days <= 14) return 'soon'
  return 'comfortable'
}

function getUrgencyColor(days: number): string {
  if (days <= 0) return '#ef4444' // overdue - red
  if (days <= 7) return '#ef4444' // critical - red
  if (days <= 14) return '#f59e0b' // soon - yellow
  return '#22c55e' // comfortable - green
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

export default function SubmissionsStep({
  submissions,
  onUpdateSubmission,
  onDeleteSubmission,
  onAddSubmission
}: SubmissionsStepProps) {
  const [filters, setFilters] = useState<SubmissionFilters>({
    status: 'all',
    award: 'all',
    urgency: 'all'
  })
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editingNotes, setEditingNotes] = useState('')

  // Get unique awards for filter dropdown
  const uniqueAwards = useMemo(() => {
    const awards = new Set(submissions.map(s => s.awardName))
    return Array.from(awards).sort()
  }, [submissions])

  // Filter submissions
  const filteredSubmissions = useMemo(() => {
    return submissions.filter(sub => {
      if (filters.status !== 'all' && sub.status !== filters.status) return false
      if (filters.award !== 'all' && sub.awardName !== filters.award) return false
      if (filters.urgency !== 'all') {
        const days = getDaysUntil(sub.deadline)
        const urgency = getUrgencyLevel(days)
        if (filters.urgency !== urgency) return false
      }
      return true
    }).sort((a, b) => new Date(a.deadline).getTime() - new Date(b.deadline).getTime())
  }, [submissions, filters])

  // Stats
  const stats = useMemo(() => {
    const total = submissions.length
    const submitted = submissions.filter(s => s.status === 'submitted').length
    const inProgress = submissions.filter(s => ['draft', 'in_review', 'elt_approved', 'client_approved'].includes(s.status)).length
    const notStarted = submissions.filter(s => s.status === 'not_started').length
    const critical = submissions.filter(s => getDaysUntil(s.deadline) <= 7 && s.status !== 'submitted').length
    const totalCost = submissions.reduce((sum, s) => sum + (s.entryCost || 0), 0)
    return { total, submitted, inProgress, notStarted, critical, totalCost }
  }, [submissions])

  const handleStatusChange = (id: string, newStatus: SubmissionStatus) => {
    onUpdateSubmission(id, { status: newStatus, lastUpdated: new Date().toISOString() })
  }

  const handleNotesEdit = (id: string, notes: string) => {
    setEditingId(id)
    setEditingNotes(notes || '')
  }

  const handleNotesSave = (id: string) => {
    onUpdateSubmission(id, { notes: editingNotes, lastUpdated: new Date().toISOString() })
    setEditingId(null)
    setEditingNotes('')
  }

  return (
    <div className="submissions-step">
      {/* Header */}
      <div className="step-header">
        <div className="step-icon">
          <ClipboardList size={24} />
        </div>
        <div>
          <h2>My Submissions</h2>
          <p>Track your award submission progress across all campaigns</p>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="submissions-stats">
        <div className="stat-card">
          <div className="stat-value">{stats.total}</div>
          <div className="stat-label">Total Entries</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: '#22c55e' }}>{stats.submitted}</div>
          <div className="stat-label">Submitted</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: '#8b5cf6' }}>{stats.inProgress}</div>
          <div className="stat-label">In Progress</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: '#ef4444' }}>{stats.critical}</div>
          <div className="stat-label">Due This Week</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">${stats.totalCost.toLocaleString()}</div>
          <div className="stat-label">Total Entry Cost</div>
        </div>
      </div>

      {/* Filters */}
      <div className="submissions-filters">
        <div className="filter-group">
          <Filter size={16} />
          <span>Filter:</span>
        </div>

        <div className="filter-select">
          <label>Status</label>
          <select
            value={filters.status}
            onChange={(e) => setFilters({ ...filters, status: e.target.value as any })}
          >
            <option value="all">All Statuses</option>
            {STATUS_ORDER.map(status => (
              <option key={status} value={status}>{STATUS_CONFIG[status].label}</option>
            ))}
          </select>
          <ChevronDown size={14} />
        </div>

        <div className="filter-select">
          <label>Award</label>
          <select
            value={filters.award}
            onChange={(e) => setFilters({ ...filters, award: e.target.value })}
          >
            <option value="all">All Awards</option>
            {uniqueAwards.map(award => (
              <option key={award} value={award}>{award}</option>
            ))}
          </select>
          <ChevronDown size={14} />
        </div>

        <div className="filter-select">
          <label>Urgency</label>
          <select
            value={filters.urgency}
            onChange={(e) => setFilters({ ...filters, urgency: e.target.value as any })}
          >
            <option value="all">All</option>
            <option value="critical">Critical (≤7 days)</option>
            <option value="soon">Soon (8-14 days)</option>
            <option value="comfortable">Comfortable (15+ days)</option>
          </select>
          <ChevronDown size={14} />
        </div>

        {onAddSubmission && (
          <button className="btn-add-submission" onClick={onAddSubmission}>
            <Plus size={16} />
            Add Entry
          </button>
        )}
      </div>

      {/* Submissions Table */}
      <div className="submissions-table-container">
        <table className="submissions-table">
          <thead>
            <tr>
              <th>Campaign</th>
              <th>Award</th>
              <th>Category</th>
              <th>Deadline</th>
              <th>Days Left</th>
              <th>Status</th>
              <th>Cost</th>
              <th>Notes</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredSubmissions.length === 0 ? (
              <tr>
                <td colSpan={9} className="empty-state">
                  <ClipboardList size={48} />
                  <p>No submissions match your filters</p>
                </td>
              </tr>
            ) : (
              filteredSubmissions.map((sub) => {
                const daysLeft = getDaysUntil(sub.deadline)
                const urgencyColor = getUrgencyColor(daysLeft)
                const StatusIcon = STATUS_CONFIG[sub.status].icon

                return (
                  <tr key={sub.id} className={daysLeft <= 7 && sub.status !== 'submitted' ? 'urgent-row' : ''}>
                    <td className="campaign-cell">
                      <div className="campaign-name">{sub.campaignName}</div>
                      <div className="submitted-by">by {sub.submittedBy.toUpperCase()}</div>
                    </td>
                    <td className="award-cell">{sub.awardName}</td>
                    <td className="category-cell">{sub.category}</td>
                    <td className="deadline-cell">
                      <Calendar size={14} />
                      {formatDate(sub.deadline)}
                    </td>
                    <td className="days-cell">
                      <span
                        className="days-badge"
                        style={{ backgroundColor: urgencyColor + '20', color: urgencyColor }}
                      >
                        {daysLeft <= 0 ? (
                          <>
                            <AlertTriangle size={12} />
                            Overdue
                          </>
                        ) : daysLeft === 1 ? (
                          '1 day'
                        ) : (
                          `${daysLeft} days`
                        )}
                      </span>
                    </td>
                    <td className="status-cell">
                      <div
                        className="status-dropdown"
                        style={{
                          backgroundColor: STATUS_CONFIG[sub.status].bgColor,
                          borderColor: STATUS_CONFIG[sub.status].color + '40'
                        }}
                      >
                        <StatusIcon size={14} style={{ color: STATUS_CONFIG[sub.status].color }} />
                        <select
                          value={sub.status}
                          onChange={(e) => handleStatusChange(sub.id, e.target.value as SubmissionStatus)}
                          style={{ color: STATUS_CONFIG[sub.status].color }}
                        >
                          {STATUS_ORDER.map(status => (
                            <option key={status} value={status}>{STATUS_CONFIG[status].label}</option>
                          ))}
                        </select>
                        <ChevronDown size={12} style={{ color: STATUS_CONFIG[sub.status].color }} />
                      </div>
                    </td>
                    <td className="cost-cell">
                      {sub.entryCost ? `$${sub.entryCost}` : '-'}
                    </td>
                    <td className="notes-cell">
                      {editingId === sub.id ? (
                        <div className="notes-edit">
                          <input
                            type="text"
                            value={editingNotes}
                            onChange={(e) => setEditingNotes(e.target.value)}
                            placeholder="Add note..."
                            autoFocus
                            onKeyDown={(e) => {
                              if (e.key === 'Enter') handleNotesSave(sub.id)
                              if (e.key === 'Escape') setEditingId(null)
                            }}
                          />
                          <button onClick={() => handleNotesSave(sub.id)}>Save</button>
                        </div>
                      ) : (
                        <div
                          className="notes-display"
                          onClick={() => handleNotesEdit(sub.id, sub.notes || '')}
                        >
                          {sub.notes || <span className="placeholder">Add note...</span>}
                        </div>
                      )}
                    </td>
                    <td className="actions-cell">
                      <button
                        className="action-btn edit"
                        onClick={() => handleNotesEdit(sub.id, sub.notes || '')}
                        title="Edit notes"
                      >
                        <Edit3 size={14} />
                      </button>
                      <button
                        className="action-btn delete"
                        onClick={() => {
                          if (confirm('Remove this submission entry?')) {
                            onDeleteSubmission(sub.id)
                          }
                        }}
                        title="Delete"
                      >
                        <Trash2 size={14} />
                      </button>
                    </td>
                  </tr>
                )
              })
            )}
          </tbody>
        </table>
      </div>

      {/* Legend */}
      <div className="submissions-legend">
        <div className="legend-section">
          <span className="legend-title">Status:</span>
          {STATUS_ORDER.map(status => {
            const config = STATUS_CONFIG[status]
            const Icon = config.icon
            return (
              <div key={status} className="legend-item">
                <Icon size={12} style={{ color: config.color }} />
                <span>{config.label}</span>
              </div>
            )
          })}
        </div>
        <div className="legend-section">
          <span className="legend-title">Urgency:</span>
          <div className="legend-item">
            <span className="urgency-dot" style={{ backgroundColor: '#ef4444' }} />
            <span>≤7 days</span>
          </div>
          <div className="legend-item">
            <span className="urgency-dot" style={{ backgroundColor: '#f59e0b' }} />
            <span>8-14 days</span>
          </div>
          <div className="legend-item">
            <span className="urgency-dot" style={{ backgroundColor: '#22c55e' }} />
            <span>15+ days</span>
          </div>
        </div>
      </div>

      <style>{`
        .submissions-step {
          max-width: 1400px;
        }

        .step-header {
          display: flex;
          align-items: flex-start;
          gap: 16px;
          margin-bottom: 32px;
        }

        .step-icon {
          width: 48px;
          height: 48px;
          border-radius: 12px;
          background: var(--accent-gradient);
          display: flex;
          align-items: center;
          justify-content: center;
          color: #000;
        }

        .step-header h2 {
          font-size: 24px;
          font-weight: 600;
          margin-bottom: 4px;
        }

        .step-header p {
          color: var(--text-secondary);
          font-size: 14px;
        }

        .submissions-stats {
          display: grid;
          grid-template-columns: repeat(5, 1fr);
          gap: 16px;
          margin-bottom: 24px;
        }

        .stat-card {
          background: var(--bg-card);
          border: 1px solid var(--border-color);
          border-radius: var(--border-radius);
          padding: 20px;
          text-align: center;
        }

        .stat-value {
          font-size: 32px;
          font-weight: 700;
          color: var(--accent-primary);
        }

        .stat-label {
          font-size: 12px;
          color: var(--text-muted);
          margin-top: 4px;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }

        .submissions-filters {
          display: flex;
          align-items: center;
          gap: 16px;
          padding: 16px;
          background: var(--bg-card);
          border: 1px solid var(--border-color);
          border-radius: var(--border-radius);
          margin-bottom: 24px;
          flex-wrap: wrap;
        }

        .filter-group {
          display: flex;
          align-items: center;
          gap: 8px;
          color: var(--text-secondary);
          font-size: 14px;
        }

        .filter-select {
          position: relative;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .filter-select label {
          font-size: 12px;
          color: var(--text-muted);
        }

        .filter-select select {
          appearance: none;
          background: var(--bg-tertiary);
          border: 1px solid var(--border-color);
          border-radius: 6px;
          padding: 8px 32px 8px 12px;
          color: var(--text-primary);
          font-size: 13px;
          cursor: pointer;
        }

        .filter-select svg:last-child {
          position: absolute;
          right: 10px;
          pointer-events: none;
          color: var(--text-muted);
        }

        .btn-add-submission {
          display: flex;
          align-items: center;
          gap: 6px;
          padding: 8px 16px;
          background: var(--accent-primary);
          color: #000;
          border: none;
          border-radius: 6px;
          font-size: 13px;
          font-weight: 500;
          cursor: pointer;
          margin-left: auto;
        }

        .btn-add-submission:hover {
          background: var(--accent-primary-hover);
        }

        .submissions-table-container {
          background: var(--bg-card);
          border: 1px solid var(--border-color);
          border-radius: var(--border-radius);
          overflow: hidden;
        }

        .submissions-table {
          width: 100%;
          border-collapse: collapse;
        }

        .submissions-table th {
          text-align: left;
          padding: 14px 16px;
          background: var(--bg-tertiary);
          font-size: 11px;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.5px;
          color: var(--text-muted);
          border-bottom: 1px solid var(--border-color);
        }

        .submissions-table td {
          padding: 14px 16px;
          border-bottom: 1px solid var(--border-color);
          font-size: 14px;
        }

        .submissions-table tr:last-child td {
          border-bottom: none;
        }

        .submissions-table tr:hover {
          background: var(--bg-hover);
        }

        .urgent-row {
          background: rgba(239, 68, 68, 0.05) !important;
        }

        .campaign-cell {
          min-width: 140px;
        }

        .campaign-name {
          font-weight: 500;
          color: var(--text-primary);
        }

        .submitted-by {
          font-size: 11px;
          color: var(--text-muted);
          margin-top: 2px;
        }

        .award-cell {
          font-weight: 500;
          color: var(--accent-primary);
        }

        .category-cell {
          color: var(--text-secondary);
          max-width: 160px;
        }

        .deadline-cell {
          display: flex;
          align-items: center;
          gap: 6px;
          color: var(--text-secondary);
          white-space: nowrap;
        }

        .days-cell {
          white-space: nowrap;
        }

        .days-badge {
          display: inline-flex;
          align-items: center;
          gap: 4px;
          padding: 4px 10px;
          border-radius: 20px;
          font-size: 12px;
          font-weight: 500;
        }

        .status-cell {
          min-width: 160px;
        }

        .status-dropdown {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          padding: 6px 10px;
          border-radius: 6px;
          border: 1px solid;
        }

        .status-dropdown select {
          appearance: none;
          background: transparent;
          border: none;
          font-size: 12px;
          font-weight: 500;
          cursor: pointer;
          padding-right: 4px;
        }

        .cost-cell {
          font-weight: 500;
          color: var(--text-secondary);
        }

        .notes-cell {
          min-width: 150px;
          max-width: 200px;
        }

        .notes-display {
          cursor: pointer;
          padding: 4px 8px;
          border-radius: 4px;
          font-size: 13px;
          color: var(--text-secondary);
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }

        .notes-display:hover {
          background: var(--bg-tertiary);
        }

        .notes-display .placeholder {
          color: var(--text-muted);
          font-style: italic;
        }

        .notes-edit {
          display: flex;
          gap: 6px;
        }

        .notes-edit input {
          flex: 1;
          padding: 4px 8px;
          background: var(--bg-tertiary);
          border: 1px solid var(--accent-primary);
          border-radius: 4px;
          color: var(--text-primary);
          font-size: 13px;
        }

        .notes-edit button {
          padding: 4px 10px;
          background: var(--accent-primary);
          color: #000;
          border: none;
          border-radius: 4px;
          font-size: 12px;
          font-weight: 500;
          cursor: pointer;
        }

        .actions-cell {
          display: flex;
          gap: 6px;
        }

        .action-btn {
          width: 28px;
          height: 28px;
          display: flex;
          align-items: center;
          justify-content: center;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          background: var(--bg-tertiary);
          color: var(--text-muted);
        }

        .action-btn:hover {
          background: var(--bg-hover);
          color: var(--text-primary);
        }

        .action-btn.delete:hover {
          background: rgba(239, 68, 68, 0.1);
          color: #ef4444;
        }

        .empty-state {
          text-align: center;
          padding: 60px 20px !important;
          color: var(--text-muted);
        }

        .empty-state svg {
          opacity: 0.3;
          margin-bottom: 12px;
        }

        .submissions-legend {
          display: flex;
          gap: 32px;
          margin-top: 16px;
          padding: 12px 16px;
          background: var(--bg-secondary);
          border-radius: var(--border-radius-sm);
        }

        .legend-section {
          display: flex;
          align-items: center;
          gap: 16px;
        }

        .legend-title {
          font-size: 11px;
          font-weight: 600;
          text-transform: uppercase;
          color: var(--text-muted);
        }

        .legend-item {
          display: flex;
          align-items: center;
          gap: 6px;
          font-size: 12px;
          color: var(--text-secondary);
        }

        .urgency-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
        }

        @media (max-width: 1200px) {
          .submissions-stats {
            grid-template-columns: repeat(3, 1fr);
          }
        }

        @media (max-width: 768px) {
          .submissions-stats {
            grid-template-columns: repeat(2, 1fr);
          }

          .submissions-filters {
            flex-direction: column;
            align-items: stretch;
          }

          .btn-add-submission {
            margin-left: 0;
          }
        }
      `}</style>
    </div>
  )
}
