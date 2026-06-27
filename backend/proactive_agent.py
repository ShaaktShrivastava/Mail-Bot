"""Proactive monitoring and autonomous actions."""
import time
from datetime import datetime, timedelta
from typing import List, Dict
from gmail_client import GmailClient
import google.generativeai as genai

class ProactiveAgent:
    """Monitors inbox and takes autonomous actions."""
    
    def __init__(self, gmail: GmailClient, model: genai.GenerativeModel, memory):
        self.gmail = gmail
        self.model = model
        self.memory = memory
        self.last_check = None
    
    def check_urgent_emails(self) -> List[Dict]:
        """Check for urgent emails that need immediate attention."""
        messages = self.gmail.list_messages(query='is:unread', max_results=20)
        urgent = []
        
        for msg in messages:
            # Check for urgency indicators
            if self._is_urgent(msg):
                urgent.append(msg)
        
        return urgent
    
    def _is_urgent(self, email: Dict) -> bool:
        """Determine if email is urgent using AI."""
        prompt = f"""Is this email urgent or time-sensitive? Respond with only 'yes' or 'no'.

From: {email['from']}
Subject: {email['subject']}
Snippet: {email['snippet']}"""
        
        try:
            response = self.model.generate_content(prompt)
            return 'yes' in response.text.lower()
        except:
            return False
    
    def suggest_actions(self, email: Dict) -> List[str]:
        """Suggest actions for an email."""
        prompt = f"""What actions should be taken for this email? Choose from:
- reply: needs a response
- archive: can be archived
- star: important to save
- delegate: forward to someone
- schedule: needs calendar entry
- ignore: no action needed

From: {email['from']}
Subject: {email['subject']}
Content: {email.get('snippet', '')}

Return as comma-separated list of action words only."""
        
        try:
            response = self.model.generate_content(prompt)
            actions = [a.strip() for a in response.text.strip().split(',')]
            return actions
        except:
            return []
    
    def auto_categorize_new_emails(self):
        """Automatically categorize and organize new emails."""
        if self.last_check is None:
            self.last_check = datetime.now() - timedelta(hours=1)
        
        # Check emails since last check
        query = f'after:{int(self.last_check.timestamp())}'
        new_emails = self.gmail.list_messages(query=query, max_results=10)
        
        categorized = {'important': [], 'newsletters': [], 'spam_likely': []}
        
        for email in new_emails:
            category = self._categorize_email(email)
            if category in categorized:
                categorized[category].append(email)
        
        self.last_check = datetime.now()
        return categorized
    
    def _categorize_email(self, email: Dict) -> str:
        """Categorize email using AI."""
        prompt = f"""Categorize this email into ONE category: important, newsletters, spam_likely, or normal.

From: {email['from']}
Subject: {email['subject']}
Snippet: {email['snippet']}

Respond with only the category word."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip().lower()
        except:
            return 'normal'
    
    def generate_daily_digest(self) -> str:
        """Generate a daily email digest."""
        today = datetime.now().strftime('%Y/%m/%d')
        emails = self.gmail.list_messages(query=f'after:{today}', max_results=50)
        
        if not emails:
            return "No emails received today."
        
        email_summary = "\n".join([
            f"• {email['from']}: {email['subject']}"
            for email in emails[:10]
        ])
        
        prompt = f"""Create a brief daily digest of these emails. Highlight:
1. Urgent/important emails
2. Action items
3. Less important updates

Emails:
{email_summary}"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return f"Received {len(emails)} emails today."
