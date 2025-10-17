# Running the MCP Server

## Simple Way (Recommended)

Just run the notification server directly:

```bash
cd notification_generator
export SNOWFLAKE_ACCOUNT=DOORDASH
export SNOWFLAKE_USER=your.name@doordash.com
export SNOWFLAKE_AUTHENTICATOR=externalbrowser
export SNOWFLAKE_WAREHOUSE=ADHOC
export SNOWFLAKE_DATABASE=PRODDB
export SNOWFLAKE_SCHEMA=PUBLIC
export SNOWFLAKE_ROLE=YOUR_ROLE
export GENAI_PROFILE_TABLE=PRODDB.ML.GENAI_CX_PROFILE_SHADOW  # optional override
python notification_server.py
```

That's it! The server will start and be ready for Claude Desktop connections.

## What Happens When You Run It

```
================================================================================
🚀 DoorDash Notification Generator MCP Server
================================================================================

✓ Environment configured
Starting MCP server...
Ready for connections...
```

The server exposes these tools:
- `generate_consumer_notifications` - Generate for single consumer
- `batch_generate_notifications` - Generate for multiple consumers  
- `validate_notification` - Validate against brand guidelines

## Using with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "doordash_notifications": {
      "command": "python",
      "args": [
        "/full/path/to/notification_generator/notification_server.py"
      ]
    }
  }
}
```

Then use in Claude:
```
"Generate notifications for consumer 1193328057"
"Validate this notification: [title] / [body]"
```

## Troubleshooting

**Error: Missing environment variables**
→ Make sure you have a `.env` file configured (copy from `../.env.example`)

**Error: notification_server.py not found**
→ Make sure you're in the `notification_generator` directory

**Error: Cannot connect to Snowflake**
→ Check your `.env` credentials and SSO authentication

## Note

No need for a separate `run_mcp.py` - just run `notification_server.py` directly!
