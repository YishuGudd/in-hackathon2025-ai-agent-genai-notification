"""
DoorDash Notification Generation MCP Server - Standalone Version

This MCP server generates personalized push notifications for DoorDash consumers
based on their GenAI profiles from Snowflake.

Run: python notification_server_standalone.py
"""

import os
import json
import logging
import asyncio
from typing import Any
from dotenv import load_dotenv

# Load environment first
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from mcp.server import Server
from mcp.types import Tool, TextContent, Resource
from pydantic import AnyUrl
import snowflake.connector

from notification_generator import NotificationGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("notification-server")


async def main():
    """Main entry point for the notification server"""
    server = Server("doordash-notification-generator")
    generator = NotificationGenerator()
    
    # Snowflake connection params
    def get_snowflake_connection():
        return snowflake.connector.connect(
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            user=os.getenv('SNOWFLAKE_USER'),
            authenticator=os.getenv('SNOWFLAKE_AUTHENTICATOR'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA'),
            role=os.getenv('SNOWFLAKE_ROLE')
        )
    
    # List available tools
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="generate_consumer_notifications",
                description="Generate personalized DoorDash push notifications for a consumer based on their GenAI profile. Applies DoorDash brand voice, dietary guardrails, and mild spicy filter. Returns JSON with notifications ranked by score.",
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
                        }
                    },
                    "required": ["consumer_id"]
                }
            ),
            Tool(
                name="validate_notification",
                description="Validate a notification against DoorDash brand guidelines and format restrictions. Checks title length, body length, and compliance with all content rules.",
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
    
    # Handle tool calls
    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> list[TextContent]:
        if name == "generate_consumer_notifications":
            consumer_id = arguments.get("consumer_id")
            min_score = arguments.get("min_score", 80)
            max_count = arguments.get("max_count", 10)
            
            try:
                # Connect to Snowflake
                conn = get_snowflake_connection()
                cursor = conn.cursor()
                
                # Query profile from SHADOW table
                query = f"SELECT CONSUMER_ID, PROFILE FROM PRODDB.ML.GENAI_CX_PROFILE_SHADOW WHERE CONSUMER_ID = {consumer_id}"
                cursor.execute(query)
                result = cursor.fetchone()
                
                if not result:
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "consumer_id": consumer_id,
                            "status": "error",
                            "message": f"No profile found for consumer {consumer_id}",
                            "notifications": []
                        }, indent=2)
                    )]
                
                _, profile_json = result
                profile = json.loads(profile_json)
                
                # Generate notifications
                notifications = generator.generate_notifications(profile, min_score, max_count)
                
                # Add URLs to notifications
                for notif in notifications:
                    notif['url'] = generator.format_for_doordash_url(notif['keyword'])
                    notif['title_length'] = len(notif['title'])
                    notif['body_length'] = len(notif['body'])
                
                overall = profile.get('overall_profile', {})
                dietary = overall.get('dietary_preferences', {})
                
                result_data = {
                    "consumer_id": consumer_id,
                    "status": "success",
                    "profile_summary": {
                        "cuisines": overall.get('cuisine_preferences', '')[:100],
                        "foods": overall.get('food_preferences', '')[:100],
                        "taste": overall.get('taste_preference', '')[:80],
                        "dietary": dietary.get('preferred_dietary_preference', 'none')
                    },
                    "notifications": notifications,
                    "count": len(notifications),
                    "avg_score": sum(n['score'] for n in notifications) / len(notifications) if notifications else 0
                }
                
                cursor.close()
                conn.close()
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result_data, indent=2, ensure_ascii=False)
                )]
                
            except Exception as e:
                logger.error(f"Error generating notifications: {e}")
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "consumer_id": consumer_id,
                        "status": "error",
                        "message": str(e)
                    }, indent=2)
                )]
        
        elif name == "validate_notification":
            title = arguments.get("title", "")
            body = arguments.get("body", "")
            
            result = generator.validate_notification(title, body)
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        return [TextContent(type="text", text="Unknown tool")]
    
    # List resources
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
    
    # Read resources
    @server.read_resource()
    async def read_resource(uri: AnyUrl) -> str:
        if str(uri) == "guidelines://brand-voice":
            return """DoorDash Brand Voice for Push Notifications

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

Version: 1.1.0 (includes mild spicy guardrail)"""
        
        elif str(uri) == "guidelines://restrictions":
            return """Push Notification Restrictions

Format:
• Title < 35 characters
• Body ≤ 140 characters
• Sentence case, JSON output

Must NOT include:
• Exclamation points
• DoorDash mentions
• Hashtags
• Meal time references
• "Authentic" descriptors
• Hyperbolic language (mouthwatering, tempting, etc.)

NEW v1.1:
• If cx profile contains 'mild spicy' taste, do not recommend 'spicy' keyword

URLs include: &filterQuery-deals-fill=true"""
        
        return ""
    
    # Run the server
    from mcp.server.stdio import stdio_server
    
    logger.info("Starting DoorDash Notification Generator MCP Server v1.1...")
    logger.info(f"Connected to Snowflake: {os.getenv('SNOWFLAKE_DATABASE')}")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
