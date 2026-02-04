import { Menu, Sun, Moon } from 'lucide-react'
import { Step } from '../App'
import { useState } from 'react'

interface HeaderProps {
  toggleSidebar: () => void
  currentStep: Step
}

const stepLabels: Record<Step, string> = {
  'upload': 'Campaign Input',
  'analyze': 'Analysis',
  'match': 'Award Matching',
  'case-study': 'Case Study',
  'calendar': 'Deadline Calendar',
  'winners': '2024 Winners',
  'export': 'Export'
}

export function Header({ toggleSidebar, currentStep }: HeaderProps) {
  const [darkMode, setDarkMode] = useState(true)

  return (
    <header className="header">
      <div className="header-left">
        <button className="menu-button" onClick={toggleSidebar}>
          <Menu size={24} />
        </button>
        <div className="header-title">
          <h1>Award Submission System</h1>
          <span className="header-subtitle">AI-Powered Award Strategy</span>
        </div>
      </div>

      <div className="header-center">
        <nav className="step-nav">
          <StepIndicator step="upload" label="Input" current={currentStep} order={1} />
          <StepIndicator step="analyze" label="Analyze" current={currentStep} order={2} />
          <StepIndicator step="match" label="Match" current={currentStep} order={3} />
          <StepIndicator step="case-study" label="Write" current={currentStep} order={4} />
          <StepIndicator step="export" label="Export" current={currentStep} order={5} />
        </nav>
      </div>

      <div className="header-right">
        <button
          className="theme-toggle"
          onClick={() => setDarkMode(!darkMode)}
        >
          {darkMode ? <Sun size={20} /> : <Moon size={20} />}
        </button>
      </div>
    </header>
  )
}

function StepIndicator({
  step,
  label,
  current,
  order
}: {
  step: Step
  label: string
  current: Step
  order: number
}) {
  const stepOrder: Record<Step, number> = {
    'upload': 1,
    'analyze': 2,
    'match': 3,
    'case-study': 4,
    'calendar': 0,
    'winners': 0,
    'export': 5
  }

  const currentOrder = stepOrder[current]
  const isActive = current === step
  const isCompleted = stepOrder[step] < currentOrder

  return (
    <div className={`step-indicator ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}>
      <div className="step-icon">
        {isCompleted ? '✓' : order}
      </div>
      <span className="step-label">{label}</span>
    </div>
  )
}
