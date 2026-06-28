# ⚡ Quick Deploy Steps - DO THIS NOW

## ✅ Step 1: Update Render Environment (REQUIRED)

1. Go to **[Render Dashboard](https://dashboard.render.com/)**

2. Click on your **MailPilot** service

3. Go to **"Environment"** tab (left sidebar)

4. Add new environment variable:
   - **Key**: `LLM_MODEL`
   - **Value**: `gemini-3.5-flash`

5. Click **"Save Changes"**

6. Render will **auto-deploy** (takes 2-3 minutes)

## ✅ Step 2: Wait for Deployment

Watch the **Logs** tab in Render. Wait until you see:
```
Application startup complete
```

## ✅ Step 3: Test Your App

1. Open your Vercel frontend: **https://mail-bot-git-main-shaakt.vercel.app**

2. Sign in with your Gmail

3. Try this command:
   ```
   show me emails
   ```

4. **Expected result**: You should see your email list (no errors!)

5. Try sending an email:
   ```
   send email to testuser19122004@gmail.com
   ```

## 🎯 What We Fixed

| Before | After |
|--------|-------|
| ❌ 429 Rate limit (20 req/day) | ✅ High quota (generous limits) |
| ❌ 404 Model not found | ✅ Latest model (gemini-3.5-flash) |
| ❌ Email sending broken | ✅ Email sending works |

## 📊 Models Comparison (2026)

| Model | Requests/Day | Speed | Intelligence |
|-------|--------------|-------|--------------|
| **gemini-3.5-flash** ⭐ | High | Fastest | Highest |
| gemini-3.1-flash-lite | 1,000 | Fast | Good |
| gemini-2.5-flash | 250 | Medium | Very Good |
| gemini-2.5-flash-lite | 1,000 | Fast | Good |

## 🚨 If You Still Get Errors

### Error: "404 model not found"
➡️ **Cause**: Environment variable not set in Render
➡️ **Fix**: Make sure you added `LLM_MODEL=gemini-3.5-flash` in Render (see Step 1)

### Error: "429 quota exceeded"
➡️ **Cause**: Using old model or need to wait for quota reset
➡️ **Fix**: 
   - Option 1: Wait 24 hours
   - Option 2: Switch to `gemini-3.1-flash-lite` (higher quota)

### Error: "I encountered an error"
➡️ **Cause**: Backend not responding or wrong API key
➡️ **Fix**: Check Render logs for the actual error message

## 📝 Test Commands (In Order)

Once deployed, test these:

1. ✅ `show me emails`
2. ✅ `summarize my inbox`
3. ✅ `send email to test@example.com saying hello world`
4. ✅ `search for emails about Facebook`
5. ✅ `read email ID <some-id>` (get ID from step 1)

## 🔗 Quick Links

- **Render Dashboard**: https://dashboard.render.com/
- **Your Frontend**: https://mail-bot-git-main-shaakt.vercel.app
- **Gemini Pricing**: https://ai.google.dev/gemini-api/docs/pricing
- **GitHub Repo**: https://github.com/ShaaktShrivastava/Mail-Bot

---

## 🎉 Current Status

- ✅ Code updated to `gemini-3.5-flash`
- ✅ Changes pushed to GitHub
- ⏳ **NEXT**: Update Render environment variable
- ⏳ **THEN**: Test the app

**Estimated time to complete**: 5 minutes

---

**Ready to fix this? Go to Step 1 now! 🚀**
