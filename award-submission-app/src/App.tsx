import { useState } from 'react'
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
import { Campaign, AwardMatch, CaseStudy } from './types'

export type Step = 'upload' | 'analyze' | 'match' | 'case-study' | 'calendar' | 'winners' | 'export'

function App() {
  const [currentStep, setCurrentStep] = useState<Step>('upload')
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [campaign, setCampaign] = useState<Campaign | null>(null)
  const [analysis, setAnalysis] = useState<any>(null)
  const [matches, setMatches] = useState<AwardMatch[]>([])
  const [selectedMatches, setSelectedMatches] = useState<AwardMatch[]>([])
  const [caseStudies, setCaseStudies] = useState<CaseStudy[]>([])

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
