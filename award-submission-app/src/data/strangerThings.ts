import type { Campaign, Submission } from '../types'

// Gatorade x Stranger Things Campaign Data
// Based on the awards kickoff meeting transcript

export const strangerThingsCampaign: Campaign = {
  id: 'gatorade-stranger-things-2024',
  name: 'Gatorade Endorses Eleven',
  client: 'PepsiCo',
  brand: 'Gatorade',
  industry: 'Beverages / Sports',
  dates: {
    campaignStart: '2024-07-01',
    campaignEnd: '2024-12-31'
  },
  brief: {
    challenge: 'Expand Gatorade\'s reach beyond traditional sports audiences while celebrating the final season of Stranger Things',
    context: 'Netflix\'s Stranger Things final season premiere was a massive cultural moment with millions of fans worldwide. Gatorade had an authentic connection - the glass bottle Eleven drinks from actually existed in the 1980s.',
    targetAudience: 'Stranger Things fans, women, younger demographics who may not identify as "athletes" in the traditional sense',
    keyInsight: 'Not every GOAT fights on courts, tracks, and fields. Some are in a whole other world.',
    budgetTier: 'large'
  },
  strategy: {
    strategicApproach: 'Position Eleven as a legitimate Gatorade-endorsed athlete alongside legends like Jordan, Serena, and Bolt - the first sports endorsement of a fictional character',
    whyThisStrategy: 'Rather than just sponsoring the show like other brands, we made Eleven one of the GOATs, creating an authentic endorsement that expanded who can be considered an "athlete"'
  },
  creative: {
    bigIdea: 'The first sports endorsement of a fictional character',
    tagline: 'Whether they\'re fighting on a field or in the Upside Down, the GOATs all use the same fuel',
    whatMadeItSpecial: 'We didn\'t just sponsor Stranger Things - we signed Eleven to the Gatorade roster. Athletes like Miles Garrett, George Kittle, and Francisco Lindor welcomed her to the team on social. The retro glass bottle she drinks from in the show was an authentic 1980s Gatorade product.',
    craftElements: [
      'NFL Christmas Game Commercial',
      'Retro glass bottle product line',
      'Merchandise collection with character artwork',
      'Athlete social content welcoming Eleven'
    ],
    innovationElements: [
      'First fictional character sports endorsement',
      'Cross-platform storytelling from show to social to retail',
      'Authentic nostalgia play with real 1980s product'
    ]
  },
  executionTypes: [
    'TV/Film',
    'Social Media',
    'OOH/Outdoor',
    'Product/Packaging',
    'Retail/POS',
    'Athlete/Influencer Content',
    'Experiential'
  ],
  talent: {
    athletes: [
      { name: 'Miles Garrett', sport: 'NFL - Cleveland Browns' },
      { name: 'George Kittle', sport: 'NFL - San Francisco 49ers' },
      { name: 'Francisco Lindor', sport: 'MLB - New York Mets' }
    ],
    celebrities: [
      { name: 'Millie Bobby Brown (Eleven)' }
    ]
  },
  partnerships: [
    {
      partnerName: 'Netflix',
      partnerType: 'Entertainment/Streaming',
      description: 'Co-developed the Eleven endorsement campaign for Stranger Things final season'
    },
    {
      partnerName: 'Target',
      partnerType: 'Retail',
      description: 'Exclusive Gatorade squeeze bottle "Property of Eleven"'
    }
  ],
  results: {
    summary: 'Became Netflix\'s most talked-about brand partnership. Merchandise sold out in 5 minutes and broke the Gatorade website.',
    business: {
      sales: { result: 'Merch sold out in 5 minutes', vsObjective: 'TBD - awaiting Adam\'s data' },
      roi: 'TBD - awaiting business results'
    },
    brand: {
      awareness: { lift: 'TBD', vsBenchmark: 'TBD' },
      consideration: { lift: 'TBD' }
    },
    engagement: {
      impressions: '2.3B+',
      socialEngagement: '4M+ social interactions',
      earnedMediaValue: 'TBD'
    },
    cultural: {
      moments: [
        'NFL Christmas Game commercial premiere',
        'Athletes welcoming Eleven to roster',
        'Retro merch drop sellout'
      ],
      celebrityMentions: [
        'Miles Garrett Instagram post',
        'George Kittle social content',
        'Francisco Lindor welcome'
      ],
      pressCoverage: [
        'Nice Kicks',
        'Complex',
        'Yahoo Sports'
      ]
    },
    verified: false,
    source: 'Internal reports + Netflix confirmation'
  },
  awardPotential: {
    craftStrength: 8,
    ideaStrength: 9,
    resultsStrength: 7, // Need more verified data
    innovationStrength: 9,
    culturalImpactStrength: 9,
    strongestAngles: [
      'First fictional character endorsement in sports',
      'Authentic nostalgia with real 1980s product',
      'Expanding who can be an "athlete"',
      'Netflix\'s most talked-about partnership'
    ],
    weaknesses: [
      'Need verified business results for Effie-tier effectiveness',
      'The TV commercial doesn\'t feature Eleven directly',
      'Competition from other Stranger Things partnerships'
    ]
  }
}

// Pre-populated submissions for Stranger Things campaign
export const strangerThingsSubmissions: Submission[] = [
  // Cannes Lions
  {
    id: 'st-cannes-entertainment',
    campaignId: 'gatorade-stranger-things-2024',
    campaignName: 'Gatorade Endorses Eleven',
    awardId: 'cannes-lions',
    awardName: 'Cannes Lions',
    category: 'Entertainment Lions - Sport',
    status: 'draft',
    deadline: '2025-03-21',
    submittedBy: 'tbwa',
    entryCost: 850,
    notes: 'Main submission - fictional endorsement angle',
    lastUpdated: new Date().toISOString(),
    createdAt: new Date().toISOString()
  },
  {
    id: 'st-cannes-brand-exp',
    campaignId: 'gatorade-stranger-things-2024',
    campaignName: 'Gatorade Endorses Eleven',
    awardId: 'cannes-lions',
    awardName: 'Cannes Lions',
    category: 'Brand Experience & Activation',
    status: 'not_started',
    deadline: '2025-03-21',
    submittedBy: 'tbwa',
    entryCost: 850,
    notes: '',
    lastUpdated: new Date().toISOString(),
    createdAt: new Date().toISOString()
  },
  // D&AD
  {
    id: 'st-dad-collab',
    campaignId: 'gatorade-stranger-things-2024',
    campaignName: 'Gatorade Endorses Eleven',
    awardId: 'dad',
    awardName: 'D&AD',
    category: 'Collaborative - Brand Collaboration',
    status: 'draft',
    deadline: '2025-02-18',
    submittedBy: 'tbwa',
    entryCost: 595,
    notes: 'Focus on Netflix partnership',
    lastUpdated: new Date().toISOString(),
    createdAt: new Date().toISOString()
  },
  {
    id: 'st-dad-integrated',
    campaignId: 'gatorade-stranger-things-2024',
    campaignName: 'Gatorade Endorses Eleven',
    awardId: 'dad',
    awardName: 'D&AD',
    category: 'Integrated',
    status: 'not_started',
    deadline: '2025-02-18',
    submittedBy: 'tbwa',
    entryCost: 595,
    notes: '',
    lastUpdated: new Date().toISOString(),
    createdAt: new Date().toISOString()
  },
  // Clio Awards
  {
    id: 'st-clio-sports-integrated',
    campaignId: 'gatorade-stranger-things-2024',
    campaignName: 'Gatorade Endorses Eleven',
    awardId: 'clio-sports',
    awardName: 'Clio Sports',
    category: 'Integrated Campaign',
    status: 'in_review',
    deadline: '2025-02-16',
    submittedBy: 'tbwa',
    entryCost: 400,
    notes: 'Extended deadline - original was Feb 6',
    lastUpdated: new Date().toISOString(),
    createdAt: new Date().toISOString()
  },
  {
    id: 'st-clio-sports-partnership',
    campaignId: 'gatorade-stranger-things-2024',
    campaignName: 'Gatorade Endorses Eleven',
    awardId: 'clio-sports',
    awardName: 'Clio Sports',
    category: 'Sports Partnership',
    status: 'draft',
    deadline: '2025-02-16',
    submittedBy: 'tbwa',
    entryCost: 400,
    notes: '',
    lastUpdated: new Date().toISOString(),
    createdAt: new Date().toISOString()
  },
  // One Show
  {
    id: 'st-oneshow-branded',
    campaignId: 'gatorade-stranger-things-2024',
    campaignName: 'Gatorade Endorses Eleven',
    awardId: 'one-show',
    awardName: 'The One Show',
    category: 'Branded Entertainment',
    status: 'not_started',
    deadline: '2025-02-28',
    submittedBy: 'tbwa',
    entryCost: 500,
    notes: '',
    lastUpdated: new Date().toISOString(),
    createdAt: new Date().toISOString()
  },
  // Netflix submissions
  {
    id: 'st-cannes-netflix',
    campaignId: 'gatorade-stranger-things-2024',
    campaignName: 'Gatorade Endorses Eleven',
    awardId: 'cannes-lions',
    awardName: 'Cannes Lions',
    category: 'Entertainment Lions for Music',
    status: 'not_started',
    deadline: '2025-03-21',
    submittedBy: 'netflix',
    entryCost: 850,
    notes: 'Netflix lead - coordinate with Reed',
    lastUpdated: new Date().toISOString(),
    createdAt: new Date().toISOString()
  },
  // Effies (later deadline)
  {
    id: 'st-effie-beverages',
    campaignId: 'gatorade-stranger-things-2024',
    campaignName: 'Gatorade Endorses Eleven',
    awardId: 'effies',
    awardName: 'Effie Awards',
    category: 'Beverages - Non-Alcohol',
    status: 'not_started',
    deadline: '2025-06-15',
    submittedBy: 'tbwa',
    entryCost: 650,
    notes: 'Need verified business results from Adam before submitting',
    lastUpdated: new Date().toISOString(),
    createdAt: new Date().toISOString()
  }
]

// Helper to calculate total entry costs
export function calculateTotalCost(submissions: Submission[]): number {
  return submissions.reduce((sum, s) => sum + (s.entryCost || 0), 0)
}

// Helper to get submissions by status
export function getSubmissionsByStatus(submissions: Submission[], status: string): Submission[] {
  return submissions.filter(s => s.status === status)
}

// Story angles for the campaign
export const strangerThingsAngles = [
  {
    id: 'fictional-endorsement',
    name: 'First Fictional Character Endorsement',
    description: 'Position this as groundbreaking - the first time a sports brand has officially endorsed a fictional character as an athlete',
    bestFor: ['Entertainment categories', 'Innovation categories', 'Integrated campaigns'],
    keyLine: 'The greatest athletes of all time all relied on Gatorade. But not every GOAT fights on courts, tracks, and fields. Some are in a whole other world.'
  },
  {
    id: 'authentic-nostalgia',
    name: 'Authentic Nostalgia',
    description: 'Unlike other Stranger Things partnerships that created gimmicky products, our glass bottle actually existed in the 1980s',
    bestFor: ['Craft categories', 'Product design', 'Authenticity-focused awards'],
    keyLine: 'While other brands created products for the Stranger Things universe, we brought back a real piece of it.'
  },
  {
    id: 'expanding-athlete',
    name: 'Expanding Who\'s an Athlete',
    description: 'Ties into broader Gatorade strategy of redefining what it means to be an athlete',
    bestFor: ['Strategy awards', 'Effectiveness (if we get the data)', 'Cultural impact'],
    keyLine: 'X% of women don\'t identify as athletes. By endorsing Eleven, we showed that being an athlete isn\'t about what sport you play - it\'s about the fight in you.'
  }
]
