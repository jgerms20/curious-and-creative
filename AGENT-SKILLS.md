# Agent Skills Framework

## Overview
This document defines specific "skills" for each marketing agent - reusable capabilities that can be invoked for common tasks. Skills are designed to work independently or as part of multi-agent workflows.

---

## 📊 Strategy Department Skills

### Communication Strategist Skills

#### `platform-recommendations`
**Purpose:** Recommend optimal platforms for a campaign or content
**Inputs:** Target audience, content type, campaign objectives, budget
**Outputs:** Platform recommendations with rationale, specs, and best practices

**Usage:**
```
@communication-strategist use skill:platform-recommendations
- Audience: Gen Z, 18-24
- Content: Product launch video
- Objective: Awareness and engagement
- Budget: $50K
```

---

#### `media-strategy`
**Purpose:** Develop comprehensive media strategy and channel mix
**Inputs:** Campaign brief, audience, objectives, budget, timeline
**Outputs:** Media plan with channel allocation, timing, budget breakdown

**Usage:**
```
@communication-strategist use skill:media-strategy
- Campaign: New product launch
- Audience: Millennials, urban, tech-savvy
- Objective: Drive 10K pre-orders
- Budget: $200K
- Timeline: 8 weeks
```

---

#### `trend-analysis`
**Purpose:** Analyze current trends on specific platforms or channels
**Inputs:** Platform(s), industry/category, time period
**Outputs:** Trend report with content formats, themes, and opportunities

**Usage:**
```
@communication-strategist use skill:trend-analysis
- Platforms: TikTok, Instagram Reels
- Category: Fitness and wellness
- Period: Last 30 days
```

---

#### `channel-specs`
**Purpose:** Provide technical specifications for platform/channel content
**Inputs:** Platform(s), content format
**Outputs:** Detailed specs (dimensions, file sizes, best practices)

**Usage:**
```
@communication-strategist use skill:channel-specs
- Platform: LinkedIn, Instagram, TikTok
- Format: Video ad
```

---

### Brand Strategist Skills

#### `brand-positioning`
**Purpose:** Develop brand positioning strategy and statement
**Inputs:** Company/product info, competitive landscape, target audience
**Outputs:** Positioning statement, differentiation strategy, competitive matrix

**Usage:**
```
@brand-strategist use skill:brand-positioning
- Company: Sustainable fashion startup
- Competitors: Patagonia, Everlane, Reformation
- Target: Conscious millennials
```

---

#### `messaging-framework`
**Purpose:** Create comprehensive messaging architecture
**Inputs:** Brand positioning, audience personas, objectives
**Outputs:** Messaging house with hierarchy, pillars, proof points

**Usage:**
```
@brand-strategist use skill:messaging-framework
- Brand: B2B SaaS platform
- Positioning: AI-powered marketing automation
- Audiences: CMOs, Marketing Directors, Marketing Ops
```

---

#### `brand-voice`
**Purpose:** Define brand voice and tone guidelines
**Inputs:** Brand personality, values, audience, competitive context
**Outputs:** Voice definition, tone spectrum, writing examples

**Usage:**
```
@brand-strategist use skill:brand-voice
- Personality: Bold, innovative, approachable
- Values: Transparency, sustainability, inclusivity
- Audience: Gen Z consumers
```

---

#### `brand-audit`
**Purpose:** Audit content or campaign for brand consistency
**Inputs:** Content/campaign materials to review, brand guidelines
**Outputs:** Consistency report with recommendations

**Usage:**
```
@brand-strategist use skill:brand-audit
- Materials: [Campaign creative, copy deck, social content]
- Focus: Voice, messaging, visual alignment
```

---

### Data Strategist Skills

#### `performance-analysis`
**Purpose:** Analyze marketing performance and identify opportunities
**Inputs:** Campaign/channel data, time period, KPIs
**Outputs:** Performance report with insights and recommendations

**Usage:**
```
@data-strategist use skill:performance-analysis
- Campaign: Q4 Holiday Campaign
- Period: Oct 1 - Dec 31
- Channels: Paid social, email, search
- KPIs: ROAS, conversion rate, CAC
```

---

#### `measurement-framework`
**Purpose:** Design measurement strategy and KPI framework
**Inputs:** Campaign objectives, available data sources, success criteria
**Outputs:** KPI framework, measurement plan, dashboard requirements

**Usage:**
```
@data-strategist use skill:measurement-framework
- Campaign: Brand awareness initiative
- Objective: Increase unaided awareness 15%
- Channels: TV, OOH, social, digital
- Duration: 12 weeks
```

---

#### `audience-segmentation`
**Purpose:** Analyze and segment audiences for targeting
**Inputs:** Customer data, behavioral data, campaign objectives
**Outputs:** Segment definitions, size, characteristics, recommendations

**Usage:**
```
@data-strategist use skill:audience-segmentation
- Data source: CRM, website analytics, purchase history
- Objective: Identify high-value segments for retention
```

---

#### `test-design`
**Purpose:** Design A/B or multivariate test strategy
**Inputs:** Hypothesis, variables to test, success metrics, sample size
**Outputs:** Test plan, methodology, duration, success criteria

**Usage:**
```
@data-strategist use skill:test-design
- Hypothesis: CTA button color affects click-through rate
- Variables: Blue vs. Green vs. Orange
- Metric: CTR
- Traffic: 50K visitors/week
```

---

#### `attribution-model`
**Purpose:** Build attribution model for multi-channel campaigns
**Inputs:** Channel data, conversion paths, business objectives
**Outputs:** Attribution model recommendation, implementation plan

**Usage:**
```
@data-strategist use skill:attribution-model
- Channels: Paid search, paid social, display, email, organic
- Conversion path: Typically 3-5 touchpoints
- Goal: Optimize budget allocation
```

---

## 🎨 Creative Department Skills

### Copywriter Skills

#### `campaign-concepts`
**Purpose:** Develop creative campaign concepts with headlines and copy
**Inputs:** Brief, brand positioning, audience, objectives
**Outputs:** 3-5 campaign concepts with headlines, taglines, supporting copy

**Usage:**
```
@copywriter use skill:campaign-concepts
- Brief: Sustainable sneaker launch
- Positioning: Performance meets planet
- Audience: Active, eco-conscious Gen Z/Millennials
- Tone: Bold, authentic, optimistic
```

---

#### `social-content`
**Purpose:** Create social media copy for multiple platforms
**Inputs:** Campaign/topic, platforms, quantity, brand voice
**Outputs:** Platform-optimized posts with copy and hashtag recommendations

**Usage:**
```
@copywriter use skill:social-content
- Topic: New product announcement
- Platforms: Instagram, LinkedIn, Twitter
- Quantity: 5 posts per platform
- Voice: Professional yet approachable
```

---

#### `email-sequence`
**Purpose:** Write email marketing sequence or campaign
**Inputs:** Campaign objective, audience, sequence type, brand voice
**Outputs:** Email series with subject lines, body copy, CTAs

**Usage:**
```
@copywriter use skill:email-sequence
- Type: Welcome series for new subscribers
- Length: 5 emails over 2 weeks
- Objective: Drive first purchase
- Offers: 10% discount, free shipping
```

---

#### `landing-page-copy`
**Purpose:** Write conversion-focused landing page copy
**Inputs:** Offer/product, audience, conversion goal, key benefits
**Outputs:** Landing page structure with headlines, body copy, CTAs

**Usage:**
```
@copywriter use skill:landing-page-copy
- Offer: Free trial of SaaS platform
- Audience: Marketing managers at SMBs
- Benefits: Save 10 hours/week, increase ROI 30%
- Goal: Trial sign-ups
```

---

#### `script-writing`
**Purpose:** Write video or audio scripts
**Inputs:** Format (video/radio/podcast), duration, message, tone
**Outputs:** Script with timing, voiceover, and scene descriptions

**Usage:**
```
@copywriter use skill:script-writing
- Format: Social video (Instagram Reels, TikTok)
- Duration: 30 seconds
- Message: Product demo with testimonial
- Tone: Energetic, authentic
```

---

### Art Director Skills

#### `visual-concepts`
**Purpose:** Develop visual concepts for campaigns or content
**Inputs:** Brief, brand guidelines, audience, message
**Outputs:** 2-3 visual concepts with mood boards and rationale

**Usage:**
```
@art-director use skill:visual-concepts
- Campaign: Premium skincare launch
- Audience: Affluent women 35-50
- Message: Science-backed luxury
- Brand: Minimalist, sophisticated
```

---

#### `mood-board`
**Purpose:** Create mood board for visual direction
**Inputs:** Project description, desired mood/feeling, references
**Outputs:** Curated mood board with images, colors, typography, references

**Usage:**
```
@art-director use skill:mood-board
- Project: Tech startup rebrand
- Mood: Innovative, trustworthy, human-centered
- Industry: Fintech
```

---

#### `design-system`
**Purpose:** Develop design system or visual guidelines
**Inputs:** Brand identity, use cases, platforms/applications
**Outputs:** Design system with typography, colors, layouts, components

**Usage:**
```
@art-director use skill:design-system
- Brand: [Brand name]
- Applications: Website, social media, email, presentations
- Style: Modern, clean, accessible
```

---

#### `photoshoot-concept`
**Purpose:** Art direct photoshoot concept and shot list
**Inputs:** Campaign brief, desired mood, assets needed
**Outputs:** Shoot concept, shot list, styling direction, location ideas

**Usage:**
```
@art-director use skill:photoshoot-concept
- Campaign: Summer collection launch
- Mood: Bright, energetic, outdoorsy
- Assets needed: Hero images, lifestyle shots, product details
- Budget: Mid-range
```

---

## 📋 Administration Department Skills

### Account Manager Skills

#### `meeting-coordination`
**Purpose:** Schedule and organize meetings with agendas
**Inputs:** Meeting type, stakeholders, objectives, materials needed
**Outputs:** Meeting invite, agenda, prep materials list

**Usage:**
```
@account-manager use skill:meeting-coordination
- Type: Creative presentation
- Stakeholders: Client CMO, Marketing Director, our team
- Objective: Present Q1 campaign concepts for approval
- Duration: 60 minutes
```

---

#### `project-timeline`
**Purpose:** Create project timeline and milestone plan
**Inputs:** Project scope, deliverables, deadline, dependencies
**Outputs:** Gantt chart or timeline with milestones and owners

**Usage:**
```
@account-manager use skill:project-timeline
- Project: Website redesign
- Key deliverables: Strategy, design, development, launch
- Deadline: 12 weeks from kickoff
- Team: 6 people across departments
```

---

#### `status-report`
**Purpose:** Generate project or account status report
**Inputs:** Project/account name, reporting period, progress, issues
**Outputs:** Status report with progress, risks, next steps

**Usage:**
```
@account-manager use skill:status-report
- Account: [Client name]
- Period: January 2026
- Projects: 3 active campaigns
- Format: Executive summary + detailed update
```

---

#### `client-communication`
**Purpose:** Draft client-facing communication
**Inputs:** Communication type, context, key messages, tone
**Outputs:** Draft email or message

**Usage:**
```
@account-manager use skill:client-communication
- Type: Timeline delay notification
- Context: Production issue causing 1-week delay
- Tone: Professional, transparent, solutions-focused
```

---

## 🎬 Production Department Skills

### Production Manager Skills

#### `cost-estimate`
**Purpose:** Generate production cost estimate
**Inputs:** Project specs, deliverables, quality tier, timeline
**Outputs:** Itemized estimate with ranges and recommendations

**Usage:**
```
@production-manager use skill:cost-estimate
- Project: 30-second commercial production
- Deliverables: Filmed content + editing + color + sound
- Quality: High-end
- Timeline: 4 weeks
```

---

#### `vendor-recommendations`
**Purpose:** Recommend vendors for production needs
**Inputs:** Production type, location, budget range, requirements
**Outputs:** 3-5 vendor recommendations with pros/cons/pricing

**Usage:**
```
@production-manager use skill:vendor-recommendations
- Type: Print production for 10,000 brochures
- Specs: 8.5x11, full color, matte finish
- Location: West Coast (shipping to SF)
- Budget: $3-5K
```

---

#### `production-timeline`
**Purpose:** Create detailed production schedule
**Inputs:** Project scope, milestones, dependencies, deadline
**Outputs:** Production timeline with tasks, owners, dates

**Usage:**
```
@production-manager use skill:production-timeline
- Project: Product packaging design and production
- Phases: Design, prototyping, approval, printing, delivery
- Deadline: Product launch in 8 weeks
```

---

#### `technical-specs`
**Purpose:** Define technical specifications for deliverables
**Inputs:** Deliverable type, intended use, platform/medium
**Outputs:** Complete technical specifications document

**Usage:**
```
@production-manager use skill:technical-specs
- Deliverable: Social media video ads
- Platforms: Instagram Stories, Facebook Feed, YouTube
- Specifications needed: Resolution, format, file size, duration
```

---

## ⭐ Specialized Agent Skills

### Presentation Builder Skills

#### `pitch-deck`
**Purpose:** Create comprehensive pitch deck
**Inputs:** Purpose, audience, key messages, data/assets
**Outputs:** Structured pitch deck with narrative and slides

**Usage:**
```
@presentation-builder use skill:pitch-deck
- Purpose: New business pitch
- Prospect: [Company name] - B2B SaaS
- Objective: Win $500K annual retainer
- Focus: Our strategy expertise + case studies
```

---

#### `results-presentation`
**Purpose:** Build campaign results or performance presentation
**Inputs:** Campaign data, metrics, insights, audience
**Outputs:** Visual presentation with data storytelling

**Usage:**
```
@presentation-builder use skill:results-presentation
- Campaign: Q4 Holiday Campaign
- Metrics: Sales, traffic, engagement, ROI
- Audience: Client executive team
- Format: Quarterly business review
```

---

#### `data-visualization`
**Purpose:** Transform data into compelling visual slides
**Inputs:** Raw data, key insights, story angle
**Outputs:** Visualized data with charts, graphs, infographics

**Usage:**
```
@presentation-builder use skill:data-visualization
- Data: Customer survey results (500 responses)
- Insights: 3 key findings about brand perception
- Style: Clean, modern, brand-aligned
```

---

#### `presentation-template`
**Purpose:** Create reusable presentation template system
**Inputs:** Brand guidelines, use cases, slide types needed
**Outputs:** Master template with layouts and style guide

**Usage:**
```
@presentation-builder use skill:presentation-template
- Use cases: Client presentations, internal updates, sales decks
- Brand: [Company name]
- Platform: Google Slides
```

---

### Awards Agent Skills

#### `case-study`
**Purpose:** Write comprehensive campaign case study
**Inputs:** Campaign details, challenge, strategy, results, assets
**Outputs:** Structured case study with narrative and supporting materials

**Usage:**
```
@awards-agent use skill:case-study
- Campaign: [Campaign name]
- Challenge: Low brand awareness in new market
- Strategy: Influencer + experiential approach
- Results: 200% awareness lift, 50K earned media impressions
```

---

#### `awards-strategy`
**Purpose:** Develop awards submission strategy
**Inputs:** Campaign/work, budget, objectives, timeline
**Outputs:** Prioritized awards list with categories and deadlines

**Usage:**
```
@awards-agent use skill:awards-strategy
- Work: Integrated cause marketing campaign
- Budget: $5K for entry fees
- Objective: Industry recognition + PR
- Timeline: Next 6 months
```

---

#### `entry-writing`
**Purpose:** Write awards entry for specific show/category
**Inputs:** Award show, category, work, judging criteria, word limit
**Outputs:** Complete entry with all required components

**Usage:**
```
@awards-agent use skill:entry-writing
- Award: Cannes Lions
- Category: Creative Effectiveness
- Campaign: [Campaign name]
- Word limit: 500 words
- Supporting: Video case study, creative samples
```

---

#### `awards-calendar`
**Purpose:** Create comprehensive awards calendar
**Inputs:** Year, priority shows, budget
**Outputs:** Calendar with deadlines, fees, category recommendations

**Usage:**
```
@awards-agent use skill:awards-calendar
- Year: 2026
- Priority: Cannes, Effies, One Show, Webbys, Clios
- Budget: $15K annual
```

---

### Research Analyst Skills

#### `brand-discovery`
**Purpose:** Comprehensive research and audit of a brand's digital presence, positioning, and competitive landscape
**Inputs:** Company website/URL, industry context, specific focus areas (optional)
**Outputs:** Brand Discovery Brief with website analysis, positioning assessment, founder backgrounds, and key insights

**Usage:**
```
@research-analyst use skill:brand-discovery
- URL: https://example.com
- Industry: SaaS / AI / Consumer goods / etc.
- Focus: Overall brand positioning and messaging
```

---

#### `social-audit`
**Purpose:** Analyze a brand's social media presence across all major platforms
**Inputs:** Brand name, social handles (if known), platforms to analyze
**Outputs:** Social Media Audit Report with follower data, content strategy analysis, engagement patterns, and recommendations

**Usage:**
```
@research-analyst use skill:social-audit
- Brand: [Company name]
- Platforms: Instagram, LinkedIn, Twitter/X, TikTok, Facebook, YouTube
- Handles: @example (if known)
```

---

#### `competitive-landscape`
**Purpose:** Map competitors and analyze positioning differences
**Inputs:** Company/brand, known competitors (optional), industry
**Outputs:** Competitive Landscape Map with positioning matrix, differentiation opportunities, and share of voice analysis

**Usage:**
```
@research-analyst use skill:competitive-landscape
- Brand: [Company name]
- Industry: [Industry]
- Known competitors: [List if available]
```

---

#### `founder-research`
**Purpose:** Research founder/leadership backgrounds and stories
**Inputs:** Company name, founder names (if known)
**Outputs:** Founder Profile Summary with career history, achievements, philosophy, and potential story angles

**Usage:**
```
@research-analyst use skill:founder-research
- Company: [Company name]
- Founders: [Names if known]
```

---

#### `intelligence-brief`
**Purpose:** Create comprehensive pre-pitch or new client intelligence package
**Inputs:** Company URL, pitch/meeting context, specific questions to answer
**Outputs:** Full Intelligence Brief combining brand discovery, social audit, competitive analysis, and opportunity identification

**Usage:**
```
@research-analyst use skill:intelligence-brief
- URL: https://example.com
- Context: New business pitch / Onboarding new client
- Key questions: What makes them unique? Who are they competing with?
```

---

## 🔗 Multi-Agent Skill Orchestrations

### `content-creation-workflow`
**Purpose:** End-to-end content creation from research to publication
**Agents:** Data Strategist → Brand Strategist → Copywriter → Art Director → Communication Strategist
**Inputs:** Topic, format, target audience, distribution channels
**Outputs:** Complete content package ready for distribution

**Usage:**
```
@orchestrate skill:content-creation-workflow
- Topic: The future of AI in marketing
- Format: Long-form blog post (1500 words) + social snippets
- Audience: Marketing professionals
- Distribution: Blog, LinkedIn, email newsletter
```

---

### `campaign-development-workflow`
**Purpose:** Full campaign development from strategy through execution planning
**Agents:** Brand Strategist → Communication Strategist → Copywriter → Art Director → Production Manager → Account Manager → Data Strategist
**Inputs:** Campaign brief, objectives, budget, timeline
**Outputs:** Complete campaign plan ready for execution

**Usage:**
```
@orchestrate skill:campaign-development-workflow
- Objective: Launch new product line
- Audience: Women 25-40, urban, health-conscious
- Budget: $250K
- Timeline: 12 weeks
- Channels: Social, influencer, experiential, PR
```

---

### `performance-review-workflow`
**Purpose:** Comprehensive campaign analysis and client presentation
**Agents:** Data Strategist → Brand Strategist → Communication Strategist → Presentation Builder → Account Manager
**Inputs:** Campaign data, time period, stakeholder audience
**Outputs:** Insights report + presentation + recommendations

**Usage:**
```
@orchestrate skill:performance-review-workflow
- Campaign: Spring 2026 Product Launch
- Period: March 1 - May 31
- Audience: Client CMO + executive team
- Format: Quarterly business review
```

---

### `pitch-development-workflow`
**Purpose:** New business pitch development
**Agents:** Brand Strategist → Communication Strategist → Data Strategist → Copywriter → Presentation Builder → Account Manager
**Inputs:** Prospect info, RFP/brief, pitch date
**Outputs:** Complete pitch deck + supporting materials + presentation plan

**Usage:**
```
@orchestrate skill:pitch-development-workflow
- Prospect: [Company name] - D2C beauty brand
- Challenge: Enter Gen Z market
- Budget: $750K annual
- Pitch date: 3 weeks
```

---

### `awards-submission-workflow`
**Purpose:** Complete awards submission from strategy to entry
**Agents:** Awards Agent → Data Strategist → Copywriter → Presentation Builder → Account Manager
**Inputs:** Campaign to submit, target awards, deadline
**Outputs:** Complete award entries with all materials

**Usage:**
```
@orchestrate skill:awards-submission-workflow
- Campaign: [Campaign name]
- Awards: Cannes Lions (3 categories), Effies (2 categories)
- Deadline: 4 weeks
- Budget: $7K
```

---

### `brand-audit-workflow`
**Purpose:** Comprehensive brand and digital presence audit for new clients or prospects
**Agents:** Research Analyst → Brand Strategist → Communication Strategist → Data Strategist → Presentation Builder
**Inputs:** Company URL, industry context, audit scope
**Outputs:** Complete Brand Audit Package with discovery brief, positioning analysis, social audit, competitive landscape, and recommendations presentation

**Usage:**
```
@orchestrate skill:brand-audit-workflow
- URL: https://example.com
- Industry: [Industry]
- Scope: Full audit / Social only / Competitive focus
- Purpose: New client onboarding / Pitch preparation / Quarterly review
```

**Workflow Stages:**
1. **Research Analyst** → Brand discovery, social audit, founder research, competitive mapping
2. **Brand Strategist** → Positioning analysis, messaging assessment, brand health evaluation
3. **Communication Strategist** → Channel strategy review, platform optimization recommendations
4. **Data Strategist** → Performance benchmarking, audience insights, measurement gaps
5. **Presentation Builder** → Compile findings into client-ready audit presentation

---

## 📝 How to Use Skills

### Invoking Individual Skills
```
@[agent-name] use skill:[skill-name]
[Input parameters]
```

### Invoking Multi-Agent Workflows
```
@orchestrate skill:[workflow-name]
[Input parameters]
```

### Chaining Skills
```
First: @brand-strategist use skill:messaging-framework
Then: @copywriter use skill:campaign-concepts (using messaging framework output)
Then: @art-director use skill:visual-concepts (using campaign concepts)
```

---

### `newsletter-fetch-and-curate`
**Purpose:** Automated weekly AI news gathering, curation, and newsletter production
**Agents:** Research Analyst → Copywriter
**Inputs:** Client name, week date, focus topics (optional)
**Outputs:**
- Updated content-log.json with sources and dates
- Newsletter in Markdown + HTML formats
- All sources tracked with timestamps

**Usage:**
```
@orchestrate skill:newsletter-fetch-and-curate
- Client: U&AI
- Week: February 8, 2026
- Focus: General AI updates (or specific topic like "agents", "enterprise AI")
```

**Workflow Steps:**
1. **Research Analyst** → Check `/Workflows/Newsletter/sources.json` for registered sources
2. **Research Analyst** → Web search each source + supplementary queries from sources.json
3. **Research Analyst** → Log all content with dates to `/Workflows/Newsletter/content-log.json`
4. **Copywriter** → Consolidate themes and prioritize by client audience relevance
5. **Copywriter** → Load client brand voice from `/Outputs/Clients/[Client]/Brand/brand-voice.md`
6. **Copywriter** → Generate newsletter with sections: Headlines, Deep Dive, Quick Hits, Looking Ahead
7. **Copywriter** → Save to `/Outputs/Clients/[Client]/Newsletters/[Year]/[Month]/`

**Schedule:** Saturday fetch → Monday send ready

**Configuration Files:**
- `/Workflows/Newsletter/sources.json` — Registered podcast/newsletter sources
- `/Workflows/Newsletter/content-log.json` — Track what's been pulled and when
- `/Workflows/Newsletter/templates/` — Newsletter templates (Markdown + HTML)
- `/Outputs/Clients/[ClientName]/Brand/brand-voice.md` — Client voice guidelines

**Output Location:**
`/Outputs/Clients/[ClientName]/Newsletters/[Year]/[Month]/[Date]-weekly-digest.md` and `.html`

---

### `strategic-brand-audit`
**Purpose:** Comprehensive brand positioning, messaging, and digital presence audit
**Agents:** Research Analyst → Brand Strategist → Communication Strategist
**Inputs:** Company URL, industry, audit scope (full/social-only/competitive-focus)
**Outputs:** Professional HTML report with:
- Executive summary & assessment scores (Positioning, Social Proof, Content Presence, Founder Credibility)
- Positioning analysis with common themes
- Inconsistencies and gaps identified
- Social media deep dive (post counts, themes, engagement patterns)
- Strategic opportunities
- Recommended actions (Quick Win / Recommended / Comprehensive options)

**Usage:**
```
@orchestrate skill:strategic-brand-audit
- URL: https://uandai.co
- Industry: AI visibility / GEO services
- Scope: Full audit
- Purpose: New client onboarding
```

**Workflow Steps:**
1. **Research Analyst** → Website analysis, founder research, social audit
2. **Brand Strategist** → Positioning analysis, messaging assessment, identify inconsistencies
3. **Communication Strategist** → Channel strategy review, platform recommendations
4. **Output** → Generate clean HTML report using Georgia font, professional layout

**Output Format:** HTML report styled like a professional consulting document
**Output Location:** `/Outputs/Clients/[Client]/Reports/[Client]-Strategic-Audit.html`

---

### `competitive-landscape`
**Purpose:** Map competitors, analyze positioning, identify differentiation opportunities
**Agents:** Research Analyst → Brand Strategist
**Inputs:** Company name, industry, known competitors (optional)
**Outputs:** Professional HTML report with:
- Executive summary and market maturity signals
- Market overview (terminology, key metrics industry tracks)
- Competitor profiles (detailed cards with strengths/weaknesses)
- Adjacent competitors / threats
- Positioning matrix visualization
- Differentiation opportunities with messaging suggestions
- Risks & recommended actions

**Usage:**
```
@orchestrate skill:competitive-landscape
- Company: U&AI
- Industry: AI visibility / GEO / AEO
- Known competitors: Profound, WebFX, First Page Sage (optional)
```

**Workflow Steps:**
1. **Research Analyst** → Web search for competitors, aggregate pricing/positioning data
2. **Research Analyst** → Profile each competitor (type, pricing, strengths, weaknesses)
3. **Brand Strategist** → Analyze positioning gaps, identify white space
4. **Brand Strategist** → Create positioning matrix and differentiation recommendations
5. **Output** → Generate clean HTML report with competitor cards and visual matrix

**Output Format:** HTML report with professional styling, competitor comparison tables
**Output Location:** `/Outputs/Clients/[Client]/Reports/competitive-landscape.html`

---

### `transcript-to-meeting-notes`
**Purpose:** Parse meeting transcripts and extract actionable summaries
**Agents:** Research Analyst
**Inputs:** Raw transcript text, meeting type (weekly-sync, kickoff, strategy, etc.)
**Outputs:** Structured meeting summary with:
- Date, attendees, meeting type
- Key discussion points
- Decisions made
- Action items with owners
- Next steps

**Usage:**
```
@research-analyst use skill:transcript-to-meeting-notes
- Transcript: [paste raw transcript]
- Type: weekly-sync
- Client: U&AI
```

**Auto-Integration:** When transcript is dropped, automatically:
1. Parse and extract key information
2. Add to `/Outputs/Clients/[Client]/Tracker/meeting-notes.json`
3. Update tracker display with new meeting entry

---

## Copywriter Skills (Newsletter)

#### `newsletter-content`
**Purpose:** Write newsletter content with brand voice application
**Inputs:** Research/source material, client brand voice, newsletter type
**Outputs:** Complete newsletter copy with headlines, summaries, implications, and outlook

**Usage:**
```
@copywriter use skill:newsletter-content
- Client: U&AI
- Source material: [Research output]
- Type: Weekly AI digest
- Sections: Headlines, Deep dive, Quick hits, Outlook
```

---

*Last Updated: February 3, 2026*
