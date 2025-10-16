"""
DoorDash Notification Generator Module

Reusable module for generating personalized push notifications
following DoorDash brand guidelines and dietary restrictions.
"""

import json
from typing import List, Dict, Optional


class NotificationGenerator:
    """
    Generate personalized push notifications for DoorDash consumers.
    
    This class encapsulates:
    - DoorDash brand voice guidelines
    - Format restrictions (title < 35 chars, body ≤ 140 chars)
    - Dietary preference guardrails
    - Scoring logic based on profile match quality
    """
    
    def __init__(self):
        self.brand_phrases = [
            "Skip the schlep",
            "You pick. We roll",
            "Deal dropped. You're up",
            "Your go-tos are here",
            "More you time",
        ]
    
    def passes_dietary_guardrail(self, notification: Dict, dietary_pref: str) -> bool:
        """
        Check if a notification respects dietary preferences.
        
        Args:
            notification: Dict with 'title', 'body', 'keyword'
            dietary_pref: Consumer's preferred dietary preference string
            
        Returns:
            True if notification passes dietary check, False otherwise
        """
        if not dietary_pref or dietary_pref.lower() in ['none', 'no preference']:
            return True
        
        dietary_lower = dietary_pref.lower()
        content = f"{notification['title']} {notification['body']} {notification['keyword']}".lower()
        
        # Vegetarian guardrails
        if 'vegetarian' in dietary_lower:
            meat_keywords = ['meat', 'chicken', 'beef', 'pork', 'bacon', 'sausage', 'steak', 'turkey']
            if any(meat in content for meat in meat_keywords):
                return False
        
        # Vegan guardrails
        if 'vegan' in dietary_lower:
            animal_products = ['meat', 'chicken', 'beef', 'dairy', 'cheese', 'egg', 'milk', 'bacon', 'butter']
            if any(product in content for product in animal_products):
                return False
        
        # Pescatarian guardrails
        if 'pescatarian' in dietary_lower:
            meats = ['chicken', 'beef', 'pork', 'bacon', 'sausage', 'steak', 'turkey', 'lamb']
            if any(meat in content for meat in meats):
                return False
        
        return True
    
    def validate_notification(self, title: str, body: str) -> Dict:
        """
        Validate a notification against DoorDash guidelines.
        
        Args:
            title: Notification title
            body: Notification body
            
        Returns:
            Dict with validation results and any issues found
        """
        issues = []
        
        # Format validation
        if len(title) >= 35:
            issues.append(f"Title too long: {len(title)}/35 characters")
        if len(body) > 140:
            issues.append(f"Body too long: {len(body)}/140 characters")
        
        # Content restrictions
        if '!' in title or '!' in body:
            issues.append("Contains exclamation points")
        if title and title[-1] in '.,:;' and title[-1] != '?':
            issues.append("Title has end punctuation")
        if '#' in title or '#' in body:
            issues.append("Contains hashtags")
        if 'DoorDash' in title or 'DoorDash' in body:
            issues.append("Mentions DoorDash")
        
        # Hyperbolic language
        hyperbolic = ['mouthwatering', 'scrumptious', 'tantalizing', 'tempting', 'indulge', 'savor']
        if any(word in title.lower() or word in body.lower() for word in hyperbolic):
            issues.append("Contains overly salesy language")
        
        # Meal time inference
        meal_times = ['breakfast', 'brunch', 'lunch', 'dinner']
        if any(meal in title.lower() or meal in body.lower() for meal in meal_times):
            issues.append("Infers meal time")
        
        # "Authentic" check
        if 'authentic' in title.lower() or 'authentic' in body.lower():
            issues.append("Uses 'authentic' descriptor")
        
        return {
            "is_valid": len(issues) == 0,
            "title_length": len(title),
            "body_length": len(body),
            "issues": issues
        }
    
    def generate_notifications(
        self, 
        profile: Dict, 
        min_score: int = 80,
        max_count: int = 10
    ) -> List[Dict]:
        """
        Generate personalized notifications from a consumer profile.
        
        Args:
            profile: Consumer profile dict from GenAI table
            min_score: Minimum quality score threshold (default: 80)
            max_count: Maximum notifications to return (default: 10)
            
        Returns:
            List of notification dicts with title, body, keyword, score
        """
        overall = profile.get('overall_profile', {})
        cuisine = overall.get('cuisine_preferences', '').lower()
        food = overall.get('food_preferences', '').lower()
        taste = overall.get('taste_preference', '').lower()
        dietary = overall.get('dietary_preferences', {})
        preferred_dietary = dietary.get('preferred_dietary_preference', '')
        
        all_notifications = []
        
        # Generate notifications based on profile (scores 98-80)
        self._add_noodle_notifications(all_notifications, food, cuisine)
        self._add_cuisine_notifications(all_notifications, cuisine, food, taste)
        self._add_universal_notifications(all_notifications)
        
        # Apply dietary guardrails
        filtered = [
            n for n in all_notifications 
            if self.passes_dietary_guardrail(n, preferred_dietary)
        ]
        
        # Filter by score and sort
        filtered = [n for n in filtered if n['score'] >= min_score]
        filtered.sort(key=lambda x: x['score'], reverse=True)
        
        return filtered[:max_count]
    
    def _add_noodle_notifications(self, notifications: List, food: str, cuisine: str):
        """Add noodle-related notifications"""
        if 'noodle' in food or 'noodle' in cuisine:
            notifications.append({
                "title": "Noodle cravings covered",
                "body": "🍜 Hot bowls and hand-pulled options ready from spots you'll love",
                "keyword": "noodles",
                "score": 98
            })
    
    def _add_cuisine_notifications(self, notifications: List, cuisine: str, food: str, taste: str):
        """Add cuisine-specific notifications"""
        
        if 'chinese' in cuisine:
            notifications.append({
                "title": "Skip the schlep",
                "body": "Get dumplings, rice dishes, and bold flavors delivered from top spots",
                "keyword": "Chinese food",
                "score": 96
            })
        
        if 'bowl' in food or 'rice' in food or 'poke' in food or 'hawaiian' in cuisine:
            notifications.append({
                "title": "You pick. We roll",
                "body": "Build your perfect bowl with fresh ingredients from places nearby",
                "keyword": "rice bowls",
                "score": 94
            })
        
        if 'spicy' in taste or 'bold' in taste:
            notifications.append({
                "title": "Heat seekers wanted",
                "body": "Get bold, spicy flavors from restaurants that bring it",
                "keyword": "spicy food",
                "score": 92
            })
        
        if 'mexican' in cuisine or 'latin' in cuisine:
            notifications.append({
                "title": "Taco time",
                "body": "Fresh tacos, burritos, and more ready to order from nearby favorites",
                "keyword": "Mexican",
                "score": 90
            })
        
        if 'pizza' in food or 'italian' in cuisine:
            notifications.append({
                "title": "Pizza. Done",
                "body": "Thin crust to deep dish, they're all just a tap away",
                "keyword": "pizza",
                "score": 88
            })
        
        if 'burger' in food or 'sandwich' in food:
            notifications.append({
                "title": "Burgers your way",
                "body": "Classic or loaded, get them delivered hot and ready",
                "keyword": "burgers",
                "score": 86
            })
        
        if 'japanese' in cuisine or 'sushi' in food or 'ramen' in food:
            notifications.append({
                "title": "Sushi and ramen ready",
                "body": "Fresh rolls and rich broths from spots you'll want to reorder",
                "keyword": "Japanese food",
                "score": 84
            })
        
        if 'thai' in cuisine:
            notifications.append({
                "title": "Curry cravings",
                "body": "Get bold Thai curries and stir-fries delivered in 30 min",
                "keyword": "Thai food",
                "score": 82
            })
        
        if 'vietnamese' in cuisine or 'pho' in food:
            notifications.append({
                "title": "Pho and more",
                "body": "Fresh Vietnamese flavors from noodle soups to banh mi sandwiches",
                "keyword": "Vietnamese food",
                "score": 82
            })
        
        if 'indian' in cuisine or 'curry' in food:
            notifications.append({
                "title": "Curry and more",
                "body": "Bold Indian flavors from tikka masala to biryani, all nearby",
                "keyword": "Indian food",
                "score": 82
            })
        
        if 'korean' in cuisine:
            notifications.append({
                "title": "Korean favorites nearby",
                "body": "From bibimbap to Korean fried chicken, flavors you'll love",
                "keyword": "Korean food",
                "score": 82
            })
        
        if 'mediterranean' in cuisine or 'greek' in cuisine:
            notifications.append({
                "title": "Mediterranean picks",
                "body": "Fresh gyros, falafel, and hummus from spots worth reordering",
                "keyword": "Mediterranean food",
                "score": 82
            })
        
        if 'salad' in food or 'healthy' in food:
            notifications.append({
                "title": "Fresh bowls nearby",
                "body": "Build your perfect meal with options that keep it light",
                "keyword": "healthy food",
                "score": 80
            })
    
    def _add_universal_notifications(self, notifications: List):
        """Add universal notifications that work for all consumers"""
        notifications.append({
            "title": "Your go-tos are here",
            "body": "Reorder favorites or find something new worth trying",
            "keyword": "restaurants",
            "score": 80
        })
    
    def format_for_doordash_url(self, keyword: str) -> str:
        """Generate DoorDash search URL from keyword"""
        encoded_keyword = keyword.replace(' ', '%20')
        return f"https://www.doordash.com/search/store/{encoded_keyword}?event_type=search&filterQuery-vertical_ids=1"

