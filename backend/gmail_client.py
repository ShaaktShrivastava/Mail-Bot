"""Gmail API client for email operations."""
import os.path
import base64
from typing import List, Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailClient:
    def __init__(self, credentials_dict: Optional[Dict] = None):
        """Initialize Gmail client with credentials dict or local file."""
        self.service = None
        if credentials_dict:
            self._authenticate_from_dict(credentials_dict)
        else:
            self._authenticate_from_file()
    
    def _authenticate_from_dict(self, credentials_dict: Dict):
        """Authenticate using credentials dictionary from database."""
        try:
            print(f"Authenticating from dict with keys: {credentials_dict.keys()}")
            
            creds = Credentials(
                token=credentials_dict.get('token'),
                refresh_token=credentials_dict.get('refresh_token'),
                token_uri=credentials_dict.get('token_uri', 'https://oauth2.googleapis.com/token'),
                client_id=credentials_dict.get('client_id'),
                client_secret=credentials_dict.get('client_secret'),
                scopes=credentials_dict.get('scopes', SCOPES)
            )
            
            print("Credentials object created, checking if expired...")
            # Refresh if expired
            if creds.expired and creds.refresh_token:
                print("Token expired, refreshing...")
                creds.refresh(Request())
                print("Token refreshed successfully")
            
            print("Building Gmail service...")
            self.service = build('gmail', 'v1', credentials=creds)
            print("Gmail service built successfully")
        except Exception as e:
            print(f"Auth from dict error: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _authenticate_from_file(self):
        """Authenticate with Gmail API using OAuth (local file method)."""
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    raise Exception("credentials.json not found. Please set up OAuth credentials.")
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)
    
    def list_messages(self, query: str = '', max_results: int = 10) -> List[Dict]:
        """List messages matching query."""
        try:
            results = self.service.users().messages().list(
                userId='me', q=query, maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            detailed_messages = []
            
            for msg in messages:
                detail = self.get_message(msg['id'])
                if detail:
                    detailed_messages.append(detail)
            
            return detailed_messages
        except Exception as e:
            print(f"Error listing messages: {e}")
            return []
    
    def get_message(self, message_id: str) -> Optional[Dict]:
        """Get full message details."""
        try:
            message = self.service.users().messages().get(
                userId='me', id=message_id, format='full'
            ).execute()
            
            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            body = self._get_message_body(message['payload'])
            
            return {
                'id': message['id'],
                'threadId': message['threadId'],
                'subject': subject,
                'from': sender,
                'date': date,
                'body': body,
                'snippet': message.get('snippet', ''),
                'labels': message.get('labelIds', [])
            }
        except Exception as e:
            print(f"Error getting message: {e}")
            return None
    
    def _get_message_body(self, payload: Dict) -> str:
        """Extract message body from payload."""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    return base64.urlsafe_b64decode(data).decode('utf-8')
        elif 'body' in payload:
            data = payload['body'].get('data', '')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8')
        return ''
    
    def send_message(self, to: str, subject: str, body: str) -> bool:
        """Send an email message."""
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            self.service.users().messages().send(
                userId='me', body={'raw': raw}
            ).execute()
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    def modify_labels(self, message_id: str, add_labels: List[str] = None, 
                     remove_labels: List[str] = None) -> bool:
        """Modify labels on a message."""
        try:
            self.service.users().messages().modify(
                userId='me', id=message_id,
                body={'addLabelIds': add_labels or [], 'removeLabelIds': remove_labels or []}
            ).execute()
            return True
        except Exception as e:
            print(f"Error modifying labels: {e}")
            return False
    
    def trash_message(self, message_id: str) -> bool:
        """Move message to trash."""
        try:
            self.service.users().messages().trash(userId='me', id=message_id).execute()
            return True
        except Exception as e:
            print(f"Error trashing message: {e}")
            return False
