# 🚀 MailPilot Setup Guide

Complete guide to set up your own MailPilot instance.

---

## 📋 Prerequisites

- **Node.js 18+** and **Python 3.11+**
- **Google Cloud Project** (free)
- **Supabase Account** (free tier)
- **Gemini API Key** (free tier)

---

## 1️⃣ Google Cloud Setup (Gmail API + OAuth)

### Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project
3. Enable **Gmail API**
4. Go to **APIs & Services** → **Credentials**
5. Create **OAuth 2.0 Client ID** (Web application)
6. Add authorized redirect URIs:
   - `http://localhost:3000/auth` (development)
   - `https://your-app.vercel.app/auth` (production)
7. Save **Client ID** and **Client Secret**

---

## 2️⃣ Gemini API Setup

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **Get API Key**
3. Copy your API key

**Free Tier Models (2026):**
- `gemini-2.5-flash-lite` - 1,000 requests/day (recommended)
- `gemini-3.5-flash` - Good performance
- `gemini-2.5-flash` - 250 requests/day

---

## 3️⃣ Supabase Setup

1. Go to [Supabase](https://supabase.com)
2. Create new project
3. Go to **SQL Editor** and run:

```sql
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    gmail_token JSONB,
    preferences JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chat_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

4. Go to **Project Settings** → **API**
5. Copy **Project URL** and **Anon Key**

---

## 4️⃣ Environment Variables

### Frontend `.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
```

### Backend `.env`

```env
GEMINI_API_KEY=your-gemini-api-key
LLM_MODEL=gemini-2.5-flash-lite
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:3000/auth
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your-supabase-anon-key
JWT_SECRET=your-random-32-char-string
```

---

## 5️⃣ Local Development

```bash
# Clone repository
git clone https://github.com/ShaaktShrivastava/Mail-Bot.git
cd Mail-Bot

# Frontend setup
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with your keys
npm run dev

# Backend setup (new terminal)
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
uvicorn app:app --reload
```

Open `http://localhost:3000` and sign in!

---

## 6️⃣ Production Deployment

### Deploy Frontend to Vercel

1. Push code to GitHub
2. Go to [Vercel](https://vercel.com)
3. Import your repository
4. Add environment variables (same as `.env.local`)
5. Deploy!

### Deploy Backend to Render

1. Go to [Render](https://render.com)
2. Create **Web Service** from GitHub
3. Select `backend` folder as root directory
4. Add environment variables (same as `.env`)
5. Deploy!

### Update OAuth Redirect URI

After deployment, add production URL to Google Cloud OAuth:
- `https://your-app.vercel.app/auth`

---

## 🧪 Testing Commands

After setup, try these:

```
show me emails
send email to test@example.com saying Hello!
summarize my inbox
search for emails about project
```

---

## 🆘 Troubleshooting

### "User not authenticated"
→ Sign in with Gmail first

### "Rate limit exceeded"
→ Using free tier? Wait 1 minute between commands  
→ Switch to `gemini-2.5-flash-lite` model

### "Gmail not connected"
→ Check OAuth credentials are correct  
→ Verify redirect URI matches exactly

### Frontend won't load
→ Check `NEXT_PUBLIC_API_URL` points to backend  
→ Verify backend is running on port 8000

---

## 📚 Resources

- [Gmail API Docs](https://developers.google.com/gmail/api)
- [Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Next.js Docs](https://nextjs.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)

---

**Need help?** [Open an issue](https://github.com/ShaaktShrivastava/Mail-Bot/issues)
