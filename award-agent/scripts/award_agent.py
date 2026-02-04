#!/usr/bin/env python3
"""
Award Agent - Universal Award Matching System
Version 2.0

An intelligent system for analyzing ANY campaign and recommending
optimal award opportunities across all major advertising and marketing awards.

Works with any brand, any category, any agency.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import subprocess
import sys

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
AWARDS_DB = DATA_DIR / "awards" / "awards_database.json"
CAMPAIGNS_DIR = DATA_DIR / "campaigns"
PROMPTS_DIR = PROJECT_ROOT / "prompts"
EXAMPLES_DB = DATA_DIR / "winning_examples.json"

def load_awards_database():
    """Load the awards database."""
    with open(AWARDS_DB, 'r') as f:
        return json.load(f)

def load_winning_examples():
    """Load winning examples for reference."""
    if EXAMPLES_DB.exists():
        with open(EXAMPLES_DB, 'r') as f:
            return json.load(f)
    return None

def load_campaign(campaign_id):
    """Load a specific campaign profile."""
    campaign_file = CAMPAIGNS_DIR / f"{campaign_id}.json"
    if campaign_file.exists():
        with open(campaign_file, 'r') as f:
            return json.load(f)
    return None

def list_campaigns():
    """List all saved campaigns."""
    campaigns = []
    for f in CAMPAIGNS_DIR.glob("*.json"):
        if f.name != "campaign_schema.json":
            campaigns.append(f.stem)
    return campaigns

def save_campaign(campaign_data):
    """Save a campaign profile."""
    campaign_file = CAMPAIGNS_DIR / f"{campaign_data['id']}.json"
    with open(campaign_file, 'w') as f:
        json.dump(campaign_data, f, indent=2)
    print(f"Campaign saved: {campaign_file}")

def get_upcoming_deadlines(awards_db, days_ahead=90):
    """Get awards with upcoming deadlines."""
    upcoming = []
    today = datetime.now()
    cutoff = today + timedelta(days=days_ahead)

    for award in awards_db['awards']:
        upcoming.append({
            'name': award['name'],
            'prestige': award['prestige_tier'],
            'deadlines': award.get('deadlines', award.get('deadlines_2026', {})),
            'categories': [c['name'] if isinstance(c, dict) else c for c in award.get('categories', [])][:5]
        })

    return sorted(upcoming, key=lambda x: x['prestige'])

def format_awards_context(awards_db):
    """Format awards database for prompt context."""
    context = "# Available Awards Database\n\n"

    # Add winning patterns
    if 'winning_patterns' in awards_db:
        context += "## 2024 WINNING PATTERNS\n"
        for pattern in awards_db['winning_patterns'].get('2024_themes', []):
            context += f"- {pattern}\n"
        context += "\n"

    for tier in [1, 2, 3]:
        tier_name = {
            1: "TIER 1 - Premier Awards (Career-defining)",
            2: "TIER 2 - Strong Industry Awards",
            3: "TIER 3 - Volume/Regional Awards"
        }[tier]
        context += f"\n## {tier_name}\n\n"

        for award in awards_db['awards']:
            if award['prestige_tier'] == tier:
                context += f"### {award['name']}\n"
                context += f"- **ID**: {award['id']}\n"
                if 'prestige_notes' in award:
                    context += f"- **Why it matters**: {award['prestige_notes']}\n"

                # Categories with what wins
                cats = award.get('categories', [])
                if cats and isinstance(cats[0], dict):
                    cat_names = [c['name'] for c in cats[:6]]
                    context += f"- **Key categories**: {', '.join(cat_names)}\n"
                elif cats:
                    context += f"- **Categories**: {', '.join(cats[:6])}\n"

                context += f"- **Cost**: {award.get('cost_per_entry', 'Varies')}\n"
                context += f"- **Strategic notes**: {award.get('strategic_notes', 'N/A')}\n"

                deadlines = award.get('deadlines', award.get('deadlines_2026', {}))
                if deadlines:
                    deadline_str = ", ".join([f"{k}: {v}" for k, v in deadlines.items() if isinstance(v, str)])
                    context += f"- **Deadlines**: {deadline_str}\n"

                # Judging intel
                judging = award.get('judging_intel', {})
                if judging:
                    if 'what_they_value' in judging:
                        context += f"- **What judges value**: {judging['what_they_value']}\n"

                context += "\n"

    return context

def create_matching_prompt(campaign_description, awards_context, matcher_prompt, examples=None):
    """Create the full prompt for Claude."""
    prompt = f"""{matcher_prompt}

---

# AWARDS DATABASE

{awards_context}

---

# CAMPAIGN TO ANALYZE

{campaign_description}

---
"""

    if examples:
        prompt += """
# WINNING EXAMPLES FOR REFERENCE

Study these 2024 winners to understand what's working:

"""
        for winner in examples.get('grand_prix_winners_2024', [])[:4]:
            prompt += f"""**{winner['campaign']}** ({winner['brand']})
- Awards: {', '.join(winner['awards_won'][:3])}
- The idea: {winner['the_idea'][:200]}...
- Why it won: {', '.join(list(winner['why_it_won'].values())[:3])}

"""

    prompt += """
---

# YOUR TASK

Analyze this campaign and provide comprehensive award recommendations following the output format in your instructions. Be specific about:
1. Which awards to enter (with exact category recommendations)
2. Why each award is a good fit (or not) - be honest
3. What assets/materials are needed
4. Deadline priorities
5. Strategic "reach" opportunities that might not be obvious
6. How to frame the case study differently for different award types

Be honest about weaknesses. Don't recommend awards where the work won't be competitive.
"""
    return prompt

def quick_analyze(description):
    """Quick analysis mode - just describe your campaign."""
    print("\n" + "="*60)
    print("AWARD AGENT v2.0 - Quick Analysis Mode")
    print("="*60)

    # Load resources
    awards_db = load_awards_database()
    examples = load_winning_examples()
    matcher_prompt_path = PROMPTS_DIR / "matcher.md"

    with open(matcher_prompt_path, 'r') as f:
        matcher_prompt = f.read()

    # Format context
    awards_context = format_awards_context(awards_db)

    # Create full prompt
    full_prompt = create_matching_prompt(description, awards_context, matcher_prompt, examples)

    # Output the prompt
    output_path = PROJECT_ROOT / "output" / "latest_prompt.md"
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(full_prompt)

    print(f"\nPrompt prepared and saved to: {output_path}")
    print(f"\nPrompt length: {len(full_prompt):,} characters")
    print("\nTo use this:")
    print("1. Copy the prompt from the output file")
    print("2. Paste into Claude and get award recommendations")
    print("3. Or integrate with Claude API for automated analysis")

    return full_prompt

def interactive_campaign_builder():
    """Build a campaign profile interactively."""
    print("\n" + "="*60)
    print("AWARD AGENT v2.0 - Campaign Builder")
    print("="*60)

    campaign = {}

    print("\nLet's capture your campaign. Answer what you know, skip what you don't.\n")

    # Basic info
    campaign['name'] = input("Campaign name: ").strip()
    campaign['id'] = input("Campaign ID (e.g., brand-campaign-2024): ").strip() or campaign['name'].lower().replace(' ', '-')
    campaign['client'] = input("Client/Company: ").strip()
    campaign['brand'] = input("Brand: ").strip()

    # Agency info
    print("\n--- Agency Info ---")
    campaign['agency'] = {}
    campaign['agency']['lead_agency'] = input("Lead creative agency: ").strip()
    campaign['agency']['media_agency'] = input("Media agency (or skip): ").strip() or None

    # Industry
    print("\n--- Industry ---")
    print("Options: sports_beverages, beverages_non_alcohol, beverages_alcohol, food_snacks,")
    print("         automotive, technology, financial_services, healthcare_pharma, retail,")
    print("         entertainment_media, fashion_apparel, beauty_personal_care, b2b_services, other")
    campaign['industry'] = input("Industry category: ").strip() or "other"

    # Dates
    print("\n--- Dates ---")
    campaign['dates'] = {}
    campaign['dates']['campaign_start'] = input("Campaign start date (YYYY-MM-DD, or skip): ").strip() or None
    campaign['dates']['campaign_end'] = input("Campaign end date (YYYY-MM-DD, or skip): ").strip() or None

    # Brief
    print("\n--- The Brief ---")
    campaign['brief'] = {}
    campaign['brief']['challenge'] = input("What business problem were you solving? ").strip()
    campaign['brief']['context'] = input("What was the competitive context? ").strip()
    campaign['brief']['target_audience'] = {
        'primary': input("Primary target audience: ").strip()
    }
    campaign['brief']['key_insight'] = input("What insight unlocked the creative? ").strip()

    print("\nBudget tier options: micro, small, medium, large, mega")
    campaign['brief']['budget_tier'] = input("Budget tier: ").strip() or "medium"

    # Strategy
    print("\n--- Strategy ---")
    campaign['strategy'] = {}
    campaign['strategy']['strategic_approach'] = input("What was the strategic approach? ").strip()
    campaign['strategy']['why_this_strategy'] = input("Why was this the RIGHT strategy? ").strip()

    # Creative
    print("\n--- The Creative ---")
    campaign['creative'] = {}
    campaign['creative']['big_idea'] = input("What was the big idea (one sentence)? ").strip()
    campaign['creative']['tagline'] = input("Campaign tagline (if any): ").strip() or None
    campaign['creative']['what_made_it_special'] = input("What makes this work potentially award-worthy? ").strip()

    print("\nAny notable craft elements? (e.g., 'exceptional VFX', 'A-list director', 'original score')")
    craft = input("Craft elements (comma-separated): ").strip()
    if craft:
        campaign['creative']['craft_elements'] = [c.strip() for c in craft.split(',')]

    print("\nAny innovation elements? (e.g., 'first-ever use of...', 'new technology')")
    innovation = input("Innovation elements (comma-separated): ").strip()
    if innovation:
        campaign['creative']['innovation_elements'] = [i.strip() for i in innovation.split(',')]

    # Executions
    print("\n--- Executions (comma-separated) ---")
    print("Common types: tv_spot_30, tv_spot_60, online_video, social_video_short, tiktok,")
    print("              instagram_reels, youtube_content, print_single, print_campaign,")
    print("              outdoor_static, outdoor_digital, experiential_event, experiential_activation,")
    print("              influencer_partnership, branded_content_short, branded_content_documentary,")
    print("              website, microsite, app, pr_stunt, pr_earned_media")
    exec_input = input("What did you create? ").strip()
    campaign['execution_types'] = [e.strip() for e in exec_input.split(',') if e.strip()]

    # Talent
    print("\n--- Talent (comma-separated, or skip) ---")
    campaign['talent'] = {}
    athletes = input("Athletes involved: ").strip()
    if athletes:
        campaign['talent']['athletes'] = [{'name': a.strip()} for a in athletes.split(',')]
    celebs = input("Celebrities: ").strip()
    if celebs:
        campaign['talent']['celebrities'] = [{'name': c.strip()} for c in celebs.split(',')]
    influencers = input("Influencers: ").strip()
    if influencers:
        campaign['talent']['influencers'] = [{'name': i.strip()} for i in influencers.split(',')]
    campaign['talent']['director'] = input("Director: ").strip() or None
    campaign['talent']['production_company'] = input("Production company: ").strip() or None

    # Partnerships
    print("\n--- Partnerships (if any) ---")
    campaign['partnerships'] = []
    add_partnership = input("Any brand/media/platform partnerships? (y/n): ").strip().lower()
    while add_partnership == 'y':
        partner = {}
        partner['partner_name'] = input("  Partner name: ").strip()
        print("  Types: league, team, event, platform, media_publisher, brand, nonprofit, retailer, other")
        partner['partner_type'] = input("  Partner type: ").strip()
        partner['partnership_description'] = input("  What did the partnership involve? ").strip()
        campaign['partnerships'].append(partner)
        add_partnership = input("Add another partnership? (y/n): ").strip().lower()

    # Results
    print("\n--- Results (IMPORTANT for effectiveness awards) ---")
    campaign['results'] = {}
    campaign['results']['results_summary'] = input("One-line headline result: ").strip()

    campaign['results']['business_results'] = {}
    print("\nBusiness results (leave blank if unknown):")
    sales = input("  Sales impact (e.g., '+40% lift'): ").strip()
    if sales:
        campaign['results']['business_results']['sales'] = {'result': sales}
    share = input("  Market share change: ").strip()
    if share:
        campaign['results']['business_results']['market_share'] = {'result': share}
    roi = input("  ROI/ROAS: ").strip()
    if roi:
        campaign['results']['business_results']['roi_roas'] = roi

    campaign['results']['brand_metrics'] = {}
    print("\nBrand metrics:")
    awareness = input("  Awareness lift: ").strip()
    if awareness:
        campaign['results']['brand_metrics']['awareness'] = {'lift': awareness}
    consideration = input("  Consideration lift: ").strip()
    if consideration:
        campaign['results']['brand_metrics']['consideration'] = {'lift': consideration}

    campaign['results']['engagement_metrics'] = {}
    print("\nEngagement metrics:")
    impressions = input("  Impressions: ").strip()
    if impressions:
        campaign['results']['engagement_metrics']['impressions'] = impressions
    views = input("  Video views: ").strip()
    if views:
        campaign['results']['engagement_metrics']['video_views'] = views
    social = input("  Social engagement: ").strip()
    if social:
        campaign['results']['engagement_metrics']['social_engagement'] = social

    campaign['results']['earned_media'] = {}
    emv = input("  Earned media value: ").strip()
    if emv:
        campaign['results']['earned_media']['earned_media_value'] = emv
    press = input("  Notable press coverage (comma-separated): ").strip()
    if press:
        campaign['results']['earned_media']['notable_coverage'] = [p.strip() for p in press.split(',')]

    verified = input("\nAre results verified and client-approved for sharing? (y/n): ").strip().lower()
    campaign['results']['results_verified'] = verified == 'y'
    campaign['results']['results_source'] = input("Source of results data (e.g., Nielsen, internal): ").strip()

    # Award potential self-assessment
    print("\n--- Award Potential Assessment (1-10 scale) ---")
    campaign['award_potential'] = {}
    campaign['award_potential']['craft_strength'] = int(input("  Craft/production quality (1-10): ").strip() or 5)
    campaign['award_potential']['idea_strength'] = int(input("  Idea originality (1-10): ").strip() or 5)
    campaign['award_potential']['results_strength'] = int(input("  Results impressiveness (1-10): ").strip() or 5)
    campaign['award_potential']['innovation_strength'] = int(input("  Innovation/newness (1-10): ").strip() or 5)
    campaign['award_potential']['cultural_impact_strength'] = int(input("  Cultural conversation (1-10): ").strip() or 5)

    print("\nWhat are the strongest angles for awards?")
    angles = input("  (comma-separated): ").strip()
    if angles:
        campaign['award_potential']['strongest_angles'] = [a.strip() for a in angles.split(',')]

    weaknesses = input("Honest weaknesses? (comma-separated): ").strip()
    if weaknesses:
        campaign['award_potential']['weaknesses'] = [w.strip() for w in weaknesses.split(',')]

    # Assets
    print("\n--- Available Assets ---")
    campaign['assets'] = {}
    has_case_video = input("Do you have a case study video? (y/n): ").strip().lower()
    campaign['assets']['case_study_video'] = {'exists': has_case_video == 'y'}
    if has_case_video == 'y':
        duration = input("  Duration (in seconds): ").strip()
        if duration:
            campaign['assets']['case_study_video']['duration_seconds'] = int(duration)

    # Save
    save_campaign(campaign)

    # Offer to analyze
    analyze = input("\nWould you like to analyze this campaign for award opportunities now? (y/n): ").strip().lower()
    if analyze == 'y':
        description = f"""
Campaign: {campaign['name']}
Brand: {campaign['brand']}
Client: {campaign['client']}
Industry: {campaign.get('industry', 'N/A')}

Challenge: {campaign['brief'].get('challenge', 'N/A')}
Insight: {campaign['brief'].get('key_insight', 'N/A')}
Big Idea: {campaign['creative'].get('big_idea', 'N/A')}
What makes it special: {campaign['creative'].get('what_made_it_special', 'N/A')}

Executions: {', '.join(campaign.get('execution_types', []))}
Talent: {json.dumps(campaign.get('talent', {}))}

Results:
- Summary: {campaign['results'].get('results_summary', 'N/A')}
- Business: {json.dumps(campaign['results'].get('business_results', {}))}
- Brand: {json.dumps(campaign['results'].get('brand_metrics', {}))}
- Engagement: {json.dumps(campaign['results'].get('engagement_metrics', {}))}
- Results verified: {campaign['results'].get('results_verified', False)}

Self-Assessment:
- Craft: {campaign['award_potential'].get('craft_strength', 'N/A')}/10
- Idea: {campaign['award_potential'].get('idea_strength', 'N/A')}/10
- Results: {campaign['award_potential'].get('results_strength', 'N/A')}/10
- Innovation: {campaign['award_potential'].get('innovation_strength', 'N/A')}/10
- Cultural Impact: {campaign['award_potential'].get('cultural_impact_strength', 'N/A')}/10
- Strengths: {campaign['award_potential'].get('strongest_angles', [])}
- Weaknesses: {campaign['award_potential'].get('weaknesses', [])}
"""
        quick_analyze(description)

    return campaign

def show_deadline_calendar():
    """Display upcoming award deadlines."""
    print("\n" + "="*60)
    print("AWARD AGENT v2.0 - Award Calendar")
    print("="*60)

    awards_db = load_awards_database()
    upcoming = get_upcoming_deadlines(awards_db)

    print("\n*** = Tier 1 (Premier)  ** = Tier 2 (Strong)  * = Tier 3 (Volume)\n")

    for award in upcoming:
        tier_badge = "***" if award['prestige'] == 1 else "**" if award['prestige'] == 2 else "*"
        print(f"\n{tier_badge} {award['name']}")
        if award['deadlines']:
            for k, v in award['deadlines'].items():
                if isinstance(v, str):
                    print(f"   {k}: {v}")
        cats = award['categories']
        if cats:
            print(f"   Key categories: {', '.join(cats[:3])}")

def show_stats():
    """Show database statistics."""
    awards_db = load_awards_database()

    print("\n" + "="*60)
    print("AWARD AGENT v2.0 - Database Stats")
    print("="*60)

    total = len(awards_db['awards'])
    tier1 = len([a for a in awards_db['awards'] if a['prestige_tier'] == 1])
    tier2 = len([a for a in awards_db['awards'] if a['prestige_tier'] == 2])
    tier3 = len([a for a in awards_db['awards'] if a['prestige_tier'] == 3])

    print(f"\nTotal awards in database: {total}")
    print(f"  Tier 1 (Premier): {tier1}")
    print(f"  Tier 2 (Strong): {tier2}")
    print(f"  Tier 3 (Volume): {tier3}")

    # Show 2024 winning patterns
    if 'winning_patterns' in awards_db:
        print("\n2024 Winning Patterns:")
        for pattern in awards_db['winning_patterns'].get('2024_themes', []):
            print(f"  - {pattern}")

    campaigns = list_campaigns()
    print(f"\nSaved campaigns: {len(campaigns)}")
    for c in campaigns:
        print(f"  - {c}")

def show_winners():
    """Show 2024 grand prix winners for reference."""
    examples = load_winning_examples()

    if not examples:
        print("No winning examples database found.")
        return

    print("\n" + "="*60)
    print("AWARD AGENT v2.0 - 2024 Grand Prix Winners")
    print("="*60)

    for winner in examples.get('grand_prix_winners_2024', []):
        print(f"\n{'='*40}")
        print(f"**{winner['campaign']}** - {winner['brand']}")
        print(f"Agency: {winner['agency']}")
        print(f"\nAwards won:")
        for award in winner['awards_won']:
            print(f"  - {award}")
        print(f"\nThe idea: {winner['the_idea'][:300]}...")
        print(f"\nWhy it won:")
        for key, value in winner['why_it_won'].items():
            print(f"  - {key}: {value}")
        print(f"\nWhat to learn:")
        for lesson in winner['what_to_learn']:
            print(f"  - {lesson}")

def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("  AWARD AGENT v2.0")
    print("  Universal Award Matching System")
    print("="*60)

    if len(sys.argv) < 2:
        print("""
Usage:
  python award_agent.py analyze "Your campaign description here..."
  python award_agent.py build      # Interactive campaign builder
  python award_agent.py deadlines  # Show award calendar
  python award_agent.py stats      # Show database statistics
  python award_agent.py winners    # Show 2024 grand prix winners
  python award_agent.py list       # List saved campaigns

Examples:
  python award_agent.py analyze "Nike 'Just Don't Quit' - Film campaign
    featuring Serena Williams. 60-second hero spot, social content, and
    stadium activations. 35% lift in brand consideration, 100M video views,
    covered by ESPN and NYT."

  python award_agent.py analyze "B2B SaaS launch campaign with LinkedIn
    thought leadership, webinar series, and targeted digital. 200% increase
    in qualified leads, 50% reduction in CAC."
        """)
        return

    command = sys.argv[1].lower()

    if command == "analyze":
        if len(sys.argv) < 3:
            print("Please provide a campaign description.")
            print('Example: python award_agent.py analyze "Your campaign description..."')
            return
        description = " ".join(sys.argv[2:])
        quick_analyze(description)

    elif command == "build":
        interactive_campaign_builder()

    elif command == "deadlines":
        show_deadline_calendar()

    elif command == "stats":
        show_stats()

    elif command == "winners":
        show_winners()

    elif command == "list":
        campaigns = list_campaigns()
        print("\nSaved campaigns:")
        for c in campaigns:
            print(f"  - {c}")
        if not campaigns:
            print("  (none yet)")

    else:
        print(f"Unknown command: {command}")
        print("Valid commands: analyze, build, deadlines, stats, winners, list")

if __name__ == "__main__":
    main()
