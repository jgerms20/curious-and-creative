# Quick Start Guide - Curious & Creative Marketing Team

## 30-Second Overview

You have a full marketing team of specialized AI agents. Use **ROUTING-RULES.md** to figure out WHO to talk to, and **AGENT-SKILLS.md** to learn WHAT they can do.

---

## Common Scenarios

### "I need to create content"

1. Check what KIND of content:
   - **Written?** → Copywriter
   - **Visual?** → Art Director
   - **Both?** → Copywriter + Art Director
   - **Need research first?** → Add Data Strategist at the start
   - **Need strategy?** → Add Brand Strategist at the start

2. Use the `content-creation-workflow` from AGENT-SKILLS.md

**Example:**
```
"Research trending topics in AI and create a LinkedIn thought leadership post"

Agents: Data Strategist → Brand Strategist → Copywriter → Art Director
```

---

### "I need to develop a campaign"

1. Always starts with strategy: Brand Strategist + Communication Strategist
2. Then creative: Copywriter + Art Director
3. Then logistics: Production Manager + Account Manager
4. Don't forget: Data Strategist for measurement

Use the `campaign-development-workflow` from AGENT-SKILLS.md

**Example:**
```
"Create a product launch campaign for Gen Z"

Agents: Brand Strategist → Communication Strategist → Copywriter →
        Art Director → Production Manager → Data Strategist → Account Manager
```

---

### "I need to analyze performance"

1. Start with: Data Strategist (crunch the numbers)
2. Add context: Brand Strategist + Communication Strategist
3. Make it pretty: Presentation Builder
4. Present it: Account Manager

Use the `performance-review-workflow` from AGENT-SKILLS.md

**Example:**
```
"Analyze our Q4 holiday campaign and present findings"

Agents: Data Strategist → Brand Strategist → Communication Strategist →
        Presentation Builder → Account Manager
```

---

### "I need to create a pitch or presentation"

1. Strategy first: Brand Strategist + Communication Strategist
2. Add data: Data Strategist (for credibility)
3. Write narrative: Copywriter
4. Design slides: Presentation Builder
5. Coordinate: Account Manager

Use the `pitch-development-workflow` from AGENT-SKILLS.md

**Example:**
```
"Create a new business pitch for [Prospect Company]"

Agents: Brand Strategist → Communication Strategist → Data Strategist →
        Copywriter → Presentation Builder → Account Manager
```

---

### "I need help with production/logistics"

Go straight to: **Production Manager**

They handle:
- Cost estimates
- Vendor recommendations
- Technical specs
- Production timelines
- Print, video, photo production

**Example:**
```
"Get estimates for printing 5,000 brochures"

Agent: Production Manager
```

---

### "I need to submit work to awards"

Start with: **Awards Agent**

They'll coordinate with:
- Data Strategist (for results)
- Copywriter (for narrative)
- Presentation Builder (for materials)
- Account Manager (for approvals)

Use the `awards-submission-workflow` from AGENT-SKILLS.md

**Example:**
```
"Submit our sustainability campaign to Cannes Lions"

Agents: Awards Agent → Data Strategist → Copywriter →
        Presentation Builder → Account Manager
```

---

## Decision Tree (Use This!)

```
START: What do you need?
│
├─ "Strategy or positioning"
│  └─ Brand Strategist or Communication Strategist
│
├─ "Content (written or visual)"
│  └─ Copywriter or Art Director (or both)
│
├─ "Data or performance analysis"
│  └─ Data Strategist
│
├─ "Meeting or project coordination"
│  └─ Account Manager
│
├─ "Production or vendor work"
│  └─ Production Manager
│
├─ "Presentation or pitch"
│  └─ Presentation Builder (+ supporting agents)
│
├─ "Awards or case study"
│  └─ Awards Agent
│
└─ "Full campaign or complex project"
   └─ ALL AGENTS (see multi-agent workflows)
```

---

## Key Skills to Remember

### Individual Agent Skills (Most Useful)

**Communication Strategist:**
- `platform-recommendations` - "What platform should I use?"
- `media-strategy` - "How should I allocate budget?"
- `trend-analysis` - "What's working right now?"

**Brand Strategist:**
- `brand-positioning` - "How should we position ourselves?"
- `messaging-framework` - "What should we say?"
- `brand-voice` - "How should we sound?"

**Data Strategist:**
- `performance-analysis` - "How did we do?"
- `audience-segmentation` - "Who should we target?"
- `test-design` - "What should we test?"

**Copywriter:**
- `campaign-concepts` - "Generate creative ideas"
- `social-content` - "Write social posts"
- `email-sequence` - "Create email series"

**Art Director:**
- `visual-concepts` - "Develop visual direction"
- `mood-board` - "Show me the vibe"
- `design-system` - "Create visual guidelines"

**Presentation Builder:**
- `pitch-deck` - "Build a pitch"
- `results-presentation` - "Present performance"
- `data-visualization` - "Make this data visual"

**Awards Agent:**
- `case-study` - "Document this campaign"
- `awards-strategy` - "Where should we submit?"
- `entry-writing` - "Write award entry"

---

## Pro Tips

1. **Most requests need 2-4 agents, not just one**
   - Rarely is it a single-agent task
   - Think about the full workflow

2. **Always start with strategy for new work**
   - Brand Strategist (what to say)
   - Communication Strategist (where to say it)
   - Then move to creative execution

3. **Loop in Account Manager for client work**
   - They coordinate approvals
   - They manage timelines
   - They handle communication

4. **Measure from the beginning**
   - Engage Data Strategist early
   - Define KPIs before launching
   - Plan measurement framework upfront

5. **Document as you go**
   - Awards Agent captures work in real-time
   - Easier than reconstructing later
   - Case studies become simple

---

## Examples by Request Type

### "Write me social posts about [topic]"
**Agents:** Brand Strategist → Copywriter
**Why:** Need brand voice, then write content

### "What's trending on TikTok?"
**Agent:** Communication Strategist
**Why:** They track platform trends

### "How did our campaign perform?"
**Agents:** Data Strategist → Presentation Builder
**Why:** Analyze data, then visualize findings

### "Create a landing page"
**Agents:** Brand Strategist → Copywriter → Art Director
**Why:** Messaging, then copy, then design

### "Plan a product launch"
**Agents:** ALL (use campaign-development-workflow)
**Why:** Complex multi-phase project

### "Get a print quote"
**Agent:** Production Manager
**Why:** They handle all production logistics

### "Schedule a client meeting"
**Agent:** Account Manager
**Why:** They coordinate all meetings

### "Make a pitch deck"
**Agents:** Brand Strategist → Copywriter → Presentation Builder
**Why:** Strategy, narrative, then design

---

## When in Doubt...

1. Start with **ROUTING-RULES.md** - tells you WHO
2. Then check **AGENT-SKILLS.md** - tells you WHAT they can do
3. Look at the **multi-agent workflows** - they cover most scenarios

Still stuck? Default to **Account Manager** - they'll help coordinate!

---

## File Reference

| File | Purpose | When to Use |
|------|---------|-------------|
| **README.md** | Overview and navigation | Starting point |
| **ROUTING-RULES.md** | Agent selection logic | Figuring out WHO to engage |
| **AGENT-SKILLS.md** | Specific capabilities | Learning WHAT agents do |
| **QUICK-START-GUIDE.md** | This file! | Quick answers |
| **Agent files** (in folders) | Deep dive on each agent | Detailed agent info |

---

*Your marketing team is ready. Let's build something great!*
