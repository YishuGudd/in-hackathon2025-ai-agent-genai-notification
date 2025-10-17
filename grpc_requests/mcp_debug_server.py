import asyncio
import json
import os
import sys
from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "grpc_requests" / "call_debug_deliver.py"


class DebugDeliverArgs(BaseModel):
    audience_id: str
    host: str | None = None
    entry_uuid: str | None = None
    program_name: str | None = None
    send_now: bool | None = None
    baggage: str | None = None


async def run_subprocess(cmd: list[str], data: bytes | None = None) -> tuple[int, bytes, bytes]:
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE if data is not None else None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=str((REPO_ROOT / "grpc_requests").resolve()),
    )
    stdout, stderr = await proc.communicate(input=data)
    return proc.returncode, stdout, stderr


async def main() -> None:
    server = Server("debug-deliver-stdio")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="debug_deliver",
                description="Call DebugDeliverNotificationContent via grpcurl wrapper",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "audience_id": {"type": "string", "description": "Audience ID"},
                        "host": {"type": "string", "description": "gRPC host:port"},
                        "entry_uuid": {"type": "string", "description": "Journey entry UUID"},
                        "program_name": {"type": "string", "description": "Program name override"},
                        "send_now": {"type": "boolean", "description": "Include fpn-send-now header"},
                        "baggage": {"type": "string", "description": "baggage header value"},
                    },
                    "required": ["audience_id"],
                },
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
        if name != "debug_deliver":
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

        args = DebugDeliverArgs(**(arguments or {}))

        python = os.environ.get("PYTHON", sys.executable or "python3")
        cmd: list[str] = [python, str(SCRIPT_PATH), "--audience-id", str(args.audience_id)]
        if args.host:
            cmd += ["--host", args.host]
        if args.entry_uuid:
            cmd += ["--entry-uuid", args.entry_uuid]
        if args.program_name:
            cmd += ["--program-name", args.program_name]
        if args.send_now is False:
            cmd += ["--no-send-now"]
        if args.baggage is not None:
            cmd += ["--baggage", args.baggage]

        code, stdout, stderr = await run_subprocess(cmd)
        if code != 0:
            body = json.dumps(
                {"status": "error", "code": code, "stderr": stderr.decode(), "stdout": stdout.decode()},
                ensure_ascii=False,
                indent=2,
            )
            return [TextContent(type="text", text=body)]

        out_text = stdout.decode() if stdout else "(no output)"
        return [TextContent(type="text", text=out_text)]

    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
