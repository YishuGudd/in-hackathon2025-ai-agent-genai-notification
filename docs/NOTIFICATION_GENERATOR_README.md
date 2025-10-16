# DoorDash Notification Generator

**Personalized push notification generator using consumer GenAI profiles**

---

## ✨ Features

- 🎯 **Profile-based personalization** - Matches consumer cuisine, food, taste preferences
- 🔒 **Dietary guardrails** - Respects vegetarian, vegan, pescatarian preferences
- ✅ **Brand compliance** - Follows DoorDash brand voice and format restrictions
- 📊 **Quality scoring** - Ranks notifications by relevance (80-98 scale)
- 🚀 **Production-ready** - All outputs validated and compliant

---

## 🚀 Quick Start

### For Your Team (Using MCP Server)

1. **Add to Claude Desktop config:**
   ```json
   "doordash_notifications": {
     "command": "uv",
     "args": ["--directory", "/path/to/mcp-snowflake-server", "run", "python", "notification_server.py"]
   }
   ```

2. **Configure Snowflake credentials** (`.env` file)

3. **Use in Claude:**
   - "Generate notifications for consumer 1193328057"
   - "Validate this notification title and body"
   - "Batch generate for these 10 consumers"

### For Developers (Using Python Module)

```python
from notification_generator import NotificationGenerator
import json

# Load consumer profile from Snowflake
profile = {...}  # JSON profile from GENAI_CX_PROFILE_SHADOW

# Generate notifications
generator = NotificationGenerator()
notifications = generator.generate_notifications(
    profile=profile,
    min_score=80,  # Only return score >= 80
    max_count=10   # Top 10 notifications
)

# Use the results
for notif in notifications:
    print(f"[{notif['score']}] {notif['title']}")
    print(f"URL: {generator.format_for_doordash_url(notif['keyword'])}")
```

---

## 📋 What's Included

### Core Files

- **`notification_generator.py`** - Main Python module with all logic
- **`notification_server.py`** - MCP server wrapper
- **`restriction`** - DoorDash brand guidelines (556 lines)
- **`.env.example`** - Snowflake credentials template

### Documentation

- **`TEAM_SHARING_GUIDE.md`** - How to share with teammates
- **`FINAL_GENERATION_SUMMARY.txt`** - Complete process documentation
- **`NOTIFICATION_GENERATOR_README.md`** - This file

### Example Outputs

- **`notifications_shadow_score80plus.csv`** - 140 example notifications
- **`consumer_ids.csv`** - Sample consumer IDs

---

## 🎯 Brand Voice Examples

Your team will generate notifications like:

| Traditional | DoorDash Brand Voice ✅ |
|------------|----------------------|
| "Order Chinese food now" | "Skip the schlep" |
| "Build your bowl" | "You pick. We roll" |
| "Special offer available" | "Deal dropped. You're up" |
| "Your favorites are available" | "Your go-tos are here" |

**Why:** More conversational, imagery-driven, and engaging while staying genuine.

---

## 🔒 Dietary Guardrails

The system automatically filters notifications based on consumer dietary preferences:

| Preference | Filters Out | Allows |
|-----------|-------------|---------|
| Vegetarian | Chicken, beef, pork notifications | Plant-based, general cuisine |
| Vegan | All animal products | Plant-based only |
| Pescatarian | Land meat notifications | Seafood, vegetarian |
| None | Nothing filtered | All notifications |

---

## 📊 Scoring System

**98-95 (Excellent):** Perfect cuisine/food match  
**94-90 (Very Good):** Strong preference alignment  
**89-85 (Good):** Taste/format aligned  
**84-80 (Fair):** Universal engagement opportunities  
**<80:** Filtered out (low quality)

---

## ✅ Compliance Checklist

All generated notifications meet:

- ✅ Title < 35 characters
- ✅ Body ≤ 140 characters
- ✅ No exclamation points
- ✅ Sentence case
- ✅ Max 1 emoji (used ~50% of time)
- ✅ No meal time references
- ✅ No "authentic" descriptions
- ✅ No DoorDash mentions
- ✅ Eighth-grade reading level
- ✅ DoorDash brand voice

---

## 📦 Data Sources

**Primary Table:** `PRODDB.ML.GENAI_CX_PROFILE_SHADOW`

**Profile Structure:**
```json
{
  "overall_profile": {
    "cuisine_preferences": "Chinese, Japanese, Thai...",
    "food_preferences": "Noodle soups, rice bowls...",
    "taste_preference": "Savory, spicy, umami...",
    "dietary_preferences": {
      "strict_dietary_preference": "none",
      "preferred_dietary_preference": "Occasional vegetarian"
    }
  }
}
```

---

## 🔄 Adding New Training Data

To incorporate new data sources:

### 1. Update the Generator Module

```python
# In notification_generator.py
def _add_new_cuisine_notifications(self, notifications, cuisine, food):
    if 'mediterranean' in cuisine:
        notifications.append({
            "title": "Mediterranean picks",
            "body": "Fresh gyros, falafel from spots worth reordering",
            "keyword": "Mediterranean food",
            "score": 82
        })
```

### 2. Pull Additional Profile Data

```python
# Query additional tables
query = """
SELECT 
    cp.CONSUMER_ID,
    cp.PROFILE,
    oh.ORDER_HISTORY_180D,
    dm.GENAI_PROFILE
FROM PRODDB.ML.GENAI_CX_PROFILE_SHADOW cp
LEFT JOIN PRODDB.PUBLIC.FACT_DASHI_CX_METADATA dm 
    ON cp.CONSUMER_ID = dm.CONSUMER_ID
WHERE cp.CONSUMER_ID = {consumer_id}
"""
```

### 3. Enhance Scoring Logic

```python
# Add order frequency scoring
if order_count > 50:
    base_score += 5  # Boost for frequent orderers
```

### 4. Test and Validate

```python
generator = NotificationGenerator()
result = generator.validate_notification(title, body)
assert result['is_valid'], "Validation failed"
```

---

## 🎓 For Your Teammates: No Training Needed

When you share this, your teammates get:

✅ **Pre-built logic** - All brand guidelines embedded  
✅ **Working examples** - 140 validated notifications  
✅ **Reusable code** - Just import and use  
✅ **Documentation** - Complete guide and restrictions  
✅ **MCP server option** - Use directly in Claude Desktop  

**They literally just need to:**
1. Set up Snowflake credentials
2. Import the module
3. Start generating

---

## 📚 Additional Resources

- **Brand Guidelines:** See `restriction` file (lines 1-556)
- **Example Output:** `notifications_shadow_score80plus.csv`
- **Team Setup:** `TEAM_SHARING_GUIDE.md`
- **Results Summary:** `FINAL_GENERATION_SUMMARY.txt`

---

## 🐛 Troubleshooting

**Issue:** "No profile found"  
**Solution:** Check if consumer is in SHADOW table, not main table

**Issue:** "Too few notifications generated"  
**Solution:** Lower `min_score` threshold or check dietary filters

**Issue:** "Validation failures"  
**Solution:** Review `restriction` file for specific rule violations

**Issue:** "Snowflake connection error"  
**Solution:** Verify `.env` credentials and SSO authentication

---

## 📧 Contact & Support

For questions about this system:
- Review `TEAM_SHARING_GUIDE.md` for setup help
- Check `restriction` for brand guideline questions
- See `FINAL_GENERATION_SUMMARY.txt` for methodology

---

**Built with:** Python 3.10+, Snowflake, MCP, DoorDash Brand Guidelines  
**Last Updated:** October 16, 2025  
**Version:** 1.0

