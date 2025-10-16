#!/usr/bin/env python3
"""
Helper to invoke DebugDeliverNotificationContent with a dynamic audienceId.

Examples:
  python grpc_requests/call_debug_deliver.py --alias lei
  python grpc_requests/call_debug_deliver.py --audience-id 1036296113
  python grpc_requests/call_debug_deliver.py --audience-id 1036296113 --host 127.0.0.1:50051
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_TEMPLATE = Path(__file__).with_name("DebugDeliverNotificationContent.sample.json")
DEFAULT_HOST = "127.0.0.1:50051"
SERVICE_METHOD = (
    "doordash.growth.intelligent.v1.NotificationContentService/DebugDeliverNotificationContent"
)

# Known aliases for convenience
ALIAS_TO_ID = {
    "lei": "1036296113",
    "annie": "661703925",
    "supriya": "1951699662",
    "akash": "1860023262",
}


def build_payload(template_path: Path, audience_id: str, entry_uuid: str | None = None,
                  program_name: str | None = None) -> dict:
    with open(template_path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    payload["audienceId"] = audience_id
    if entry_uuid:
        payload.setdefault("journeyTrackingAttributes", {})["entryUuid"] = entry_uuid
    if program_name:
        payload["programName"] = program_name
    return payload


def call_grpc(payload: dict, host: str, send_now: bool, baggage: str | None) -> int:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    cmd = ["grpcurl", "-plaintext"]
    if send_now:
        cmd += ["-H", "fpn-send-now: true"]
    if baggage:
        cmd += ["-H", f"baggage: {baggage}"]

    cmd += ["-d", "@", host, SERVICE_METHOD]

    proc = subprocess.run(cmd, input=data, capture_output=True)
    if proc.stdout:
        sys.stdout.buffer.write(proc.stdout)
        if not proc.stdout.endswith(b"\n"):
            sys.stdout.write("\n")
    if proc.stderr:
        sys.stderr.buffer.write(proc.stderr)
        if not proc.stderr.endswith(b"\n"):
            sys.stderr.write("\n")
    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Call DebugDeliverNotificationContent")
    src = parser.add_mutually_exclusive_group(required=False)
    src.add_argument("--audience-id", help="Audience ID to use")
    src.add_argument("--alias", choices=sorted(ALIAS_TO_ID.keys()), help="Alias to use")

    parser.add_argument(
        "--host", default=DEFAULT_HOST, help=f"gRPC host:port (default: {DEFAULT_HOST})"
    )
    parser.add_argument(
        "--template", default=str(DEFAULT_TEMPLATE), help="Path to JSON template"
    )
    parser.add_argument("--entry-uuid", help="Override entryUuid")
    parser.add_argument("--program-name", help="Override programName")
    parser.add_argument(
        "--send-now", action="store_true", default=True, help="Include fpn-send-now header"
    )
    parser.add_argument(
        "--no-send-now", dest="send_now", action="store_false", help="Disable send-now header"
    )
    parser.add_argument(
        "--baggage",
        default=(
            "tid=doortest:default,dd-routing-context=%5B%7B%22service%22%3A%22growth-service%22%2C%22app%22%3A%22notification-platform%22%2C%22host%22%3A%22growth-service-notification-platform-sandbox-lei-np%22%2C%22port%22%3A%2250051%22%7D%5D"
        ),
        help="Value for 'baggage' header (set empty string to omit)",
    )

    args = parser.parse_args()

    audience_id = args.audience_id or (ALIAS_TO_ID.get(args.alias) if args.alias else None)
    if not audience_id:
        parser.error("Provide --audience-id or --alias")

    template_path = Path(args.template)
    if not template_path.exists():
        parser.error(f"Template not found: {template_path}")

    payload = build_payload(template_path, audience_id, args.entry_uuid, args.program_name)
    baggage = args.baggage if args.baggage else None
    return call_grpc(payload, args.host, args.send_now, baggage)


if __name__ == "__main__":
    raise SystemExit(main())


