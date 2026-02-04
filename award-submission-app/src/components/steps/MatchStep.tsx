import { useState, useEffect } from 'react'
import {
  Search,
  Trophy,
  Calendar,
  DollarSign,
  CheckCircle,
  ArrowRight,
  ArrowLeft,
  Filter,
  Star,
  Clock,
  AlertCircle
} from 'lucide-react'
import { Campaign, AwardMatch, Award, AwardCategory } from '../../types'
import { awardsDatabase } from '../../data/awards'

interface MatchStepProps {
  campaign: Campaign | null
  analysis: any
  matches: AwardMatch[]
  setMatches: (matches: AwardMatch[]) => void
  selectedMatches: AwardMatch[]
  setSelectedMatches: (matches: AwardMatch[]) => void
  onNext: () => void
  onBack: () => void
}

export function MatchStep({
  campaign,
  analysis,
  matches,
  setMatches,
  selectedMatches,
  setSelectedMatches,
  onNext,
  onBack
}: MatchStepProps) {
  const [isMatching, setIsMatching] = useState(false)
  const [filter, setFilter] = useState<'all' | 'primary' | 'strong' | 'reach'>('all')
  const [tierFilter, setTierFilter] = useState<number | null>(null)

  useEffect(() => {
    if (campaign && matches.length === 0) {
      generateMatches()
    }
  }, [campaign])

  const generateMatches = async () => {
    setIsMatching(true)
    await new Promise(resolve => setTimeout(resolve, 1500))

    const generatedMatches = matchCampaignToAwards(campaign!, analysis)
    setMatches(generatedMatches)
    setIsMatching(false)
  }

  const toggleMatch = (match: AwardMatch) => {
    const isSelected = selectedMatches.some(
      m => m.award.id === match.award.id && m.category.name === match.category.name
    )

    if (isSelected) {
      setSelectedMatches(selectedMatches.filter(
        m => !(m.award.id === match.award.id && m.category.name === match.category.name)
      ))
    } else {
      setSelectedMatches([...selectedMatches, match])
    }
  }

  const filteredMatches = matches.filter(m => {
    if (filter !== 'all' && m.tier !== filter) return false
    if (tierFilter !== null && m.award.prestigeTier !== tierFilter) return false
    return true
  })

  const totalCost = selectedMatches.reduce((sum, m) => {
    const cost = parseInt(m.cost?.replace(/[^0-9]/g, '') || '0')
    return sum + cost
  }, 0)

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
    <div className="step-container match-step">
      <div className="step-header">
        <div className="step-icon-large">
          <Search size={32} />
        </div>
        <div className="step-header-text">
          <h2>Award Matches</h2>
          <p>Select the awards you want to pursue</p>
        </div>
      </div>

      {isMatching && (
        <div className="analyzing-state">
          <div className="spinner"></div>
          <h3>Finding Matches...</h3>
          <p>Analyzing 60+ awards against your campaign profile</p>
        </div>
      )}

      {!isMatching && matches.length > 0 && (
        <>
          {/* Summary Bar */}
          <div className="match-summary">
            <div className="summary-stat">
              <span className="stat-number">{matches.filter(m => m.tier === 'primary').length}</span>
              <span className="stat-label">Primary Matches</span>
            </div>
            <div className="summary-stat">
              <span className="stat-number">{matches.filter(m => m.tier === 'strong').length}</span>
              <span className="stat-label">Strong Opportunities</span>
            </div>
            <div className="summary-stat">
              <span className="stat-number">{matches.filter(m => m.tier === 'reach').length}</span>
              <span className="stat-label">Strategic Reaches</span>
            </div>
            <div className="summary-stat selected">
              <span className="stat-number">{selectedMatches.length}</span>
              <span className="stat-label">Selected</span>
            </div>
            <div className="summary-stat cost">
              <span className="stat-number">${totalCost.toLocaleString()}</span>
              <span className="stat-label">Est. Entry Cost</span>
            </div>
          </div>

          {/* Filters */}
          <div className="match-filters">
            <div className="filter-group">
              <span className="filter-label">Fit Level:</span>
              <button
                className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
                onClick={() => setFilter('all')}
              >
                All
              </button>
              <button
                className={`filter-btn primary ${filter === 'primary' ? 'active' : ''}`}
                onClick={() => setFilter('primary')}
              >
                Primary (90%+)
              </button>
              <button
                className={`filter-btn strong ${filter === 'strong' ? 'active' : ''}`}
                onClick={() => setFilter('strong')}
              >
                Strong (75-89%)
              </button>
              <button
                className={`filter-btn reach ${filter === 'reach' ? 'active' : ''}`}
                onClick={() => setFilter('reach')}
              >
                Reach (60-74%)
              </button>
            </div>
            <div className="filter-group">
              <span className="filter-label">Prestige:</span>
              <button
                className={`filter-btn ${tierFilter === null ? 'active' : ''}`}
                onClick={() => setTierFilter(null)}
              >
                All
              </button>
              <button
                className={`filter-btn tier1 ${tierFilter === 1 ? 'active' : ''}`}
                onClick={() => setTierFilter(1)}
              >
                <Star size={14} /> Tier 1
              </button>
              <button
                className={`filter-btn tier2 ${tierFilter === 2 ? 'active' : ''}`}
                onClick={() => setTierFilter(2)}
              >
                Tier 2
              </button>
            </div>
          </div>

          {/* Match Cards */}
          <div className="matches-grid">
            {filteredMatches.map((match, i) => (
              <MatchCard
                key={`${match.award.id}-${match.category.name}-${i}`}
                match={match}
                isSelected={selectedMatches.some(
                  m => m.award.id === match.award.id && m.category.name === match.category.name
                )}
                onToggle={() => toggleMatch(match)}
              />
            ))}
          </div>

          {filteredMatches.length === 0 && (
            <div className="no-matches">
              <AlertCircle size={48} />
              <p>No matches found with current filters</p>
            </div>
          )}
        </>
      )}

      <div className="step-actions">
        <button className="btn btn-secondary" onClick={onBack}>
          <ArrowLeft size={18} />
          Back to Analysis
        </button>
        <button
          className="btn btn-primary btn-large"
          onClick={onNext}
          disabled={selectedMatches.length === 0}
        >
          Write Case Studies ({selectedMatches.length})
          <ArrowRight size={20} />
        </button>
      </div>
    </div>
  )
}

function MatchCard({
  match,
  isSelected,
  onToggle
}: {
  match: AwardMatch
  isSelected: boolean
  onToggle: () => void
}) {
  const tierColors = {
    primary: 'tier-primary',
    strong: 'tier-strong',
    reach: 'tier-reach',
    skip: 'tier-skip'
  }

  const prestigeLabels = {
    1: 'Premier',
    2: 'Strong',
    3: 'Volume'
  }

  return (
    <div
      className={`match-card ${tierColors[match.tier]} ${isSelected ? 'selected' : ''}`}
      onClick={onToggle}
    >
      <div className="match-header">
        <div className="match-title">
          <h4>{match.award.name}</h4>
          <span className="match-category">{match.category.name}</span>
        </div>
        <div className="match-select">
          {isSelected ? (
            <CheckCircle size={24} className="check-icon" />
          ) : (
            <div className="select-circle" />
          )}
        </div>
      </div>

      <div className="match-badges">
        <span className={`badge prestige-${match.award.prestigeTier}`}>
          {match.award.prestigeTier === 1 && <Star size={12} />}
          Tier {match.award.prestigeTier}
        </span>
        <span className={`badge fit-${match.tier}`}>
          {match.fitScore}% fit
        </span>
        <span className="badge effort">
          {match.effortRequired} effort
        </span>
      </div>

      <p className="match-reasoning">{match.reasoning}</p>

      <div className="match-framing">
        <strong>Framing angle:</strong> {match.framingAngle}
      </div>

      <div className="match-meta">
        {match.deadline && (
          <span className="meta-item">
            <Calendar size={14} />
            {match.deadline}
          </span>
        )}
        {match.cost && (
          <span className="meta-item">
            <DollarSign size={14} />
            {match.cost}
          </span>
        )}
      </div>

      {match.award.judgingIntel?.whatTheyValue && (
        <div className="match-intel">
          <strong>Judges value:</strong> {match.award.judgingIntel.whatTheyValue}
        </div>
      )}
    </div>
  )
}

// Match campaign to awards
function matchCampaignToAwards(campaign: Campaign, analysis: any): AwardMatch[] {
  const matches: AwardMatch[] = []
  const scores = campaign.awardPotential

  // Process each award
  awardsDatabase.forEach(award => {
    award.categories.forEach(category => {
      const fitScore = calculateFitScore(campaign, award, category, scores)

      if (fitScore >= 60) {
        const tier =
          fitScore >= 90 ? 'primary' :
          fitScore >= 75 ? 'strong' :
          'reach'

        matches.push({
          award,
          category,
          fitScore,
          tier,
          reasoning: generateReasoning(campaign, award, category, fitScore),
          framingAngle: generateFramingAngle(campaign, award, category),
          effortRequired: determineEffort(award, category),
          deadline: award.deadlines?.finalDeadline || award.deadlines?.regularDeadline,
          cost: award.costPerEntry
        })
      }
    })
  })

  // Sort by fit score
  matches.sort((a, b) => b.fitScore - a.fitScore)

  return matches
}

function calculateFitScore(
  campaign: Campaign,
  award: Award,
  category: AwardCategory,
  scores: Campaign['awardPotential']
): number {
  let baseScore = 50

  // Award type bonuses
  const categoryLower = category.name.toLowerCase()

  // Effectiveness categories
  if (categoryLower.includes('effectiveness') || award.id === 'effies') {
    baseScore += scores.resultsStrength * 4
    if (campaign.results?.verified) baseScore += 10
    if (campaign.results?.business?.sales?.result) baseScore += 5
  }

  // Craft categories
  if (categoryLower.includes('craft') || categoryLower.includes('film') ||
      categoryLower.includes('direction') || categoryLower.includes('cinematography')) {
    baseScore += scores.craftStrength * 4
  }

  // Innovation categories
  if (categoryLower.includes('innovation') || categoryLower.includes('data')) {
    baseScore += scores.innovationStrength * 4
  }

  // Social/PR categories
  if (categoryLower.includes('social') || categoryLower.includes('pr') ||
      categoryLower.includes('influencer')) {
    baseScore += scores.culturalImpactStrength * 3
    if (campaign.executionTypes?.some(e => ['tiktok', 'instagram_reels'].includes(e))) {
      baseScore += 10
    }
  }

  // Sports categories
  if (categoryLower.includes('sport') || award.id === 'clio-sports') {
    if (campaign.industry === 'sports_beverages' || campaign.talent?.athletes?.length) {
      baseScore += 20
    }
  }

  // Experiential categories
  if (categoryLower.includes('experiential') || categoryLower.includes('activation') ||
      categoryLower.includes('experience')) {
    if (campaign.executionTypes?.some(e => e.includes('experiential'))) {
      baseScore += 15
    }
  }

  // Integrated categories
  if (categoryLower.includes('integrated')) {
    const execCount = campaign.executionTypes?.length || 0
    if (execCount >= 5) baseScore += 15
    else if (execCount >= 3) baseScore += 10
  }

  // Prestige tier adjustments (harder to win tier 1)
  if (award.prestigeTier === 1) {
    baseScore -= 5 // Tougher competition
  }

  // Idea strength general bonus
  baseScore += scores.ideaStrength * 2

  return Math.min(99, Math.max(0, baseScore))
}

function generateReasoning(
  campaign: Campaign,
  award: Award,
  category: AwardCategory,
  fitScore: number
): string {
  const categoryLower = category.name.toLowerCase()

  if (categoryLower.includes('effectiveness') || award.id === 'effies') {
    return campaign.results?.verified
      ? 'Strong verified results align with effectiveness focus'
      : 'Results data could compete here - verify with client'
  }

  if (categoryLower.includes('sport') || award.id === 'clio-sports') {
    return 'Sports connection is authentic and central to the work'
  }

  if (categoryLower.includes('film') || categoryLower.includes('craft')) {
    return 'Production quality and craft excellence are strengths'
  }

  if (categoryLower.includes('innovation')) {
    return 'Innovation elements could differentiate this entry'
  }

  if (categoryLower.includes('social') || categoryLower.includes('influencer')) {
    return 'Social-native approach and cultural conversation potential'
  }

  return fitScore >= 80
    ? 'Strong overall fit based on campaign strengths'
    : 'Worth considering with right framing'
}

function generateFramingAngle(
  campaign: Campaign,
  award: Award,
  category: AwardCategory
): string {
  const categoryLower = category.name.toLowerCase()

  if (categoryLower.includes('effectiveness') || award.id === 'effies') {
    return 'Lead with business results, then show the creative that drove them'
  }

  if (categoryLower.includes('craft') || categoryLower.includes('film')) {
    return 'Lead with the creative idea and showcase exceptional execution'
  }

  if (categoryLower.includes('innovation')) {
    return 'Lead with what\'s genuinely new and demonstrate the breakthrough'
  }

  if (categoryLower.includes('social')) {
    return 'Lead with platform insight and show native creative approach'
  }

  if (categoryLower.includes('experiential')) {
    return 'Lead with what people DID, not just what you built'
  }

  if (categoryLower.includes('integrated')) {
    return 'Show how channels worked together, not just in parallel'
  }

  return 'Lead with the insight and show how the idea came to life'
}

function determineEffort(award: Award, category: AwardCategory): 'low' | 'medium' | 'high' {
  // Effies require most effort (client letter, detailed case study)
  if (award.id === 'effies') return 'high'

  // Tier 1 awards generally need more polished materials
  if (award.prestigeTier === 1) return 'medium'

  return 'low'
}
