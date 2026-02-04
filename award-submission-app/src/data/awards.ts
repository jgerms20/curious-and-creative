import { Award } from '../types'

export const awardsDatabase: Award[] = [
  // TIER 1 - Premier Awards
  {
    id: 'cannes-lions',
    name: 'Cannes Lions',
    organization: 'Lions',
    website: 'https://www.canneslions.com',
    prestigeTier: 1,
    prestigeNotes: 'The Oscars of advertising. A Grand Prix is a career-defining achievement.',
    description: 'The most prestigious advertising awards globally.',
    categories: [
      { name: 'Film Lions', whatWins: 'Exceptional storytelling and emotional resonance' },
      { name: 'Film Craft Lions', whatWins: 'Technical excellence in direction, cinematography, editing' },
      { name: 'Outdoor Lions', whatWins: 'Smart use of space and context' },
      { name: 'Media Lions', whatWins: 'Innovative media thinking and channel use' },
      { name: 'PR Lions', whatWins: 'Genuine newsworthiness and earned media' },
      { name: 'Brand Experience & Activation', whatWins: 'Immersive experiences that create participation' },
      { name: 'Creative Effectiveness', whatWins: 'Creativity proven to drive business results' },
      { name: 'Creative Strategy', whatWins: 'Strategic thinking that redefines brands' },
      { name: 'Creative Data', whatWins: 'Data used creatively, not just analytically' },
      { name: 'Entertainment Lions', whatWins: 'Branded content people choose to watch' },
      { name: 'Entertainment Lions for Sport', whatWins: 'Sports-related branded entertainment' },
      { name: 'Social & Influencer', whatWins: 'Native social creativity' },
      { name: 'Innovation Lions', whatWins: 'Genuine breakthrough innovation' },
      { name: 'Titanium Lions', whatWins: 'Provocative, boundary-busting work' },
      { name: 'Glass: The Lion for Change', whatWins: 'Work challenging gender bias' }
    ],
    deadlines: {
      entryOpens: 'January 2026',
      earlyDeadline: 'March 15, 2026',
      finalDeadline: 'April 9, 2026'
    },
    costPerEntry: '$800-1500',
    judgingIntel: {
      juryComposition: 'Senior creatives, CMOs, strategists from top agencies globally',
      whatTheyValue: 'Bravery, craft, cultural impact, fresh thinking',
      redFlags: 'Work that feels safe, derivative, or overly complicated'
    },
    strategicNotes: 'Most competitive but highest prestige. Enter your absolute best work.'
  },
  {
    id: 'dandad',
    name: 'D&AD Awards',
    organization: 'D&AD',
    website: 'https://www.dandad.org/awards',
    prestigeTier: 1,
    prestigeNotes: 'Black Pencil is the rarest award in advertising. Known for brutal judging.',
    description: 'Famous for giving "no award" when work isn\'t strong enough.',
    categories: [
      { name: 'TV/Cinema Advertising', whatWins: 'Exceptional film craft' },
      { name: 'Digital Design', whatWins: 'Digital craft excellence' },
      { name: 'Direct', whatWins: 'Response-driving creativity' },
      { name: 'Integrated', whatWins: 'Campaign thinking' },
      { name: 'Media', whatWins: 'Innovative media use' },
      { name: 'Design - Branding', whatWins: 'Design excellence without compromise' },
      { name: 'Impact', whatWins: 'Purpose-driven work with real impact' },
      { name: 'Writing for Advertising', whatWins: 'Copy craft' }
    ],
    deadlines: {
      earlyDeadline: 'January',
      finalDeadline: 'February'
    },
    costPerEntry: '$500-700',
    judgingIntel: {
      whatTheyValue: 'Groundbreaking craft, bravery, work that advances the industry',
      redFlags: 'Safe work, derivative ideas, poor execution'
    },
    strategicNotes: 'A Wood Pencil is still an honor here. Only enter your absolute best.'
  },
  {
    id: 'effies',
    name: 'Effie Awards',
    organization: 'Effie Worldwide',
    website: 'https://www.effie.org',
    prestigeTier: 1,
    prestigeNotes: 'THE effectiveness awards. The only award CMOs and CFOs fully understand.',
    description: 'Championing marketing effectiveness. Results are everything.',
    categories: [
      { name: 'Beverages - Non-Alcohol', whatWins: 'Clear sales/share results' },
      { name: 'Beverages - Alcohol', whatWins: 'Responsible marketing with strong results' },
      { name: 'Consumer Products', whatWins: 'CPG marketing effectiveness' },
      { name: 'Retail', whatWins: 'Retail marketing driving performance' },
      { name: 'Financial Services', whatWins: 'Financial marketing results' },
      { name: 'Positive Change', whatWins: 'Purpose-driven work with impact metrics' },
      { name: 'Brand Experience', whatWins: 'Experiential with measurable results' },
      { name: 'Data-Driven', whatWins: 'Data-powered marketing effectiveness' },
      { name: 'Sustained Success', whatWins: 'Long-term effectiveness over multiple years' },
      { name: 'Small Budget', whatWins: 'Outsized results on limited budget' }
    ],
    deadlines: {
      earlyDeadline: 'February',
      finalDeadline: 'March'
    },
    costPerEntry: '$600-900',
    judgingIntel: {
      juryComposition: 'CMOs, marketing directors - more client-side than other awards',
      whatTheyValue: 'RESULTS. Business impact is everything. Clear objectives and attribution.',
      redFlags: 'Vague results, unverified claims, weak business connection'
    },
    strategicNotes: 'If you have strong results, this should be a priority. Requires client endorsement letter.'
  },
  {
    id: 'one-show',
    name: 'The One Show',
    organization: 'The One Club for Creativity',
    website: 'https://www.oneclub.org/theoneshow',
    prestigeTier: 1,
    prestigeNotes: 'A Gold Pencil is one of the most coveted awards. Pure creative excellence.',
    description: 'Celebrates the best in advertising and design creativity.',
    categories: [
      { name: 'Film', whatWins: 'Exceptional craft and storytelling' },
      { name: 'Print', whatWins: 'Visual impact and simplicity' },
      { name: 'Outdoor', whatWins: 'Smart contextual use of space' },
      { name: 'Interactive', whatWins: 'Digital innovation' },
      { name: 'Social Media', whatWins: 'Native social creativity' },
      { name: 'Integrated', whatWins: 'Campaigns greater than sum of parts' },
      { name: 'Creative Effectiveness', whatWins: 'Creativity proven to drive results' },
      { name: 'Innovation', whatWins: 'Genuine breakthrough ideas' }
    ],
    deadlines: {
      earlyDeadline: 'January',
      finalDeadline: 'March'
    },
    costPerEntry: '$400-600',
    judgingIntel: {
      whatTheyValue: 'Pure creativity, craft excellence, fresh ideas',
      redFlags: 'Derivative work, poor craft'
    },
    strategicNotes: 'Creative directors particularly value One Show pencils.'
  },
  {
    id: 'clio-sports',
    name: 'Clio Sports',
    organization: 'Clios',
    website: 'https://clios.com/sports',
    prestigeTier: 1,
    prestigeNotes: 'THE award for sports marketing. Essential for sports brands.',
    description: 'Celebrates creative excellence in sports marketing globally.',
    categories: [
      { name: 'Film', whatWins: 'Exceptional sports storytelling' },
      { name: 'Branded Entertainment & Content', whatWins: 'Long-form sports content people want to watch' },
      { name: 'Fan Engagement', whatWins: 'Work that connects fans to teams/sports' },
      { name: 'Experiential/Activation', whatWins: 'Live sports activations' },
      { name: 'Social Media', whatWins: 'Social-first sports content' },
      { name: 'Partnership & Sponsorship', whatWins: 'Effective sponsor activations' },
      { name: 'Athlete/Talent', whatWins: 'Exceptional use of athlete partnerships' },
      { name: 'Creative Use of Data', whatWins: 'Data-driven sports creativity' },
      { name: 'Innovation', whatWins: 'Breakthrough sports marketing innovation' },
      { name: 'Social Good', whatWins: 'Sports used for positive social impact' }
    ],
    deadlines: {
      earlyDeadline: 'December',
      finalDeadline: 'February'
    },
    costPerEntry: '$350-450',
    judgingIntel: {
      whatTheyValue: 'Authentic sports connection, fan passion, cultural impact',
      redFlags: 'Work that uses sports superficially'
    },
    strategicNotes: 'ESSENTIAL for any sports brand. FCB New York has dominated recently.'
  },
  {
    id: 'clios',
    name: 'Clio Awards',
    organization: 'Clios',
    website: 'https://clios.com',
    prestigeTier: 1,
    prestigeNotes: 'One of the oldest and most respected advertising awards (founded 1959).',
    description: 'Celebrates creative excellence across advertising and marketing.',
    categories: [
      { name: 'Film', whatWins: 'Exceptional storytelling and craft' },
      { name: 'Film Technique', whatWins: 'Technical excellence in craft areas' },
      { name: 'Out of Home', whatWins: 'Smart use of outdoor spaces' },
      { name: 'Digital/Mobile', whatWins: 'Digital innovation and craft' },
      { name: 'Social Media', whatWins: 'Native social creativity' },
      { name: 'PR', whatWins: 'Earned media excellence' },
      { name: 'Branded Entertainment', whatWins: 'Content people choose to engage with' },
      { name: 'Integrated Campaign', whatWins: 'Multi-channel work greater than sum of parts' },
      { name: 'Innovation', whatWins: 'Genuine breakthrough' },
      { name: 'Creative Use of Data', whatWins: 'Data-driven creativity' }
    ],
    deadlines: {
      earlyDeadline: 'December',
      finalDeadline: 'February'
    },
    costPerEntry: '$350-600',
    judgingIntel: {
      whatTheyValue: 'Exceptional craft, memorable creative, cultural relevance',
      redFlags: 'Work that needs heavy explanation'
    },
    strategicNotes: 'More accessible than Cannes, strong industry respect.'
  },
  {
    id: 'aicp',
    name: 'AICP Awards',
    organization: 'AICP',
    website: 'https://www.aicp.com/awards',
    prestigeTier: 1,
    prestigeNotes: 'Winning work enters the permanent MoMA collection.',
    description: 'The definitive award for production craft excellence.',
    categories: [
      { name: 'Direction', whatWins: 'Exceptional directing' },
      { name: 'Cinematography', whatWins: 'Visual excellence' },
      { name: 'Editing', whatWins: 'Edit craft' },
      { name: 'Visual Effects', whatWins: 'VFX excellence' },
      { name: 'Animation', whatWins: 'Animation craft' },
      { name: 'Color Grading', whatWins: 'Color excellence' },
      { name: 'Sound Design', whatWins: 'Audio craft' },
      { name: 'Music', whatWins: 'Music excellence' }
    ],
    deadlines: {
      finalDeadline: 'April'
    },
    costPerEntry: '$400-600',
    judgingIntel: {
      whatTheyValue: 'Technical excellence in production craft'
    },
    strategicNotes: 'Essential if you have exceptional production craft.'
  },

  // TIER 2 - Strong Industry Awards
  {
    id: 'webby-awards',
    name: 'Webby Awards',
    organization: 'IADAS',
    website: 'https://www.webbyawards.com',
    prestigeTier: 2,
    description: 'The internet\'s highest honor. Two chances to win: jury and People\'s Voice.',
    categories: [
      { name: 'Advertising, Media & PR', whatWins: 'Digital advertising excellence' },
      { name: 'Video', whatWins: 'Online video excellence' },
      { name: 'Social', whatWins: 'Social media excellence' },
      { name: 'Apps & Software', whatWins: 'App innovation' },
      { name: 'AI, Metaverse & Virtual', whatWins: 'Emerging tech' }
    ],
    deadlines: {
      finalDeadline: 'February'
    },
    costPerEntry: '$350-500',
    strategicNotes: 'Great for digital-first campaigns. Famous 5-word acceptance speeches.'
  },
  {
    id: 'shorty-awards',
    name: 'Shorty Awards',
    organization: 'Shorty Awards',
    website: 'https://shortyawards.com',
    prestigeTier: 2,
    description: 'Leading social media awards. Essential for social-first campaigns.',
    categories: [
      { name: 'Best Brand Presence', whatWins: 'Overall social presence' },
      { name: 'Best TikTok Campaign', whatWins: 'TikTok excellence' },
      { name: 'Best Instagram Campaign', whatWins: 'Instagram excellence' },
      { name: 'Best Influencer Campaign', whatWins: 'Influencer marketing' },
      { name: 'Best Real-Time Response', whatWins: 'Quick-turn cultural response' }
    ],
    deadlines: {
      finalDeadline: 'February'
    },
    costPerEntry: '$200-350',
    strategicNotes: 'Great for TikTok/social campaigns. Growing in prestige.'
  },
  {
    id: 'andy-awards',
    name: 'Andy Awards',
    organization: 'The Advertising Club of New York',
    website: 'https://www.andyawards.com',
    prestigeTier: 2,
    description: 'Creativity-focused awards with strong industry reputation.',
    categories: [
      { name: 'Film', whatWins: 'Film creativity' },
      { name: 'Print', whatWins: 'Print creativity' },
      { name: 'Interactive', whatWins: 'Digital creativity' },
      { name: 'Experiential', whatWins: 'Experiential creativity' },
      { name: 'Integrated', whatWins: 'Integrated creativity' }
    ],
    deadlines: {
      finalDeadline: 'February'
    },
    costPerEntry: '$300-450',
    strategicNotes: 'Good mid-tier option. Strong NY advertising community ties.'
  },
  {
    id: 'lia-awards',
    name: 'LIA (London International Awards)',
    organization: 'LIA',
    website: 'https://www.liaawards.com',
    prestigeTier: 2,
    description: 'Global awards judged exclusively by senior creatives.',
    categories: [
      { name: 'TV/Cinema/Online Film', whatWins: 'Film excellence' },
      { name: 'Print', whatWins: 'Print excellence' },
      { name: 'The NEW (Innovation)', whatWins: 'Innovation' },
      { name: 'Non-Traditional', whatWins: 'Non-traditional approaches' },
      { name: 'Health & Wellness', whatWins: 'Health marketing' }
    ],
    deadlines: {
      finalDeadline: 'September'
    },
    costPerEntry: '$400-600',
    strategicNotes: 'Good timing if you miss Cannes deadline. Judged only by creatives.'
  },
  {
    id: 'content-marketing-awards',
    name: 'Content Marketing Awards',
    organization: 'Content Marketing Institute',
    website: 'https://www.contentmarketingawards.com',
    prestigeTier: 2,
    description: 'Premier content marketing recognition.',
    categories: [
      { name: 'Best Overall Content Marketing', whatWins: 'Content strategy excellence' },
      { name: 'Best Video Content Program', whatWins: 'Video content' },
      { name: 'Best Social Media Content', whatWins: 'Social content' },
      { name: 'Best Podcast', whatWins: 'Podcast excellence' }
    ],
    deadlines: {
      finalDeadline: 'May'
    },
    costPerEntry: '$350-500',
    strategicNotes: 'Good for ongoing content efforts. Focus on strategic programs.'
  },
  {
    id: 'prweek-awards',
    name: 'PRWeek Awards',
    organization: 'PRWeek',
    website: 'https://www.prweek.com/us/awards',
    prestigeTier: 2,
    description: 'Top PR industry awards.',
    categories: [
      { name: 'Campaign of the Year', whatWins: 'Overall PR excellence' },
      { name: 'Best Product Launch', whatWins: 'Launch PR' },
      { name: 'Best Influencer Strategy', whatWins: 'Influencer PR' },
      { name: 'Best Integrated Campaign', whatWins: 'Integrated PR' }
    ],
    costPerEntry: '$350-500',
    strategicNotes: 'Good for campaigns with significant earned media component.'
  },
  {
    id: 'event-marketer-ex',
    name: 'Event Marketer Ex Awards',
    organization: 'Event Marketer',
    website: 'https://www.eventmarketer.com/ex-awards',
    prestigeTier: 2,
    description: 'Top experiential marketing awards.',
    categories: [
      { name: 'Best Sports Experience', whatWins: 'Sports experiential' },
      { name: 'Best Sampling', whatWins: 'Sampling programs' },
      { name: 'Best Festival Activation', whatWins: 'Festival activations' },
      { name: 'Best Pop-Up', whatWins: 'Pop-up experiences' }
    ],
    costPerEntry: '$350-500',
    strategicNotes: 'Essential for experiential activations. Has dedicated sports category.'
  },
  {
    id: 'digiday-awards',
    name: 'Digiday Awards',
    organization: 'Digiday',
    website: 'https://digiday.com/awards',
    prestigeTier: 2,
    description: 'Multiple programs for media, marketing, content excellence.',
    categories: [
      { name: 'Marketing Awards', whatWins: 'Marketing excellence' },
      { name: 'Content Awards', whatWins: 'Content excellence' },
      { name: 'Video Awards', whatWins: 'Video excellence' }
    ],
    strategicNotes: 'Multiple opportunities throughout year.'
  },
  {
    id: 'tiktok-ad-awards',
    name: 'TikTok Ad Awards',
    organization: 'TikTok',
    website: 'https://www.tiktok.com/business/ad-awards',
    prestigeTier: 2,
    description: 'Platform-specific recognition for TikTok advertising.',
    categories: [
      { name: 'Best Creative Excellence', whatWins: 'TikTok-native creativity' },
      { name: 'Best Brand Community', whatWins: 'Community building' },
      { name: 'Best Brand Partnership', whatWins: 'Creator partnerships' }
    ],
    costPerEntry: 'Often free',
    strategicNotes: 'Less competition than major awards. Great for TikTok-native work.'
  },
  {
    id: 'youtube-works',
    name: 'YouTube Works Awards',
    organization: 'YouTube/Google',
    website: 'https://www.youtube.com/ads/youtube-works',
    prestigeTier: 2,
    description: 'Recognizes the best YouTube advertising.',
    categories: [
      { name: 'Best Long-Form', whatWins: 'Long-form YouTube content' },
      { name: 'Best Brand Builder', whatWins: 'Brand-building video' },
      { name: 'Grand Prix', whatWins: 'Overall YouTube excellence' }
    ],
    costPerEntry: 'Often free',
    strategicNotes: 'Free to enter, platform recognition.'
  },

  // TIER 3 - Volume/Regional
  {
    id: 'addys',
    name: 'ADDY Awards',
    organization: 'AAF',
    website: 'https://www.aaf.org',
    prestigeTier: 3,
    description: 'Largest advertising competition. Local to National ladder.',
    categories: [
      { name: 'Film/Video/Sound', whatWins: 'Video work' },
      { name: 'Print', whatWins: 'Print work' },
      { name: 'Cross-Platform', whatWins: 'Multi-platform' },
      { name: 'Interactive', whatWins: 'Digital work' }
    ],
    deadlines: {
      finalDeadline: 'January (local)'
    },
    costPerEntry: '$100-300',
    strategicNotes: 'Volume play - enter lots at local level. Must win local to advance.'
  },
  {
    id: 'telly-awards',
    name: 'Telly Awards',
    organization: 'Telly Awards',
    website: 'https://www.tellyawards.com',
    prestigeTier: 3,
    description: 'Honors video and television excellence. Multiple winner tiers.',
    categories: [
      { name: 'Television', whatWins: 'TV content' },
      { name: 'Video', whatWins: 'Video content' },
      { name: 'Branded Content', whatWins: 'Branded video' },
      { name: 'Social Video', whatWins: 'Social video' }
    ],
    deadlines: {
      finalDeadline: 'March'
    },
    costPerEntry: '$200-400',
    strategicNotes: 'Higher win rate. Good for building momentum.'
  }
]
