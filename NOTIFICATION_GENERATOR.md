# Notification Generator

## Overview

AI-powered push notification generator for DoorDash consumers. Generates personalized notifications based on GenAI consumer profiles from Snowflake.

## Features

- 🎯 **Personalization**: Matches consumer cuisine, food, taste preferences
- 🔒 **Dietary Guardrails**: Respects vegetarian, vegan, pescatarian preferences
- ✅ **Brand Compliance**: Follows DoorDash brand voice guidelines
- 📊 **Quality Scoring**: Ranks notifications 80-98 based on relevance
- 🚀 **Production Ready**: All outputs validated and compliant

## Quick Start

```bash
cd notification_generator
python quick_start.py <consumer_id>
```

See `notification_generator/README.md` for detailed setup.

## Example Output

```json
{
  "title": "Noodle cravings covered",
  "body": "🍜 Hot bowls and hand-pulled options ready from spots you'll love",
  "keyword": "noodles",
  "score": 98
}
```

## Documentation

- `/docs/NOTIFICATION_GENERATOR_README.md` - Complete guide
- `/docs/TEAM_SHARING_GUIDE.md` - Setup for teammates
- `/docs/FINAL_GENERATION_SUMMARY.txt` - Methodology & results
- `/notification_generator/brand_guidelines.txt` - DoorDash brand rules

## Examples

See `/examples/notifications_shadow_score80plus.csv` for 140 validated examples.

## Data Source

**Snowflake Table**: `PRODDB.ML.GENAI_CX_PROFILE_SHADOW`

Requires Snowflake access with SSO authentication (see root `.env.example`).
