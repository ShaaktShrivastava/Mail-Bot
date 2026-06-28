# MailPilot 📧🤖

**AI-powered email management agent that understands natural language and manages your Gmail inbox intelligently.**

![MailPilot](https://img.shields.io/badge/AI-Gemini%202.5%20Flash--Lite-blue) ![Gmail API](https://img.shields.io/badge/Gmail-API-red) ![Next.js](https://img.shields.io/badge/Next.js-15-black) ![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)

> **🚀 [Live Demo](https://mail-bot-git-main-shaakt.vercel.app)**

---

## 🌟 What is MailPilot?

MailPilot is an intelligent email assistant that lets you manage your Gmail inbox using natural language. Instead of clicking through menus, simply tell MailPilot what you want:

- *"Show me unread emails from this week"*
- *"Summarize my inbox"*
- *"Send email to john@example.com saying hello"*
- *"Archive all newsletters"*
- *"Find emails with deadlines"*

**Powered by Google Gemini 2.5 Flash-Lite** (`gemini-2.5-flash-lite`) + **Gmail API** + **Next.js 15** + **FastAPI**

---

## ✨ Key Features

🧠 **Natural Language Interface** — Talk to your emails conversationally  
📧 **Smart Email Management** — Read, search, categorize, and organize  
✍️ **AI-Powered Composition** — Draft context-aware replies instantly  
📅 **Intelligent Organization** — Auto-extract deadlines and action items  
⚡ **One-Click Actions** — Archive, star, delete with beautiful UI  
🔄 **Workflow Automation** — Handle complex multi-step tasks  

---

## 📸 Screenshots

<div align="center">

### Dashboard
<img src="./assets/screenshots/dashboard.png" alt="Dashboard" width="800"/>

### Email Reading
<img src="./assets/screenshots/email-read.png" alt="Email Reading" width="800"/>

### Email List Cards
<img src="./assets/screenshots/email-list.png" alt="Email List" width="800"/>

### AI Features
<img src="./assets/screenshots/ai-response.png" alt="AI Response" width="800"/>

</div>

---

## 🎬 Demo Video

<div align="center">

**[📥 Download Demo Video](./assets/demo/demo-video.mp4)**

</div>

> **💡 Tip:** GitHub doesn't play videos inline. Click the link above to download and watch the demo.

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, TypeScript, Tailwind CSS |
| Backend | FastAPI (Python 3.11), Uvicorn |
| AI Model | Google Gemini 2.5 Flash-Lite (`gemini-2.5-flash-lite`) |
| Auth | Google OAuth 2.0 + JWT |
| Database | Supabase (PostgreSQL) |
| APIs | Gmail API, Gemini AI API |
| Hosting | Vercel (frontend) + Render (backend) |

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and Python 3.11+
- [Google Cloud Project](https://console.cloud.google.com) with Gmail API enabled
- [Supabase account](https://supabase.com) (free tier works)
- [Gemini API key](https://aistudio.google.com/app/apikey) (free tier works)

### 1. Clone the repository

```bash
git clone https://github.com/ShaaktShrivastava/Mail-Bot.git
cd Mail-Bot
```

### 2. Set up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com) → **APIs & Services** → **Credentials**
2. Create an **OAuth 2.0 Client ID** (Web application type)
3. Add authorized redirect URI: `http://localhost:3000/auth` (and your Vercel URL for production)
4. Enable these APIs: **Gmail API**, **Google People API**
5. In **OAuth consent screen**, add the scope: `https://www.googleapis.com/auth/gmail.modify`
6. If the app is in **Testing** mode, add your Gmail address as a test user
7. Save your **Client ID** and **Client Secret**

### 3. Set up Supabase

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to **SQL Editor** and run the full schema:

```bash
# Run the provided schema file in your Supabase SQL editor
supabase/schema.sql
```

The schema creates 4 tables with indexes and Row Level Security:
- `users` — stores Gmail OAuth tokens
- `chat_history` — conversation history per user
- `email_cache` — optional cache for faster email loading
- `agent_memory` — persistent agent preferences per user

### 4. Configure environment variables

**Backend** — copy and fill in `backend/.env.example` → `backend/.env`:

```env
GEMINI_API_KEY=your-gemini-api-key
LLM_MODEL=gemini-2.5-flash-lite
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
JWT_SECRET=your-long-random-secret-key
GOOGLE_CLIENT_ID=your-google-oauth-client-id
GOOGLE_CLIENT_SECRET=your-google-oauth-client-secret
GOOGLE_REDIRECT_URI=http://localhost:3000/auth
```

**Frontend** — copy and fill in `frontend/.env.local.example` → `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-oauth-client-id
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
```

> **Note:** Use the **service role key** (from Supabase Settings → API) for `SUPABASE_KEY` in the backend, and the **anon/public key** for `NEXT_PUBLIC_SUPABASE_ANON_KEY` in the frontend.

### 5. Install and run

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
# Runs on http://localhost:8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
# Runs on http://localhost:3000
```

Open `http://localhost:3000` and sign in with Gmail.

---

## 🚢 Deployment

### Frontend → Vercel

1. Push to GitHub and import the repo in [Vercel](https://vercel.com)
2. Set **Root Directory** to `frontend`
3. Add all `NEXT_PUBLIC_*` environment variables, pointing `NEXT_PUBLIC_API_URL` at your Render backend URL

### Backend → Render

1. Create a new **Web Service** in [Render](https://render.com)
2. Set **Root Directory** to `backend`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Add all environment variables from `backend/.env.example`
6. Update `GOOGLE_REDIRECT_URI` to your production Vercel URL (e.g. `https://your-app.vercel.app/auth`)

> The `backend/render.yaml` file pre-configures all required env vars for Render's Blueprint deployment.

---

## 💡 Example Commands

```
"Show me emails"
"Show me unread emails"
"Summarize my inbox"
"Send email to test@example.com saying Hello!"
"Search for emails about the project"
"Find emails with attachments"
"Archive email ID xyz123"
"Delete email ID xyz123"
"Star email ID xyz123"
"Check urgent emails"
"Generate daily digest"
"My name is Alex"
```

---

## 🔐 Security & Privacy

✅ OAuth 2.0 secure authentication — no passwords stored  
✅ Gmail tokens encrypted and stored per-user in Supabase  
✅ Row Level Security (RLS) on all database tables  
✅ Your emails stay in your Gmail account — MailPilot never stores email content  
✅ Open source — fully transparent codebase  

> **For production:** Set `allow_origins` in `backend/app.py` to your specific Vercel domain instead of `"*"`.

---

## 📁 Project Structure

```
Mail-Bot/
├── backend/               # FastAPI Python backend
│   ├── app.py             # API routes
│   ├── agent.py           # Gemini AI agent (gemini-2.5-flash-lite)
│   ├── agent_memory.py    # User preference memory
│   ├── agent_planner.py   # Multi-step task planner
│   ├── gmail_client.py    # Gmail API wrapper
│   ├── proactive_agent.py # Proactive email monitoring
│   ├── requirements.txt   # Python dependencies
│   └── render.yaml        # Render deployment config
├── frontend/              # Next.js 15 frontend
│   └── app/
│       ├── page.tsx       # Main chat interface
│       ├── auth/          # Google OAuth callback
│       └── landing/       # Landing page
├── supabase/
│   └── schema.sql         # Full database schema with RLS
└── assets/
    ├── screenshots/       # App screenshots
    └── demo/              # Demo video
```

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- 🐛 Report bugs via GitHub Issues
- ✨ Suggest features
- 📝 Improve documentation
- 🎨 Enhance the UI

---

## 📝 License

MIT License — see [LICENSE](./LICENSE) for details.

---

## 🙏 Acknowledgments

Built with: Google Gemini AI · Gmail API · Next.js · FastAPI · Supabase

---

**Built with ❤️ for developers tired of email overload**

[⭐ Star this repo](https://github.com/ShaaktShrivastava/Mail-Bot) if you find it useful!
