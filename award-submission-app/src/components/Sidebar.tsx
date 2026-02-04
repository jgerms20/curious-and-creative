import {
  Upload,
  Search,
  Trophy,
  FileText,
  Calendar,
  Download,
  Award,
  BarChart3,
  Sparkles,
  ChevronRight
} from 'lucide-react'
import { Step } from '../App'
import { Campaign } from '../types'

interface SidebarProps {
  isOpen: boolean
  currentStep: Step
  setCurrentStep: (step: Step) => void
  campaign: Campaign | null
}

export function Sidebar({ isOpen, currentStep, setCurrentStep, campaign }: SidebarProps) {
  if (!isOpen) return null

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <Trophy size={32} className="logo-icon" />
          <div className="logo-text">
            <span className="logo-title">Award Agent</span>
            <span className="logo-version">v2.0</span>
          </div>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section">
          <span className="nav-section-title">Workflow</span>
          <NavItem
            icon={<Upload size={20} />}
            label="Campaign Input"
            active={currentStep === 'upload'}
            onClick={() => setCurrentStep('upload')}
          />
          <NavItem
            icon={<BarChart3 size={20} />}
            label="Analyze"
            active={currentStep === 'analyze'}
            onClick={() => setCurrentStep('analyze')}
            disabled={!campaign}
          />
          <NavItem
            icon={<Search size={20} />}
            label="Match Awards"
            active={currentStep === 'match'}
            onClick={() => setCurrentStep('match')}
            disabled={!campaign}
          />
          <NavItem
            icon={<FileText size={20} />}
            label="Write Case Study"
            active={currentStep === 'case-study'}
            onClick={() => setCurrentStep('case-study')}
            disabled={!campaign}
          />
          <NavItem
            icon={<Download size={20} />}
            label="Export"
            active={currentStep === 'export'}
            onClick={() => setCurrentStep('export')}
            disabled={!campaign}
          />
        </div>

        <div className="nav-section">
          <span className="nav-section-title">Resources</span>
          <NavItem
            icon={<Calendar size={20} />}
            label="Deadline Calendar"
            active={currentStep === 'calendar'}
            onClick={() => setCurrentStep('calendar')}
          />
          <NavItem
            icon={<Sparkles size={20} />}
            label="2024 Winners"
            active={currentStep === 'winners'}
            onClick={() => setCurrentStep('winners')}
          />
        </div>
      </nav>

      {campaign && (
        <div className="sidebar-campaign">
          <div className="campaign-card">
            <span className="campaign-label">Current Campaign</span>
            <h4 className="campaign-name">{campaign.name}</h4>
            <span className="campaign-brand">{campaign.brand}</span>
            <div className="campaign-scores">
              <ScoreBadge label="Craft" score={campaign.awardPotential.craftStrength} />
              <ScoreBadge label="Idea" score={campaign.awardPotential.ideaStrength} />
              <ScoreBadge label="Results" score={campaign.awardPotential.resultsStrength} />
            </div>
          </div>
        </div>
      )}

      <div className="sidebar-footer">
        <div className="ai-badge">
          <Sparkles size={16} />
          <span>Powered by Claude</span>
        </div>
      </div>
    </aside>
  )
}

function NavItem({
  icon,
  label,
  active,
  onClick,
  disabled
}: {
  icon: React.ReactNode
  label: string
  active: boolean
  onClick: () => void
  disabled?: boolean
}) {
  return (
    <button
      className={`nav-item ${active ? 'active' : ''} ${disabled ? 'disabled' : ''}`}
      onClick={onClick}
      disabled={disabled}
    >
      <span className="nav-item-icon">{icon}</span>
      <span className="nav-item-label">{label}</span>
      {active && <ChevronRight size={16} className="nav-item-arrow" />}
    </button>
  )
}

function ScoreBadge({ label, score }: { label: string; score: number }) {
  const color = score >= 8 ? 'green' : score >= 6 ? 'yellow' : 'red'
  return (
    <div className={`score-badge ${color}`}>
      <span className="score-label">{label}</span>
      <span className="score-value">{score}/10</span>
    </div>
  )
}
