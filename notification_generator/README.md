# DoorDash Notification Generator

Personalized push notification generator using consumer GenAI profiles from Snowflake.

## Quick Start

```bash
# 1. Install dependencies
pip install snowflake-connector-python python-dotenv

# 2. Configure Snowflake (copy from root .env.example)
cp ../.env.example .env
# Edit .env with your credentials

# 3. Generate notifications for a consumer
python quick_start.py 1193328057
```

## Files

- `notification_generator.py` - Core Python module (reusable)
- `notification_server.py` - MCP server for Claude Desktop
- `quick_start.py` - Command-line script for testing
- `brand_guidelines.txt` - Complete DoorDash brand guidelines

## Features

✅ Profile-based personalization
✅ DoorDash brand voice compliance  
✅ Dietary preference guardrails
✅ Quality scoring (80-98 scale)
✅ Format validation

## Documentation

See `/docs` folder for:
- NOTIFICATION_GENERATOR_README.md - Full feature docs
- TEAM_SHARING_GUIDE.md - Setup instructions
- FINAL_GENERATION_SUMMARY.txt - Methodology

## Examples

See `/examples` folder for:
- 140 validated notifications
- Sample consumer IDs
- Generation statistics
