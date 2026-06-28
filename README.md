# MailPilot 📧🤖

**AI-powered email management agent that understands natural language and manages your Gmail inbox intelligently.**

![MailPilot](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-blue) ![Gmail API](https://img.shields.io/badge/Gmail-API-red) ![Next.js](https://img.shields.io/badge/Next.js-15-black) ![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)

> **🚀 [Live Demo](https://mail-bot-git-main-shaakt.vercel.app)** | **📖 [Setup Guide](./DEMO_SETUP.md)**

---

## 🌟 What is MailPilot?

MailPilot is an intelligent email assistant that lets you manage your Gmail inbox using natural language. Instead of clicking through menus, simply tell MailPilot what you want:

- *"Show me unread emails from this week"*
- *"Summarize my inbox"*
- *"Send email to john@example.com saying hello"*
- *"Archive all newsletters"*
- *"Find emails with deadlines"*

**Powered by Google Gemini 2.5 Flash AI** + **Gmail API** + **Next.js** + **FastAPI**

---

## ✨ Key Features

🧠 **Natural Language Interface** - Talk to your emails conversationally  
📧 **Smart Email Management** - Read, search, categorize, and organize  
✍️ **AI-Powered Composition** - Draft context-aware replies instantly  
📅 **Intelligent Organization** - Auto-extract deadlines and action items  
⚡ **One-Click Actions** - Archive, star, delete with beautiful UI  
🔄 **Workflow Automation** - Handle complex multi-step tasks  

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
  <video width="800" controls>
    <source src="./assets/demo/demo-video.mp4" type="video/mp4">
    <a href="./assets/demo/demo-video.mp4">Download Demo Video</a>
  </video>
</div>

> **📹 Can't play video?** [Download it here](./assets/demo/demo-video.mp4)

---

## 🏗️ Tech Stack

**Frontend:** Next.js 15, TypeScript, Tailwind CSS  
**Backend:** FastAPI (Python), Google Gemini 2.5 Flash  
**Database:** Supabase (PostgreSQL)  
**APIs:** Gmail API, Gemini AI API  

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and Python 3.11+
- Google Cloud Project with Gmail API enabled
- Supabase account (free tier)
- Gemini API key (free tier)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/ShaaktShrivastava/Mail-Bot.git
cd Mail-Bot
```

2. **Set up environment variables:**

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-key
```

**Backend** (`backend/.env`):
```env
GEMINI_API_KEY=your-gemini-api-key
LLM_MODEL=gemini-2.5-flash-lite
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:3000/auth
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
JWT_SECRET=your-secret-key
```

3. **Install dependencies:**
```bash
# Frontend
cd frontend && npm install

# Backend
cd backend && pip install -r requirements.txt
```

4. **Run development servers:**
```bash
# Frontend (in frontend folder)
npm run dev

# Backend (in backend folder)
uvicorn app:app --reload
```

5. **Open** `http://localhost:3000` and sign in with Gmail!

📖 **Detailed setup guide:** [DEMO_SETUP.md](./DEMO_SETUP.md)

---

## 💡 Example Commands

```
"Show me emails from last week"
"Summarize my inbox"
"Send email to test@example.com saying Hello!"
"Search for emails about the project"
"Archive email ID xyz123"
"Check urgent emails"
"Generate daily digest"
"Find emails with attachments"
```

---

## 🔐 Security & Privacy

✅ OAuth 2.0 secure authentication  
✅ No password storage  
✅ Encrypted token management  
✅ Your emails stay in your Gmail account  
✅ Open source - transparent codebase  

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- 🐛 Report bugs
- ✨ Suggest features
- 📝 Improve documentation
- 🎨 Enhance UI/UX

---

## 📝 License

MIT License - see [LICENSE](./LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with: Google Gemini AI • Gmail API • Next.js • FastAPI • Supabase

---

**Built with ❤️ for developers tired of email overload**

[⭐ Star this repo](https://github.com/ShaaktShrivastava/Mail-Bot) if you find it useful!
