import { useState, useEffect } from 'react'
import './App.css'
import { Sidebar } from './components/Sidebar'
import { Header } from './components/Header'
import { UploadStep } from './components/steps/UploadStep'
import { AnalyzeStep } from './components/steps/AnalyzeStep'
import { MatchStep } from './components/steps/MatchStep'
import { CaseStudyStep } from './components/steps/CaseStudyStep'
import { CalendarStep } from './components/steps/CalendarStep'
import { ExportStep } from './components/steps/ExportStep'
import { WinnersStep } from './components/steps/WinnersStep'
import SubmissionsStep from './components/steps/SubmissionsStep'
import { Campaign, AwardMatch, CaseStudy, Submission } from './types'
import { strangerThingsSubmissions } from './data/strangerThings'

export type Step = 'upload' | 'analyze' | 'match' | 'case-study' | 'calendar' | 'winners' | 'export' | 'submissions'

// LocalStorage key for submissions
const SUBMISSIONS_STORAGE_KEY = 'award-agent-submissions'

// Load submissions from localStorage or use defaults
function loadSubmissions(): Submission[] {
  try {
    const stored = localStorage.getItem(SUBMISSIONS_STORAGE_KEY)
    if (stored) {
      return JSON.parse(stored)
    }
  } catch (e) {
    console.error('Failed to load submissions from localStorage:', e)
  }
  // Return pre-populated Stranger Things submissions as default
  return strangerThingsSubmissions
}

// Save submissions to localStorage
function saveSubmissions(submissions: Submission[]) {
  try {
    localStorage.setItem(SUBMISSIONS_STORAGE_KEY, JSON.stringify(submissions))
  } catch (e) {
    console.error('Failed to save submissions to localStorage:', e)
  }
}

function App() {
  const [currentStep, setCurrentStep] = useState<Step>('upload')
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [campaign, setCampaign] = useState<Campaign | null>(null)
  const [analysis, setAnalysis] = useState<any>(null)
  const [matches, setMatches] = useState<AwardMatch[]>([])
  const [selectedMatches, setSelectedMatches] = useState<AwardMatch[]>([])
  const [caseStudies, setCaseStudies] = useState<CaseStudy[]>([])
  const [submissions, setSubmissions] = useState<Submission[]>(loadSubmissions)

  // Persist submissions to localStorage whenever they change
  useEffect(() => {
    saveSubmissions(submissions)
  }, [submissions])

  // Submission handlers
  const handleUpdateSubmission = (id: string, updates: Partial<Submission>) => {
    setSubmissions(prev =>
      prev.map(sub => (sub.id === id ? { ...sub, ...updates } : sub))
    )
  }

  const handleDeleteSubmission = (id: string) => {
    setSubmissions(prev => prev.filter(sub => sub.id !== id))
  }

  const renderStep = () => {
    switch (currentStep) {
      case 'upload':
        return (
          <UploadStep
            campaign={campaign}
            setCampaign={setCampaign}
            onNext={() => setCurrentStep('analyze')}
          />
        )
      case 'analyze':
        return (
          <AnalyzeStep
            campaign={campaign}
            analysis={analysis}
            setAnalysis={setAnalysis}
            onNext={() => setCurrentStep('match')}
            onBack={() => setCurrentStep('upload')}
          />
        )
      case 'match':
        return (
          <MatchStep
            campaign={campaign}
            analysis={analysis}
            matches={matches}
            setMatches={setMatches}
            selectedMatches={selectedMatches}
            setSelectedMatches={setSelectedMatches}
            onNext={() => setCurrentStep('case-study')}
            onBack={() => setCurrentStep('analyze')}
          />
        )
      case 'case-study':
        return (
          <CaseStudyStep
            campaign={campaign}
            selectedMatches={selectedMatches}
            caseStudies={caseStudies}
            setCaseStudies={setCaseStudies}
            onNext={() => setCurrentStep('export')}
            onBack={() => setCurrentStep('match')}
          />
        )
      case 'calendar':
        return (
          <CalendarStep
            selectedMatches={selectedMatches}
            onBack={() => setCurrentStep('match')}
          />
        )
      case 'winners':
        return (
          <WinnersStep
            onBack={() => setCurrentStep('upload')}
          />
        )
      case 'submissions':
        return (
          <SubmissionsStep
            submissions={submissions}
            onUpdateSubmission={handleUpdateSubmission}
            onDeleteSubmission={handleDeleteSubmission}
          />
        )
      case 'export':
        return (
          <ExportStep
            campaign={campaign}
            selectedMatches={selectedMatches}
            caseStudies={caseStudies}
            onBack={() => setCurrentStep('case-study')}
          />
        )
      default:
        return null
    }
  }

  return (
    <div className="app">
      <Sidebar
        isOpen={sidebarOpen}
        currentStep={currentStep}
        setCurrentStep={setCurrentStep}
        campaign={campaign}
        submissions={submissions}
      />
      <div className={`main-content ${sidebarOpen ? '' : 'sidebar-closed'}`}>
        <Header
          toggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          currentStep={currentStep}
        />
        <main className="content">
          {renderStep()}
        </main>
      </div>
    </div>
  )
}

export default App
