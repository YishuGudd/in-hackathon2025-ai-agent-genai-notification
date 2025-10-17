## gRPC Requests

### DebugDeliverNotificationContent

Use the saved JSON payload and required headers to invoke the debug delivery endpoint:

```bash
grpcurl -plaintext \
  -H 'fpn-send-now: true' \
  -H 'baggage: tid=doortest:default,dd-routing-context=%5B%7B%22service%22%3A%22growth-service%22%2C%22app%22%3A%22notification-platform%22%2C%22host%22%3A%22growth-service-notification-platform-sandbox-lei-np%22%2C%22port%22%3A%2250051%22%7D%5D' \
  -d @ 127.0.0.1:50051 doordash.growth.intelligent.v1.NotificationContentService/DebugDeliverNotificationContent \
  < grpc_requests/DebugDeliverNotificationContent.sample.json
```

Notes:
- Edit `grpc_requests/DebugDeliverNotificationContent.sample.json` to change `audienceId`, `programName`, or `specifications`.
- Headers:
  - `fpn-send-now: true` triggers immediate send.
  - `baggage: ...` carries routing context for the request path.

---

### MCP Client: debug_deliver (Cursor, stdio)

This repo includes a Python MCP stdio server exposing a tool named `debug_deliver` that shells out to `grpcurl` via `grpc_requests/call_debug_deliver.py`.

Setup:
1. Ensure venv and dependencies are installed:
```bash
python3 -m venv venv
./venv/bin/pip install mcp "pydantic>=2.8.0"
```

2. Start the MCP server:
```bash
./venv/bin/python grpc_requests/mcp_debug_server.py
```

3. Configure Cursor (if not already): add server `debug_deliver` in your MCP config, pointing to stdio command:
```json
{
  "mcpServers": {
    "debug_deliver": {
      "command": "/absolute/path/to/repo/venv/bin/python",
      "args": ["grpc_requests/mcp_debug_server.py"],
      "cwd": "/absolute/path/to/repo",
      "env": { "PYTHONUNBUFFERED": "1" }
    }
  }
}
```

Use in Cursor:
- Tool name: `debug_deliver`
- Minimal input:
```json
{ "audience_id": "1036296113" }
```
- Optional inputs:
  - `host` (default `127.0.0.1:50051`)
  - `entry_uuid`
  - `program_name`
  - `send_now` (boolean, default true)
  - `baggage` (string)

The tool returns the raw JSON response from the gRPC call.


