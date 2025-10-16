"""
DoorDash Notification Generator Module

Version: 1.2.0 - Added pricing filter and smart deal targeting
"""

import json
import re
from typing import List, Dict, Optional


class NotificationGenerator:
    """
    Generate personalized push notifications for DoorDash consumers.
    
    Version History:
    - v1.0: Initial release with dietary guardrails
    - v1.1: Added mild spicy guardrail
    - v1.2: Added pricing filter for smart deal targeting
    """
    
    __version__ = "1.2.0"
    
    def __init__(self):
        self.brand_phrases = [
            "Skip the schlep",
            "You pick. We roll",
            "Deal dropped. You're up",
            "Your go-tos are here",
            "More you time",
        ]
    
    def extract_promo_usage(self, price_sensitivity: str) -> float:
        """Extract promo usage percentage from price_sensitivity field"""
        if not price_sensitivity:
            return 0.0
        
        match = re.search(r'(\d+\.?\d*)%\s*promo', price_sensitivity.lower())
        if match:
            return float(match.group(1))
        return 0.0
    
    def is_value_conscious(self, price_sensitivity: str) -> bool:
        """Determine if consumer is value-conscious based on price sensitivity"""
        if not price_sensitivity:
            return False
        
        price_lower = price_sensitivity.lower()
        
        # Check for explicit labels
        if 'value seeker' in price_lower or 'budget' in price_lower:
            return True
        
        # Check promo usage
        promo_usage = self.extract_promo_usage(price_sensitivity)
        if promo_usage > 25:
            return True
        
        return False
    
    def passes_dietary_guardrail(self, notification: Dict, dietary_pref: str) -> bool:
        """Check if a notification respects dietary preferences."""
        if not dietary_pref or dietary_pref.lower() in ['none', 'no preference']:
            return True
        
        dietary_lower = dietary_pref.lower()
        content = f"{notification['title']} {notification['body']} {notification['keyword']}".lower()
        
        if 'vegetarian' in dietary_lower:
            meat_keywords = ['meat', 'chicken', 'beef', 'pork', 'bacon', 'sausage', 'steak', 'turkey']
            if any(meat in content for meat in meat_keywords):
                return False
        
        if 'vegan' in dietary_lower:
            animal_products = ['meat', 'chicken', 'beef', 'dairy', 'cheese', 'egg', 'milk', 'bacon', 'butter']
            if any(product in content for product in animal_products):
                return False
        
        if 'pescatarian' in dietary_lower:
            meats = ['chicken', 'beef', 'pork', 'bacon', 'sausage', 'steak', 'turkey', 'lamb']
            if any(meat in content for meat in meats):
                return False
        
        return True
    
    def passes_mild_spicy_guardrail(self, notification: Dict, taste_pref: str) -> bool:
        """
        v1.1: If taste preference contains 'mild spicy', filter out 'spicy' keyword.
        """
        if not taste_pref:
            return True
        
        taste_lower = taste_pref.lower()
        
        if 'mild' in taste_lower and 'spicy' in taste_lower:
            content = f"{notification['title']} {notification['body']} {notification['keyword']}".lower()
            if 'spicy' in content:
                return False
        
        return True
    
    def validate_notification(self, title: str, body: str) -> Dict:
        """Validate a notification against DoorDash guidelines."""
        issues = []
        
        if len(title) >= 35:
            issues.append(f"Title too long: {len(title)}/35 characters")
        if len(body) > 140:
            issues.append(f"Body too long: {len(body)}/140 characters")
        
        if '!' in title or '!' in body:
            issues.append("Contains exclamation points")
        if title and title[-1] in '.,:;' and title[-1] != '?':
            issues.append("Title has end punctuation")
        if '#' in title or '#' in body:
            issues.append("Contains hashtags")
        if 'DoorDash' in title or 'DoorDash' in body:
            issues.append("Mentions DoorDash")
        
        hyperbolic = ['mouthwatering', 'scrumptious', 'tantalizing', 'tempting', 'indulge', 'savor']
        if any(word in title.lower() or word in body.lower() for word in hyperbolic):
            issues.append("Contains overly salesy language")
        
        meal_times = ['breakfast', 'brunch', 'lunch', 'dinner']
        if any(meal in title.lower() or meal in body.lower() for meal in meal_times):
            issues.append("Infers meal time")
        
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
        """Generate personalized notifications from a consumer profile."""
        overall = profile.get('overall_profile', {})
        cuisine = overall.get('cuisine_preferences', '').lower()
        food = overall.get('food_preferences', '').lower()
        taste = overall.get('taste_preference', '').lower()
        dietary = overall.get('dietary_preferences', {})
        preferred_dietary = dietary.get('preferred_dietary_preference', '')
        price_sensitivity = overall.get('price_sensitivity', '')
        
        all_notifications = []
        
        # Generate base notifications
        self._add_noodle_notifications(all_notifications, food, cuisine)
        self._add_cuisine_notifications(all_notifications, cuisine, food, taste)
        self._add_pricing_aware_notifications(all_notifications, price_sensitivity)
        self._add_universal_notifications(all_notifications)
        
        # Apply guardrails
        filtered = []
        for notif in all_notifications:
            if not self.passes_dietary_guardrail(notif, preferred_dietary):
                continue
            if not self.passes_mild_spicy_guardrail(notif, taste):
                continue
            filtered.append(notif)
        
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
                "body": "Get bold flavors from restaurants that bring it",
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
        
        if 'indian' in cuisine:
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
    
    def _add_pricing_aware_notifications(self, notifications: List, price_sensitivity: str):
        """
        v1.2: Add deal notifications with pricing-aware scoring
        
        Value-conscious consumers get boosted deal notification scores
        """
        is_value = self.is_value_conscious(price_sensitivity)
        
        if is_value:
            # Boost deal notifications for value-conscious consumers
            notifications.append({
                "title": "Deal dropped. You're up",
                "body": "Save on restaurants you order from most with deals ready now",
                "keyword": "food deals",
                "score": 95  # Boosted score
            })
            
            notifications.append({
                "title": "$0 delivery fee",
                "body": "Skip the fee on orders from top-rated spots near you",
                "keyword": "free delivery",
                "score": 93  # Boosted score
            })
        else:
            # Lower score for balanced spenders (will likely be filtered out)
            notifications.append({
                "title": "Deal dropped. You're up",
                "body": "Get savings on restaurants you visit most",
                "keyword": "food deals",
                "score": 78  # Below typical threshold
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
        """
        Generate DoorDash search URL from keyword.
        
        v1.1: Added deals filter parameter
        """
        encoded_keyword = keyword.replace(' ', '%20')
        return f"https://www.doordash.com/search/store/{encoded_keyword}?event_type=search&filterQuery-vertical_ids=1&filterQuery-deals-fill=true"
