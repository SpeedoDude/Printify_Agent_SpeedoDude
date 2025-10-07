# community.py

import json
import random
import string
from datetime import datetime, timedelta

class ProductReviews:
    def __init__(self, db_path='reviews.json'):
        self.db_path = db_path
        self.reviews = self._load_reviews()

    def _load_reviews(self):
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_reviews(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.reviews, f)

    def add_review(self, product_id, username, rating, review):
        if product_id not in self.reviews:
            self.reviews[product_id] = []
        self.reviews[product_id].append({'username': username, 'rating': rating, 'review': review})
        self._save_reviews()

    def get_reviews(self, product_id):
        return self.reviews.get(product_id, [])

class Contests:
    def __init__(self, db_path='contests.json'):
        self.db_path = db_path
        self.contests = self._load_contests()

    def _load_contests(self):
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_contests(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.contests, f)

    def create_contest(self, name, description, end_date):
        contest_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        self.contests[contest_id] = {
            'name': name,
            'description': description,
            'end_date': end_date.isoformat(),
            'participants': []
        }
        self._save_contests()
        return contest_id

    def enter_contest(self, contest_id, username):
        if contest_id in self.contests:
            self.contests[contest_id]['participants'].append(username)
            self._save_contests()
            return True
        return False

    def get_contests(self):
        return self.contests

class Referrals:
    def __init__(self, db_path='referrals.json'):
        self.db_path = db_path
        self.referrals = self._load_referrals()

    def _load_referrals(self):
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_referrals(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.referrals, f)

    def add_referral(self, referrer_username, new_username):
        if referrer_username not in self.referrals:
            self.referrals[referrer_username] = []
        self.referrals[referrer_username].append(new_username)
        self._save_referrals()

    def get_referrals(self, username):
        return self.referrals.get(username, [])
