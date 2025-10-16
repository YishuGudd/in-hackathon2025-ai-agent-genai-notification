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


