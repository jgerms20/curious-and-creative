import { useState } from 'react'
import {
  Download,
  ArrowLeft,
  FileText,
  Table,
  Film,
  CheckCircle,
  Copy,
  Check,
  FileDown
} from 'lucide-react'
import { Campaign, AwardMatch, CaseStudy } from '../../types'

interface ExportStepProps {
  campaign: Campaign | null
  selectedMatches: AwardMatch[]
  caseStudies: CaseStudy[]
  onBack: () => void
}

export function ExportStep({
  campaign,
  selectedMatches,
  caseStudies,
  onBack
}: ExportStepProps) {
  const [exportedItems, setExportedItems] = useState<string[]>([])
  const [copiedId, setCopiedId] = useState<string | null>(null)

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const downloadFile = (content: string, filename: string, type: string) => {
    const blob = new Blob([content], { type })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    setExportedItems([...exportedItems, filename])
  }

  const generateEntryTracker = () => {
    const headers = ['Award', 'Category', 'Fit Score', 'Deadline', 'Cost', 'Effort', 'Status']
    const rows = selectedMatches.map(m => [
      m.award.name,
      m.category.name,
      `${m.fitScore}%`,
      m.deadline || 'TBD',
      m.cost || 'TBD',
      m.effortRequired,
      'Not Started'
    ])

    const csv = [headers.join(','), ...rows.map(r => r.join(','))].join('\n')
    downloadFile(csv, `${campaign?.name || 'campaign'}-entry-tracker.csv`, 'text/csv')
  }

  const generateCampaignProfile = () => {
    const json = JSON.stringify(campaign, null, 2)
    downloadFile(json, `${campaign?.name || 'campaign'}-profile.json`, 'application/json')
  }

  const generateAllCaseStudies = () => {
    const content = caseStudies.map(study => `
================================================================================
${study.awardName} - ${study.categoryName}
Type: ${study.type}
================================================================================

## 50-WORD VERSION
${study.versions.elevator}

## 300-WORD VERSION
${study.versions.short}

## 750-WORD VERSION
${study.versions.standard}

${study.versions.full ? `## FULL EFFIE VERSION\n${study.versions.full}` : ''}

## KEY QUOTES
${study.keyQuotes.map(q => `- "${q}"`).join('\n')}

## RESULTS CALLOUTS
${study.resultsCallouts.map(r => `- ${r}`).join('\n')}

${study.videoScript ? `
## VIDEO SCRIPT (90 seconds)
0:00-0:10 HOOK: ${study.videoScript.hook}
0:10-0:30 CHALLENGE: ${study.videoScript.challenge}
0:30-0:50 INSIGHT: ${study.videoScript.insight}
0:50-1:10 EXECUTION: ${study.videoScript.execution}
1:10-1:30 RESULTS: ${study.videoScript.results}
` : ''}
`).join('\n\n')

    downloadFile(content, `${campaign?.name || 'campaign'}-case-studies.txt`, 'text/plain')
  }

  const generateSubmissionChecklist = () => {
    const content = `
# AWARD SUBMISSION CHECKLIST
Campaign: ${campaign?.name}
Brand: ${campaign?.brand}
Generated: ${new Date().toLocaleDateString()}

## SELECTED AWARDS (${selectedMatches.length})

${selectedMatches.map((m, i) => `
### ${i + 1}. ${m.award.name} - ${m.category.name}
- Fit Score: ${m.fitScore}%
- Deadline: ${m.deadline || 'TBD'}
- Entry Cost: ${m.cost || 'TBD'}
- Effort Required: ${m.effortRequired}

#### Submission Checklist
[ ] Case study written (${caseStudies.some(c => c.awardId === m.award.id) ? 'DONE' : 'PENDING'})
[ ] Case study video created
[ ] Supporting images prepared
[ ] Entry form completed
[ ] Payment processed
[ ] Final review completed
[ ] Submitted

#### Framing Angle
${m.framingAngle}

#### What Judges Value
${m.award.judgingIntel?.whatTheyValue || 'N/A'}
`).join('\n')}

## TOTAL ESTIMATED COST
$${selectedMatches.reduce((sum, m) => {
  const cost = parseInt(m.cost?.replace(/[^0-9]/g, '') || '0')
  return sum + cost
}, 0).toLocaleString()}

## TIMELINE SUMMARY
${[...new Set(selectedMatches.map(m => m.deadline).filter(Boolean))].sort().map(d => `- ${d}`).join('\n')}
`
    downloadFile(content, `${campaign?.name || 'campaign'}-submission-checklist.md`, 'text/markdown')
  }

  const totalCost = selectedMatches.reduce((sum, m) => {
    const cost = parseInt(m.cost?.replace(/[^0-9]/g, '') || '0')
    return sum + cost
  }, 0)

  return (
    <div className="step-container export-step">
      <div className="step-header">
        <div className="step-icon-large">
          <Download size={32} />
        </div>
        <div className="step-header-text">
          <h2>Export Materials</h2>
          <p>Download everything you need for submissions</p>
        </div>
      </div>

      {/* Summary */}
      <div className="export-summary">
        <div className="summary-card">
          <span className="summary-number">{selectedMatches.length}</span>
          <span className="summary-label">Awards Selected</span>
        </div>
        <div className="summary-card">
          <span className="summary-number">{caseStudies.length}</span>
          <span className="summary-label">Case Studies</span>
        </div>
        <div className="summary-card">
          <span className="summary-number">${totalCost.toLocaleString()}</span>
          <span className="summary-label">Est. Entry Cost</span>
        </div>
      </div>

      {/* Export Options */}
      <div className="export-options">
        <h3>Export Options</h3>

        <div className="export-grid">
          <ExportCard
            icon={<Table size={24} />}
            title="Entry Tracker"
            description="CSV spreadsheet to track all entries, deadlines, and status"
            filename="entry-tracker.csv"
            exported={exportedItems.includes(`${campaign?.name || 'campaign'}-entry-tracker.csv`)}
            onExport={generateEntryTracker}
          />

          <ExportCard
            icon={<FileText size={24} />}
            title="All Case Studies"
            description="All generated case studies in multiple lengths"
            filename="case-studies.txt"
            exported={exportedItems.includes(`${campaign?.name || 'campaign'}-case-studies.txt`)}
            onExport={generateAllCaseStudies}
          />

          <ExportCard
            icon={<CheckCircle size={24} />}
            title="Submission Checklist"
            description="Detailed checklist for each award submission"
            filename="submission-checklist.md"
            exported={exportedItems.includes(`${campaign?.name || 'campaign'}-submission-checklist.md`)}
            onExport={generateSubmissionChecklist}
          />

          <ExportCard
            icon={<FileDown size={24} />}
            title="Campaign Profile"
            description="Full campaign data in JSON format"
            filename="profile.json"
            exported={exportedItems.includes(`${campaign?.name || 'campaign'}-profile.json`)}
            onExport={generateCampaignProfile}
          />
        </div>
      </div>

      {/* Quick Copy Section */}
      <div className="quick-copy-section">
        <h3>Quick Copy</h3>
        <div className="quick-copy-grid">
          <QuickCopyCard
            title="Elevator Pitch"
            content={caseStudies[0]?.versions.elevator || 'Generate case studies first'}
            onCopy={(text) => copyToClipboard(text, 'elevator')}
            copied={copiedId === 'elevator'}
          />
          <QuickCopyCard
            title="Headline Result"
            content={campaign?.results.summary || 'No results summary'}
            onCopy={(text) => copyToClipboard(text, 'result')}
            copied={copiedId === 'result'}
          />
          <QuickCopyCard
            title="Big Idea"
            content={campaign?.creative.bigIdea || 'No big idea'}
            onCopy={(text) => copyToClipboard(text, 'idea')}
            copied={copiedId === 'idea'}
          />
          <QuickCopyCard
            title="Key Insight"
            content={campaign?.brief.keyInsight || 'No insight'}
            onCopy={(text) => copyToClipboard(text, 'insight')}
            copied={copiedId === 'insight'}
          />
        </div>
      </div>

      {/* Next Steps */}
      <div className="next-steps">
        <h3>Next Steps</h3>
        <ol className="steps-list">
          <li>
            <CheckCircle size={18} />
            <span>Download your entry tracker and case studies</span>
          </li>
          <li>
            <span className="step-number">2</span>
            <span>Create case study videos using the provided scripts</span>
          </li>
          <li>
            <span className="step-number">3</span>
            <span>Gather high-resolution images and supporting materials</span>
          </li>
          <li>
            <span className="step-number">4</span>
            <span>Get client approval on results and case study content</span>
          </li>
          <li>
            <span className="step-number">5</span>
            <span>For Effies: Obtain client endorsement letter</span>
          </li>
          <li>
            <span className="step-number">6</span>
            <span>Complete entry forms and submit before deadlines</span>
          </li>
        </ol>
      </div>

      <div className="step-actions">
        <button className="btn btn-secondary" onClick={onBack}>
          <ArrowLeft size={18} />
          Back to Case Studies
        </button>
      </div>
    </div>
  )
}

function ExportCard({
  icon,
  title,
  description,
  filename,
  exported,
  onExport
}: {
  icon: React.ReactNode
  title: string
  description: string
  filename: string
  exported: boolean
  onExport: () => void
}) {
  return (
    <div className={`export-card ${exported ? 'exported' : ''}`}>
      <div className="export-card-icon">{icon}</div>
      <div className="export-card-content">
        <h4>{title}</h4>
        <p>{description}</p>
      </div>
      <button
        className={`btn ${exported ? 'btn-success' : 'btn-primary'}`}
        onClick={onExport}
      >
        {exported ? (
          <>
            <CheckCircle size={16} />
            Downloaded
          </>
        ) : (
          <>
            <Download size={16} />
            Download
          </>
        )}
      </button>
    </div>
  )
}

function QuickCopyCard({
  title,
  content,
  onCopy,
  copied
}: {
  title: string
  content: string
  onCopy: (text: string) => void
  copied: boolean
}) {
  return (
    <div className="quick-copy-card">
      <div className="quick-copy-header">
        <span>{title}</span>
        <button
          className="copy-btn-small"
          onClick={() => onCopy(content)}
        >
          {copied ? <Check size={14} /> : <Copy size={14} />}
        </button>
      </div>
      <p className="quick-copy-content">{content}</p>
    </div>
  )
}
