# MailPilot 📧🤖

**An AI-powered email management agent that revolutionizes how you interact with your inbox.**

MailPilot combines the power of Google's Gemini 2.5 Flash AI with Gmail's API to create an intelligent assistant that understands natural language, manages your emails proactively, and helps you stay organized effortlessly.

> **⚠️ Note**: This project requires Google OAuth authentication with Gmail. To try it yourself, you'll need to set up your own Google Cloud project with Gmail API access.
> 
> **📖 [Complete Setup Guide](./DEMO_SETUP.md)** | **🎥 [Demo Video](#-demo-video)** | **� [Screenshots](#-screenshots)**

![MailPilot](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-blue) ![Gmail API](https://img.shields.io/badge/Gmail-API%20Integrated-red) ![Next.js](https://img.shields.io/badge/Next.js-15-black) ![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)

---

## 🌟 What is MailPilot?

MailPilot is not just another email client. It's an **intelligent email assistant** that:

- 🧠 **Understands Natural Language** - Talk to your emails like you talk to a person
- 🤖 **AI-Powered Actions** - Automatically categorizes, summarizes, and prioritizes your inbox
- ⚡ **Smart Responses** - Drafts context-aware replies based on email content
- 📊 **Intelligent Insights** - Extracts deadlines, action items, and key information
- 🔄 **Workflow Automation** - Handles repetitive tasks like archiving, starring, and organizing
- 🎯 **Proactive Monitoring** - Alerts you to urgent emails and important updates

Instead of manually sorting through hundreds of emails, MailPilot lets you simply ask:
- *"Show me unread emails from this week"*
- *"Summarize my inbox"*
- *"Draft a reply to John's meeting request"*
- *"Find all emails with deadlines"*
- *"Archive all newsletters"*

---

## ✨ Key Features

### 🎯 Natural Language Interface
Interact with your emails using conversational commands. No complex filters or rules required.

### 📧 Smart Email Management
- **Read & Parse** - Beautiful, formatted email viewing
- **Categorize** - Automatic classification (Work, Personal, Newsletter, Important)
- **Summarize** - AI-generated summaries of long email threads
- **Search** - Intelligent semantic search beyond keywords

### ✍️ AI-Powered Composition
- **Draft Replies** - Context-aware email responses
- **Templates** - Learn your writing style and preferences
- **Tone Adjustment** - Professional, casual, or formal tones

### 📅 Smart Organization
- **Deadline Extraction** - Automatically finds dates and action items
- **Priority Detection** - Identifies urgent emails
- **Auto-Archive** - Cleans up newsletters and promotions
- **Smart Labels** - Intelligent tagging and categorization

### 🔄 Workflow Automation
- **Multi-Step Tasks** - Execute complex email workflows
- **Batch Operations** - Handle multiple emails at once
- **Task Planning** - Break down complex requests into steps
- **Memory System** - Remembers your preferences and patterns

### 🎨 Beautiful UI
- Modern, responsive design
- Interactive email cards
- One-click actions (Read, Archive, Star)
- Real-time updates

---

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Modern, responsive styling
- **Axios** - HTTP client for API calls

**Backend:**
- **FastAPI** - High-performance Python API framework
- **Google Gemini 2.5 Flash** - Advanced LLM for understanding and generation
- **Gmail API** - Secure email access via OAuth 2.0
- **Supabase** - PostgreSQL database for user data and chat history

**AI & Intelligence:**
- **Agent System** - Autonomous task execution
- **Memory Management** - User preference tracking
- **Task Planning** - Multi-step workflow orchestration
- **Proactive Monitoring** - Background email analysis

---

## 🚀 How It Works

1. **Authentication** - Secure OAuth 2.0 with Google Gmail
2. **Natural Language Processing** - Gemini AI understands your intent
3. **Function Calling** - AI determines which email operations to perform
4. **Gmail API Execution** - Actions are executed on your actual inbox
5. **Smart Response** - Results formatted and presented beautifully
6. **Learning** - System remembers your preferences over time

---

## 💡 Use Cases

### For Professionals
- Quickly triage morning inbox
- Find all emails mentioning specific projects
- Auto-respond to meeting requests
- Track action items across email threads

### For Busy Individuals
- Clean up promotional emails automatically
- Never miss important deadlines
- Generate quick summaries of long conversations
- Smart prioritization of what needs attention

### For Teams
- Share email insights and summaries
- Collaborative inbox management
- Consistent response templates
- Automated workflow triggers

---

## 🎯 Example Commands

```
"Show me unread emails from last week"
"Summarize the email thread with Sarah about the project"
"Draft a professional reply declining the meeting"
"Find all emails with attachments from John"
"Archive all emails from newsletters@example.com"
"Star all emails mentioning 'urgent' or 'deadline'"
"Extract all action items from today's emails"
"Check for urgent emails that need my attention"
"Generate a daily digest of important emails"
```

---

## 📸 Screenshots

### 🏠 Dashboard - Natural Language Email Management
<div align="center">
  <img src="./assets/screenshots/dashboard.png" alt="MailPilot Dashboard" width="900"/>
  <p><i>Interactive dashboard with AI assistant chat and real-time email sidebar</i></p>
</div>

**Features shown:**
- 💬 Natural language chat interface
- 📧 Live email inbox sidebar
- 🎯 Quick action suggestions
- ⚡ Real-time email updates

---

### 📖 Beautiful Email Reading Experience
<div align="center">
  <img src="./assets/screenshots/email-read.png" alt="Email Reading View" width="900"/>
  <p><i>Beautifully formatted emails with gradient headers and action buttons</i></p>
</div>

**Features shown:**
- 🎨 Clean, formatted email display
- 📅 Smart date formatting
- 🔗 Clickable links
- ✍️ Draft Reply & Summarize buttons

---

### 📋 Smart Email Lists
<div align="center">
  <img src="./assets/screenshots/email-list.png" alt="Email List Cards" width="900"/>
  <p><i>Email lists displayed as interactive cards with instant actions</i></p>
</div>

**Features shown:**
- 🃏 Card-based email display
- 📖 Read, 📦 Archive, ⭐ Star buttons
- 📱 Responsive design
- 🎯 Sender and subject highlights

---

### 🤖 AI-Powered Features
<div align="center">
  <img src="./assets/screenshots/ai-response.png" alt="AI Features" width="900"/>
  <p><i>Intelligent email summaries, deadline extraction, and smart suggestions</i></p>
</div>

**AI Capabilities:**
- 📝 Email summarization
- 📅 Deadline extraction
- ✍️ Context-aware reply drafting
- 🏷️ Auto-categorization
- ⚠️ Urgent email detection

> **📝 Note**: Add your screenshots to `./assets/screenshots/` folder. See [assets/README.md](./assets/README.md) for guidelines.

---

## 🎬 Demo Video

> **📹 Add your demo video**: Place `demo-video.mp4` in `./assets/demo/` folder
> 
> ### What to Show in Your Demo:
> 1. **OAuth Authentication** - Secure Gmail sign-in (3 sec)
> 2. **Natural Language Queries** - "Show me unread emails" (5 sec)
> 3. **Email Reading** - Beautiful formatted view (5 sec)
> 4. **AI Actions** - Summaries, replies, smart organization (10 sec)
> 5. **One-Click Operations** - Archive, star, manage emails (5 sec)
> 6. **Send Email** - "Send email to..." command (5 sec)
> 
> **Duration**: 30-60 seconds | **Format**: MP4 | **Resolution**: 1280x720 or 1920x1080

**See [assets/README.md](./assets/README.md) for video recording guidelines.**

---

## 🔐 Security & Privacy

- **OAuth 2.0** - Industry-standard secure authentication
- **No Password Storage** - Credentials never stored locally
- **Token Management** - Secure, encrypted token storage
- **User Control** - All actions require confirmation for destructive operations
- **Privacy First** - Your emails stay in your Gmail account
- **Open Source** - Transparent codebase for security review

---

## 🛠️ Quick Start

> **👥 For Visitors**: This project requires your own Gmail OAuth setup. Follow the instructions below to deploy your own instance!
> 
> **🚀 For Developers**: Clone, configure, and deploy in under 10 minutes!

### Prerequisites
- Node.js 18+ and Python 3.11+
- Gmail account
- Google Cloud Project with Gmail API enabled
- Supabase account (free tier)
- Gemini API key (free tier available)
- Supabase account
- Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ShaaktShrivastava/Mail-Bot.git
cd Mail-Bot
```

2. Set up environment variables (see `.env.example`)

3. Install dependencies:
```bash
# Frontend
cd frontend && npm install

# Backend
cd backend && pip install -r requirements.txt
```

4. Run development servers:
```bash
# Frontend
npm run dev

# Backend
uvicorn app:app --reload
```

---

## 🤝 Contributing

We welcome contributions! Whether it's:
- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🎨 UI/UX enhancements

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](./LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini** - Advanced AI capabilities
- **Gmail API** - Secure email access
- **Next.js & FastAPI** - Modern frameworks
- **Supabase** - Backend infrastructure

---

## 🌐 Links

- **Live Demo**: [MailPilot](https://mail-bot-git-main-shaakt.vercel.app)
- **GitHub**: [Repository](https://github.com/ShaaktShrivastava/Mail-Bot)

---

**Built with ❤️ by developers who understand email overload**
