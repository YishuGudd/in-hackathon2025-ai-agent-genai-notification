"""
DoorDash Notification Generator Module

Version: 1.3.0 - Added locale-aware copy helpers (es, fr-CA, en-CA)
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
    - v1.3: Added locale-aware copy helpers (Spanish, French-CA, English-CA)
    """
    
    __version__ = "1.3.0"
    
    def __init__(self):
        self.brand_phrases = [
            "Skip the schlep",
            "You pick. We roll",
            "Deal dropped. You're up",
            "Your go-tos are here",
            "More you time",
        ]

        # Title translations by locale key
        self.title_translations = {
            "es": {
                "Noodle cravings covered": "Antojo de fideos, listo",
                "Deal dropped. You're up": "Bajó la oferta. Es tu turno",
                "Skip the schlep": "Evita el viaje",
                "You pick. We roll": "Tú eliges. Nosotros llevamos",
                "Your go-tos are here": "Tus favoritos están aquí",
                "Heat seekers wanted": "Para amantes del picante",
                "Pizza. Done": "Pizza. Listo",
                "Burgers your way": "Hamburguesas a tu modo",
                "Sushi and ramen ready": "Sushi y ramen listos",
                "Curry cravings": "Antojo de curry",
                "Pho and more": "Pho y más",
                "Curry and more": "Curry y más",
                "Korean favorites nearby": "Favoritos coreanos cerca",
                "Mediterranean picks": "Opciones mediterráneas",
                "Fresh bowls nearby": "Bowls frescos cerca",
                "Taco time": "Hora de tacos",
                "$0 delivery fee": "Envío a $0",
            },
            "fr-CA": {
                "Noodle cravings covered": "Envie de nouilles? On livre",
                "Deal dropped. You're up": "Promo en cours. À toi",
                "Skip the schlep": "Évite le déplacement",
                "You pick. We roll": "Tu choisis. On s’en charge",
                "Your go-tos are here": "Tes favoris sont là",
                "Heat seekers wanted": "Pour amateurs de piquant",
                "Pizza. Done": "Pizza. C’est fait",
                "Burgers your way": "Burgers à ta façon",
                "Sushi and ramen ready": "Sushi et ramen prêts",
                "Curry cravings": "Envie de curry",
                "Pho and more": "Pho et plus",
                "Curry and more": "Curry et plus",
                "Korean favorites nearby": "Classiques coréens près de toi",
                "Mediterranean picks": "Sélections méditerranéennes",
                "Fresh bowls nearby": "Bols frais près de toi",
                "Taco time": "Heure des tacos",
                "$0 delivery fee": "Frais de livraison 0 $",
            },
        }

        # Body translations for common templates
        self.body_translations = {
            "es": {
                "🍜 Hot bowls and hand-pulled options ready from spots you'll love": "🍜 Tazones calientes y fideos a mano de lugares que te encantarán",
                "Get dumplings, rice dishes, and bold flavors delivered from top spots": "Dumplings, platos de arroz y sabores intensos de los mejores lugares",
                "Build your perfect bowl with fresh ingredients from places nearby": "Arma tu bowl perfecto con ingredientes frescos cerca de ti",
                "Get bold flavors from restaurants that bring it": "Sabores intensos de restaurantes que lo dan todo",
                "Fresh tacos, burritos, and more ready to order from nearby favorites": "Tacos, burritos y más listos para ordenar de favoritos cercanos",
                "Thin crust to deep dish, they're all just a tap away": "De masa fina a deep dish, a un toque",
                "Classic or loaded, get them delivered hot and ready": "Clásicas o cargadas, llegan calientes y listas",
                "Fresh rolls and rich broths from spots you'll want to reorder": "Rollos frescos y caldos intensos de lugares para repetir",
                "Get bold Thai curries and stir-fries delivered in 30 min": "Curries y salteados tailandeses en 30 min",
                "Fresh Vietnamese flavors from noodle soups to banh mi sandwiches": "Sabores vietnamitas: sopas de fideos y banh mi",
                "Bold Indian flavors from tikka masala to biryani, all nearby": "Sabores indios: tikka masala, biryani y más",
                "From bibimbap to Korean fried chicken, flavors you'll love": "De bibimbap a pollo frito coreano, sabores que amarás",
                "Fresh gyros, falafel, and hummus from spots worth reordering": "Gyros, falafel y hummus de lugares que valen repetir",
                "Build your perfect meal with options that keep it light": "Arma tu comida ligera con opciones frescas",
                "Save on restaurants you order from most with deals ready now": "Ahorra en tus restaurantes de siempre con ofertas listas ahora",
                "Skip the fee on orders from top-rated spots near you": "Evita la tarifa en lugares mejor calificados cerca",
                "Get savings on restaurants you visit most": "Ahorra en los restaurantes que más visitas",
                "Reorder favorites or find something new worth trying": "Repite favoritos o descubre algo nuevo",
            },
            "fr-CA": {
                "🍜 Hot bowls and hand-pulled options ready from spots you'll love": "🍜 Bols chauds et nouilles maison de restos que tu vas adorer",
                "Get dumplings, rice dishes, and bold flavors delivered from top spots": "Dumplings, plats de riz et saveurs audacieuses des meilleurs restos",
                "Build your perfect bowl with fresh ingredients from places nearby": "Compose ton bol parfait avec des ingrédients frais tout près",
                "Get bold flavors from restaurants that bring it": "Saveurs audacieuses de restos qui livrent la dose",
                "Fresh tacos, burritos, and more ready to order from nearby favorites": "Tacos, burritos et plus, prêts à commander des favoris près de toi",
                "Thin crust to deep dish, they're all just a tap away": "De mince à épaisse, à un seul geste",
                "Classic or loaded, get them delivered hot and ready": "Classiques ou chargés, livrés chauds et prêts",
                "Fresh rolls and rich broths from spots you'll want to reorder": "Rouleaux frais et bouillons riches de restos à recommander",
                "Get bold Thai curries and stir-fries delivered in 30 min": "Currys et sautés thaïs en 30 min",
                "Fresh Vietnamese flavors from noodle soups to banh mi sandwiches": "Saveurs vietnamiennes: soupes de nouilles et banh mi",
                "Bold Indian flavors from tikka masala to biryani, all nearby": "Saveurs indiennes: tikka masala, biryani et plus",
                "From bibimbap to Korean fried chicken, flavors you'll love": "De bibimbap au poulet frit coréen, saveurs à aimer",
                "Fresh gyros, falafel, and hummus from spots worth reordering": "Gyros, falafels, houmous de restos à recommander",
                "Build your perfect meal with options that keep it light": "Compose un repas léger avec des options fraîches",
                "Save on restaurants you order from most with deals ready now": "Économise sur tes restos habituels avec des promos prêtes maintenant",
                "Skip the fee on orders from top-rated spots near you": "Zéro frais de livraison sur des restos bien cotés près de toi",
                "Get savings on restaurants you visit most": "Économies sur les restos que tu visites le plus",
                "Reorder favorites or find something new worth trying": "Recommande tes favoris ou essaie quelque chose de nouveau",
            },
        }

    def _detect_locale_key(self, dd_user_locale: str, language: str) -> str:
        """Return canonical locale key: 'es', 'fr-CA', 'en-CA', or 'en-US' default."""
        loc = (dd_user_locale or "").lower()
        lang = (language or "").lower()

        if loc.startswith("es") or lang.startswith("es"):
            return "es"
        if loc.startswith("fr") or lang.startswith("fr"):
            return "fr-CA"
        if loc == "en-ca" or lang == "en-ca":
            return "en-CA"
        return "en-US"

    def localize_copy(self, title: str, body: str, dd_user_locale: str = "", language: str = "") -> Dict[str, str]:
        """
        Localize a title/body pair for supported locales while respecting length limits.
        Returns a dict with 'title', 'body', and 'locale_applied'.
        """
        locale_key = self._detect_locale_key(dd_user_locale, language)

        if locale_key == "en-CA":
            body_ca = body
            body_ca = body_ca.replace("favorites", "favourites").replace("flavors", "flavours")
            title_ca = title
            return {"title": title_ca, "body": body_ca, "locale_applied": locale_key}

        translations_t = self.title_translations.get(locale_key, {})
        translations_b = self.body_translations.get(locale_key, {})

        localized_title = translations_t.get(title, title)
        localized_body = translations_b.get(body, body)

        # Enforce hard limits
        if len(localized_title) >= 35:
            localized_title = localized_title[:34]
        if len(localized_body) > 140:
            localized_body = localized_body[:140]

        return {"title": localized_title, "body": localized_body, "locale_applied": locale_key}
    
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
