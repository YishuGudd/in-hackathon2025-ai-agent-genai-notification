"""
DoorDash Notification Generation MCP Server

This MCP server provides tools for generating personalized push notifications
for DoorDash consumers based on their GenAI profiles from Snowflake.
"""

import os
import json
import logging
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent, Resource
from pydantic import AnyUrl
import asyncio

from db_client import SnowflakeClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("notification-server")

class NotificationGenerator:
    """Generate personalized notifications with brand guidelines and dietary guardrails"""
    
    def __init__(self, db_client: SnowflakeClient):
        self.db = db_client
        
    def passes_dietary_guardrail(self, notification: dict, dietary_pref: str) -> bool:
        """Check if notification respects dietary preferences"""
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
    
    def generate_notifications(self, profile: dict, min_score: int = 80, max_count: int = 10) -> list:
        """Generate personalized notifications following DoorDash brand voice"""
        overall = profile.get('overall_profile', {})
        cuisine = overall.get('cuisine_preferences', '').lower()
        food = overall.get('food_preferences', '').lower()
        taste = overall.get('taste_preference', '').lower()
        dietary = overall.get('dietary_preferences', {})
        preferred_dietary = dietary.get('preferred_dietary_preference', '')
        
        all_notifications = []
        
        # High-scoring notifications (98-95) - Perfect profile matches
        if 'noodle' in food or 'noodle' in cuisine:
            all_notifications.append({
                "title": "Noodle cravings covered",
                "body": "🍜 Hot bowls and hand-pulled options ready from spots you'll love",
                "keyword": "noodles",
                "score": 98
            })
        
        if 'chinese' in cuisine:
            all_notifications.append({
                "title": "Skip the schlep",
                "body": "Get dumplings, rice dishes, and bold flavors delivered from top spots",
                "keyword": "Chinese food",
                "score": 96
            })
        
        if 'bowl' in food or 'rice' in food or 'poke' in food or 'hawaiian' in cuisine:
            all_notifications.append({
                "title": "You pick. We roll",
                "body": "Build your perfect bowl with fresh ingredients from places nearby",
                "keyword": "rice bowls",
                "score": 94
            })
        
        if 'spicy' in taste or 'bold' in taste:
            all_notifications.append({
                "title": "Heat seekers wanted",
                "body": "Get bold, spicy flavors from restaurants that bring it",
                "keyword": "spicy food",
                "score": 92
            })
        
        if 'mexican' in cuisine or 'latin' in cuisine:
            all_notifications.append({
                "title": "Taco time",
                "body": "Fresh tacos, burritos, and more ready to order from nearby favorites",
                "keyword": "Mexican",
                "score": 90
            })
        
        if 'pizza' in food or 'italian' in cuisine:
            all_notifications.append({
                "title": "Pizza. Done",
                "body": "Thin crust to deep dish, they're all just a tap away",
                "keyword": "pizza",
                "score": 88
            })
        
        if 'burger' in food or 'sandwich' in food:
            all_notifications.append({
                "title": "Burgers your way",
                "body": "Classic or loaded, get them delivered hot and ready",
                "keyword": "burgers",
                "score": 86
            })
        
        if 'japanese' in cuisine or 'sushi' in food or 'ramen' in food:
            all_notifications.append({
                "title": "Sushi and ramen ready",
                "body": "Fresh rolls and rich broths from spots you'll want to reorder",
                "keyword": "Japanese food",
                "score": 84
            })
        
        if 'thai' in cuisine:
            all_notifications.append({
                "title": "Curry cravings",
                "body": "Get bold Thai curries and stir-fries delivered in 30 min",
                "keyword": "Thai food",
                "score": 82
            })
        
        if 'vietnamese' in cuisine or 'pho' in food:
            all_notifications.append({
                "title": "Pho and more",
                "body": "Fresh Vietnamese flavors from noodle soups to banh mi sandwiches",
                "keyword": "Vietnamese food",
                "score": 82
            })
        
        if 'indian' in cuisine or 'curry' in food:
            all_notifications.append({
                "title": "Curry and more",
                "body": "Bold Indian flavors from tikka masala to biryani, all nearby",
                "keyword": "Indian food",
                "score": 82
            })
        
        if 'korean' in cuisine:
            all_notifications.append({
                "title": "Korean favorites nearby",
                "body": "From bibimbap to Korean fried chicken, flavors you'll love",
                "keyword": "Korean food",
                "score": 82
            })
        
        if 'mediterranean' in cuisine or 'greek' in cuisine:
            all_notifications.append({
                "title": "Mediterranean picks",
                "body": "Fresh gyros, falafel, and hummus from spots worth reordering",
                "keyword": "Mediterranean food",
                "score": 82
            })
        
        # Universal notifications (80+)
        all_notifications.append({
            "title": "Your go-tos are here",
            "body": "Reorder favorites or find something new worth trying",
            "keyword": "restaurants",
            "score": 80
        })
        
        if 'salad' in food or 'healthy' in food:
            all_notifications.append({
                "title": "Fresh bowls nearby",
                "body": "Build your perfect meal with options that keep it light",
                "keyword": "healthy food",
                "score": 80
            })
        
        # Apply dietary guardrails
        filtered_notifications = [
            n for n in all_notifications 
            if self.passes_dietary_guardrail(n, preferred_dietary)
        ]
        
        # Filter by minimum score and take top N
        filtered_notifications = [n for n in filtered_notifications if n['score'] >= min_score]
        filtered_notifications.sort(key=lambda x: x['score'], reverse=True)
        
        return filtered_notifications[:max_count]
    
    async def generate_for_consumer(self, consumer_id: str, min_score: int = 80, 
                                   max_count: int = 10, use_shadow: bool = True) -> dict:
        """Generate notifications for a specific consumer"""
        table = "PRODDB.ML.GENAI_CX_PROFILE_SHADOW" if use_shadow else "PRODDB.ML.GENAI_CX_PROFILE"
        
        query = f"SELECT CONSUMER_ID, PROFILE FROM {table} WHERE CONSUMER_ID = {consumer_id}"
        result = await self.db.execute_read_query(query)
        
        if not result or len(result) == 0:
            return {
                "consumer_id": consumer_id,
                "status": "error",
                "message": f"No profile found in {table}",
                "notifications": []
            }
        
        profile_json = result[0].get('PROFILE')
        profile = json.loads(profile_json)
        
        notifications = self.generate_notifications(profile, min_score, max_count)
        
        overall = profile.get('overall_profile', {})
        dietary = overall.get('dietary_preferences', {})
        
        return {
            "consumer_id": consumer_id,
            "status": "success",
            "profile_summary": {
                "cuisines": overall.get('cuisine_preferences', '')[:100],
                "foods": overall.get('food_preferences', '')[:100],
                "taste": overall.get('taste_preference', '')[:80],
                "dietary": dietary.get('preferred_dietary_preference', 'none')
            },
            "notifications": [
                {
                    **notif,
                    "url": f"https://www.doordash.com/search/store/{notif['keyword'].replace(' ', '%20')}?event_type=search&filterQuery-vertical_ids=1",
                    "title_length": len(notif['title']),
                    "body_length": len(notif['body'])
                }
                for notif in notifications
            ],
            "count": len(notifications),
            "avg_score": sum(n['score'] for n in notifications) / len(notifications) if notifications else 0
        }


async def main():
    """Main entry point for the notification server"""
    server = Server("doordash-notification-generator")
    db_client = SnowflakeClient()
    generator = NotificationGenerator(db_client)
    
    # Tool: Generate notifications for a single consumer
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="generate_consumer_notifications",
                description="Generate personalized DoorDash push notifications for a consumer based on their GenAI profile. Applies DoorDash brand voice, dietary guardrails, and quality filters.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "consumer_id": {
                            "type": "string",
                            "description": "Consumer ID to generate notifications for"
                        },
                        "min_score": {
                            "type": "integer",
                            "description": "Minimum score threshold (default: 80)",
                            "default": 80
                        },
                        "max_count": {
                            "type": "integer",
                            "description": "Maximum number of notifications to return (default: 10)",
                            "default": 10
                        },
                        "use_shadow": {
                            "type": "boolean",
                            "description": "Use SHADOW table instead of main table (default: true)",
                            "default": True
                        }
                    },
                    "required": ["consumer_id"]
                }
            ),
            Tool(
                name="batch_generate_notifications",
                description="Generate notifications for multiple consumers at once. Returns CSV-formatted data.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "consumer_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of consumer IDs"
                        },
                        "min_score": {
                            "type": "integer",
                            "description": "Minimum score threshold (default: 80)",
                            "default": 80
                        }
                    },
                    "required": ["consumer_ids"]
                }
            ),
            Tool(
                name="validate_notification",
                description="Validate a notification against DoorDash brand guidelines and format restrictions",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Notification title to validate"
                        },
                        "body": {
                            "type": "string",
                            "description": "Notification body to validate"
                        }
                    },
                    "required": ["title", "body"]
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> list[TextContent]:
        if name == "generate_consumer_notifications":
            consumer_id = arguments.get("consumer_id")
            min_score = arguments.get("min_score", 80)
            max_count = arguments.get("max_count", 10)
            use_shadow = arguments.get("use_shadow", True)
            
            result = await generator.generate_for_consumer(
                consumer_id, min_score, max_count, use_shadow
            )
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
        
        elif name == "batch_generate_notifications":
            consumer_ids = arguments.get("consumer_ids", [])
            min_score = arguments.get("min_score", 80)
            
            results = []
            for consumer_id in consumer_ids:
                result = await generator.generate_for_consumer(
                    consumer_id, min_score, 10, True
                )
                results.append(result)
            
            return [TextContent(
                type="text",
                text=json.dumps(results, indent=2, ensure_ascii=False)
            )]
        
        elif name == "validate_notification":
            title = arguments.get("title", "")
            body = arguments.get("body", "")
            
            issues = []
            
            # Format validation
            if len(title) >= 35:
                issues.append(f"Title too long: {len(title)}/35 characters")
            if len(body) > 140:
                issues.append(f"Body too long: {len(body)}/140 characters")
            
            # Content restrictions
            if '!' in title or '!' in body:
                issues.append("Contains exclamation points (not allowed)")
            if title and title[-1] in '.,:;' and title[-1] != '?':
                issues.append("Title has end punctuation (except ? allowed)")
            if '#' in title or '#' in body:
                issues.append("Contains hashtags (not allowed)")
            if 'DoorDash' in title or 'DoorDash' in body:
                issues.append("Mentions DoorDash (not allowed)")
            
            # Hyperbolic language
            hyperbolic = ['mouthwatering', 'scrumptious', 'tantalizing', 'tempting', 'indulge', 'savor']
            if any(word in title.lower() or word in body.lower() for word in hyperbolic):
                issues.append("Contains overly salesy language")
            
            # Meal time inference
            meal_times = ['breakfast', 'brunch', 'lunch', 'dinner']
            if any(meal in title.lower() or meal in body.lower() for meal in meal_times):
                issues.append("Infers meal time (not allowed)")
            
            validation_result = {
                "title": title,
                "body": body,
                "title_length": len(title),
                "body_length": len(body),
                "is_valid": len(issues) == 0,
                "issues": issues
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(validation_result, indent=2)
            )]
        
        return [TextContent(type="text", text="Unknown tool")]
    
    # Resources for brand guidelines
    @server.list_resources()
    async def list_resources() -> list[Resource]:
        return [
            Resource(
                uri=AnyUrl("guidelines://brand-voice"),
                name="DoorDash Brand Voice Guidelines",
                mimeType="text/plain",
                description="Core brand voice and tone guidelines for DoorDash notifications"
            ),
            Resource(
                uri=AnyUrl("guidelines://restrictions"),
                name="Notification Format Restrictions",
                mimeType="text/plain",
                description="Complete list of format and content restrictions"
            )
        ]
    
    @server.read_resource()
    async def read_resource(uri: AnyUrl) -> str:
        if str(uri) == "guidelines://brand-voice":
            return """
DoorDash Brand Voice for Push Notifications

Core Principles:
• Conversational: We write like we talk — easy, approachable, and clear
• Genuine: Never stiff, never salesy, never trying too hard
• Straightforward: Use everyday, familiar language
• Lightly playful: Use charm or delight when it fits

Approved Brand Phrases:
• "Skip the schlep"
• "You pick. We roll"
• "Deal dropped. You're up"
• "Your go-tos are here"
• "More you time. Less to-do time"

Tone Guidelines:
• Friendly, but not forced
• Lightly playful when appropriate
• Realistic optimism
• Delightful when possible
"""
        elif str(uri) == "guidelines://restrictions":
            return """
Push Notification Restrictions

Format:
• Title < 35 characters
• Body ≤ 140 characters
• Sentence case
• JSON format output

Must NOT:
• Use exclamation points
• Mention DoorDash
• Use hashtags
• Mention cuisine in title (unless provided)
• Include end punctuation in title (except ?)
• Use hyperbolic language (mouthwatering, tempting, etc.)
• Infer meal times (breakfast, lunch, dinner)
• Use "authentic" to describe food
• Use emoji redundantly
• Mention same item twice

Must HAVE:
• Third-person pronouns (they, them, their)
• Max 1 emoji per notification (if it adds value)
• Eighth-grade reading level
• Conversational, casual tone
"""
        return ""
    
    # Run the server
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

