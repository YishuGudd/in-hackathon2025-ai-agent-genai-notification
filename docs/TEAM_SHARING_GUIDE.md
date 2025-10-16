# Team Sharing Guide - DoorDash Notification Generator

This guide explains how to share the notification generation system with your teammates so they can use it without retraining from scratch.

---

## 📦 Option 1: Share as MCP Server (Recommended)

### For Your Teammates

Your teammates can add this to their Claude Desktop config:

```json
{
  "mcpServers": {
    "doordash_notifications": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/path/to/mcp-snowflake-server",
        "run",
        "python",
        "notification_server.py"
      ],
      "env": {
        "SNOWFLAKE_ACCOUNT": "DOORDASH",
        "SNOWFLAKE_USER": "their_username",
        "SNOWFLAKE_AUTHENTICATOR": "externalbrowser",
        "SNOWFLAKE_WAREHOUSE": "ADHOC",
        "SNOWFLAKE_DATABASE": "PRODDB",
        "SNOWFLAKE_SCHEMA": "PUBLIC",
        "SNOWFLAKE_ROLE": "their_role"
      }
    }
  }
}
```

### Available Tools

Once connected, they can use:

1. **`generate_consumer_notifications`** - Generate for a single consumer
   ```
   Consumer ID: 1193328057
   Min Score: 80
   Max Count: 10
   ```

2. **`batch_generate_notifications`** - Generate for multiple consumers
   ```
   Consumer IDs: [1193328057, 1036296113, ...]
   Min Score: 80
   ```

3. **`validate_notification`** - Check compliance
   ```
   Title: "Your go-tos are here"
   Body: "Reorder favorites or find something new"
   ```

---

## 📚 Option 2: Share as Python Module

### Installation for Teammates

1. **Clone the repo:**
   ```bash
   git clone <your-repo-url>
   cd mcp-snowflake-server
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Configure credentials:**
   Create their own `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env with their Snowflake credentials
   ```

### Usage Example

```python
from mcp_snowflake_server.notification_generator import NotificationGenerator
from mcp_snowflake_server.db_client import SnowflakeClient
import json

# Initialize
db = SnowflakeClient()
generator = NotificationGenerator()

# Get consumer profile
query = "SELECT PROFILE FROM PRODDB.ML.GENAI_CX_PROFILE_SHADOW WHERE CONSUMER_ID = 1193328057"
result = db.execute_read_query(query)
profile = json.loads(result[0]['PROFILE'])

# Generate notifications
notifications = generator.generate_notifications(
    profile=profile,
    min_score=80,
    max_count=10
)

# Print results
for i, notif in enumerate(notifications, 1):
    print(f"{i}. [{notif['score']}] {notif['title']}")
    print(f"   {notif['body']}")
    print(f"   Keyword: {notif['keyword']}\n")
```

---

## 📝 Option 3: Share Documentation & Scripts

### What to Share

Create a shared folder with these files:

1. **`restriction`** - Brand guidelines and restrictions
2. **`consumer_ids.csv`** - Sample consumer IDs
3. **`notifications_shadow_score80plus.csv`** - Example output
4. **`FINAL_GENERATION_SUMMARY.txt`** - Full documentation
5. **Reusable script** (see below)

### Standalone Script for Teammates

```python
# save as: generate_notifications.py
import os
import json
from dotenv import load_dotenv
import snowflake.connector
from notification_generator import NotificationGenerator

load_dotenv()

# Connect to Snowflake
conn = snowflake.connector.connect(
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    user=os.getenv('SNOWFLAKE_USER'),
    authenticator=os.getenv('SNOWFLAKE_AUTHENTICATOR'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    database=os.getenv('SNOWFLAKE_DATABASE'),
    schema=os.getenv('SNOWFLAKE_SCHEMA'),
    role=os.getenv('SNOWFLAKE_ROLE')
)

generator = NotificationGenerator()

# Generate for a consumer
consumer_id = input("Enter Consumer ID: ")
cursor = conn.cursor()
cursor.execute(f"SELECT PROFILE FROM PRODDB.ML.GENAI_CX_PROFILE_SHADOW WHERE CONSUMER_ID = {consumer_id}")
result = cursor.fetchone()

if result:
    profile = json.loads(result[0])
    notifications = generator.generate_notifications(profile, min_score=80)
    
    print(f"\nGenerated {len(notifications)} notifications:\n")
    for i, n in enumerate(notifications, 1):
        print(f"{i}. Score {n['score']}: {n['title']}")
        print(f"   {n['body']}\n")
else:
    print("Consumer not found")

conn.close()
```

---

## 🔄 Option 4: Export Knowledge Base

### Create a Knowledge Package

Package everything your teammates need:

```bash
# Create a shareable package
tar -czf doordash-notification-kit.tar.gz \
  restriction \
  consumer_ids.csv \
  notifications_shadow_score80plus.csv \
  FINAL_GENERATION_SUMMARY.txt \
  src/mcp_snowflake_server/notification_generator.py \
  notification_server.py \
  TEAM_SHARING_GUIDE.md
```

### Share via:
- Internal file share (Google Drive, Dropbox)
- Git repository (private repo)
- Confluence/Wiki documentation
- Slack/Teams with attachments

---

## 🎓 Training Resources to Share

### Quick Start Guide for Teammates

1. **Read `restriction`** - Complete brand guidelines (556 lines)
2. **Review `FINAL_GENERATION_SUMMARY.txt`** - Results and examples
3. **Import `notifications_shadow_score80plus.csv`** - See actual output
4. **Use `notification_generator.py`** - Ready-to-use Python module

### Key Concepts to Communicate

**1. DoorDash Brand Voice:**
- Conversational, not salesy
- Imagery-driven phrases ("Skip the schlep")
- Lightly playful, genuinely helpful

**2. Format Restrictions:**
- Title < 35 characters
- Body ≤ 140 characters
- No exclamation points
- Sentence case only

**3. Dietary Guardrails:**
- Extract preferred_dietary_preference from profile
- Filter out conflicting notifications
- Respect vegetarian, vegan, pescatarian preferences

**4. Scoring System:**
- 98-95: Perfect profile match
- 94-90: Strong alignment
- 89-80: Good engagement potential
- <80: Filtered out

---

## 🔧 Setting Up Teammates

### Step-by-Step Setup

**1. Environment Setup:**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone or copy the project
cd mcp-snowflake-server

# Install dependencies
uv sync
```

**2. Snowflake Access:**
Each teammate needs their own `.env`:
```bash
SNOWFLAKE_ACCOUNT=DOORDASH
SNOWFLAKE_USER=their.username
SNOWFLAKE_AUTHENTICATOR=externalbrowser
SNOWFLAKE_WAREHOUSE=ADHOC
SNOWFLAKE_DATABASE=PRODDB
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=their_role
```

**3. Test the Setup:**
```bash
uv run python -c "from notification_generator import NotificationGenerator; print('✓ Module loaded')"
```

---

## 💾 Preserving Your Work

### What Gets Preserved

Your current setup includes:

**1. Code & Logic:**
- ✅ `notification_generator.py` - Reusable Python module
- ✅ `notification_server.py` - MCP server implementation
- ✅ `db_client.py` - Snowflake connection handler

**2. Knowledge & Context:**
- ✅ `restriction` - Complete brand guidelines
- ✅ `FINAL_GENERATION_SUMMARY.txt` - Documentation
- ✅ `notifications_shadow_score80plus.csv` - Example outputs

**3. Data:**
- ✅ `consumer_ids.csv` - Sample consumers
- ✅ Profile analysis logic embedded in code

### What Teammates DON'T Need to Recreate

- ❌ Brand voice guidelines (saved in `restriction`)
- ❌ Dietary guardrail logic (in `notification_generator.py`)
- ❌ Scoring system (embedded in code)
- ❌ Format validation (in module)
- ❌ DoorDash-approved phrases (hardcoded)

---

## 🚀 Quick Start Commands for Teammates

### Generate for One Consumer
```bash
uv run python -c "
from notification_generator import NotificationGenerator
import json

generator = NotificationGenerator()
profile = {...}  # Load from Snowflake
notifications = generator.generate_notifications(profile, min_score=80)
print(json.dumps(notifications, indent=2))
"
```

### Validate a Notification
```python
from notification_generator import NotificationGenerator

generator = NotificationGenerator()
result = generator.validate_notification(
    title="Your go-tos are here",
    body="Reorder favorites or find something new worth trying"
)

if result['is_valid']:
    print("✓ Valid notification")
else:
    print("Issues:", result['issues'])
```

### Batch Generate (Using Script)
```bash
uv run python generate_shadow_high_score.py
# Output: notifications_shadow_score80plus.csv
```

---

## 📊 Sharing via Git Repository

### Recommended Git Workflow

**1. Create a dedicated repo:**
```bash
cd /Users/yishu.gu/Projects/mcp-snowflake-server
git add notification_generator.py notification_server.py
git add restriction TEAM_SHARING_GUIDE.md
git add example_consumer_ids.csv
git commit -m "Add DoorDash notification generator with brand guidelines"
git push
```

**2. Teammates clone:**
```bash
git clone <repo-url>
cd mcp-snowflake-server
uv sync
cp .env.example .env
# Edit .env with their credentials
```

**3. They're ready to go!**
```bash
uv run python notification_server.py  # Start MCP server
# Or use the Python module directly
```

---

## 🎯 What Makes This Shareable

1. **Self-contained module** - `notification_generator.py` has all the logic
2. **Clear documentation** - Guidelines and examples included
3. **Validated output** - 140+ examples in CSV
4. **Reusable patterns** - Teammates can extend with new cuisines
5. **No retraining needed** - All knowledge embedded in code

---

## 💡 Tips for Team Adoption

1. **Demo Session** - Show live generation for a consumer
2. **Share CSV Output** - Let them explore actual results
3. **Provide Examples** - Show before/after with brand voice
4. **Document Edge Cases** - Note dietary restrictions, score thresholds
5. **Set Up MCP** - Enable in Claude Desktop for easy access

---

## 🔐 Security Notes

- ⚠️ **Never commit `.env` files** (contains credentials)
- ✅ Share `.env.example` template instead
- ✅ Each teammate uses their own Snowflake credentials
- ✅ Keep consumer data secure (follow data governance policies)

---

## 📞 Support for Teammates

If teammates have issues:

1. **Can't connect to Snowflake** → Check their `.env` credentials
2. **Module import errors** → Run `uv sync` to install dependencies
3. **No notifications generated** → Consumer might not be in SHADOW table
4. **Dietary guardrails too strict** → Adjust in `notification_generator.py`
5. **Score threshold questions** → Review `FINAL_GENERATION_SUMMARY.txt`

---

## ✅ Checklist: What to Share

- [ ] `notification_generator.py` - Core module
- [ ] `notification_server.py` - MCP server (optional)
- [ ] `restriction` - Brand guidelines
- [ ] `TEAM_SHARING_GUIDE.md` - This file
- [ ] `FINAL_GENERATION_SUMMARY.txt` - Documentation
- [ ] `notifications_shadow_score80plus.csv` - Example output
- [ ] `.env.example` - Template (NOT actual `.env`)
- [ ] `consumer_ids.csv` - Sample data
- [ ] Setup instructions (included in this guide)

---

## 🎉 You're Ready to Share!

Your teammates will have:
- ✅ Working code they can run immediately
- ✅ Complete brand guidelines embedded
- ✅ Dietary guardrail logic ready
- ✅ Example outputs to learn from
- ✅ MCP server option for Claude Desktop

**No retraining needed - everything is documented and ready to use!**

