"""
Composio + Claude Agent SDK: GitHub coding agent example.

Prerequisites:
  pip install -r requirements.txt

Environment variables (see .env.example):
  COMPOSIO_API_KEY  - your Composio API key
  ANTHROPIC_API_KEY - your Anthropic API key
  USER_ID           - your Composio user identifier (default: "default")
"""

import asyncio
import os
import sys

from composio import Composio
from composio_claude_agent_sdk import ClaudeAgentSDKProvider
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, create_sdk_mcp_server


def create_session():
    api_key = os.environ.get("COMPOSIO_API_KEY")
    if not api_key:
        sys.exit("COMPOSIO_API_KEY is not set. Copy .env.example to .env and fill it in.")

    composio = Composio(
        api_key=api_key,
        provider=ClaudeAgentSDKProvider(),
    )

    session = composio.create(
        user_id=os.environ.get("USER_ID", "default"),
        toolkits=["github"],
    )
    return session


async def main():
    session = create_session()

    tools = session.tools()
    mcp_server = create_sdk_mcp_server(name="composio", version="1.0.0", tools=tools)

    # permission_mode="default" requires explicit user approval for each tool call.
    # Use "bypassPermissions" ONLY for local demos; never in production.
    options = ClaudeAgentOptions(
        system_prompt=(
            "You are a coding agent. You can read GitHub issues, create branches, "
            "open pull requests, and comment on issues using Composio tools."
        ),
        permission_mode="default",
        mcp_servers={"composio": mcp_server},
    )

    prompt = os.environ.get(
        "AGENT_PROMPT",
        "List the 5 most recent open issues in composio-bot.",
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query(prompt)
        async for msg in client.receive_response():
            print(msg)


if __name__ == "__main__":
    asyncio.run(main())
