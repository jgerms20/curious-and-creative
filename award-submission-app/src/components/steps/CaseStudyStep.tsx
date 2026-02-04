import { useState } from 'react'
import {
  FileText,
  ArrowRight,
  ArrowLeft,
  Sparkles,
  Copy,
  Check,
  ChevronDown,
  ChevronUp,
  Film,
  BarChart3,
  Lightbulb,
  Layers
} from 'lucide-react'
import { Campaign, AwardMatch, CaseStudy } from '../../types'

interface CaseStudyStepProps {
  campaign: Campaign | null
  selectedMatches: AwardMatch[]
  caseStudies: CaseStudy[]
  setCaseStudies: (studies: CaseStudy[]) => void
  onNext: () => void
  onBack: () => void
}

export function CaseStudyStep({
  campaign,
  selectedMatches,
  caseStudies,
  setCaseStudies,
  onNext,
  onBack
}: CaseStudyStepProps) {
  const [isGenerating, setIsGenerating] = useState(false)
  const [activeStudy, setActiveStudy] = useState<string | null>(null)
  const [activeVersion, setActiveVersion] = useState<'elevator' | 'short' | 'standard' | 'full'>('standard')
  const [copiedId, setCopiedId] = useState<string | null>(null)

  const generateCaseStudies = async () => {
    setIsGenerating(true)

    // Simulate AI generation - would call Claude API in production
    await new Promise(resolve => setTimeout(resolve, 2000))

    const studies = selectedMatches.map(match => {
      const type = determineStudyType(match)
      return generateStudyContent(campaign!, match, type)
    })

    setCaseStudies(studies)
    setIsGenerating(false)
    if (studies.length > 0) {
      setActiveStudy(`${studies[0].awardId}-${studies[0].categoryName}`)
    }
  }

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  const getActiveStudy = () => {
    return caseStudies.find(s => `${s.awardId}-${s.categoryName}` === activeStudy)
  }

  if (!campaign) {
    return (
      <div className="step-container">
        <p>No campaign loaded.</p>
        <button className="btn btn-secondary" onClick={onBack}>
          <ArrowLeft size={18} />
          Go Back
        </button>
      </div>
    )
  }

  return (
    <div className="step-container case-study-step">
      <div className="step-header">
        <div className="step-icon-large">
          <FileText size={32} />
        </div>
        <div className="step-header-text">
          <h2>Case Study Generator</h2>
          <p>AI-generated case studies tailored to each award</p>
        </div>
      </div>

      {selectedMatches.length === 0 ? (
        <div className="empty-state">
          <p>No awards selected. Go back and select awards to generate case studies for.</p>
          <button className="btn btn-secondary" onClick={onBack}>
            <ArrowLeft size={18} />
            Select Awards
          </button>
        </div>
      ) : caseStudies.length === 0 ? (
        <div className="generate-prompt">
          <div className="prompt-card">
            <Sparkles size={48} className="prompt-icon" />
            <h3>Ready to Generate</h3>
            <p>
              Generate tailored case studies for {selectedMatches.length} selected award
              {selectedMatches.length > 1 ? 's' : ''}. Each study will be customized based on what
              judges value in that specific category.
            </p>
            <div className="selected-awards-preview">
              {selectedMatches.slice(0, 5).map((match, i) => (
                <span key={i} className="award-tag">
                  {match.award.name} - {match.category.name}
                </span>
              ))}
              {selectedMatches.length > 5 && (
                <span className="award-tag more">+{selectedMatches.length - 5} more</span>
              )}
            </div>
            <button
              className="btn btn-primary btn-large"
              onClick={generateCaseStudies}
              disabled={isGenerating}
            >
              {isGenerating ? (
                <>
                  <div className="spinner-small"></div>
                  Generating...
                </>
              ) : (
                <>
                  <Sparkles size={20} />
                  Generate Case Studies
                </>
              )}
            </button>
          </div>
        </div>
      ) : (
        <div className="case-studies-layout">
          {/* Sidebar with study list */}
          <div className="studies-sidebar">
            <h3>Generated Studies ({caseStudies.length})</h3>
            <div className="studies-list">
              {caseStudies.map(study => {
                const id = `${study.awardId}-${study.categoryName}`
                const TypeIcon = getTypeIcon(study.type)
                return (
                  <button
                    key={id}
                    className={`study-item ${activeStudy === id ? 'active' : ''}`}
                    onClick={() => setActiveStudy(id)}
                  >
                    <TypeIcon size={18} />
                    <div className="study-item-text">
                      <span className="study-award">{study.awardName}</span>
                      <span className="study-category">{study.categoryName}</span>
                    </div>
                    <span className={`study-type-badge ${study.type}`}>
                      {study.type}
                    </span>
                  </button>
                )
              })}
            </div>
          </div>

          {/* Main content area */}
          <div className="study-content">
            {getActiveStudy() && (
              <>
                <div className="study-header">
                  <div>
                    <h3>{getActiveStudy()!.awardName}</h3>
                    <span className="study-category-label">{getActiveStudy()!.categoryName}</span>
                  </div>
                  <div className="version-tabs">
                    <button
                      className={`version-tab ${activeVersion === 'elevator' ? 'active' : ''}`}
                      onClick={() => setActiveVersion('elevator')}
                    >
                      50 words
                    </button>
                    <button
                      className={`version-tab ${activeVersion === 'short' ? 'active' : ''}`}
                      onClick={() => setActiveVersion('short')}
                    >
                      300 words
                    </button>
                    <button
                      className={`version-tab ${activeVersion === 'standard' ? 'active' : ''}`}
                      onClick={() => setActiveVersion('standard')}
                    >
                      750 words
                    </button>
                    {getActiveStudy()!.versions.full && (
                      <button
                        className={`version-tab ${activeVersion === 'full' ? 'active' : ''}`}
                        onClick={() => setActiveVersion('full')}
                      >
                        Full (Effie)
                      </button>
                    )}
                  </div>
                </div>

                <div className="study-body">
                  <div className="study-text-container">
                    <button
                      className="copy-btn"
                      onClick={() => copyToClipboard(
                        getActiveStudy()!.versions[activeVersion] || '',
                        `${activeStudy}-${activeVersion}`
                      )}
                    >
                      {copiedId === `${activeStudy}-${activeVersion}` ? (
                        <>
                          <Check size={16} />
                          Copied!
                        </>
                      ) : (
                        <>
                          <Copy size={16} />
                          Copy
                        </>
                      )}
                    </button>
                    <div className="study-text">
                      {getActiveStudy()!.versions[activeVersion]}
                    </div>
                  </div>

                  {/* Video Script */}
                  {getActiveStudy()!.videoScript && (
                    <div className="video-script-section">
                      <h4>
                        <Film size={18} />
                        90-Second Video Script
                      </h4>
                      <div className="script-timeline">
                        <ScriptSegment
                          time="0:00-0:10"
                          label="Hook"
                          content={getActiveStudy()!.videoScript!.hook}
                        />
                        <ScriptSegment
                          time="0:10-0:30"
                          label="Challenge"
                          content={getActiveStudy()!.videoScript!.challenge}
                        />
                        <ScriptSegment
                          time="0:30-0:50"
                          label="Insight & Strategy"
                          content={getActiveStudy()!.videoScript!.insight}
                        />
                        <ScriptSegment
                          time="0:50-1:10"
                          label="Execution"
                          content={getActiveStudy()!.videoScript!.execution}
                        />
                        <ScriptSegment
                          time="1:10-1:30"
                          label="Results"
                          content={getActiveStudy()!.videoScript!.results}
                        />
                      </div>
                    </div>
                  )}

                  {/* Key Quotes */}
                  <div className="key-quotes-section">
                    <h4>Key Quotes for Title Cards</h4>
                    <div className="quotes-grid">
                      {getActiveStudy()!.keyQuotes.map((quote, i) => (
                        <div key={i} className="quote-card">
                          <span className="quote-text">"{quote}"</span>
                          <button
                            className="copy-btn-small"
                            onClick={() => copyToClipboard(quote, `quote-${i}`)}
                          >
                            {copiedId === `quote-${i}` ? <Check size={14} /> : <Copy size={14} />}
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Results Callouts */}
                  <div className="results-callouts-section">
                    <h4>Results Callouts</h4>
                    <div className="callouts-grid">
                      {getActiveStudy()!.resultsCallouts.map((callout, i) => (
                        <div key={i} className="callout-card">
                          <span className="callout-text">{callout}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      )}

      <div className="step-actions">
        <button className="btn btn-secondary" onClick={onBack}>
          <ArrowLeft size={18} />
          Back to Matches
        </button>
        <button
          className="btn btn-primary btn-large"
          onClick={onNext}
          disabled={caseStudies.length === 0}
        >
          Export Materials
          <ArrowRight size={20} />
        </button>
      </div>
    </div>
  )
}

function ScriptSegment({
  time,
  label,
  content
}: {
  time: string
  label: string
  content: string
}) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div className="script-segment">
      <div className="segment-header" onClick={() => setExpanded(!expanded)}>
        <span className="segment-time">{time}</span>
        <span className="segment-label">{label}</span>
        {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
      </div>
      {expanded && <div className="segment-content">{content}</div>}
    </div>
  )
}

function getTypeIcon(type: string) {
  switch (type) {
    case 'effectiveness':
      return BarChart3
    case 'craft':
      return Film
    case 'innovation':
      return Lightbulb
    case 'integrated':
      return Layers
    default:
      return FileText
  }
}

function determineStudyType(match: AwardMatch): CaseStudy['type'] {
  const categoryLower = match.category.name.toLowerCase()
  const awardId = match.award.id

  if (categoryLower.includes('effectiveness') || awardId === 'effies') {
    return 'effectiveness'
  }
  if (categoryLower.includes('craft') || categoryLower.includes('film') ||
      categoryLower.includes('direction') || awardId === 'aicp') {
    return 'craft'
  }
  if (categoryLower.includes('innovation') || categoryLower.includes('data')) {
    return 'innovation'
  }
  if (categoryLower.includes('integrated')) {
    return 'integrated'
  }
  return 'general'
}

function generateStudyContent(
  campaign: Campaign,
  match: AwardMatch,
  type: CaseStudy['type']
): CaseStudy {
  // Generate elevator pitch (50 words)
  const elevator = `${campaign.brand}'s "${campaign.name}" campaign tackled ${campaign.brief.challenge.slice(0, 50)}... with a bold idea: ${campaign.creative.bigIdea}. The result? ${campaign.results.summary || 'Exceptional results'}. A textbook example of ${type === 'effectiveness' ? 'marketing effectiveness' : 'creative excellence'}.`

  // Generate short version (300 words)
  const short = `
THE CHALLENGE
${campaign.brief.challenge}

THE INSIGHT
${campaign.brief.keyInsight || 'We discovered a powerful truth about our audience that changed everything.'}

THE IDEA
${campaign.creative.bigIdea}

${campaign.creative.whatMadeItSpecial ? `What made it special: ${campaign.creative.whatMadeItSpecial}` : ''}

THE EXECUTION
We brought this idea to life through ${campaign.executionTypes?.join(', ') || 'multiple touchpoints'}.
${campaign.talent?.athletes?.length ? `Featuring ${campaign.talent.athletes.map(a => a.name).join(', ')}.` : ''}

THE RESULTS
${campaign.results.summary || 'The campaign exceeded all objectives.'}
${campaign.results.business?.sales?.result ? `Sales: ${campaign.results.business.sales.result}` : ''}
${campaign.results.engagement?.videoViews ? `Video views: ${campaign.results.engagement.videoViews}` : ''}
${campaign.results.brand?.awareness?.lift ? `Awareness lift: ${campaign.results.brand.awareness.lift}` : ''}
  `.trim()

  // Generate standard version (750 words)
  const standard = `
# ${campaign.name}

## THE CHALLENGE
${campaign.brief.challenge}

${campaign.brief.context ? `The competitive context was challenging: ${campaign.brief.context}` : ''}

Our target audience was ${campaign.brief.targetAudience}, and we needed to break through in a crowded market.

## THE INSIGHT
${campaign.brief.keyInsight || 'We discovered a powerful truth about our audience.'}

This insight changed everything. It gave us permission to approach the challenge in a completely new way.

## THE STRATEGY
${campaign.strategy?.strategicApproach || 'We developed a strategy that put our audience at the center.'}

${campaign.strategy?.whyThisStrategy || ''}

## THE IDEA
**${campaign.creative.bigIdea}**

${campaign.creative.whatMadeItSpecial || ''}

${campaign.creative.tagline ? `Campaign tagline: "${campaign.creative.tagline}"` : ''}

## THE EXECUTION
We brought this idea to life through a carefully orchestrated campaign:

${campaign.executionTypes?.map(e => `- ${e.replace(/_/g, ' ')}`).join('\n') || '- Multiple touchpoints'}

${campaign.talent?.athletes?.length ? `\nAthlete partners: ${campaign.talent.athletes.map(a => a.name).join(', ')}` : ''}
${campaign.talent?.director ? `\nDirected by ${campaign.talent.director}` : ''}
${campaign.creative.craftElements?.length ? `\nNotable craft elements: ${campaign.creative.craftElements.join(', ')}` : ''}

## THE RESULTS
${campaign.results.summary || 'The campaign exceeded all objectives.'}

**Business Impact:**
${campaign.results.business?.sales?.result ? `- Sales: ${campaign.results.business.sales.result}` : ''}
${campaign.results.business?.marketShare?.result ? `- Market share: ${campaign.results.business.marketShare.result}` : ''}
${campaign.results.business?.roi ? `- ROI: ${campaign.results.business.roi}` : ''}

**Brand Metrics:**
${campaign.results.brand?.awareness?.lift ? `- Awareness: ${campaign.results.brand.awareness.lift}` : ''}
${campaign.results.brand?.consideration?.lift ? `- Consideration: ${campaign.results.brand.consideration.lift}` : ''}

**Engagement:**
${campaign.results.engagement?.impressions ? `- Impressions: ${campaign.results.engagement.impressions}` : ''}
${campaign.results.engagement?.videoViews ? `- Video views: ${campaign.results.engagement.videoViews}` : ''}
${campaign.results.engagement?.socialEngagement ? `- Social engagement: ${campaign.results.engagement.socialEngagement}` : ''}
${campaign.results.engagement?.earnedMediaValue ? `- Earned media value: ${campaign.results.engagement.earnedMediaValue}` : ''}

${campaign.results.cultural?.pressCoverage?.length ? `\nPress coverage included: ${campaign.results.cultural.pressCoverage.join(', ')}` : ''}

${campaign.results.source ? `\n*Results verified by ${campaign.results.source}*` : ''}
  `.trim()

  // Video script
  const videoScript = {
    hook: `What happens when ${campaign.brand} decides to ${campaign.creative.bigIdea?.slice(0, 50)}...?`,
    challenge: campaign.brief.challenge,
    insight: campaign.brief.keyInsight || 'We discovered a powerful insight that changed everything.',
    execution: `We created ${campaign.executionTypes?.slice(0, 3).join(', ') || 'a multi-channel campaign'}. ${campaign.creative.whatMadeItSpecial || ''}`,
    results: campaign.results.summary || 'The results exceeded expectations.'
  }

  // Key quotes for title cards
  const keyQuotes = [
    campaign.creative.bigIdea,
    campaign.brief.keyInsight,
    campaign.results.summary,
    campaign.creative.whatMadeItSpecial
  ].filter(Boolean).slice(0, 4) as string[]

  // Results callouts
  const resultsCallouts = [
    campaign.results.business?.sales?.result,
    campaign.results.business?.marketShare?.result,
    campaign.results.brand?.awareness?.lift ? `+${campaign.results.brand.awareness.lift} awareness` : null,
    campaign.results.engagement?.videoViews,
    campaign.results.engagement?.earnedMediaValue
  ].filter(Boolean) as string[]

  return {
    awardId: match.award.id,
    awardName: match.award.name,
    categoryName: match.category.name,
    type,
    versions: {
      elevator,
      short,
      standard,
      full: type === 'effectiveness' ? generateEffieVersion(campaign) : undefined
    },
    videoScript,
    keyQuotes,
    resultsCallouts
  }
}

function generateEffieVersion(campaign: Campaign): string {
  return `
# EFFIE ENTRY: ${campaign.name}

## SECTION 1: CHALLENGE, CONTEXT & OBJECTIVES (23.3%)

### The Challenge
${campaign.brief.challenge}

### Market Context
${campaign.brief.context || 'The market presented significant challenges.'}

### Objectives
We set clear, measurable objectives before the campaign launched:
1. ${campaign.results.business?.sales?.result ? `Drive sales growth (Target: measurable lift)` : 'Drive business growth'}
2. ${campaign.results.brand?.awareness?.lift ? `Increase brand awareness` : 'Strengthen brand metrics'}
3. Achieve strong engagement and earned media

---

## SECTION 2: INSIGHTS & STRATEGY (23.3%)

### The Insight
${campaign.brief.keyInsight || 'Our research revealed a powerful consumer truth.'}

### Strategic Approach
${campaign.strategy?.strategicApproach || 'We developed a strategy centered on our audience insight.'}

### Why This Strategy
${campaign.strategy?.whyThisStrategy || 'This was the right approach because it directly addressed our insight and business challenge.'}

---

## SECTION 3: BRINGING STRATEGY TO LIFE (23.3%)

### The Idea
${campaign.creative.bigIdea}

### Execution
${campaign.creative.whatMadeItSpecial || 'We brought this idea to life in unexpected ways.'}

Channels and touchpoints:
${campaign.executionTypes?.map(e => `- ${e.replace(/_/g, ' ')}`).join('\n') || '- Multi-channel approach'}

${campaign.talent?.athletes?.length ? `\nTalent: ${campaign.talent.athletes.map(a => a.name).join(', ')}` : ''}

---

## SECTION 4: RESULTS (30% - HIGHEST WEIGHT)

### Headline Result
${campaign.results.summary || 'The campaign exceeded all objectives.'}

### Business Results
${campaign.results.business?.sales?.result ? `**Sales:** ${campaign.results.business.sales.result}` : ''}
${campaign.results.business?.marketShare?.result ? `**Market Share:** ${campaign.results.business.marketShare.result}` : ''}
${campaign.results.business?.roi ? `**ROI:** ${campaign.results.business.roi}` : ''}

### Brand Metrics
${campaign.results.brand?.awareness?.lift ? `**Awareness:** ${campaign.results.brand.awareness.lift}` : ''}
${campaign.results.brand?.consideration?.lift ? `**Consideration:** ${campaign.results.brand.consideration.lift}` : ''}
${campaign.results.brand?.favorability?.lift ? `**Favorability:** ${campaign.results.brand.favorability.lift}` : ''}

### Engagement & Earned Media
${campaign.results.engagement?.impressions ? `**Impressions:** ${campaign.results.engagement.impressions}` : ''}
${campaign.results.engagement?.videoViews ? `**Video Views:** ${campaign.results.engagement.videoViews}` : ''}
${campaign.results.engagement?.socialEngagement ? `**Social Engagement:** ${campaign.results.engagement.socialEngagement}` : ''}
${campaign.results.engagement?.earnedMediaValue ? `**Earned Media Value:** ${campaign.results.engagement.earnedMediaValue}` : ''}

### Attribution
${campaign.results.source ? `Results verified by ${campaign.results.source}.` : 'Results from internal measurement.'}

---

*Client endorsement letter required for submission*
  `.trim()
}
