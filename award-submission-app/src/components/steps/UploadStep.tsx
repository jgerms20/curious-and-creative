import { useState } from 'react'
import {
  Upload,
  FileText,
  Briefcase,
  Target,
  Lightbulb,
  Palette,
  Users,
  BarChart3,
  ArrowRight,
  Plus,
  X,
  ChevronDown,
  ChevronUp
} from 'lucide-react'
import { Campaign } from '../../types'

interface UploadStepProps {
  campaign: Campaign | null
  setCampaign: (campaign: Campaign) => void
  onNext: () => void
}

const industries = [
  { value: 'sports_beverages', label: 'Sports & Beverages' },
  { value: 'beverages_non_alcohol', label: 'Beverages (Non-Alcohol)' },
  { value: 'beverages_alcohol', label: 'Beverages (Alcohol)' },
  { value: 'food_snacks', label: 'Food & Snacks' },
  { value: 'automotive', label: 'Automotive' },
  { value: 'technology', label: 'Technology' },
  { value: 'financial_services', label: 'Financial Services' },
  { value: 'healthcare_pharma', label: 'Healthcare & Pharma' },
  { value: 'retail', label: 'Retail' },
  { value: 'entertainment_media', label: 'Entertainment & Media' },
  { value: 'fashion_apparel', label: 'Fashion & Apparel' },
  { value: 'beauty_personal_care', label: 'Beauty & Personal Care' },
  { value: 'b2b_services', label: 'B2B Services' },
  { value: 'nonprofit', label: 'Nonprofit' },
  { value: 'other', label: 'Other' }
]

const executionTypes = [
  { value: 'tv_spot_30', label: 'TV Spot (:30)' },
  { value: 'tv_spot_60', label: 'TV Spot (:60)' },
  { value: 'online_video', label: 'Online Video' },
  { value: 'social_video_short', label: 'Social Video (Short)' },
  { value: 'tiktok', label: 'TikTok' },
  { value: 'instagram_reels', label: 'Instagram Reels' },
  { value: 'youtube_content', label: 'YouTube Content' },
  { value: 'print_single', label: 'Print (Single)' },
  { value: 'print_campaign', label: 'Print (Campaign)' },
  { value: 'outdoor_static', label: 'Outdoor/OOH (Static)' },
  { value: 'outdoor_digital', label: 'Outdoor/OOH (Digital)' },
  { value: 'experiential_event', label: 'Experiential Event' },
  { value: 'experiential_activation', label: 'Activation' },
  { value: 'influencer_partnership', label: 'Influencer Partnership' },
  { value: 'branded_content_short', label: 'Branded Content (Short)' },
  { value: 'branded_content_documentary', label: 'Documentary' },
  { value: 'website', label: 'Website' },
  { value: 'app', label: 'App' },
  { value: 'pr_stunt', label: 'PR Stunt' },
  { value: 'pr_earned_media', label: 'PR/Earned Media' },
  { value: 'podcast', label: 'Podcast' },
  { value: 'radio_audio', label: 'Radio/Audio' }
]

export function UploadStep({ campaign, setCampaign, onNext }: UploadStepProps) {
  const [mode, setMode] = useState<'form' | 'paste' | 'upload'>('form')
  const [expandedSections, setExpandedSections] = useState<string[]>(['basics', 'brief'])
  const [pastedText, setPastedText] = useState('')

  const [formData, setFormData] = useState<Partial<Campaign>>(campaign || {
    id: '',
    name: '',
    client: '',
    brand: '',
    industry: '',
    dates: {},
    brief: {
      challenge: '',
      context: '',
      targetAudience: '',
      keyInsight: '',
      budgetTier: 'medium'
    },
    strategy: {
      strategicApproach: '',
      whyThisStrategy: ''
    },
    creative: {
      bigIdea: '',
      tagline: '',
      whatMadeItSpecial: '',
      craftElements: [],
      innovationElements: []
    },
    executionTypes: [],
    talent: {
      athletes: [],
      celebrities: [],
      influencers: []
    },
    partnerships: [],
    results: {
      summary: '',
      business: {},
      brand: {},
      engagement: {},
      cultural: {},
      verified: false,
      source: ''
    },
    awardPotential: {
      craftStrength: 5,
      ideaStrength: 5,
      resultsStrength: 5,
      innovationStrength: 5,
      culturalImpactStrength: 5,
      strongestAngles: [],
      weaknesses: []
    }
  })

  const toggleSection = (section: string) => {
    setExpandedSections(prev =>
      prev.includes(section)
        ? prev.filter(s => s !== section)
        : [...prev, section]
    )
  }

  const updateForm = (path: string, value: any) => {
    setFormData(prev => {
      const newData = { ...prev }
      const parts = path.split('.')
      let current: any = newData
      for (let i = 0; i < parts.length - 1; i++) {
        if (!current[parts[i]]) current[parts[i]] = {}
        current = current[parts[i]]
      }
      current[parts[parts.length - 1]] = value
      return newData
    })
  }

  const handleSubmit = () => {
    const id = formData.name?.toLowerCase().replace(/\s+/g, '-') + '-' + Date.now()
    const fullCampaign: Campaign = {
      ...formData as Campaign,
      id
    }
    setCampaign(fullCampaign)
    onNext()
  }

  const isFormValid = () => {
    return formData.name && formData.brand && formData.brief?.challenge && formData.creative?.bigIdea
  }

  return (
    <div className="step-container upload-step">
      <div className="step-header">
        <div className="step-icon-large">
          <Upload size={32} />
        </div>
        <div className="step-header-text">
          <h2>Campaign Input</h2>
          <p>Enter your campaign details or paste from a brief</p>
        </div>
      </div>

      <div className="input-mode-tabs">
        <button
          className={`mode-tab ${mode === 'form' ? 'active' : ''}`}
          onClick={() => setMode('form')}
        >
          <FileText size={18} />
          Structured Form
        </button>
        <button
          className={`mode-tab ${mode === 'paste' ? 'active' : ''}`}
          onClick={() => setMode('paste')}
        >
          <Briefcase size={18} />
          Paste Brief/Deck
        </button>
        <button
          className={`mode-tab ${mode === 'upload' ? 'active' : ''}`}
          onClick={() => setMode('upload')}
        >
          <Upload size={18} />
          Upload Document
        </button>
      </div>

      {mode === 'form' && (
        <div className="form-sections">
          {/* BASICS */}
          <FormSection
            title="Campaign Basics"
            icon={<Briefcase size={20} />}
            id="basics"
            expanded={expandedSections.includes('basics')}
            onToggle={() => toggleSection('basics')}
          >
            <div className="form-grid">
              <FormField label="Campaign Name" required>
                <input
                  type="text"
                  value={formData.name || ''}
                  onChange={e => updateForm('name', e.target.value)}
                  placeholder="e.g., 'Just Do It' 2024"
                />
              </FormField>
              <FormField label="Brand" required>
                <input
                  type="text"
                  value={formData.brand || ''}
                  onChange={e => updateForm('brand', e.target.value)}
                  placeholder="e.g., Nike"
                />
              </FormField>
              <FormField label="Client/Company">
                <input
                  type="text"
                  value={formData.client || ''}
                  onChange={e => updateForm('client', e.target.value)}
                  placeholder="e.g., Nike Inc."
                />
              </FormField>
              <FormField label="Industry">
                <select
                  value={formData.industry || ''}
                  onChange={e => updateForm('industry', e.target.value)}
                >
                  <option value="">Select industry...</option>
                  {industries.map(i => (
                    <option key={i.value} value={i.value}>{i.label}</option>
                  ))}
                </select>
              </FormField>
              <FormField label="Campaign Start">
                <input
                  type="date"
                  value={formData.dates?.campaignStart || ''}
                  onChange={e => updateForm('dates.campaignStart', e.target.value)}
                />
              </FormField>
              <FormField label="Campaign End">
                <input
                  type="date"
                  value={formData.dates?.campaignEnd || ''}
                  onChange={e => updateForm('dates.campaignEnd', e.target.value)}
                />
              </FormField>
            </div>
          </FormSection>

          {/* BRIEF */}
          <FormSection
            title="The Brief"
            icon={<Target size={20} />}
            id="brief"
            expanded={expandedSections.includes('brief')}
            onToggle={() => toggleSection('brief')}
          >
            <FormField label="Business Challenge" required>
              <textarea
                value={formData.brief?.challenge || ''}
                onChange={e => updateForm('brief.challenge', e.target.value)}
                placeholder="What business problem were you solving?"
                rows={3}
              />
            </FormField>
            <FormField label="Competitive Context">
              <textarea
                value={formData.brief?.context || ''}
                onChange={e => updateForm('brief.context', e.target.value)}
                placeholder="Market dynamics, competitor landscape..."
                rows={2}
              />
            </FormField>
            <FormField label="Target Audience">
              <input
                type="text"
                value={formData.brief?.targetAudience || ''}
                onChange={e => updateForm('brief.targetAudience', e.target.value)}
                placeholder="Who were you trying to reach?"
              />
            </FormField>
            <FormField label="Key Insight" hint="The human/cultural truth that unlocked the creative">
              <textarea
                value={formData.brief?.keyInsight || ''}
                onChange={e => updateForm('brief.keyInsight', e.target.value)}
                placeholder="What did you discover that others missed?"
                rows={2}
              />
            </FormField>
            <FormField label="Budget Tier">
              <select
                value={formData.brief?.budgetTier || 'medium'}
                onChange={e => updateForm('brief.budgetTier', e.target.value)}
              >
                <option value="micro">Micro (under $100K)</option>
                <option value="small">Small ($100K-$500K)</option>
                <option value="medium">Medium ($500K-$2M)</option>
                <option value="large">Large ($2M-$10M)</option>
                <option value="mega">Mega ($10M+)</option>
              </select>
            </FormField>
          </FormSection>

          {/* CREATIVE */}
          <FormSection
            title="The Creative"
            icon={<Lightbulb size={20} />}
            id="creative"
            expanded={expandedSections.includes('creative')}
            onToggle={() => toggleSection('creative')}
          >
            <FormField label="The Big Idea" required hint="In one sentence">
              <textarea
                value={formData.creative?.bigIdea || ''}
                onChange={e => updateForm('creative.bigIdea', e.target.value)}
                placeholder="The core creative concept..."
                rows={2}
              />
            </FormField>
            <FormField label="Campaign Tagline">
              <input
                type="text"
                value={formData.creative?.tagline || ''}
                onChange={e => updateForm('creative.tagline', e.target.value)}
                placeholder="If applicable..."
              />
            </FormField>
            <FormField label="What Made It Special" hint="What's genuinely award-worthy about this work?">
              <textarea
                value={formData.creative?.whatMadeItSpecial || ''}
                onChange={e => updateForm('creative.whatMadeItSpecial', e.target.value)}
                placeholder="Why should this win?"
                rows={3}
              />
            </FormField>
            <FormField label="Strategy">
              <textarea
                value={formData.strategy?.strategicApproach || ''}
                onChange={e => updateForm('strategy.strategicApproach', e.target.value)}
                placeholder="What was the strategic approach?"
                rows={2}
              />
            </FormField>
          </FormSection>

          {/* EXECUTIONS */}
          <FormSection
            title="Executions"
            icon={<Palette size={20} />}
            id="executions"
            expanded={expandedSections.includes('executions')}
            onToggle={() => toggleSection('executions')}
          >
            <FormField label="What did you create?">
              <div className="checkbox-grid">
                {executionTypes.map(exec => (
                  <label key={exec.value} className="checkbox-item">
                    <input
                      type="checkbox"
                      checked={formData.executionTypes?.includes(exec.value) || false}
                      onChange={e => {
                        const current = formData.executionTypes || []
                        updateForm(
                          'executionTypes',
                          e.target.checked
                            ? [...current, exec.value]
                            : current.filter(v => v !== exec.value)
                        )
                      }}
                    />
                    <span>{exec.label}</span>
                  </label>
                ))}
              </div>
            </FormField>
            <FormField label="Craft Elements" hint="Notable production details">
              <TagInput
                tags={formData.creative?.craftElements || []}
                onChange={tags => updateForm('creative.craftElements', tags)}
                placeholder="Add craft element..."
              />
            </FormField>
            <FormField label="Innovation Elements" hint="First-ever, new technology, etc.">
              <TagInput
                tags={formData.creative?.innovationElements || []}
                onChange={tags => updateForm('creative.innovationElements', tags)}
                placeholder="Add innovation element..."
              />
            </FormField>
          </FormSection>

          {/* TALENT */}
          <FormSection
            title="Talent & Partnerships"
            icon={<Users size={20} />}
            id="talent"
            expanded={expandedSections.includes('talent')}
            onToggle={() => toggleSection('talent')}
          >
            <FormField label="Athletes">
              <TagInput
                tags={formData.talent?.athletes?.map(a => a.name) || []}
                onChange={tags => updateForm('talent.athletes', tags.map(name => ({ name })))}
                placeholder="Add athlete..."
              />
            </FormField>
            <FormField label="Celebrities">
              <TagInput
                tags={formData.talent?.celebrities?.map(c => c.name) || []}
                onChange={tags => updateForm('talent.celebrities', tags.map(name => ({ name })))}
                placeholder="Add celebrity..."
              />
            </FormField>
            <FormField label="Influencers">
              <TagInput
                tags={formData.talent?.influencers?.map(i => i.name) || []}
                onChange={tags => updateForm('talent.influencers', tags.map(name => ({ name })))}
                placeholder="Add influencer..."
              />
            </FormField>
            <div className="form-grid">
              <FormField label="Director">
                <input
                  type="text"
                  value={formData.talent?.director || ''}
                  onChange={e => updateForm('talent.director', e.target.value)}
                  placeholder="Director name..."
                />
              </FormField>
              <FormField label="Production Company">
                <input
                  type="text"
                  value={formData.talent?.productionCompany || ''}
                  onChange={e => updateForm('talent.productionCompany', e.target.value)}
                  placeholder="Production company..."
                />
              </FormField>
            </div>
          </FormSection>

          {/* RESULTS */}
          <FormSection
            title="Results"
            icon={<BarChart3 size={20} />}
            id="results"
            expanded={expandedSections.includes('results')}
            onToggle={() => toggleSection('results')}
            badge="Critical for Effies"
          >
            <FormField label="Headline Result" hint="One-line summary of the most impressive result">
              <input
                type="text"
                value={formData.results?.summary || ''}
                onChange={e => updateForm('results.summary', e.target.value)}
                placeholder="e.g., '+40% sales lift, highest in category history'"
              />
            </FormField>

            <div className="results-grid">
              <div className="results-section">
                <h4>Business Results</h4>
                <FormField label="Sales Impact">
                  <input
                    type="text"
                    value={formData.results?.business?.sales?.result || ''}
                    onChange={e => updateForm('results.business.sales.result', e.target.value)}
                    placeholder="e.g., +40% lift"
                  />
                </FormField>
                <FormField label="Market Share">
                  <input
                    type="text"
                    value={formData.results?.business?.marketShare?.result || ''}
                    onChange={e => updateForm('results.business.marketShare.result', e.target.value)}
                    placeholder="e.g., +3 pts share"
                  />
                </FormField>
                <FormField label="ROI/ROAS">
                  <input
                    type="text"
                    value={formData.results?.business?.roi || ''}
                    onChange={e => updateForm('results.business.roi', e.target.value)}
                    placeholder="e.g., 5:1 ROAS"
                  />
                </FormField>
              </div>

              <div className="results-section">
                <h4>Brand Metrics</h4>
                <FormField label="Awareness Lift">
                  <input
                    type="text"
                    value={formData.results?.brand?.awareness?.lift || ''}
                    onChange={e => updateForm('results.brand.awareness.lift', e.target.value)}
                    placeholder="e.g., +15 pts"
                  />
                </FormField>
                <FormField label="Consideration Lift">
                  <input
                    type="text"
                    value={formData.results?.brand?.consideration?.lift || ''}
                    onChange={e => updateForm('results.brand.consideration.lift', e.target.value)}
                    placeholder="e.g., +8 pts"
                  />
                </FormField>
                <FormField label="Favorability Lift">
                  <input
                    type="text"
                    value={formData.results?.brand?.favorability?.lift || ''}
                    onChange={e => updateForm('results.brand.favorability.lift', e.target.value)}
                    placeholder="e.g., +12 pts"
                  />
                </FormField>
              </div>

              <div className="results-section">
                <h4>Engagement</h4>
                <FormField label="Impressions">
                  <input
                    type="text"
                    value={formData.results?.engagement?.impressions || ''}
                    onChange={e => updateForm('results.engagement.impressions', e.target.value)}
                    placeholder="e.g., 500M"
                  />
                </FormField>
                <FormField label="Video Views">
                  <input
                    type="text"
                    value={formData.results?.engagement?.videoViews || ''}
                    onChange={e => updateForm('results.engagement.videoViews', e.target.value)}
                    placeholder="e.g., 100M views"
                  />
                </FormField>
                <FormField label="Social Engagement">
                  <input
                    type="text"
                    value={formData.results?.engagement?.socialEngagement || ''}
                    onChange={e => updateForm('results.engagement.socialEngagement', e.target.value)}
                    placeholder="e.g., 2M engagements"
                  />
                </FormField>
                <FormField label="Earned Media Value">
                  <input
                    type="text"
                    value={formData.results?.engagement?.earnedMediaValue || ''}
                    onChange={e => updateForm('results.engagement.earnedMediaValue', e.target.value)}
                    placeholder="e.g., $10M EMV"
                  />
                </FormField>
              </div>
            </div>

            <FormField label="Notable Press Coverage">
              <TagInput
                tags={formData.results?.cultural?.pressCoverage || []}
                onChange={tags => updateForm('results.cultural.pressCoverage', tags)}
                placeholder="Add publication..."
              />
            </FormField>

            <div className="form-row">
              <label className="checkbox-single">
                <input
                  type="checkbox"
                  checked={formData.results?.verified || false}
                  onChange={e => updateForm('results.verified', e.target.checked)}
                />
                <span>Results are verified and client-approved for sharing</span>
              </label>
            </div>

            <FormField label="Results Source">
              <input
                type="text"
                value={formData.results?.source || ''}
                onChange={e => updateForm('results.source', e.target.value)}
                placeholder="e.g., Nielsen, internal data, YouGov"
              />
            </FormField>
          </FormSection>

          {/* SELF ASSESSMENT */}
          <FormSection
            title="Award Potential"
            icon={<BarChart3 size={20} />}
            id="assessment"
            expanded={expandedSections.includes('assessment')}
            onToggle={() => toggleSection('assessment')}
          >
            <p className="section-intro">Be honest - this helps match to the right awards</p>

            <div className="sliders-grid">
              <SliderField
                label="Craft/Production Quality"
                value={formData.awardPotential?.craftStrength || 5}
                onChange={v => updateForm('awardPotential.craftStrength', v)}
              />
              <SliderField
                label="Idea Originality"
                value={formData.awardPotential?.ideaStrength || 5}
                onChange={v => updateForm('awardPotential.ideaStrength', v)}
              />
              <SliderField
                label="Results Impressiveness"
                value={formData.awardPotential?.resultsStrength || 5}
                onChange={v => updateForm('awardPotential.resultsStrength', v)}
              />
              <SliderField
                label="Innovation/Newness"
                value={formData.awardPotential?.innovationStrength || 5}
                onChange={v => updateForm('awardPotential.innovationStrength', v)}
              />
              <SliderField
                label="Cultural Impact"
                value={formData.awardPotential?.culturalImpactStrength || 5}
                onChange={v => updateForm('awardPotential.culturalImpactStrength', v)}
              />
            </div>

            <FormField label="Strongest Angles" hint="What's most award-worthy?">
              <TagInput
                tags={formData.awardPotential?.strongestAngles || []}
                onChange={tags => updateForm('awardPotential.strongestAngles', tags)}
                placeholder="Add strength..."
              />
            </FormField>

            <FormField label="Honest Weaknesses" hint="What will judges question?">
              <TagInput
                tags={formData.awardPotential?.weaknesses || []}
                onChange={tags => updateForm('awardPotential.weaknesses', tags)}
                placeholder="Add weakness..."
              />
            </FormField>
          </FormSection>
        </div>
      )}

      {mode === 'paste' && (
        <div className="paste-section">
          <div className="paste-area">
            <textarea
              value={pastedText}
              onChange={e => setPastedText(e.target.value)}
              placeholder="Paste your creative brief, campaign deck content, or any campaign documentation here. Our AI will extract the relevant information..."
              rows={20}
            />
          </div>
          <button
            className="btn btn-primary"
            disabled={!pastedText}
            onClick={() => {
              // TODO: Parse with AI
              alert('AI parsing coming soon - use the form for now')
            }}
          >
            <Lightbulb size={18} />
            Extract with AI
          </button>
        </div>
      )}

      {mode === 'upload' && (
        <div className="upload-area">
          <div className="upload-dropzone">
            <Upload size={48} className="upload-icon" />
            <h3>Drop your file here</h3>
            <p>or</p>
            <button className="btn btn-primary">
              Browse Files
            </button>
            <p className="upload-formats">
              Supports: PDF, PPTX, DOCX, TXT
            </p>
          </div>
        </div>
      )}

      <div className="step-actions">
        <div className="action-hint">
          {!isFormValid() && (
            <span className="hint-text">
              Fill in Campaign Name, Brand, Challenge, and Big Idea to continue
            </span>
          )}
        </div>
        <button
          className="btn btn-primary btn-large"
          onClick={handleSubmit}
          disabled={!isFormValid()}
        >
          Analyze Campaign
          <ArrowRight size={20} />
        </button>
      </div>
    </div>
  )
}

// Helper Components
function FormSection({
  title,
  icon,
  id,
  expanded,
  onToggle,
  badge,
  children
}: {
  title: string
  icon: React.ReactNode
  id: string
  expanded: boolean
  onToggle: () => void
  badge?: string
  children: React.ReactNode
}) {
  return (
    <div className={`form-section ${expanded ? 'expanded' : ''}`}>
      <button className="section-header" onClick={onToggle}>
        <div className="section-title">
          {icon}
          <span>{title}</span>
          {badge && <span className="section-badge">{badge}</span>}
        </div>
        {expanded ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
      </button>
      {expanded && <div className="section-content">{children}</div>}
    </div>
  )
}

function FormField({
  label,
  required,
  hint,
  children
}: {
  label: string
  required?: boolean
  hint?: string
  children: React.ReactNode
}) {
  return (
    <div className="form-field">
      <label>
        {label}
        {required && <span className="required">*</span>}
        {hint && <span className="hint">{hint}</span>}
      </label>
      {children}
    </div>
  )
}

function TagInput({
  tags,
  onChange,
  placeholder
}: {
  tags: string[]
  onChange: (tags: string[]) => void
  placeholder: string
}) {
  const [input, setInput] = useState('')

  const addTag = () => {
    if (input.trim() && !tags.includes(input.trim())) {
      onChange([...tags, input.trim()])
      setInput('')
    }
  }

  const removeTag = (tag: string) => {
    onChange(tags.filter(t => t !== tag))
  }

  return (
    <div className="tag-input">
      <div className="tags">
        {tags.map(tag => (
          <span key={tag} className="tag">
            {tag}
            <button onClick={() => removeTag(tag)}>
              <X size={14} />
            </button>
          </span>
        ))}
      </div>
      <div className="tag-input-row">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && (e.preventDefault(), addTag())}
          placeholder={placeholder}
        />
        <button className="btn btn-small" onClick={addTag}>
          <Plus size={16} />
        </button>
      </div>
    </div>
  )
}

function SliderField({
  label,
  value,
  onChange
}: {
  label: string
  value: number
  onChange: (value: number) => void
}) {
  const getColor = (v: number) => {
    if (v >= 8) return 'green'
    if (v >= 6) return 'yellow'
    return 'red'
  }

  return (
    <div className="slider-field">
      <div className="slider-header">
        <label>{label}</label>
        <span className={`slider-value ${getColor(value)}`}>{value}/10</span>
      </div>
      <input
        type="range"
        min="1"
        max="10"
        value={value}
        onChange={e => onChange(parseInt(e.target.value))}
        className={`slider ${getColor(value)}`}
      />
    </div>
  )
}
