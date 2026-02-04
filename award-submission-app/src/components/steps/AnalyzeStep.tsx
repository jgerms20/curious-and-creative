import { useState, useEffect } from 'react'
import {
  BarChart3,
  CheckCircle,
  AlertTriangle,
  ArrowRight,
  ArrowLeft,
  Sparkles,
  Target,
  Lightbulb,
  Trophy,
  TrendingUp,
  Zap
} from 'lucide-react'
import { Campaign } from '../../types'

interface AnalyzeStepProps {
  campaign: Campaign | null
  analysis: any
  setAnalysis: (analysis: any) => void
  onNext: () => void
  onBack: () => void
}

export function AnalyzeStep({ campaign, analysis, setAnalysis, onNext, onBack }: AnalyzeStepProps) {
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisComplete, setAnalysisComplete] = useState(false)

  useEffect(() => {
    if (campaign && !analysis) {
      runAnalysis()
    } else if (analysis) {
      setAnalysisComplete(true)
    }
  }, [campaign])

  const runAnalysis = async () => {
    setIsAnalyzing(true)

    // Simulate analysis - in production this would call Claude API
    await new Promise(resolve => setTimeout(resolve, 2000))

    const newAnalysis = generateAnalysis(campaign!)
    setAnalysis(newAnalysis)
    setIsAnalyzing(false)
    setAnalysisComplete(true)
  }

  if (!campaign) {
    return (
      <div className="step-container">
        <p>No campaign loaded. Please go back and enter campaign details.</p>
        <button className="btn btn-secondary" onClick={onBack}>
          <ArrowLeft size={18} />
          Go Back
        </button>
      </div>
    )
  }

  return (
    <div className="step-container analyze-step">
      <div className="step-header">
        <div className="step-icon-large">
          <BarChart3 size={32} />
        </div>
        <div className="step-header-text">
          <h2>Campaign Analysis</h2>
          <p>AI assessment of your campaign's award potential</p>
        </div>
      </div>

      {isAnalyzing && (
        <div className="analyzing-state">
          <div className="spinner"></div>
          <h3>Analyzing Campaign...</h3>
          <p>Evaluating against award criteria and 2024 winning patterns</p>
        </div>
      )}

      {analysisComplete && analysis && (
        <div className="analysis-results">
          {/* Overall Score */}
          <div className="overall-score-card">
            <div className="score-circle">
              <svg viewBox="0 0 100 100">
                <circle
                  className="score-bg"
                  cx="50"
                  cy="50"
                  r="45"
                />
                <circle
                  className="score-fill"
                  cx="50"
                  cy="50"
                  r="45"
                  strokeDasharray={`${analysis.overallScore * 2.83} 283`}
                />
              </svg>
              <div className="score-text">
                <span className="score-number">{analysis.overallScore}</span>
                <span className="score-label">/ 100</span>
              </div>
            </div>
            <div className="score-details">
              <h3>Award Potential: {analysis.potentialLevel}</h3>
              <p>{analysis.summary}</p>
            </div>
          </div>

          {/* Dimension Scores */}
          <div className="dimension-scores">
            <h3>Strength Analysis</h3>
            <div className="dimensions-grid">
              <DimensionCard
                icon={<Lightbulb size={24} />}
                label="Creative Idea"
                score={campaign.awardPotential.ideaStrength}
                description={analysis.dimensions.idea}
              />
              <DimensionCard
                icon={<Target size={24} />}
                label="Craft Quality"
                score={campaign.awardPotential.craftStrength}
                description={analysis.dimensions.craft}
              />
              <DimensionCard
                icon={<TrendingUp size={24} />}
                label="Results"
                score={campaign.awardPotential.resultsStrength}
                description={analysis.dimensions.results}
              />
              <DimensionCard
                icon={<Zap size={24} />}
                label="Innovation"
                score={campaign.awardPotential.innovationStrength}
                description={analysis.dimensions.innovation}
              />
              <DimensionCard
                icon={<Trophy size={24} />}
                label="Cultural Impact"
                score={campaign.awardPotential.culturalImpactStrength}
                description={analysis.dimensions.cultural}
              />
            </div>
          </div>

          {/* Best Fit Categories */}
          <div className="best-fit-section">
            <h3>Best Fit Award Categories</h3>
            <div className="categories-list">
              {analysis.bestCategories.map((cat: any, i: number) => (
                <div key={i} className="category-card">
                  <div className="category-rank">#{i + 1}</div>
                  <div className="category-info">
                    <h4>{cat.category}</h4>
                    <p>{cat.reasoning}</p>
                  </div>
                  <div className="category-fit">
                    <span className="fit-score">{cat.fitScore}%</span>
                    <span className="fit-label">fit</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Strengths & Weaknesses */}
          <div className="swot-section">
            <div className="strengths">
              <h3>
                <CheckCircle size={20} className="icon-green" />
                Strengths
              </h3>
              <ul>
                {analysis.strengths.map((s: string, i: number) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>
            <div className="weaknesses">
              <h3>
                <AlertTriangle size={20} className="icon-yellow" />
                Areas to Address
              </h3>
              <ul>
                {analysis.weaknesses.map((w: string, i: number) => (
                  <li key={i}>{w}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* 2024 Pattern Match */}
          <div className="pattern-match">
            <h3>
              <Sparkles size={20} />
              2024 Winning Pattern Match
            </h3>
            <div className="patterns">
              {analysis.patternMatches.map((pattern: any, i: number) => (
                <div key={i} className={`pattern-tag ${pattern.matches ? 'matches' : ''}`}>
                  {pattern.matches && <CheckCircle size={14} />}
                  {pattern.name}
                </div>
              ))}
            </div>
          </div>

          {/* Recommended Strategy */}
          <div className="strategy-recommendation">
            <h3>Recommended Award Strategy</h3>
            <p>{analysis.strategy}</p>
          </div>
        </div>
      )}

      <div className="step-actions">
        <button className="btn btn-secondary" onClick={onBack}>
          <ArrowLeft size={18} />
          Edit Campaign
        </button>
        <button
          className="btn btn-primary btn-large"
          onClick={onNext}
          disabled={!analysisComplete}
        >
          Find Award Matches
          <ArrowRight size={20} />
        </button>
      </div>
    </div>
  )
}

function DimensionCard({
  icon,
  label,
  score,
  description
}: {
  icon: React.ReactNode
  label: string
  score: number
  description: string
}) {
  const getScoreClass = (s: number) => {
    if (s >= 8) return 'excellent'
    if (s >= 6) return 'good'
    if (s >= 4) return 'fair'
    return 'weak'
  }

  return (
    <div className={`dimension-card ${getScoreClass(score)}`}>
      <div className="dimension-header">
        {icon}
        <span className="dimension-label">{label}</span>
        <span className="dimension-score">{score}/10</span>
      </div>
      <div className="dimension-bar">
        <div className="dimension-fill" style={{ width: `${score * 10}%` }} />
      </div>
      <p className="dimension-description">{description}</p>
    </div>
  )
}

// Generate analysis based on campaign data
function generateAnalysis(campaign: Campaign) {
  const scores = campaign.awardPotential
  const avgScore = (
    scores.craftStrength +
    scores.ideaStrength +
    scores.resultsStrength +
    scores.innovationStrength +
    scores.culturalImpactStrength
  ) / 5

  const overallScore = Math.round(avgScore * 10)

  const potentialLevel =
    overallScore >= 80 ? 'Excellent - Grand Prix Contender' :
    overallScore >= 65 ? 'Strong - Medal Potential' :
    overallScore >= 50 ? 'Competitive - Shortlist Possible' :
    'Developing - Consider Selective Entry'

  // Determine best categories based on strengths
  const bestCategories = []

  if (scores.resultsStrength >= 7) {
    bestCategories.push({
      category: 'Effectiveness Awards (Effies, Creative Effectiveness)',
      reasoning: 'Strong business results are your biggest asset',
      fitScore: Math.min(95, scores.resultsStrength * 10 + 15)
    })
  }

  if (scores.craftStrength >= 7) {
    bestCategories.push({
      category: 'Film/Craft Awards (Cannes Film, D&AD, AICP)',
      reasoning: 'High production quality stands out in craft categories',
      fitScore: Math.min(95, scores.craftStrength * 10 + 10)
    })
  }

  if (scores.ideaStrength >= 7) {
    bestCategories.push({
      category: 'Creative Excellence (One Show, Clios)',
      reasoning: 'Original idea is the foundation of creative awards',
      fitScore: Math.min(95, scores.ideaStrength * 10 + 10)
    })
  }

  if (scores.innovationStrength >= 7) {
    bestCategories.push({
      category: 'Innovation Awards (Cannes Innovation, Webby)',
      reasoning: 'Genuine innovation stands out in these categories',
      fitScore: Math.min(95, scores.innovationStrength * 10 + 10)
    })
  }

  if (scores.culturalImpactStrength >= 7) {
    bestCategories.push({
      category: 'Social/PR Awards (PR Lions, Social & Influencer)',
      reasoning: 'Cultural conversation drives these categories',
      fitScore: Math.min(95, scores.culturalImpactStrength * 10 + 10)
    })
  }

  if (campaign.industry === 'sports_beverages' || campaign.talent?.athletes?.length) {
    bestCategories.push({
      category: 'Clio Sports',
      reasoning: 'Sports connection makes this essential',
      fitScore: 90
    })
  }

  // Ensure we have at least 3 categories
  if (bestCategories.length < 3) {
    bestCategories.push({
      category: 'Integrated Campaign Awards',
      reasoning: 'Multi-channel work can compete across platforms',
      fitScore: 60
    })
  }

  // Sort by fit score
  bestCategories.sort((a, b) => b.fitScore - a.fitScore)

  // Generate strengths
  const strengths: string[] = []
  if (scores.ideaStrength >= 7) strengths.push('Strong, original creative concept')
  if (scores.craftStrength >= 7) strengths.push('Exceptional production quality')
  if (scores.resultsStrength >= 7) strengths.push('Impressive business results with clear attribution')
  if (scores.innovationStrength >= 7) strengths.push('Genuine innovation in approach or technology')
  if (scores.culturalImpactStrength >= 7) strengths.push('Generated significant cultural conversation')
  if (campaign.results?.verified) strengths.push('Results are verified and client-approved')
  if (campaign.talent?.athletes?.length) strengths.push('Strong athlete partnerships')
  if (campaign.creative?.whatMadeItSpecial) strengths.push('Clear articulation of what makes work special')

  // Generate weaknesses
  const weaknesses: string[] = []
  if (scores.resultsStrength < 6) weaknesses.push('Business results need strengthening for effectiveness awards')
  if (scores.craftStrength < 6) weaknesses.push('Production quality may not compete in craft categories')
  if (scores.innovationStrength < 5) weaknesses.push('Limited innovation angle - focus on other strengths')
  if (!campaign.results?.verified) weaknesses.push('Results not yet verified - needed for Effies')
  if (campaign.awardPotential.weaknesses?.length) {
    weaknesses.push(...campaign.awardPotential.weaknesses)
  }

  // 2024 winning patterns
  const patternMatches = [
    { name: 'Purpose with Proof', matches: scores.culturalImpactStrength >= 6 && scores.resultsStrength >= 6 },
    { name: 'Smart Data Use', matches: scores.innovationStrength >= 6 },
    { name: 'Brand Utility', matches: campaign.creative?.whatMadeItSpecial?.toLowerCase().includes('utility') || false },
    { name: 'Challenging Norms', matches: campaign.creative?.whatMadeItSpecial?.toLowerCase().includes('bias') || campaign.creative?.whatMadeItSpecial?.toLowerCase().includes('challenge') || false },
    { name: 'Humor', matches: campaign.creative?.whatMadeItSpecial?.toLowerCase().includes('humor') || campaign.creative?.whatMadeItSpecial?.toLowerCase().includes('funny') || false },
    { name: 'Experiential Participation', matches: campaign.executionTypes?.some(e => e.includes('experiential')) || false },
    { name: 'Platform-Native', matches: campaign.executionTypes?.some(e => ['tiktok', 'instagram_reels', 'youtube_content'].includes(e)) || false }
  ]

  // Strategy recommendation
  const strategy = overallScore >= 70
    ? `Focus on Tier 1 awards where you have the strongest fit. Your ${bestCategories[0]?.category} potential is highest. Consider a "wide then deep" approach: enter several categories at key shows, then double down on shortlisted work.`
    : overallScore >= 50
    ? `Focus on Tier 2 awards and specific categories where your strengths align. ${bestCategories[0]?.category} is your best opportunity. Be selective to maximize ROI on entry fees.`
    : `Consider selective entry in specialized categories where your specific strengths matter most. Build results data for future award seasons.`

  return {
    overallScore,
    potentialLevel,
    summary: `This campaign shows ${potentialLevel.split(' - ')[0].toLowerCase()} award potential with particular strength in ${
      scores.resultsStrength >= scores.craftStrength ? 'effectiveness' : 'creative'
    } categories.`,
    dimensions: {
      idea: scores.ideaStrength >= 7 ? 'Original concept that stands out' : scores.ideaStrength >= 5 ? 'Solid idea with room to sharpen' : 'Consider strengthening the core concept',
      craft: scores.craftStrength >= 7 ? 'Production quality is exceptional' : scores.craftStrength >= 5 ? 'Good craft, may not lead in craft awards' : 'Craft may not be the winning angle',
      results: scores.resultsStrength >= 7 ? 'Strong results for effectiveness awards' : scores.resultsStrength >= 5 ? 'Decent results, strengthen if possible' : 'Results are a weak point',
      innovation: scores.innovationStrength >= 7 ? 'Genuine innovation to highlight' : scores.innovationStrength >= 5 ? 'Some innovation elements' : 'Not an innovation play',
      cultural: scores.culturalImpactStrength >= 7 ? 'Generated significant conversation' : scores.culturalImpactStrength >= 5 ? 'Some cultural resonance' : 'Limited cultural impact'
    },
    bestCategories: bestCategories.slice(0, 5),
    strengths: strengths.length ? strengths : ['Campaign has been captured - add more details to strengthen analysis'],
    weaknesses: weaknesses.length ? weaknesses : ['No major weaknesses identified'],
    patternMatches,
    strategy
  }
}
