export interface Campaign {
  id: string
  name: string
  client: string
  brand: string
  industry: string
  dates: {
    campaignStart?: string
    campaignEnd?: string
  }
  brief: {
    challenge: string
    context?: string
    targetAudience: string
    keyInsight: string
    budgetTier?: 'micro' | 'small' | 'medium' | 'large' | 'mega'
  }
  strategy: {
    strategicApproach: string
    whyThisStrategy?: string
  }
  creative: {
    bigIdea: string
    tagline?: string
    whatMadeItSpecial: string
    craftElements?: string[]
    innovationElements?: string[]
  }
  executionTypes: string[]
  talent?: {
    athletes?: { name: string; sport?: string }[]
    celebrities?: { name: string }[]
    influencers?: { name: string; platform?: string }[]
    director?: string
    productionCompany?: string
  }
  partnerships?: {
    partnerName: string
    partnerType: string
    description: string
  }[]
  results: {
    summary: string
    business?: {
      sales?: { result: string; vsObjective?: string }
      marketShare?: { result: string }
      roi?: string
    }
    brand?: {
      awareness?: { lift: string; vsBenchmark?: string }
      consideration?: { lift: string }
      favorability?: { lift: string }
    }
    engagement?: {
      impressions?: string
      videoViews?: string
      socialEngagement?: string
      earnedMediaValue?: string
    }
    cultural?: {
      moments?: string[]
      celebrityMentions?: string[]
      pressCoverage?: string[]
    }
    verified: boolean
    source?: string
  }
  awardPotential: {
    craftStrength: number
    ideaStrength: number
    resultsStrength: number
    innovationStrength: number
    culturalImpactStrength: number
    strongestAngles?: string[]
    weaknesses?: string[]
  }
}

export interface Award {
  id: string
  name: string
  organization: string
  website?: string
  prestigeTier: 1 | 2 | 3
  prestigeNotes?: string
  description: string
  categories: AwardCategory[]
  deadlines?: {
    entryOpens?: string
    earlyDeadline?: string
    regularDeadline?: string
    finalDeadline?: string
  }
  costPerEntry?: string
  judgingIntel?: {
    juryComposition?: string
    whatTheyValue?: string
    redFlags?: string
  }
  strategicNotes?: string
}

export interface AwardCategory {
  name: string
  whatWins?: string
  subcategories?: string[]
  winners2024?: string[]
}

export interface AwardMatch {
  award: Award
  category: AwardCategory
  fitScore: number
  tier: 'primary' | 'strong' | 'reach' | 'skip'
  reasoning: string
  framingAngle: string
  effortRequired: 'low' | 'medium' | 'high'
  deadline?: string
  cost?: string
  selected?: boolean
}

export interface CaseStudy {
  awardId: string
  awardName: string
  categoryName: string
  type: 'effectiveness' | 'craft' | 'innovation' | 'integrated' | 'general'
  versions: {
    elevator: string // 50 words
    short: string // 300 words
    standard: string // 750 words
    full?: string // 1500 words (for Effie)
  }
  videoScript?: {
    hook: string
    challenge: string
    insight: string
    execution: string
    results: string
  }
  keyQuotes: string[]
  resultsCallouts: string[]
}

export interface WinningExample {
  campaign: string
  brand: string
  agency: string
  awardsWon: string[]
  theIdea: string
  whyItWon: Record<string, string>
  whatToLearn: string[]
  categoryFit: string[]
}

// Submission Status Tracking
export type SubmissionStatus =
  | 'not_started'
  | 'draft'
  | 'in_review'
  | 'elt_approved'
  | 'client_approved'
  | 'submitted'

export interface Submission {
  id: string
  campaignId: string
  campaignName: string
  awardId: string
  awardName: string
  category: string
  status: SubmissionStatus
  deadline: string // ISO date string
  submittedBy: 'tbwa' | 'netflix' | 'client'
  entryCost?: number
  notes?: string
  lastUpdated: string // ISO date string
  createdAt: string // ISO date string
}

export interface SubmissionFilters {
  status?: SubmissionStatus | 'all'
  award?: string | 'all'
  urgency?: 'critical' | 'soon' | 'comfortable' | 'all'
}
