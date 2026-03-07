# GitHub Coding Agent Use Case

A concrete example of an AI coding agent that uses Composio to automate a GitHub issue-to-PR workflow.

---

## The scenario

1. Agent receives a GitHub issue number.
2. Agent reads the issue, understands the requirement.
3. Agent creates a branch, makes code changes, commits, and opens a PR referencing the issue.
4. Agent comments on the original issue with the PR link.

---

## Implementation paths

### Path A: Cursor + Rube MCP (interactive)

Use when working inside Cursor with the Rube MCP server attached.

```
RUBE_SEARCH_TOOLS → queries: [
  {"use_case": "read a GitHub issue by number"},
  {"use_case": "create a GitHub pull request"},
  {"use_case": "comment on a GitHub issue"}
]
↓ session_id returned
↓
RUBE_MANAGE_CONNECTIONS → toolkits: ["github"] (if not active)
↓
RUBE_WAIT_FOR_CONNECTIONS → toolkits: ["github"]
↓
RUBE_MULTI_EXECUTE_TOOL → [GITHUB_GET_ISSUE] (read the issue)
↓ agent processes issue, writes code locally, commits, pushes
↓
RUBE_MULTI_EXECUTE_TOOL → [
  GITHUB_CREATE_PULL_REQUEST,
  GITHUB_CREATE_COMMENT_ON_ISSUE
] (batch: independent)
```

### Path B: Claude Agent SDK + Composio session (programmatic)

Use when building a standalone agent script.

```python
import os
import asyncio
from composio import Composio
from composio_claude_agent_sdk import convert_tools
from claude_agent_sdk import Agent, Conversation

composio = Composio(api_key=os.environ["COMPOSIO_API_KEY"])

session = composio.create(
    user_id=os.environ.get("USER_ID", "default"),
    toolkits=["github"],
)

tools = convert_tools(session.tools())

agent = Agent(
    model="claude-sonnet-4-20250514",
    tools=tools,
    instructions="You are a coding agent. Read the GitHub issue, implement a fix, and open a PR.",
)

async def main():
    conversation = agent.create_conversation()
    response = await conversation.send(
        f"Read issue #{os.environ['ISSUE_NUMBER']} from {os.environ['REPO']} and implement a fix."
    )
    print(response.content)

asyncio.run(main())
```

### Path C: Direct tool fetching (backend automation)

Use for narrow, deterministic pipelines with known tools.

```python
import os
from composio import Composio

composio = Composio(api_key=os.environ["COMPOSIO_API_KEY"])
user_id = os.environ.get("USER_ID", "default")

issue = composio.tools.execute(
    "GITHUB_GET_ISSUE",
    {"owner": "jswil", "repo": "composio-bot", "issue_number": 42},
    user_id=user_id,
)

pr = composio.tools.execute(
    "GITHUB_CREATE_PULL_REQUEST",
    {"owner": "jswil", "repo": "composio-bot", "head": "fix/issue-42", "base": "main", "title": "Fix #42"},
    user_id=user_id,
)
```

### Path D: Composio CLI (quick testing)

Use for manual discovery and one-off execution from the terminal.

```bash
composio search "create a github pull request"
composio execute GITHUB_CREATE_PULL_REQUEST -d '{"owner":"jswil","repo":"composio-bot","head":"fix/issue-42","base":"main","title":"Fix #42"}'
```

---

## Decision table

| Dimension | Cursor + Rube MCP | SDK Session | Direct Fetch | CLI |
|-----------|------------------|-------------|-------------|-----|
| **Interactive?** | Yes (user in loop) | Can be | No | Yes |
| **Discovery** | Dynamic via SEARCH | Dynamic via SEARCH | Manual / known slugs | `composio search` |
| **Auth flow** | MANAGE/WAIT | Built into session | Pre-connected | `composio connect` |
| **Permission control** | Managed by Rube | `permission_mode` | Per-call | N/A |
| **Toolkit restriction** | Via search scope | `toolkits=["github"]` | By choosing slugs | N/A |
| **Best for** | Cursor/IDE workflows | Standalone agents | Backend services | Testing/prototyping |

---

## Security considerations

- Never hardcode API keys. Use `.env` and `os.environ`.
- Use `permission_mode="default"` in production; `"bypassPermissions"` is demo-only.
- Restrict toolkits to what the agent actually needs.
- Pin toolkit versions in production to avoid breaking changes.
- Rotate API keys periodically; treat `COMPOSIO_API_KEY` as a secret.
