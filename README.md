# Marketing Team - Claude Agency

A comprehensive marketing team structure with specialized AI agents organized by department. This system enables sophisticated multi-agent orchestration for complex marketing workflows.

## Team Structure

### 📊 Strategy Department
- **Communication Strategist** - Platform specialist understanding specs, trends, and channel strategies (OOH, digital, social, TV, radio, audio, email)
- **Brand Strategist** - Brand positioning expert, messaging, and what the brand stands for
- **Data Strategist** - Data analysis and insights specialist

### 🎨 Creative Department
- **Copywriter** - Creative writing for all marketing materials
- **Art Director** - Visual design and creative direction

### 📋 Administration Department
- **Account Manager** - Meeting coordination, client relations, billing, and administrative operations

### 🎬 Production Department
- **Production Manager** - Logistics coordination, cost management, and production oversight

### ⭐ Specialized Agents
- **Presentation Builder** - Creates compelling presentations and decks
- **Awards Agent** - Handles award submissions, case study drafting, and recognition programs

---

## 🎯 How to Use This System

### Quick Start
1. **Single-Agent Tasks**: Consult [ROUTING-RULES.md](ROUTING-RULES.md) to identify which agent to engage
2. **Multi-Agent Workflows**: Use pre-built orchestrations in [AGENT-SKILLS.md](AGENT-SKILLS.md)
3. **Agent Details**: Review individual agent files in department folders for specific capabilities

### Key Documents

#### [ROUTING-RULES.md](ROUTING-RULES.md) - Agent Delegation Guide
Comprehensive routing rules that define:
- When to delegate to each agent (trigger keywords, request types)
- Single-agent vs. multi-agent decision logic
- Handoff protocols between agents
- Special routing scenarios (urgent, budget-sensitive, client-facing)
- Decision tree for complex requests

**Use this when:** You need to determine which agent(s) should handle a request

#### [AGENT-SKILLS.md](AGENT-SKILLS.md) - Reusable Capabilities
Specific skills for each agent including:
- Individual agent skills (40+ pre-defined capabilities)
- Multi-agent workflow orchestrations
- Usage syntax and examples
- Input/output specifications

**Use this when:** You want to invoke specific capabilities or chain multiple agents together

---

## 🔄 Common Workflows

### Content Creation
**Agents:** Data Strategist → Brand Strategist → Copywriter → Art Director → Communication Strategist

**Example:** "Research AI trends and create a blog post with supporting graphics"

### Campaign Development
**Agents:** Brand Strategist → Communication Strategist → Copywriter → Art Director → Production Manager → Data Strategist

**Example:** "Develop an integrated campaign to launch our new product line"

### Performance Analysis & Reporting
**Agents:** Data Strategist → Communication Strategist → Brand Strategist → Presentation Builder → Account Manager

**Example:** "Analyze Q4 campaign performance and create executive presentation"

### Pitch/Proposal Creation
**Agents:** Brand Strategist → Communication Strategist → Data Strategist → Copywriter → Presentation Builder

**Example:** "Create a new business pitch for [prospect company]"

### Awards Submission
**Agents:** Data Strategist → Awards Agent → Copywriter → Presentation Builder → Account Manager

**Example:** "Submit our sustainability campaign to Cannes Lions"

---

## 📁 Directory Structure

```
Claude Agency/
├── README.md (this file)
├── ROUTING-RULES.md (agent delegation guide)
├── AGENT-SKILLS.md (reusable capabilities)
├── Strategy/
│   ├── communication-strategist.md
│   ├── brand-strategist.md
│   └── data-strategist.md
├── Creative/
│   ├── copywriter.md
│   └── art-director.md
├── Administration/
│   └── account-manager.md
├── Production/
│   └── production-manager.md
└── Specialized/
    ├── presentation-builder.md
    └── awards-agent.md
```

---

## 💡 Best Practices

1. **Start with Routing Rules**: Always consult ROUTING-RULES.md first to identify the right agent(s)
2. **Use Skills for Common Tasks**: Leverage pre-built skills in AGENT-SKILLS.md for efficiency
3. **Consider Handoffs**: Most requests need 2-3 agents working in sequence
4. **Include Account Manager**: For client-facing work, always loop in Account Manager
5. **Measure Everything**: Engage Data Strategist early to define success metrics
6. **Brand Alignment First**: For new initiatives, start with Brand Strategist
7. **Document as You Go**: Use Awards Agent to capture campaign stories in real-time

---

## 🚀 Quick Reference

| Need | Primary Agent | Supporting Agents |
|------|---------------|-------------------|
| Platform strategy | Communication Strategist | Data Strategist |
| Brand positioning | Brand Strategist | Communication Strategist |
| Performance analysis | Data Strategist | - |
| Written content | Copywriter | Brand Strategist |
| Visual content | Art Director | Brand Strategist |
| Client meetings | Account Manager | Relevant specialists |
| Production quotes | Production Manager | Art Director |
| Presentations | Presentation Builder | Data Strategist |
| Case studies | Awards Agent | Data Strategist, Copywriter |
| Full campaigns | All agents | Account Manager (coordinator) |

---

## 📞 Getting Help

Each agent file contains:
- Detailed role overview and expertise
- Specific use cases and trigger scenarios
- Example prompts for common requests
- Skills and capabilities breakdown

For complex requests involving multiple agents, refer to the Multi-Agent Workflow section in ROUTING-RULES.md.

---

*Created: January 2026*
*Last Updated: January 2026*
