import { useState } from 'react'
import {
  Calendar,
  ArrowLeft,
  Star,
  Clock,
  AlertCircle,
  CheckCircle
} from 'lucide-react'
import { AwardMatch } from '../../types'
import { awardsDatabase } from '../../data/awards'

interface CalendarStepProps {
  selectedMatches: AwardMatch[]
  onBack: () => void
}

const months = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
]

export function CalendarStep({ selectedMatches, onBack }: CalendarStepProps) {
  const [view, setView] = useState<'timeline' | 'list'>('timeline')

  // Group awards by deadline month
  const deadlinesByMonth: Record<string, typeof awardsDatabase> = {}

  awardsDatabase.forEach(award => {
    const deadline = award.deadlines?.finalDeadline || award.deadlines?.regularDeadline
    if (deadline) {
      // Extract month from deadline string
      const month = months.find(m => deadline.toLowerCase().includes(m.toLowerCase()))
      if (month) {
        if (!deadlinesByMonth[month]) {
          deadlinesByMonth[month] = []
        }
        deadlinesByMonth[month].push(award)
      }
    }
  })

  const isSelected = (awardId: string) => {
    return selectedMatches.some(m => m.award.id === awardId)
  }

  return (
    <div className="step-container calendar-step">
      <div className="step-header">
        <div className="step-icon-large">
          <Calendar size={32} />
        </div>
        <div className="step-header-text">
          <h2>Award Calendar 2026</h2>
          <p>Upcoming deadlines across all major awards</p>
        </div>
      </div>

      <div className="view-toggle">
        <button
          className={`toggle-btn ${view === 'timeline' ? 'active' : ''}`}
          onClick={() => setView('timeline')}
        >
          Timeline View
        </button>
        <button
          className={`toggle-btn ${view === 'list' ? 'active' : ''}`}
          onClick={() => setView('list')}
        >
          List View
        </button>
      </div>

      {view === 'timeline' && (
        <div className="timeline-view">
          {months.map(month => {
            const awards = deadlinesByMonth[month] || []
            if (awards.length === 0) return null

            return (
              <div key={month} className="month-section">
                <div className="month-header">
                  <h3>{month} 2026</h3>
                  <span className="award-count">{awards.length} deadlines</span>
                </div>
                <div className="month-awards">
                  {awards.map(award => (
                    <div
                      key={award.id}
                      className={`calendar-award ${isSelected(award.id) ? 'selected' : ''}`}
                    >
                      <div className="award-info">
                        <div className="award-name-row">
                          {award.prestigeTier === 1 && <Star size={14} className="tier-star" />}
                          <h4>{award.name}</h4>
                          {isSelected(award.id) && (
                            <CheckCircle size={16} className="selected-check" />
                          )}
                        </div>
                        <span className="award-deadline">
                          <Clock size={12} />
                          {award.deadlines?.finalDeadline || award.deadlines?.regularDeadline}
                        </span>
                      </div>
                      <div className="award-meta">
                        <span className={`tier-badge tier-${award.prestigeTier}`}>
                          Tier {award.prestigeTier}
                        </span>
                        <span className="cost-badge">{award.costPerEntry}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {view === 'list' && (
        <div className="list-view">
          <table className="calendar-table">
            <thead>
              <tr>
                <th>Award</th>
                <th>Tier</th>
                <th>Early Deadline</th>
                <th>Final Deadline</th>
                <th>Cost</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {awardsDatabase
                .sort((a, b) => a.prestigeTier - b.prestigeTier)
                .map(award => (
                  <tr key={award.id} className={isSelected(award.id) ? 'selected' : ''}>
                    <td>
                      <div className="award-cell">
                        {award.prestigeTier === 1 && <Star size={14} />}
                        {award.name}
                      </div>
                    </td>
                    <td>
                      <span className={`tier-badge tier-${award.prestigeTier}`}>
                        Tier {award.prestigeTier}
                      </span>
                    </td>
                    <td>{award.deadlines?.earlyDeadline || '-'}</td>
                    <td>{award.deadlines?.finalDeadline || award.deadlines?.regularDeadline || '-'}</td>
                    <td>{award.costPerEntry || '-'}</td>
                    <td>
                      {isSelected(award.id) ? (
                        <span className="status-selected">
                          <CheckCircle size={14} />
                          Selected
                        </span>
                      ) : (
                        <span className="status-available">Available</span>
                      )}
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="calendar-legend">
        <div className="legend-item">
          <Star size={14} className="tier-star" />
          <span>Tier 1 (Premier)</span>
        </div>
        <div className="legend-item">
          <CheckCircle size={14} className="selected-check" />
          <span>Selected for entry</span>
        </div>
      </div>

      <div className="step-actions">
        <button className="btn btn-secondary" onClick={onBack}>
          <ArrowLeft size={18} />
          Back
        </button>
      </div>
    </div>
  )
}
