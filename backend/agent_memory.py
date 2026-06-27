"""Memory system for MailPilot agent to remember user preferences and context."""
import json
import os
from datetime import datetime
from typing import Dict, List, Any

class AgentMemory:
    """Persistent memory for the agent."""
    
    def __init__(self, memory_file: str = 'agent_memory.json'):
        self.memory_file = memory_file
        self.memory = self._load_memory()
    
    def _load_memory(self) -> Dict:
        """Load memory from disk."""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {
            'user_preferences': {},
            'frequent_contacts': {},
            'email_patterns': {},
            'task_history': [],
            'learned_behaviors': {}
        }
    
    def _save_memory(self):
        """Save memory to disk."""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def remember_preference(self, key: str, value: Any):
        """Store user preference."""
        self.memory['user_preferences'][key] = value
        self._save_memory()
    
    def get_preference(self, key: str, default=None):
        """Retrieve user preference."""
        return self.memory['user_preferences'].get(key, default)
    
    def track_contact(self, email: str):
        """Track frequent contacts."""
        if email not in self.memory['frequent_contacts']:
            self.memory['frequent_contacts'][email] = 0
        self.memory['frequent_contacts'][email] += 1
        self._save_memory()
    
    def get_frequent_contacts(self, limit: int = 10) -> List[str]:
        """Get most frequent contacts."""
        sorted_contacts = sorted(
            self.memory['frequent_contacts'].items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [email for email, _ in sorted_contacts[:limit]]
    
    def log_task(self, task: str, result: str):
        """Log completed task."""
        self.memory['task_history'].append({
            'timestamp': datetime.now().isoformat(),
            'task': task,
            'result': result
        })
        # Keep only last 100 tasks
        self.memory['task_history'] = self.memory['task_history'][-100:]
        self._save_memory()
    
    def learn_pattern(self, pattern_name: str, pattern_data: Any):
        """Learn email handling patterns."""
        self.memory['email_patterns'][pattern_name] = pattern_data
        self._save_memory()
    
    def get_pattern(self, pattern_name: str):
        """Retrieve learned pattern."""
        return self.memory['email_patterns'].get(pattern_name)
