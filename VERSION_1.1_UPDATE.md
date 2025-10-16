# 🚀 Version 1.1 Update - Now on GitHub Master Branch

## ✅ Successfully Pushed to GitHub!

**Repository:** `YishuGudd/in-hackathon2025-ai-agent-genai-notification`  
**Branch:** `master`  
**Version:** 1.1.0  
**Status:** ✅ All changes committed and pushed

---

## 🆕 What's New in v1.1

### 1. Mild Spicy Guardrail 🌶️

**New Restriction (line 33):**
> "If cx profile contains 'mild spicy' taste, do not recommend 'spicy' keyword"

**Implementation:**
- New method: `passes_mild_spicy_guardrail()`
- Checks if taste preference has both "mild" AND "spicy"
- Filters out notifications containing "spicy" in title, body, or keyword
- Protects users who prefer mild flavors from overly spicy recommendations

**Example:**
```
Consumer with "mild spicy" preference:
  ❌ "Heat seekers wanted" (keyword: spicy food) - FILTERED OUT
  ❌ "Get spicy Thai curry" - FILTERED OUT
  ✅ "Noodle cravings covered" - ALLOWED
  ✅ "You pick. We roll" - ALLOWED
```

### 2. Updated URLs with Deals Filter 🔗

**Old URL:**
```
https://www.doordash.com/search/store/noodles?event_type=search&filterQuery-vertical_ids=1
```

**New URL:**
```
https://www.doordash.com/search/store/noodles?event_type=search&filterQuery-vertical_ids=1&filterQuery-deals-fill=true
```

**Benefits:**
- Users see available deals when clicking notification links
- Better engagement through deal visibility
- Aligns with DoorDash's promo-driven strategy

---

## 📊 Updated Results

**File:** `examples/notifications_updated_restrictions.csv`

- ✅ **128 notifications** (down from 140)
- 📈 **Average score:** 87.8/100 (up from 87.2)
- 🎯 **All scores ≥ 80**
- ✅ **100% compliance** with updated restrictions

**Why fewer notifications?**
- Stricter quality control
- Some consumers had fewer high-scoring matches (≥80)
- Result: Higher average quality

---

## 🔄 Changes Made to Code

### notification_generator.py

**Added:**
```python
__version__ = "1.1.0"

def passes_mild_spicy_guardrail(self, notification: Dict, taste_pref: str) -> bool:
    """NEW v1.1: Filter spicy if taste preference is 'mild spicy'"""
    if not taste_pref:
        return True
    
    taste_lower = taste_pref.lower()
    
    if 'mild' in taste_lower and 'spicy' in taste_lower:
        content = f"{notification['title']} {notification['body']} {notification['keyword']}".lower()
        if 'spicy' in content:
            return False
    
    return True

def format_for_doordash_url(self, keyword: str) -> str:
    """Updated v1.1: Now includes deals filter"""
    encoded_keyword = keyword.replace(' ', '%20')
    return f"https://www.doordash.com/search/store/{encoded_keyword}?event_type=search&filterQuery-vertical_ids=1&filterQuery-deals-fill=true"
```

**Updated:**
```python
# In generate_notifications() method
# Apply guardrails in order:
# 1. Dietary guardrail
# 2. NEW: Mild spicy guardrail
for notif in all_notifications:
    if not self.passes_dietary_guardrail(notif, preferred_dietary):
        continue
    if not self.passes_mild_spicy_guardrail(notif, taste):
        continue
    filtered.append(notif)
```

### brand_guidelines.txt

**Added line 33:**
```
* If cx profile contains 'mild spicy' taste, do not recommend 'spicy' keyword
```

---

## 📤 How Your Team Gets the Update

### If They Already Cloned:

```bash
cd in-hackathon2025-ai-agent-genai-notification
git pull origin master
# They now have v1.1!
```

### If They Haven't Cloned Yet:

```bash
git clone https://github.com/YishuGudd/in-hackathon2025-ai-agent-genai-notification.git
cd in-hackathon2025-ai-agent-genai-notification
# Automatically on master with v1.1
```

---

## 📋 Files Updated on GitHub

1. **notification_generator/notification_generator.py** ⬆️ v1.1.0
   - Added mild spicy guardrail method
   - Updated URL generation with deals filter
   - Added version number

2. **notification_generator/brand_guidelines.txt** ⬆️ Updated
   - Added line 33: mild spicy restriction

3. **examples/notifications_updated_restrictions.csv** 🆕 New file
   - 128 notifications with updated URLs
   - All scores ≥ 80

4. **examples/UPDATED_GENERATION_SUMMARY.txt** 🆕 New file
   - Documents v1.1 changes
   - Shows before/after comparisons

---

## ✅ Verification

**Git commit:** `dc64bfc`  
**Pushed to:** `origin/master`  
**Files changed:** 4  
**Lines added:** 346  

View on GitHub:
```
https://github.com/YishuGudd/in-hackathon2025-ai-agent-genai-notification
```

---

## 🎯 Summary for Your Team

**What to tell them:**
> "Updated to v1.1 with mild spicy guardrail and deals-enabled URLs. Pull the latest from master to get the updates!"

**They run:**
```bash
git pull origin master
```

**They immediately get:**
- ✅ Mild spicy guardrail protection
- ✅ URLs with deals filter
- ✅ Updated examples (128 notifications)
- ✅ Higher quality output (87.8 avg score)

---

## 🔄 Version History

**v1.0** (Initial release)
- Basic notification generation
- DoorDash brand voice compliance
- Dietary guardrails (vegetarian, vegan, pescatarian)
- 140 notifications, avg score 87.2

**v1.1** (Current) ⭐
- Added mild spicy guardrail
- Updated URLs with deals filter
- 128 notifications, avg score 87.8
- Improved quality through stricter filtering

---

**Everything is now on GitHub master branch and ready for your team to use!** 🚀
