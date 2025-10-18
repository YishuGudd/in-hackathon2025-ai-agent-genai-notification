"""
DoorDash Notification Generator Module

Version: 1.4.0 - Updated restrictions (min_score=82, no promo phrases, short dashes only)
"""

import json
import re
import os
from typing import List, Dict, Optional


class NotificationGenerator:
    """
    Generate personalized push notifications for DoorDash consumers.
    
    Version History:
    - v1.0: Initial release with dietary guardrails
    - v1.1: Added mild spicy guardrail
    - v1.2: Added pricing filter for smart deal targeting
    - v1.3: Added locale-aware copy helpers (Spanish, French-CA, English-CA)
    - v1.4: Updated restrictions (min_score=82, removed promo phrases, short dashes, no cuisine in titles, auto url+image_url)
    """
    
    __version__ = "1.4.0"
    
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

        # Optional: keyword -> image URL mapping for enriching outputs
        self.keyword_to_image: Dict[str, str] = {}
        try:
            mapping_path = os.path.join(os.path.dirname(__file__), '..', 'keyword_image_map.json')
            if os.path.exists(mapping_path):
                with open(mapping_path, 'r', encoding='utf-8') as f:
                    raw_map = json.load(f)
                    self.keyword_to_image = {str(k).lower(): str(v) for k, v in raw_map.items()}
        except Exception:
            self.keyword_to_image = {}

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
            return {"title": title_ca, "body": body_ca, "locale_applied": locale_key, "was_truncated": False}

        translations_t = self.title_translations.get(locale_key, {})
        translations_b = self.body_translations.get(locale_key, {})

        localized_title = translations_t.get(title, title)
        localized_body = translations_b.get(body, body)

        # Enforce hard limits and record truncation
        truncated = False
        if len(localized_title) >= 35:
            localized_title = localized_title[:34]
            truncated = True
        if len(localized_body) > 140:
            localized_body = localized_body[:140]
            truncated = True

        return {"title": localized_title, "body": localized_body, "locale_applied": locale_key, "was_truncated": truncated}
    
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
        min_score: int = 82,
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
        top = filtered[:max_count]
        
        # Enrich with URL and image URL for downstream consumers
        for n in top:
            kw = (n.get('keyword') or '').strip()
            if kw:
                n['url'] = self.format_for_doordash_url(kw)
                n['image_url'] = self.keyword_to_image.get(kw.lower()) if self.keyword_to_image else None
            else:
                n['url'] = None
                n['image_url'] = None
        
        return top
    
    def _add_noodle_notifications(self, notifications: List, food: str, cuisine: str):
        """Add noodle-related notifications"""
        if 'noodle' in food or 'noodle' in cuisine:
            body_templates = [
                "🍜 Hot bowls and hand-pulled options ready from spots you'll love",
                "🍜 Fresh noodles delivered fast from places you'll reorder",
                "🍜 Hand-pulled noodles and hot bowls, made easy",
            ]
            body_text = self._choose_variant(body_templates, 'noodles')
            body_text = self._ensure_keyword_in_body('noodles', body_text)
            notifications.append({
                "title": "Noodle cravings covered",
                "body": body_text,
                "keyword": "noodles",
                "score": 98
            })
    
    def _add_cuisine_notifications(self, notifications: List, cuisine: str, food: str, taste: str):
        """Add cuisine-specific notifications"""
        
        if 'chinese' in cuisine:
            body_templates = [
                "Get dumplings, rice dishes, and bold flavors delivered from top spots",
                "Top Chinese spots near you with dumplings and rice dishes",
                "Bold Chinese flavors from nearby favorites, delivered",
            ]
            body_text = self._choose_variant(body_templates, 'Chinese food')
            body_text = self._ensure_keyword_in_body('Chinese food', body_text)
            notifications.append({
                "title": "Skip the schlep",
                "body": body_text,
                "keyword": "Chinese food",
                "score": 96
            })
        
        if 'bowl' in food or 'rice' in food or 'poke' in food or 'hawaiian' in cuisine:
            body_templates = [
                "Build your perfect bowl with fresh ingredients from places nearby",
                "Custom rice bowls with fresh picks from spots around you",
                "Fresh rice bowls, built your way and delivered",
            ]
            body_text = self._choose_variant(body_templates, 'rice bowls')
            body_text = self._ensure_keyword_in_body('rice bowls', body_text)
            notifications.append({
                "title": "You pick. We roll",
                "body": body_text,
                "keyword": "rice bowls",
                "score": 94
            })
        
        if 'spicy' in taste or 'bold' in taste:
            body_templates = [
                "Get bold flavors from restaurants that bring it",
                "Spicy picks ready to deliver from places you’ll like",
                "Turn up the heat with spicy food near you",
            ]
            body_text = self._choose_variant(body_templates, 'spicy food')
            body_text = self._ensure_keyword_in_body('spicy food', body_text)
            notifications.append({
                "title": "Heat seekers wanted",
                "body": body_text,
                "keyword": "spicy food",
                "score": 92
            })
        
        if 'mexican' in cuisine or 'latin' in cuisine:
            body_templates = [
                "Fresh tacos, burritos, and more ready to order from nearby favorites",
                "Tacos and burritos from top Mexican spots near you",
                "Mexican classics, delivered from places you’ll reorder",
            ]
            body_text = self._choose_variant(body_templates, 'Mexican')
            body_text = self._ensure_keyword_in_body('Mexican', body_text)
            notifications.append({
                "title": "Taco time",
                "body": body_text,
                "keyword": "Mexican",
                "score": 90
            })
        
        if 'pizza' in food or 'italian' in cuisine:
            body_templates = [
                "Thin crust to deep dish, they're all just a tap away",
                "Hot pizza from top spots, just a tap away",
                "Classic and new pizza picks delivered fast",
            ]
            body_text = self._choose_variant(body_templates, 'pizza')
            body_text = self._ensure_keyword_in_body('pizza', body_text)
            notifications.append({
                "title": "Pizza. Done",
                "body": body_text,
                "keyword": "pizza",
                "score": 88
            })
        
        if 'burger' in food or 'sandwich' in food:
            body_templates = [
                "Classic or loaded, get them delivered hot and ready",
                "Stacked burgers, cooked right and delivered",
                "Burgers your way, hot and ready at your door",
            ]
            body_text = self._choose_variant(body_templates, 'burgers')
            body_text = self._ensure_keyword_in_body('burgers', body_text)
            notifications.append({
                "title": "Burgers your way",
                "body": body_text,
                "keyword": "burgers",
                "score": 86
            })
        
        if 'japanese' in cuisine or 'sushi' in food or 'ramen' in food:
            body_templates = [
                "Fresh rolls and rich broths from spots you'll want to reorder",
                "Sushi and ramen from nearby favorites, delivered",
                "Rolls and ramen, prepped fast from top Japanese spots",
            ]
            body_text = self._choose_variant(body_templates, 'Japanese food')
            body_text = self._ensure_keyword_in_body('Japanese food', body_text)
            notifications.append({
                "title": "Sushi and ramen ready",
                "body": body_text,
                "keyword": "Japanese food",
                "score": 84
            })
        
        if 'thai' in cuisine:
            body_templates = [
                "Get bold Thai curries and stir-fries delivered in 30 min",
                "Thai curries and stir-fries, ready to deliver",
                "Thai flavors from nearby spots, delivered quick",
            ]
            body_text = self._choose_variant(body_templates, 'Thai food')
            body_text = self._ensure_keyword_in_body('Thai food', body_text)
            notifications.append({
                "title": "Curry cravings",
                "body": body_text,
                "keyword": "Thai food",
                "score": 82
            })
        
        if 'vietnamese' in cuisine or 'pho' in food:
            body_templates = [
                "Fresh Vietnamese flavors from noodle soups to banh mi sandwiches",
                "Pho and banh mi from nearby favorites, delivered",
                "Vietnamese picks like pho and banh mi, made easy",
            ]
            body_text = self._choose_variant(body_templates, 'Vietnamese food')
            body_text = self._ensure_keyword_in_body('Vietnamese food', body_text)
            notifications.append({
                "title": "Pho and more",
                "body": body_text,
                "keyword": "Vietnamese food",
                "score": 82
            })
        
        if 'indian' in cuisine:
            body_templates = [
                "Bold Indian flavors from tikka masala to biryani, all nearby",
                "Biryani and tikka masala from top Indian spots",
                "Indian favorites delivered from places you’ll reorder",
            ]
            body_text = self._choose_variant(body_templates, 'Indian food')
            body_text = self._ensure_keyword_in_body('Indian food', body_text)
            notifications.append({
                "title": "Curry and more",
                "body": body_text,
                "keyword": "Indian food",
                "score": 82
            })
        
        if 'korean' in cuisine:
            body_templates = [
                "From bibimbap to Korean fried chicken, flavors you'll love",
                "Bibimbap and Korean fried chicken, delivered hot",
                "Korean favorites near you, ready to deliver",
            ]
            body_text = self._choose_variant(body_templates, 'Korean food')
            body_text = self._ensure_keyword_in_body('Korean food', body_text)
            notifications.append({
                "title": "Favorites nearby",
                "body": body_text,
                "keyword": "Korean food",
                "score": 82
            })
        
        if 'mediterranean' in cuisine or 'greek' in cuisine:
            body_templates = [
                "Fresh gyros, falafel, and hummus from spots worth reordering",
                "Mediterranean bowls and plates from nearby favorites",
                "Gyros, falafel, hummus - Mediterranean picks delivered",
            ]
            body_text = self._choose_variant(body_templates, 'Mediterranean food')
            body_text = self._ensure_keyword_in_body('Mediterranean food', body_text)
            notifications.append({
                "title": "Fresh picks nearby",
                "body": body_text,
                "keyword": "Mediterranean food",
                "score": 82
            })
        
        if 'salad' in food or 'healthy' in food:
            body_templates = [
                "Build your perfect meal with options that keep it light",
                "Light and fresh options ready to go",
                "Healthy picks you can customize and deliver",
            ]
            body_text = self._choose_variant(body_templates, 'healthy food')
            body_text = self._ensure_keyword_in_body('healthy food', body_text)
            notifications.append({
                "title": "Fresh bowls nearby",
                "body": body_text,
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
            # Boost deal notifications for value-conscious consumers (avoid specific promo phrases)
            body_templates_deals = [
                "Save on restaurants you order from most with deals ready now",
                "Deals you’ll actually use from places you reorder",
            ]
            body_text_deals = self._choose_variant(body_templates_deals, 'food deals')
            body_text_deals = self._ensure_keyword_in_body('food deals', body_text_deals)
            notifications.append({
                "title": "Deal dropped. You're up",
                "body": body_text_deals,
                "keyword": "food deals",
                "score": 95  # Boosted score
            })
        else:
            # Lower score for balanced spenders (will likely be filtered out)
            body_templates_deals_low = [
                "Get savings on restaurants you visit most",
                "Deals available from places you visit",
            ]
            body_text_deals_low = self._choose_variant(body_templates_deals_low, 'food deals')
            body_text_deals_low = self._ensure_keyword_in_body('food deals', body_text_deals_low)
            notifications.append({
                "title": "Deal dropped. You're up",
                "body": body_text_deals_low,
                "keyword": "food deals",
                "score": 78  # Below typical threshold
            })
    
    def _add_universal_notifications(self, notifications: List):
        """Add universal notifications that work for all consumers"""
        notifications.append({
            "title": "Your go-tos are here",
            "body": self._ensure_keyword_in_body('restaurants', "Reorder favorites or find something new worth trying"),
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

    # --- Helpers for diversity and keyword inclusion ---
    def _choose_variant(self, templates: List[str], keyword: str) -> str:
        if not templates:
            return ''
        idx = sum(ord(c) for c in (keyword or '')) % len(templates)
        return templates[idx]

    def _ensure_keyword_in_body(self, keyword: str, body: str) -> str:
        if not keyword:
            return body
        # if already present (case-insensitive), return
        if keyword.lower() in (body or '').lower():
            return body
        # try appending with a short separator (use short dash, avoid long dash)
        sep = " - "
        addition = sep + keyword
        if len(body) + len(addition) <= 140:
            return body + addition
        # fallback to simple space
        addition = " " + keyword
        if len(body) + len(addition) <= 140:
            return body + addition
        # final fallback: truncate to fit
        max_len = 140 - (len(keyword) + 1)
        if max_len > 0:
            return body[:max_len].rstrip() + " " + keyword
        return body  # as-is if pathological
