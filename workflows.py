"""Workflow automation for MailPilot"""
from typing import List, Dict, Callable
from gmail_client import GmailClient
from agent import MailPilotAgent

class Workflow:
    """Base workflow class."""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def execute(self, context: Dict) -> Dict:
        """Execute the workflow."""
        raise NotImplementedError

class AutoArchiveNewsletters(Workflow):
    """Automatically archive newsletter emails."""
    def __init__(self, gmail_client: GmailClient):
        super().__init__(
            "Auto-Archive Newsletters",
            "Automatically archive emails identified as newsletters"
        )
        self.gmail = gmail_client
    
    def execute(self, context: Dict) -> Dict:
        query = "category:promotions OR category:updates"
        messages = self.gmail.list_messages(query=query, max_results=20)
        
        archived_count = 0
        for msg in messages:
            if self.gmail.modify_labels(msg['id'], remove_labels=['INBOX']):
                archived_count += 1
        
        return {
            'success': True,
            'archived_count': archived_count,
            'message': f"Archived {archived_count} newsletters"
        }

class SummarizeUnread(Workflow):
    """Summarize all unread emails."""
    def __init__(self, agent: MailPilotAgent):
        super().__init__(
            "Summarize Unread",
            "Create a summary of all unread emails"
        )
        self.agent = agent
    
    def execute(self, context: Dict) -> Dict:
        messages = self.agent.gmail.list_messages(query='is:unread', max_results=10)
        
        if not messages:
            return {
                'success': True,
                'message': 'No unread emails'
            }
        
        summaries = []
        for msg in messages:
            summaries.append(f"• {msg['from']}: {msg['subject']}\n  {msg['snippet']}")
        
        summary = "\n\n".join(summaries)
        
        return {
            'success': True,
            'summary': summary,
            'count': len(messages)
        }

class WorkflowManager:
    """Manage and execute workflows."""
    def __init__(self, agent: MailPilotAgent):
        self.agent = agent
        self.workflows: Dict[str, Workflow] = {}
        self._register_default_workflows()
    
    def _register_default_workflows(self):
        """Register default workflows."""
        self.register_workflow(AutoArchiveNewsletters(self.agent.gmail))
        self.register_workflow(SummarizeUnread(self.agent))
    
    def register_workflow(self, workflow: Workflow):
        """Register a new workflow."""
        self.workflows[workflow.name] = workflow
    
    def execute_workflow(self, workflow_name: str, context: Dict = None) -> Dict:
        """Execute a workflow by name."""
        if workflow_name not in self.workflows:
            return {
                'success': False,
                'message': f"Workflow '{workflow_name}' not found"
            }
        
        workflow = self.workflows[workflow_name]
        return workflow.execute(context or {})
    
    def list_workflows(self) -> List[Dict]:
        """List all available workflows."""
        return [
            {'name': wf.name, 'description': wf.description}
            for wf in self.workflows.values()
        ]
