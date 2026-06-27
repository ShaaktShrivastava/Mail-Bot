"""FastAPI Backend for MailPilot"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
from agent import MailPilotAgent
from supabase import create_client, Client
import jwt
from datetime import datetime, timedelta

load_dotenv()

app = FastAPI(title="MailPilot API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Request models
class EmailRequest(BaseModel):
    to: str
    subject: str
    body: str

class QueryRequest(BaseModel):
    query: str
    max_results: Optional[int] = 10

class UserQuery(BaseModel):
    message: str
    user_id: str

class AuthRequest(BaseModel):
    email: str
    gmail_token: dict

# Response models
class EmailResponse(BaseModel):
    id: str
    from_email: str
    subject: str
    date: str
    snippet: str

# Initialize agent per user
agents = {}

def get_agent(user_id: str) -> MailPilotAgent:
    """Get or create agent for user."""
    if user_id not in agents:
        agents[user_id] = MailPilotAgent()
    return agents[user_id]

@app.get("/")
def root():
    return {"message": "MailPilot API", "version": "1.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/auth/login")
async def login(auth_req: AuthRequest):
    """Authenticate user and save Gmail token."""
    try:
        # Save user to Supabase
        user_data = {
            "email": auth_req.email,
            "gmail_token": auth_req.gmail_token,
            "created_at": datetime.now().isoformat()
        }
        
        result = supabase.table("users").upsert(user_data).execute()
        
        # Generate JWT token
        token = jwt.encode(
            {"email": auth_req.email, "exp": datetime.utcnow() + timedelta(days=30)},
            os.getenv("JWT_SECRET", "your-secret-key"),
            algorithm="HS256"
        )
        
        return {"token": token, "user": result.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/emails/list")
async def list_emails(query_req: QueryRequest):
    """List emails."""
    try:
        agent = MailPilotAgent()
        result = agent.list_emails(query=query_req.query, max_results=query_req.max_results)
        return {"emails": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/emails/send")
async def send_email(email_req: EmailRequest):
    """Send an email."""
    try:
        agent = MailPilotAgent()
        # Note: Bypassing confirmation for API
        result = agent.gmail.send_message(email_req.to, email_req.subject, email_req.body)
        
        if result:
            return {"success": True, "message": "Email sent successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/emails/{email_id}")
async def read_email(email_id: str):
    """Read a specific email."""
    try:
        agent = MailPilotAgent()
        result = agent.read_email(email_id)
        return {"email": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/emails/{email_id}/archive")
async def archive_email(email_id: str):
    """Archive an email."""
    try:
        agent = MailPilotAgent()
        result = agent.archive_email(email_id)
        return {"success": True, "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/emails/{email_id}/star")
async def star_email(email_id: str):
    """Star an email."""
    try:
        agent = MailPilotAgent()
        result = agent.star_email(email_id, star=True)
        return {"success": True, "message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/emails/{email_id}/delete")
async def delete_email(email_id: str):
    """Delete an email."""
    try:
        agent = MailPilotAgent()
        result = agent.gmail.trash_message(email_id)
        return {"success": result, "message": "Email deleted" if result else "Failed to delete"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent/query")
async def agent_query(query: UserQuery):
    """Process natural language query through agent."""
    try:
        agent = get_agent(query.user_id)
        result = agent.process_request(query.message)
        
        # Save to history in Supabase
        supabase.table("chat_history").insert({
            "user_id": query.user_id,
            "message": query.message,
            "response": result,
            "timestamp": datetime.now().isoformat()
        }).execute()
        
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/emails/summarize")
async def summarize_emails(query_req: QueryRequest):
    """Get email summary."""
    try:
        agent = MailPilotAgent()
        result = agent.get_email_summary(query=query_req.query, max_emails=query_req.max_results)
        return {"summary": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/emails/urgent")
async def check_urgent():
    """Check for urgent emails."""
    try:
        agent = MailPilotAgent()
        result = agent.check_urgent_emails()
        return {"urgent_emails": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/digest/daily")
async def daily_digest():
    """Generate daily digest."""
    try:
        agent = MailPilotAgent()
        result = agent.generate_daily_digest()
        return {"digest": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
