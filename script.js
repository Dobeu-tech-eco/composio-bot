import asyncio
from composio import Composio
from composio_claude_agent_sdk import ClaudeAgentSDKProvider
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, create_sdk_mcp_server

# Initialize Composio
composio = Composio(
    api_key="ak_J2wEU3LY0u3wh7-7Pa4E",
    provider=ClaudeAgentSDKProvider()
)

external_user_id = "pg-test-a0c10f84-3316-405c-afe9-54635741414c"

# Create a tool router session
session = composio.create(
    user_id=external_user_id,
)

# Get tools from the session (native)
tools = session.tools()
custom_server = create_sdk_mcp_server(name="composio", version="1.0.0", tools=tools)

# Query Claude with MCP tools
async def main():
    options = ClaudeAgentOptions(
        system_prompt="You are a helpful assistant",
        permission_mode="bypassPermissions",
        mcp_servers={
            "composio": custom_server,
        },
    )

    async with ClaudeSDKClient(options=options) as client:
        await client.query(f"Send an email to jeremyw@dobeu.net with the subject 'Hello from Composio' and the body 'This is a test email!'")
        # Extract and print response
        async for msg in client.receive_response():
            print(msg)

asyncio.run(main())
