# MailPilot

AI-powered email management agent built with Gemini AI. Manage your Gmail through natural conversation.

LIVE PROJECT LINK :- [mail-bot-git-main-shaakt.vercel.app](https://mail-bot-git-main-shaakt.vercel.app/)

## Features

- Natural language email control
- AI-powered inbox summaries
- Autonomous email operations
- Smart priority detection
- Memory system that learns preferences
- Multi-step task planning

## Tech Stack

**Frontend:** Next.js 14, TypeScript, Tailwind CSS  
**Backend:** Python 3.11, FastAPI, Gemini AI  
**Database:** PostgreSQL (Supabase)

## Quick Deploy

### 1. Supabase Setup

Create project at supabase.com:
- Run SQL from `supabase/schema.sql`
- Copy Project URL, anon key, and service_role key

### 2. Backend (Render)

Deploy to render.com:
- Root: `backend`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app:app --host 0.0.0.0 --port $PORT`
- Add env vars:
  ```
  GEMINI_API_KEY=your-key
  SUPABASE_URL=your-url
  SUPABASE_KEY=your-service-key
  JWT_SECRET=random-secret
  PYTHON_VERSION=3.11.0
  ```

### 3. Google OAuth

In Google Cloud Console:
- Enable Gmail API
- Create OAuth 2.0 Client ID
- Add redirect: `https://your-app.vercel.app/auth`

### 4. Frontend (Vercel)

Deploy to vercel.com:
- Root: `frontend`
- Add env vars:
  ```
  NEXT_PUBLIC_API_URL=your-render-url
  NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
  NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
  NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
  ```

### 5. Update CORS

Edit `backend/app.py` line 17 with your Vercel URL, then push to redeploy.

## Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
# Create .env with keys
uvicorn app:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
# Create .env.local with keys
npm run dev
```

## Project Structure

```
├── backend/          # FastAPI server
├── frontend/         # Next.js app
├── supabase/         # Database schema
├── agent.py          # AI agent core
├── gmail_client.py   # Gmail API
└── requirements.txt
```

## Commands

```
"Show me unread emails"
"Summarize my inbox"
"Send email to john@example.com"
"Find urgent emails"
"Archive newsletters"
```

## License

MIT
