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

class GoogleAuthRequest(BaseModel):
    code: str
    redirect_uri: Optional[str] = None

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

@app.post("/api/auth/google")
async def google_auth(auth_req: GoogleAuthRequest):
    """Handle Google OAuth callback."""
    try:
        print(f"Received auth request with code: {auth_req.code[:20]}...")
        
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import Flow
        import json
        
        # Get environment variables
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        # Use redirect_uri from request, fallback to env var
        redirect_uri = auth_req.redirect_uri or os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:3000/auth")
        
        print(f"Using client_id: {client_id[:20] if client_id else 'MISSING'}...")
        print(f"Using redirect_uri: {redirect_uri}")
        
        if not client_id or not client_secret:
            raise HTTPException(status_code=500, detail="Missing Google OAuth credentials in environment")
        
        # Create client config from environment variables
        client_config = {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }
        
        print("Creating OAuth flow...")
        # Exchange authorization code for tokens
        flow = Flow.from_client_config(
            client_config,
            scopes=['https://www.googleapis.com/auth/gmail.modify'],
            redirect_uri=redirect_uri
        )
        
        print("Fetching token...")
        flow.fetch_token(code=auth_req.code)
        credentials = flow.credentials
        
        print("Getting user profile...")
        # Get user email from token
        from googleapiclient.discovery import build
        service = build('gmail', 'v1', credentials=credentials)
        profile = service.users().getProfile(userId='me').execute()
        email = profile['emailAddress']
        
        print(f"User authenticated: {email}")
        
        # Save user to Supabase
        user_data = {
            "email": email,
            "gmail_token": {
                "token": credentials.token,
                "refresh_token": credentials.refresh_token,
                "token_uri": credentials.token_uri,
                "client_id": credentials.client_id,
                "client_secret": credentials.client_secret,
                "scopes": list(credentials.scopes) if credentials.scopes else []
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        print(f"Saving user to Supabase: {email}")
        result = supabase.table("users").upsert(user_data, on_conflict="email").execute()
        print(f"User saved successfully")
        
        # Generate JWT token
        token = jwt.encode(
            {"email": email, "exp": datetime.utcnow() + timedelta(days=30)},
            os.getenv("JWT_SECRET", "your-secret-key"),
            algorithm="HS256"
        )
        
        return {"token": token, "user": {"email": email, "id": email}}
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"Auth error: {error_detail}")
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")

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
        # This endpoint needs authentication - should be called from agent
        raise HTTPException(status_code=400, detail="Please use /api/agent/query endpoint with natural language")
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
        print(f"Agent query from user: {query.user_id}")
        print(f"Supabase URL: {os.getenv('SUPABASE_URL')}")
        
        # Get user's gmail token from Supabase
        user_data = supabase.table("users").select("*").eq("email", query.user_id).execute()
        
        print(f"Supabase response: {user_data}")
        
        if not user_data.data:
            raise HTTPException(status_code=401, detail="User not authenticated. Please sign in first.")
        
        gmail_token = user_data.data[0].get('gmail_token')
        if not gmail_token:
            raise HTTPException(status_code=401, detail="Gmail not connected. Please authenticate with Gmail.")
        
        # Create agent with user's Gmail credentials
        agent = MailPilotAgent(gmail_credentials=gmail_token)
        
        result = agent.process_request(query.message)
        
        # Save to history in Supabase
        try:
            supabase.table("chat_history").insert({
                "user_id": query.user_id,
                "message": query.message,
                "response": result,
                "timestamp": datetime.now().isoformat()
            }).execute()
        except:
            pass  # Don't fail if chat history save fails
        
        return {"response": result}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Query error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

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
