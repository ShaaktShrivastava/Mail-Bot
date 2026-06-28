# 🎥 Setting Up Your Own MailPilot Demo

Since MailPilot requires OAuth authentication with Gmail, you'll need to set up your own instance to try it. Don't worry - it's free and takes about 10 minutes!

---

## ⚡ Quick Deploy (Recommended)

### Option 1: Deploy to Vercel + Render (Free Tier)

**Frontend (Vercel):**
1. Fork this repository
2. Go to [Vercel](https://vercel.com) and import your fork
3. Add environment variables (see below)
4. Deploy!

**Backend (Render):**
1. Go to [Render](https://render.com)
2. Create a new Web Service from your GitHub repo
3. Select the `backend` folder
4. Add environment variables (see below)
5. Deploy!

---

## 🔑 Required API Keys (All Free Tier)

### 1. Google Cloud (Gmail API + OAuth)

**Cost**: FREE (1 billion requests/day limit)

**Steps**:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Web application)
5. Add authorized redirect URIs:
   - `http://localhost:3000/auth` (for local testing)
   - `https://your-app.vercel.app/auth` (for production)
6. Download credentials and note:
   - Client ID
   - Client Secret

### 2. Google AI Studio (Gemini API)

**Cost**: FREE (Free tier with generous limits)

**Available Free Models (2026)**:
- `gemini-3.5-flash` - Most intelligent speed model (RECOMMENDED)
- `gemini-3.1-flash-lite` - 1,000 requests/day
- `gemini-2.5-flash` - 250 requests/day
- `gemini-2.5-flash-lite` - 1,000 requests/day

**Steps**:
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create API key
3. Copy the key

### 3. Supabase (Database)

**Cost**: FREE (500MB database)

**Steps**:
1. Go to [Supabase](https://supabase.com)
2. Create a new project
3. Go to Project Settings → API
4. Copy:
   - Project URL
   - Anon/Public Key
5. Go to SQL Editor and run:
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

---

## 🌍 Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
```

### Backend (.env or Render Environment)
```env
GEMINI_API_KEY=your-gemini-api-key
LLM_MODEL=gemini-3.5-flash
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=https://your-app.vercel.app/auth
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your-supabase-anon-key
JWT_SECRET=generate-a-random-32-char-string
```

---

## 🧪 Local Development

### 1. Clone the repository
```bash
git clone https://github.com/ShaaktShrivastava/Mail-Bot.git
cd Mail-Bot
```

### 2. Set up backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
uvicorn app:app --reload
```

### 3. Set up frontend
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with your keys
npm run dev
```

### 4. Open browser
Go to `http://localhost:3000` and sign in with your Gmail account!

---

## 🎬 Recording a Demo

Want to contribute a demo video? Here's how:

### Tools:
- **Screen Recording**: OBS Studio (free), Loom, or built-in screen recorder
- **Video Editing**: DaVinci Resolve (free) or iMovie

### What to Show:
1. **Landing page** (2 seconds)
2. **Sign in with Google** (5 seconds)
3. **Dashboard view** (5 seconds)
4. **Type command**: "Show me unread emails" (10 seconds)
5. **Email list cards** (5 seconds)
6. **Click "Read" button** (3 seconds)
7. **Formatted email view** (5 seconds)
8. **Type command**: "Summarize this email" (10 seconds)
9. **AI summary response** (5 seconds)
10. **One-click actions**: Archive, Star (5 seconds)

**Total**: ~60 seconds

### Where to Upload:
- YouTube (unlisted or public)
- GitHub Release
- Submit PR with link in README

---

## 📸 Taking Screenshots

### Recommended Resolution:
- **Desktop**: 1920x1080 (then crop to 900x500)
- **Format**: PNG or WebP

### What to Capture:
1. Dashboard with email sidebar + chat
2. Email reading view with formatted content
3. Email list with cards and buttons
4. AI response showing summary or actions

### Tools:
- **Mac**: Cmd + Shift + 4
- **Windows**: Win + Shift + S
- **Browser Extension**: Awesome Screenshot

---

## 🆘 Need Help?

- **Issues**: [GitHub Issues](https://github.com/ShaaktShrivastava/Mail-Bot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ShaaktShrivastava/Mail-Bot/discussions)
- **Documentation**: See [README.md](./README.md)

---

## 💡 Pro Tips

1. **Use test emails** for screenshots (don't expose personal data)
2. **Create a test Gmail account** for demos
3. **Blur sensitive information** in recordings
4. **Keep videos under 2 minutes** for better engagement
5. **Add captions** to explain what's happening

---

**Happy demoing! 🎉**
