"""
Quick Start Script for DoorDash Notification Generator

Usage:
  python quick_start.py <consumer_id>

Example:
  python quick_start.py 1193328057
"""

import sys
import json
import os
from dotenv import load_dotenv
import snowflake.connector

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))
from notification_generator import NotificationGenerator

load_dotenv()

def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_start.py <consumer_id>")
        sys.exit(1)
    
    consumer_id = sys.argv[1]
    
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        user=os.getenv('SNOWFLAKE_USER'),
        authenticator=os.getenv('SNOWFLAKE_AUTHENTICATOR'),
        warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
        database=os.getenv('SNOWFLAKE_DATABASE'),
        schema=os.getenv('SNOWFLAKE_SCHEMA'),
        role=os.getenv('SNOWFLAKE_ROLE')
    )
    
    cursor = conn.cursor()
    
    # Query profile
    query = f"SELECT CONSUMER_ID, PROFILE FROM PRODDB.ML.GENAI_CX_PROFILE_SHADOW WHERE CONSUMER_ID = {consumer_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    
    if not result:
        print(f"❌ No profile found for consumer {consumer_id}")
        sys.exit(1)
    
    _, profile_json = result
    profile = json.loads(profile_json)
    
    # Generate notifications
    generator = NotificationGenerator()
    notifications = generator.generate_notifications(profile, min_score=80, max_count=10)
    
    # Display results
    print(f"\n{'='*80}")
    print(f"CONSUMER {consumer_id} - GENERATED {len(notifications)} NOTIFICATIONS")
    print(f"{'='*80}\n")
    
    overall = profile.get('overall_profile', {})
    dietary = overall.get('dietary_preferences', {})
    
    print(f"Profile:")
    print(f"  Cuisines: {overall.get('cuisine_preferences', '')[:80]}...")
    print(f"  Foods: {overall.get('food_preferences', '')[:80]}...")
    print(f"  Dietary: {dietary.get('preferred_dietary_preference', 'none')}\n")
    
    print(f"Top {len(notifications)} Notifications (Score >= 80):\n")
    
    for i, notif in enumerate(notifications, 1):
        rank = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        print(f"{rank} SCORE: {notif['score']}/100")
        print(f"   Title: {notif['title']}")
        print(f"   Body: {notif['body']}")
        print(f"   Keyword: {notif['keyword']}")
        url = generator.format_for_doordash_url(notif['keyword'])
        print(f"   URL: {url}\n")
    
    conn.close()

if __name__ == "__main__":
    main()
