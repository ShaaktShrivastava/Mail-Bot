"""MailPilot AI Agent with LLM-powered email management."""
import os
import json
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from gmail_client import GmailClient
from agent_memory import AgentMemory
from agent_planner import TaskPlanner
from proactive_agent import ProactiveAgent
from rich.console import Console
from rich.table import Table

console = Console()

class MailPilotAgent:
    def __init__(self, gmail_credentials: Optional[Dict] = None):
        """Initialize agent with optional Gmail credentials from database."""
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model_name = os.getenv('LLM_MODEL', 'gemini-2.5-flash')
        self.gmail = GmailClient(credentials_dict=gmail_credentials)
        self.chat = None
        
        # Agent capabilities
        self.memory = AgentMemory()
        self.model = genai.GenerativeModel(model_name=self.model_name)
        self.planner = TaskPlanner(self.model)
        self.proactive = ProactiveAgent(self.gmail, self.model, self.memory)
        
        # Define function declarations for Gemini
        self.function_declarations = [
            {
                "name": "list_emails",
                "description": "List emails from inbox with optional search query",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "query": {
                            "type": "STRING",
                            "description": "Gmail search query (e.g., 'is:unread', 'from:john@example.com')"
                        },
                        "max_results": {
                            "type": "INTEGER",
                            "description": "Maximum number of emails to retrieve"
                        }
                    }
                }
            },
            {
                "name": "read_email",
                "description": "Read full content of a specific email by ID",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "message_id": {
                            "type": "STRING",
                            "description": "The ID of the email message"
                        }
                    },
                    "required": ["message_id"]
                }
            },
            {
                "name": "send_email",
                "description": "Send an email to a recipient",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "to": {
                            "type": "STRING",
                            "description": "Recipient email address"
                        },
                        "subject": {
                            "type": "STRING",
                            "description": "Email subject"
                        },
                        "body": {
                            "type": "STRING",
                            "description": "Email body content"
                        }
                    },
                    "required": ["to", "subject", "body"]
                }
            },
            {
                "name": "mark_as_read",
                "description": "Mark an email as read",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "message_id": {
                            "type": "STRING",
                            "description": "The ID of the email to mark as read"
                        }
                    },
                    "required": ["message_id"]
                }
            },
            {
                "name": "star_email",
                "description": "Star/unstar an important email",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "message_id": {
                            "type": "STRING",
                            "description": "The ID of the email to star"
                        },
                        "star": {
                            "type": "BOOLEAN",
                            "description": "True to star, False to unstar"
                        }
                    },
                    "required": ["message_id"]
                }
            },
            {
                "name": "delete_email",
                "description": "Permanently delete an email (move to trash)",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "message_id": {
                            "type": "STRING",
                            "description": "The ID of the email to delete"
                        }
                    },
                    "required": ["message_id"]
                }
            },
            {
                "name": "search_emails",
                "description": "Search emails with specific criteria like attachments, date range, keywords",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "search_query": {
                            "type": "STRING",
                            "description": "Search query (e.g., 'has:attachment', 'after:2024/01/01', 'subject:meeting')"
                        },
                        "max_results": {
                            "type": "INTEGER",
                            "description": "Maximum results to return"
                        }
                    },
                    "required": ["search_query"]
                }
            },
            {
                "name": "get_email_summary",
                "description": "Get AI-generated summary of inbox or specific emails",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "query": {
                            "type": "STRING",
                            "description": "Query to filter emails (e.g., 'is:unread', 'from:boss')"
                        },
                        "max_emails": {
                            "type": "INTEGER",
                            "description": "Number of emails to summarize"
                        }
                    }
                }
            },
            {
                "name": "check_urgent_emails",
                "description": "Proactively check for urgent emails needing attention",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {}
                }
            },
            {
                "name": "generate_daily_digest",
                "description": "Generate a daily summary of emails",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {}
                }
            },
            {
                "name": "suggest_actions",
                "description": "Get AI suggestions for what to do with emails",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "message_id": {
                            "type": "STRING",
                            "description": "Email ID to analyze"
                        }
                    },
                    "required": ["message_id"]
                }
            },
            {
                "name": "learn_preference",
                "description": "Remember user preferences for future interactions",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "preference_key": {
                            "type": "STRING",
                            "description": "What to remember"
                        },
                        "preference_value": {
                            "type": "STRING",
                            "description": "The value to remember"
                        }
                    },
                    "required": ["preference_key", "preference_value"]
                }
            },
            {
                "name": "execute_plan",
                "description": "Execute a multi-step plan for complex email tasks",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "task_description": {
                            "type": "STRING",
                            "description": "Description of complex task to execute"
                        }
                    },
                    "required": ["task_description"]
                }
            },
            {
                "name": "archive_email",
                "description": "Archive an email (remove from inbox)",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "message_id": {
                            "type": "STRING",
                            "description": "The ID of the email to archive"
                        }
                    },
                    "required": ["message_id"]
                }
            }
        ]
        
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            tools=self.function_declarations
        )
    
    def list_emails(self, query: str = '', max_results: int = 10) -> str:
        """List emails from Gmail."""
        # Default to inbox if no query specified
        if not query or query.strip() == '':
            query = 'in:inbox'
        
        messages = self.gmail.list_messages(query=query, max_results=max_results)
        
        if not messages:
            return "No emails found matching your criteria."
        
        result = []
        for msg in messages:
            result.append({
                'id': msg['id'],
                'from': msg['from'],
                'subject': msg['subject'],
                'date': msg['date'],
                'snippet': msg['snippet']
            })
        
        return json.dumps(result, indent=2)
    
    def read_email(self, message_id: str) -> str:
        """Read full email content."""
        message = self.gmail.get_message(message_id)
        if not message:
            return "Email not found."
        
        return json.dumps({
            'from': message['from'],
            'subject': message['subject'],
            'date': message['date'],
            'body': message['body']
        }, indent=2)
    
    def draft_reply(self, email_content: str, instructions: str = '') -> str:
        """Use LLM to draft a reply."""
        prompt = f"Draft a professional email reply to the following email:\n\n{email_content}\n\n"
        if instructions:
            prompt += f"Additional instructions: {instructions}\n\n"
        prompt += "Write only the reply body, keep it concise and professional."
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def classify_email(self, email_content: str) -> str:
        """Classify email using LLM."""
        prompt = f"""Classify this email into one of these categories:
- Personal
- Work
- Newsletter
- Promotional
- Important
- Spam

Email content:
{email_content}

Respond with only the category name and a brief reason."""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def extract_deadlines(self, email_content: str) -> str:
        """Extract deadlines from email."""
        prompt = f"""Extract all deadlines, dates, and time-sensitive information from this email.
Format as a list with date and description.

Email content:
{email_content}"""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def archive_email(self, message_id: str) -> str:
        """Archive an email."""
        success = self.gmail.modify_labels(message_id, remove_labels=['INBOX'])
        return "Email archived successfully." if success else "Failed to archive email."
    
    def send_email(self, to: str, subject: str, body: str) -> str:
        """Send an email."""
        console.print(f"[yellow]⚠️  About to send email to: {to}[/yellow]")
        console.print(f"[yellow]Subject: {subject}[/yellow]")
        confirm = console.input("[yellow]Confirm send? (yes/no): [/yellow]")
        
        if confirm.lower() in ['yes', 'y']:
            success = self.gmail.send_message(to, subject, body)
            return "Email sent successfully!" if success else "Failed to send email."
        return "Email send cancelled."
    
    def mark_as_read(self, message_id: str) -> str:
        """Mark email as read."""
        success = self.gmail.modify_labels(message_id, remove_labels=['UNREAD'])
        return "Marked as read." if success else "Failed to mark as read."
    
    def star_email(self, message_id: str, star: bool = True) -> str:
        """Star or unstar an email."""
        if star:
            success = self.gmail.modify_labels(message_id, add_labels=['STARRED'])
            return "Email starred." if success else "Failed to star email."
        else:
            success = self.gmail.modify_labels(message_id, remove_labels=['STARRED'])
            return "Email unstarred." if success else "Failed to unstar email."
    
    def delete_email(self, message_id: str) -> str:
        """Delete an email (move to trash)."""
        console.print(f"[red]⚠️  About to delete email ID: {message_id}[/red]")
        confirm = console.input("[red]Confirm delete? (yes/no): [/red]")
        
        if confirm.lower() in ['yes', 'y']:
            success = self.gmail.trash_message(message_id)
            return "Email deleted." if success else "Failed to delete email."
        return "Delete cancelled."
    
    def search_emails(self, search_query: str, max_results: int = 10) -> str:
        """Search emails with specific criteria."""
        messages = self.gmail.list_messages(query=search_query, max_results=max_results)
        
        if not messages:
            return "No emails found matching your search."
        
        result = []
        for msg in messages:
            result.append({
                'id': msg['id'],
                'from': msg['from'],
                'subject': msg['subject'],
                'date': msg['date'],
                'snippet': msg['snippet']
            })
        
        return json.dumps(result, indent=2)
    
    def get_email_summary(self, query: str = '', max_emails: int = 10) -> str:
        """Get AI summary of emails."""
        if not query:
            query = 'in:inbox'
        
        messages = self.gmail.list_messages(query=query, max_results=max_emails)
        
        if not messages:
            return "No emails to summarize."
        
        # Create summary prompt
        email_list = []
        for msg in messages:
            email_list.append(f"From: {msg['from']}\nSubject: {msg['subject']}\n{msg['snippet']}")
        
        emails_text = "\n\n---\n\n".join(email_list)
        
        prompt = f"""Provide a concise summary of these emails. Group by importance and highlight any action items or deadlines:

{emails_text}"""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def check_urgent_emails(self) -> str:
        """Check for urgent emails."""
        urgent = self.proactive.check_urgent_emails()
        if not urgent:
            return "No urgent emails found."
        
        result = []
        for email in urgent:
            result.append({
                'id': email['id'],
                'from': email['from'],
                'subject': email['subject'],
                'snippet': email['snippet']
            })
            self.memory.track_contact(email['from'])
        
        return f"Found {len(urgent)} urgent emails:\n" + json.dumps(result, indent=2)
    
    def generate_daily_digest(self) -> str:
        """Generate daily digest."""
        return self.proactive.generate_daily_digest()
    
    def suggest_actions(self, message_id: str) -> str:
        """Suggest actions for an email."""
        email = self.gmail.get_message(message_id)
        if not email:
            return "Email not found."
        
        actions = self.proactive.suggest_actions(email)
        return f"Suggested actions: {', '.join(actions)}"
    
    def learn_preference(self, preference_key: str, preference_value: str) -> str:
        """Learn user preference."""
        self.memory.remember_preference(preference_key, preference_value)
        return f"Remembered: {preference_key} = {preference_value}"
    
    def execute_plan(self, task_description: str) -> str:
        """Execute multi-step plan."""
        console.print(f"[cyan]🧠 Planning task: {task_description}[/cyan]")
        
        plan = self.planner.create_plan(task_description)
        if not plan:
            return "Could not create a plan for this task."
        
        console.print(f"[cyan]📋 Created plan with {len(plan)} steps[/cyan]")
        
        results = []
        for i, step in enumerate(plan, 1):
            console.print(f"[yellow]Step {i}/{len(plan)}: {step.get('reasoning', 'Executing...')}[/yellow]")
            
            action = step.get('action')
            params = step.get('parameters', {})
            
            try:
                result = self.execute_function(action, params)
                results.append(f"Step {i} ✓: {result[:100]}...")
                self.memory.log_task(f"{action} - {step.get('reasoning')}", "success")
            except Exception as e:
                error_msg = f"Step {i} ✗: {str(e)}"
                results.append(error_msg)
                console.print(f"[red]{error_msg}[/red]")
        
        return "\n".join(results)
    
    def execute_function(self, function_name: str, arguments: Dict) -> str:
        """Execute a function call."""
        function_map = {
            'list_emails': self.list_emails,
            'read_email': self.read_email,
            'send_email': self.send_email,
            'mark_as_read': self.mark_as_read,
            'star_email': self.star_email,
            'delete_email': self.delete_email,
            'search_emails': self.search_emails,
            'get_email_summary': self.get_email_summary,
            'archive_email': self.archive_email,
            'draft_reply': self.draft_reply,
            'classify_email': self.classify_email,
            'extract_deadlines': self.extract_deadlines,
            'check_urgent_emails': self.check_urgent_emails,
            'generate_daily_digest': self.generate_daily_digest,
            'suggest_actions': self.suggest_actions,
            'learn_preference': self.learn_preference,
            'execute_plan': self.execute_plan
        }
        
        func = function_map.get(function_name)
        if func:
            result = func(**arguments)
            # Log task execution
            self.memory.log_task(function_name, "success")
            return result
        return f"Unknown function: {function_name}"
    
    def process_request(self, user_input: str) -> str:
        """Process user request using Gemini with function calling."""
        # Check if this needs planning
        if self.planner.should_plan(user_input):
            console.print("[cyan]🤖 This looks like a complex task, creating a plan...[/cyan]")
            return self.execute_plan(user_input)
        
        # Use simpler approach without automatic function calling
        try:
            # Check for keywords that indicate function calls needed
            user_lower = user_input.lower()
            
            if 'show' in user_lower or 'list' in user_lower or 'display' in user_lower:
                if 'unread' in user_lower:
                    return self.list_emails(query='is:unread')
                elif 'urgent' in user_lower:
                    return self.check_urgent_emails()
                else:
                    return self.list_emails()
            
            elif 'summarize' in user_lower or 'summary' in user_lower:
                if 'daily' in user_lower or 'digest' in user_lower:
                    return self.generate_daily_digest()
                else:
                    return self.get_email_summary()
            
            elif 'search' in user_lower or 'find' in user_lower:
                # Extract search terms
                query = user_input.replace('search', '').replace('find', '').strip()
                return self.search_emails(query)
            
            elif 'my name is' in user_lower or 'remember my name' in user_lower or 'set my name' in user_lower:
                # Extract name
                name = user_input.lower().replace('my name is', '').replace('remember my name', '').replace('set my name', '').replace('to', '').strip()
                if name:
                    self.memory.remember_preference('user_name', name.title())
                    return f"✓ I'll remember your name as {name.title()} for email signatures."
                return "Please tell me your name. Say: 'My name is [Your Name]'"
            
            elif 'send' in user_lower or 'email to' in user_lower or 'write to' in user_lower or 'compose' in user_lower:
                console.print("[cyan]📧 Preparing to send email...[/cyan]")
                
                # Get user's email for signature
                user_email = self.memory.get_preference('user_email', 'User')
                user_name = self.memory.get_preference('user_name', 'MailPilot User')
                
                # Use LLM to extract and generate email details
                prompt = f"""You are drafting a professional email. Extract details and create a complete, well-formatted email.

Request: {user_input}

Create a JSON with:
- to: recipient email address (extract from request)
- subject: appropriate email subject (extract or generate based on context)
- body: complete professional email body with:
  * Greeting (Dear/Hi [Name] or Hello,)
  * Main message content (if provided, use it; if not, create a brief professional message)
  * Professional closing
  * Signature with sender name "{user_name}"

IMPORTANT: If the user provides minimal information (like just "send email to xyz@example.com"), 
create a simple, friendly test message.

Example format:
{{
  "to": "john@example.com",
  "subject": "Hello from MailPilot",
  "body": "Hi,\\n\\nThis is a test email sent via MailPilot.\\n\\nBest regards,\\n{user_name}"
}}

Return ONLY the JSON object, no other text.

JSON:"""
                
                response = self.model.generate_content(prompt)
                email_text = response.text.strip()
                
                # Clean up response
                if '```json' in email_text:
                    email_text = email_text.split('```json')[1].split('```')[0]
                elif '```' in email_text:
                    email_text = email_text.split('```')[1].split('```')[0]
                
                email_text = email_text.strip()
                
                try:
                    email_data = json.loads(email_text)
                    to = email_data.get('to', '').strip()
                    subject = email_data.get('subject', '').strip()
                    body = email_data.get('body', '').strip()
                    
                    # Validate
                    if not to or '@' not in to:
                        return "❌ I couldn't find a valid recipient email address. Please specify an email like:\n• 'Send email to john@example.com'\n• 'Send email to john@example.com saying Hello!'\n• 'Email john@example.com with subject Test'"
                    
                    if not subject:
                        subject = "Hello from MailPilot"
                    
                    if not body:
                        body = f"Hi,\n\nThis is a test email sent via MailPilot.\n\nBest regards,\n{user_name}"
                    
                    # Ensure proper signature if missing
                    if 'best regards' in body.lower() or 'sincerely' in body.lower() or 'regards' in body.lower():
                        # Check if name is after closing
                        if not any(name_part in body for name_part in user_name.split()):
                            body = body.rstrip() + f"\n{user_name}"
                    else:
                        # Add closing and signature
                        body = body.rstrip() + f"\n\nBest regards,\n{user_name}"
                    
                    # Show what will be sent
                    console.print(f"\n[yellow]📨 Email Preview:[/yellow]")
                    console.print(f"[yellow]To: {to}[/yellow]")
                    console.print(f"[yellow]Subject: {subject}[/yellow]")
                    console.print(f"[yellow]Body:\n{body}[/yellow]\n")
                    
                    # Send directly
                    return self.send_email(to, subject, body)
                    
                except json.JSONDecodeError as e:
                    console.print(f"[red]JSON parse error: {e}[/red]")
                    console.print(f"[red]Response was: {email_text}[/red]")
                    return "❌ I couldn't understand your email request. Try being more specific:\n'Send email to john@example.com with subject Hello saying Hi John, how are you?'"
            
            elif 'read' in user_lower and 'email' in user_lower:
                # Try to extract email ID
                words = user_input.split()
                for word in words:
                    if len(word) > 10 and not ' ' in word:
                        return self.read_email(word)
                return "Please provide the email ID to read."
            
            elif 'archive' in user_lower:
                # Extract email ID
                words = user_input.split()
                for word in words:
                    if len(word) > 10 and not ' ' in word:
                        return self.archive_email(word)
                return "Please provide the email ID to archive."
            
            elif 'delete' in user_lower:
                # Extract email ID
                words = user_input.split()
                for word in words:
                    if len(word) > 10 and not ' ' in word:
                        return self.delete_email(word)
                return "Please provide the email ID to delete."
            
            elif 'star' in user_lower:
                # Extract email ID
                words = user_input.split()
                for word in words:
                    if len(word) > 10 and not ' ' in word:
                        return self.star_email(word, star=True)
                return "Please provide the email ID to star."
            
            elif 'mark as read' in user_lower or 'mark read' in user_lower:
                # Extract email ID
                words = user_input.split()
                for word in words:
                    if len(word) > 10 and not ' ' in word:
                        return self.mark_as_read(word)
                return "Please provide the email ID to mark as read."
            
            elif 'draft' in user_lower and 'reply' in user_lower:
                # Extract email content or ID
                return "Please provide the email content or ID you want to reply to."
            
            elif 'urgent' in user_lower or 'check urgent' in user_lower:
                return self.check_urgent_emails()
            
            elif 'digest' in user_lower or 'daily report' in user_lower:
                return self.generate_daily_digest()
            
            else:
                # For unrecognized commands, try to be helpful without overthinking
                if '?' in user_input:
                    # It's a question, answer it
                    system_prompt = """You are MailPilot, an AI email management agent. 
Answer the user's question briefly and directly. Don't ask follow-up questions."""
                    
                    prompt = f"{system_prompt}\n\nUser: {user_input}\n\nAnswer:"
                    response = self.model.generate_content(prompt)
                    return response.text
                else:
                    # Unclear command
                    return """I'm not sure what you want me to do. Here are some commands:

📧 Email Actions:
• "Show me emails" - List recent emails
• "Send email to john@example.com saying Hello" - Send an email
• "Read email ID [xyz]" - Read full email
• "Archive/Delete/Star email ID [xyz]"

🔍 Search & Analysis:
• "Search for emails with attachments"
• "Summarize my inbox"
• "Check urgent emails"
• "Generate daily digest"

What would you like to do?"""
            
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            console.print(f"[red]Error: {str(e)}[/red]")
            console.print(f"[red]Full traceback:\n{error_trace}[/red]")
            return f"❌ Error: {str(e)}\n\nTry a simpler command like 'show me emails' or check the logs."
