# Setting Master as Default Branch on GitHub

## ✅ Current Status

✓ Master branch created and pushed
✓ All notification generator files on master
✓ Documentation updated to reference master
✓ Ready to share with team

## 🔧 To Make Master the Default Branch on GitHub

### Option 1: Via GitHub Website (Recommended)

1. **Go to your repository:**
   https://github.com/YishuGudd/in-hackathon2025-ai-agent-genai-notification

2. **Click "Settings"** (top right, near the repository name)

3. **In the left sidebar, click "General"**

4. **Scroll to "Default branch" section**

5. **Click the switch/pencil icon** next to the current default branch

6. **Select "master"** from the dropdown

7. **Click "Update"** and confirm

8. **Done!** Master is now the default branch

### Option 2: Via GitHub CLI (If you have gh installed)

```bash
gh repo edit --default-branch master
```

### After Setting Default

When teammates clone, they'll automatically get the master branch:
```bash
git clone https://github.com/YishuGudd/in-hackathon2025-ai-agent-genai-notification.git
cd in-hackathon2025-ai-agent-genai-notification
# Automatically on master - ready to use!
```

## 🧹 Optional: Clean Up Old Branches

Once master is the default, you can optionally delete other branches:

### Delete yishutest branch (optional)

**Locally:**
```bash
git branch -d yishutest
```

**On GitHub:**
```bash
git push origin --delete yishutest
```

### Delete main branch (optional)

**Locally:**
```bash
git branch -d main
```

**On GitHub:**
```bash
git push origin --delete main
```

## ✅ Current Branches

After setting master as default:
- `master` ← Default branch (contains all notification generator code)
- `yishutest` ← Can be deleted if no longer needed
- `main` ← Can be deleted if no longer needed

## 🎯 Recommended: Keep It Clean

For your hackathon project, I recommend:
1. Set master as default ✅
2. Delete yishutest and main branches
3. All teammates work from master

This keeps it simple and follows standard GitHub practices!

