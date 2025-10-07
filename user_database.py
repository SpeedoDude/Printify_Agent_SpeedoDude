# user_database.py

import json
import hashlib

class User:
    def __init__(self, username, password, role='user', subscription_tier='free', otp_secret=None):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.role = role
        self.subscription_tier = subscription_tier
        self.otp_secret = otp_secret

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == self._hash_password(password)

class UserDB:
    def __init__(self, db_path='users.json'):
        self.db_path = db_path
        self.users = self._load_users()

    def _load_users(self):
        try:
            with open(self.db_path, 'r') as f:
                users_data = json.load(f)
                return {username: User(username, data['password_hash'], data.get('role', 'user'), data.get('subscription_tier', 'free'), data.get('otp_secret')) for username, data in users_data.items()}
        except FileNotFoundError:
            return {}

    def _save_users(self):
        with open(self.db_path, 'w') as f:
            users_data = {username: {'password_hash': user.password_hash, 'role': user.role, 'subscription_tier': user.subscription_tier, 'otp_secret': user.otp_secret} for username, user in self.users.items()}
            json.dump(users_data, f)

    def add_user(self, username, password, role='user', subscription_tier='free'):
        if username in self.users:
            return False, "Username already exists."
        self.users[username] = User(username, password, role, subscription_tier)
        self._save_users()
        return True, "User created successfully."

    def get_user(self, username):
        return self.users.get(username)

    def authenticate_user(self, username, password):
        user = self.get_user(username)
        if user and user.check_password(password):
            return user
        return None
        
    def set_subscription_tier(self, username, tier):
        """Sets the subscription tier for a user."""
        user = self.get_user(username)
        if user:
            user.subscription_tier = tier
            self._save_users()
            return True
        return False
        
    def set_otp_secret(self, username, secret):
        """Sets the OTP secret for a user."""
        user = self.get_user(username)
        if user:
            user.otp_secret = secret
            self._save_users()
            return True
        return False
