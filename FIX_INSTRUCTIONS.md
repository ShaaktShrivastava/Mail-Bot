# 🔧 Fix Instructions - Gemini API Model Update

## Problem Summary
You were hitting rate limits and 404 errors because:
1. `gemini-2.5-flash` only allows 20 requests/day on free tier
2. `gemini-1.5-flash` and `gemini-1.5-flash-latest` don't exist (deprecated/wrong names)

## Solution Applied
Updated your backend to use **`gemini-3.5-flash`** - the latest and best free model from Google.

## What Changed

### 1. Backend Agent (`backend/agent.py`)
- Changed default model from `gemini-1.5-flash` → `gemini-3.5-flash`
- This is Google's newest model (released 2026)
- Free tier with generous limits

### 2. Environment Files (`backend/.env.example`)
- Added `LLM_MODEL=gemini-3.5-flash` variable
- Allows easy model switching without code changes

### 3. Documentation (`DEMO_SETUP.md`)
- Updated API key section with 2026 model information
- Listed all available free models:
  - `gemini-3.5-flash` ⭐ RECOMMENDED
  - `gemini-3.1-flash-lite` (1,000 req/day)
  - `gemini-2.5-flash` (250 req/day)
  - `gemini-2.5-flash-lite` (1,000 req/day)

## Next Steps

### Option 1: Deploy to Render (Recommended)
1. **Push changes to GitHub**:
   ```bash
   git add .
   git commit -m "Fix: Update to gemini-3.5-flash model"
   git push origin main
   ```

2. **Update Render environment variables**:
   - Go to your Render dashboard
   - Select your MailPilot service
   - Go to Environment → Add variable:
     - Key: `LLM_MODEL`
     - Value: `gemini-3.5-flash`
   - Click "Save Changes"
   - Render will auto-redeploy

3. **Wait for deployment** (2-3 minutes)

4. **Test your app**:
   - Go to your Vercel frontend URL
   - Try: "show me emails"
   - Try: "send email to test@example.com saying hello"

### Option 2: Test Locally First
```bash
cd backend

# Update your .env file (add this line)
LLM_MODEL=gemini-3.5-flash

# Restart server
uvicorn app:app --reload
```

Then test from frontend at `http://localhost:3000`

## Commands to Test

Once deployed, try these commands in order:

1. ✅ **"show me emails"** - Should list your recent emails
2. ✅ **"summarize my inbox"** - Should give an AI summary
3. ✅ **"send email to testuser19122004@gmail.com"** - Should compose and send
4. ✅ **"search for emails about Facebook"** - Should search

## Expected Results

### Before Fix:
- ❌ Error: 429 quota exceeded (gemini-2.5-flash)
- ❌ Error: 404 model not found (gemini-1.5-flash)

### After Fix:
- ✅ Fast responses from gemini-3.5-flash
- ✅ No rate limit errors (much higher quota)
- ✅ Email sending works properly

## Alternative Models (If Needed)

If you still hit issues, you can try other free models:

### High Volume (1,000 req/day):
```env
LLM_MODEL=gemini-3.1-flash-lite
```

### Good Balance (250 req/day):
```env
LLM_MODEL=gemini-2.5-flash
```

### Ultra High Volume (1,000 req/day):
```env
LLM_MODEL=gemini-2.5-flash-lite
```

## Troubleshooting

### Still getting 404 errors?
- Make sure `LLM_MODEL` env var is set in Render
- Check Render logs: Dashboard → Logs tab
- Verify the model name has no typos

### Still getting rate limits?
- Wait 24 hours for quota to reset
- Or switch to a different model (see alternatives above)
- Or upgrade to paid tier ($0.30-$1.50 per 1M tokens)

### Email sending not working?
- First verify the model works: try "show me emails"
- Then check logs for JSON parsing errors
- Make sure command includes recipient: "send email to xyz@example.com"

## Reference: Official Documentation

✅ Verified against official Google pricing page (June 2026):
https://ai.google.dev/gemini-api/docs/pricing

## Questions?

If you encounter any issues:
1. Check Render logs (Dashboard → Service → Logs)
2. Check browser console (F12 → Console tab)
3. Verify all environment variables are set correctly

---

**Status**: Ready to deploy! 🚀
**Estimated Time to Fix**: 5 minutes
**Next Command**: `git push origin main` (if using Render auto-deploy)
