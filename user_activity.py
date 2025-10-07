# user_activity.py

import json
from datetime import datetime

class UserActivity:
    def __init__(self, db_path='user_activity.json'):
        self.db_path = db_path
        self.activity = self._load_activity()

    def _load_activity(self):
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_activity(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.activity, f, indent=4)

    def log_activity(self, username, action, details=None):
        """Logs a user activity."""
        if username not in self.activity:
            self.activity[username] = {
                'login_count': 0,
                'last_login': None,
                'features_used': {}
            }
        
        timestamp = datetime.now().isoformat()

        if action == 'login':
            self.activity[username]['login_count'] += 1
            self.activity[username]['last_login'] = timestamp
        
        elif action == 'use_feature':
            feature = details.get('feature')
            if feature:
                if feature not in self.activity[username]['features_used']:
                    self.activity[username]['features_used'][feature] = {'count': 0, 'last_used': None}
                self.activity[username]['features_used'][feature]['count'] += 1
                self.activity[username]['features_used'][feature]['last_used'] = timestamp

        self._save_activity()

    def get_user_activity(self, username):
        return self.activity.get(username, {})
