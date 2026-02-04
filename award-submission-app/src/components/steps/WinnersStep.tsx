import { useState } from 'react'
import {
  Trophy,
  ArrowLeft,
  Star,
  Lightbulb,
  CheckCircle,
  ExternalLink
} from 'lucide-react'

interface WinnersStepProps {
  onBack: () => void
}

const winners2024 = [
  {
    id: 'womens-football',
    campaign: "WoMen's Football",
    brand: 'Orange',
    agency: 'Marcel Paris',
    awards: [
      'Cannes Lions Grand Prix - Film',
      'Cannes Lions Grand Prix - Social & Influencer',
      'D&AD Black Pencil - Digital & Social',
      'Clio Grand - Film',
      'Clio Grand - Partnerships'
    ],
    idea: "Showed footage of what appeared to be men's football team performing impressive moves, then revealed through VFX it was actually the French women's national team - exposing gender bias in how we perceive athletic excellence.",
    whyItWon: [
      'Simple, powerful insight: gender bias in football',
      'Brilliant twist reveal using VFX',
      'Cultural conversation starter',
      'Became an educational tool'
    ],
    lessons: [
      'Great ideas often expose what people don\'t realize about themselves',
      'The reveal/twist structure is powerful when executed well',
      'Work that changes behavior/perception > work that just entertains',
      'Production craft must serve the idea, not overshadow it'
    ],
    categories: ['Film', 'Social', 'Partnerships', 'Glass/Gender']
  },
  {
    id: 'all-the-ads',
    campaign: 'All The Ads',
    brand: 'DoorDash',
    agency: 'Wieden+Kennedy',
    awards: [
      'Cannes Lions Titanium Grand Prix',
      'Cannes Lions Grand Prix - Direct'
    ],
    idea: 'During the Super Bowl, DoorDash ran a promotion where one person could win every single product advertised during the entire game by entering a code made up of all the other advertisers\' promo codes.',
    whyItWon: [
      'Audacious idea that hijacked competitors\' Super Bowl moments',
      'Simple to explain, easy to participate',
      'Genuine brand utility - actually gave away $3M+ in products',
      'Owned the Super Bowl conversation without biggest spend'
    ],
    lessons: [
      'Titanium rewards work that\'s genuinely provocative/new',
      'The idea itself became the story (meta-advertising)',
      'Brand utility > brand messaging',
      'Sometimes the best Super Bowl ad isn\'t an ad'
    ],
    categories: ['Titanium', 'Direct', 'Media', 'PR']
  },
  {
    id: 'edible-mascot',
    campaign: 'The First Edible Mascot',
    brand: 'Pop-Tarts',
    agency: 'Weber Shandwick',
    awards: [
      'Cannes Lions Grand Prix - Brand Experience & Activation'
    ],
    idea: 'Created a giant edible Pop-Tart mascot that was lowered into a giant toaster at halftime of the Pop-Tarts Bowl and eaten by players/fans after the game.',
    whyItWon: [
      'Genuinely unexpected - no one had ever made an edible mascot',
      'Created real participation - people actually ate the mascot',
      'Perfect for social - visually absurd and memorable',
      'Matched Pop-Tarts\' playful brand personality perfectly'
    ],
    lessons: [
      'Experiential judges want genuine participation, not just installations',
      'First-ever claims are powerful if legitimate',
      'Match the activation to the brand personality',
      'Create moments that people naturally want to share'
    ],
    categories: ['Brand Experience', 'Experiential', 'PR', 'Social']
  },
  {
    id: 'wheretosettle',
    campaign: 'WhereToSettle',
    brand: 'Mastercard',
    agency: 'McCann Poland',
    awards: [
      'D&AD Black Pencil - Experiential',
      'Cannes Lions Grand Prix - Creative Data',
      'Clio Grand - Real-Time',
      'Clio Grand - Creative Use of Data'
    ],
    idea: 'Created a data platform that analyzed 17 different factors to help Ukrainian refugees find the best place to settle in Poland based on their skills, needs, and available opportunities.',
    whyItWon: [
      'Genuine utility - solved a real, urgent human problem',
      'Smart data use - data for good, not just targeting',
      'Scalable impact - helped 500K+ people make life decisions',
      'Made Mastercard\'s "priceless" positioning tangible'
    ],
    lessons: [
      'Data awards want to see data used creatively, not just analytically',
      'Purpose work wins when impact is real and measurable',
      'Brand utility > brand advertising',
      'Solve actual problems, not manufactured ones'
    ],
    categories: ['Creative Data', 'Innovation', 'Real-Time', 'Social Good']
  },
  {
    id: 'voice-2-diabetes',
    campaign: 'Voice 2 Diabetes',
    brand: 'Klick Health',
    agency: 'Klick Health',
    awards: [
      'Cannes Lions Grand Prix - Innovation'
    ],
    idea: 'Developed AI technology that can detect Type 2 diabetes through voice analysis with 89% accuracy, making screening accessible via smartphone.',
    whyItWon: [
      'Genuine breakthrough - actually invented something new and useful',
      'Accessibility - made health screening available to anyone with a phone',
      'Proof of concept - 89% accuracy is clinically significant',
      'Scalable potential - could change how diabetes is detected globally'
    ],
    lessons: [
      'Innovation judges want genuine breakthroughs, not feature tweaks',
      'Health/pharma work wins when it actually helps patients',
      'Prove it works with real data',
      'Show scalable potential, not just proof of concept'
    ],
    categories: ['Innovation', 'Health', 'Technology']
  },
  {
    id: 'misheard-version',
    campaign: 'The Misheard Version',
    brand: 'Specsavers',
    agency: 'Golin',
    awards: [
      'Cannes Lions Grand Prix - Radio & Audio',
      'Cannes Lions Grand Prix - PR'
    ],
    idea: 'To highlight hearing loss, Specsavers had Rick Astley re-record "Never Gonna Give You Up" as people with hearing loss mishear it, turning viral "rickrolling" into an awareness campaign.',
    whyItWon: [
      'Cultural hijack - took existing phenomenon and repurposed it',
      'Authentic insight - based on real misheard lyrics from people with hearing loss',
      'Earned media - Rick Astley participation generated massive coverage',
      'The re-recorded song itself was the creative work'
    ],
    lessons: [
      'Audio awards rarely given - this was genuinely innovative in the space',
      'Cultural hijacks work when they add meaning, not just attention',
      'Celebrity participation amplifies when authentic to concept',
      'Humor + purpose can coexist'
    ],
    categories: ['Audio', 'PR', 'Entertainment', 'Social Good']
  },
  {
    id: 'handshake-hunt',
    campaign: 'Handshake Hunt',
    brand: 'Mercado Libre',
    agency: 'Gut Buenos Aires',
    awards: [
      'Cannes Lions Grand Prix - Media'
    ],
    idea: 'Turned handshakes in other brands\' TV commercials into QR codes that, when scanned, delivered Mercado Libre discounts - essentially hijacking competitors\' media spend.',
    whyItWon: [
      'Media innovation - used other people\'s ads as their media channel',
      'Interactivity - made passive TV viewing interactive',
      'Clever mechanics - handshakes are everywhere in ads',
      'Brand fit - Mercado Libre\'s logo IS a handshake'
    ],
    lessons: [
      'Media awards want to see channels used in genuinely new ways',
      'Hijacking existing behavior/content can be brilliant',
      'Connect the mechanic to something true about your brand',
      'Interactive TV is an underexplored space'
    ],
    categories: ['Media', 'Innovation', 'Digital', 'Mobile']
  },
  {
    id: 'heinz',
    campaign: 'It Has to be Heinz',
    brand: 'Heinz',
    agency: 'Rethink',
    awards: [
      'Cannes Lions Grand Prix - Creative Effectiveness',
      'One Show Penta Pencil (5+ year partnership)'
    ],
    idea: 'A multi-year platform proving that when it comes to ketchup, consumers irrationally insist on Heinz - shown through various creative expressions including AI-generated images, restaurant swaps, and cultural moments.',
    whyItWon: [
      'Strategic platform - not just a campaign but an ongoing brand truth',
      'Consistency - 5+ years of the same strategic direction',
      'Strong, verified business results',
      'Creative flexibility - platform flexed across many executions'
    ],
    lessons: [
      'Creative Effectiveness needs BOTH great creative AND proven results',
      'Long-term platforms beat one-off campaigns',
      'The Penta Pencil rewards client/agency partnership longevity',
      'Strategic consistency across years is highly valued'
    ],
    categories: ['Creative Effectiveness', 'Integrated', 'Film']
  }
]

export function WinnersStep({ onBack }: WinnersStepProps) {
  const [activeWinner, setActiveWinner] = useState(winners2024[0].id)

  const getActiveWinner = () => winners2024.find(w => w.id === activeWinner)

  return (
    <div className="step-container winners-step">
      <div className="step-header">
        <div className="step-icon-large">
          <Trophy size={32} />
        </div>
        <div className="step-header-text">
          <h2>2024 Grand Prix Winners</h2>
          <p>Learn from the best - what won and why</p>
        </div>
      </div>

      <div className="winners-layout">
        {/* Sidebar */}
        <div className="winners-sidebar">
          <h3>Grand Prix Winners</h3>
          <div className="winners-list">
            {winners2024.map(winner => (
              <button
                key={winner.id}
                className={`winner-item ${activeWinner === winner.id ? 'active' : ''}`}
                onClick={() => setActiveWinner(winner.id)}
              >
                <div className="winner-item-content">
                  <span className="winner-campaign">{winner.campaign}</span>
                  <span className="winner-brand">{winner.brand}</span>
                </div>
                <span className="winner-awards-count">{winner.awards.length}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="winner-detail">
          {getActiveWinner() && (
            <>
              <div className="winner-header">
                <div>
                  <h3>{getActiveWinner()!.campaign}</h3>
                  <p className="winner-meta">
                    {getActiveWinner()!.brand} • {getActiveWinner()!.agency}
                  </p>
                </div>
              </div>

              <div className="winner-awards">
                <h4>
                  <Trophy size={18} />
                  Awards Won
                </h4>
                <div className="awards-list">
                  {getActiveWinner()!.awards.map((award, i) => (
                    <span key={i} className="award-badge">
                      <Star size={12} />
                      {award}
                    </span>
                  ))}
                </div>
              </div>

              <div className="winner-idea">
                <h4>
                  <Lightbulb size={18} />
                  The Idea
                </h4>
                <p>{getActiveWinner()!.idea}</p>
              </div>

              <div className="winner-section">
                <h4>
                  <CheckCircle size={18} />
                  Why It Won
                </h4>
                <ul>
                  {getActiveWinner()!.whyItWon.map((reason, i) => (
                    <li key={i}>{reason}</li>
                  ))}
                </ul>
              </div>

              <div className="winner-section lessons">
                <h4>
                  <Star size={18} />
                  Key Lessons
                </h4>
                <ul>
                  {getActiveWinner()!.lessons.map((lesson, i) => (
                    <li key={i}>{lesson}</li>
                  ))}
                </ul>
              </div>

              <div className="winner-categories">
                <h4>Best Fit Categories</h4>
                <div className="category-tags">
                  {getActiveWinner()!.categories.map((cat, i) => (
                    <span key={i} className="category-tag">{cat}</span>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Patterns Summary */}
      <div className="patterns-summary">
        <h3>2024 Winning Patterns</h3>
        <div className="patterns-grid">
          <div className="pattern-card">
            <h4>Purpose with Proof</h4>
            <p>Social good work that has REAL impact metrics, not just awareness</p>
          </div>
          <div className="pattern-card">
            <h4>Smart Data Use</h4>
            <p>Data as creative fuel, not just targeting</p>
          </div>
          <div className="pattern-card">
            <h4>Brand Utility</h4>
            <p>Brands solving actual problems for people</p>
          </div>
          <div className="pattern-card">
            <h4>Challenging Norms</h4>
            <p>Work that questions bias or convention</p>
          </div>
          <div className="pattern-card">
            <h4>Humor Returns</h4>
            <p>Making a comeback after years of serious advertising</p>
          </div>
          <div className="pattern-card">
            <h4>Experiential Participation</h4>
            <p>Activations where people DO things, not just watch</p>
          </div>
        </div>
      </div>

      <div className="step-actions">
        <button className="btn btn-secondary" onClick={onBack}>
          <ArrowLeft size={18} />
          Back
        </button>
      </div>
    </div>
  )
}
