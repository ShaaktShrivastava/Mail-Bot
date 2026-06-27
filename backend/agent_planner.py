"""Planning and task decomposition for complex email tasks."""
import json
from typing import List, Dict, Any
import google.generativeai as genai

class TaskPlanner:
    """Breaks down complex tasks into executable steps."""
    
    def __init__(self, model: genai.GenerativeModel):
        self.model = model
    
    def create_plan(self, user_request: str, context: Dict = None) -> List[Dict]:
        """Create a step-by-step plan for complex tasks."""
        prompt = f"""You are an AI agent planning email management tasks.
Break down this request into specific, executable steps:

Request: {user_request}

Context: {json.dumps(context) if context else 'None'}

Return a JSON array of steps, each with:
- action: the function to call (list_emails, send_email, etc.)
- parameters: dict of parameters for that function
- reasoning: why this step is needed

Example format:
[
  {{"action": "list_emails", "parameters": {{"query": "is:unread"}}, "reasoning": "First find unread emails"}},
  {{"action": "send_email", "parameters": {{"to": "...", "subject": "..."}}, "reasoning": "Send response"}}
]

Return ONLY the JSON array, no other text."""
        
        try:
            response = self.model.generate_content(prompt)
            # Extract JSON from response
            text = response.text.strip()
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                text = text.split('```')[1].split('```')[0]
            
            plan = json.loads(text.strip())
            return plan if isinstance(plan, list) else []
        except Exception as e:
            print(f"Planning error: {e}")
            return []
    
    def should_plan(self, user_request: str) -> bool:
        """Determine if request needs multi-step planning."""
        keywords = ['all', 'multiple', 'batch', 'every', 'organize', 'clean up', 'summarize and']
        return any(keyword in user_request.lower() for keyword in keywords)
