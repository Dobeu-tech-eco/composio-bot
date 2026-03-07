# Direct Tool Fetching vs Sessions

Composio supports two main integration modes. Choose based on how open-ended your agent is.

## Sessions (recommended for agents)

```python
session = composio.create(user_id="user_123", toolkits=["github"])
tools = session.tools()       # native tools for your SDK
mcp_url = session.mcp.url     # MCP URL for MCP-compatible clients
```

**Use sessions when:**
- Building an open-ended conversational agent.
- The user may need to authenticate interactively during the run.
- You want MCP exposure (Cursor, claude-code, codex).
- The tool surface may expand mid-task as the agent discovers more.
- You want Composio's meta tools (SEARCH, MANAGE_CONNECTIONS, etc.) to handle discovery.

**Session options:**
- `toolkits=["github"]` or `toolkits={"enable": ["github"]}` to restrict the catalog.
- `toolkits={"disable": ["exa", "firecrawl"]}` to block specific toolkits.
- `auth_configs={"github": "ac_..."}` for custom OAuth credentials.
- `connected_accounts={"gmail": "ca_work_gmail"}` for multi-account selection.

## Direct tool fetching (for deterministic workflows)

```python
tools = composio.tools.get("user_123", toolkits=["GITHUB"], limit=10)
result = composio.tools.execute("GITHUB_CREATE_ISSUE", {...}, user_id="user_123")
```

**Use direct fetching when:**
- You know the exact toolkit or tool slugs in advance.
- The workflow is narrow and predictable (e.g. "always create an issue then comment").
- You want tight control over which tools the agent sees.
- You are building a backend service, not an interactive agent.

**Notes:**
- Returns top 20 tools by default; use `limit` to adjust.
- Pin toolkit versions in production (`toolkit_versions="20250901_00"`); never use `"latest"`.
- Raw schema inspection without `user_id` is useful for codegen and validation: `composio.tools.get_raw_composio_tools(toolkits=["GITHUB"])`.

## Decision table

| Scenario | Mode | Why |
|----------|------|-----|
| Open-ended agent (any app) | Session, full catalog | Let SEARCH_TOOLS discover dynamically |
| Coding agent, GitHub only | Session, `toolkits=["github"]` | Restricted but still uses meta tools |
| Backend automation, known tools | Direct fetching | Deterministic, no discovery overhead |
| CLI testing | `composio search` + `composio execute` | Quick iteration |
| MCP client (Cursor, claude-code, codex) | Session MCP URL or Rube | `session.mcp.url` or `https://rube.app/mcp` |

## Current Composio guidance

Composio's docs explicitly recommend sessions for agent builds and treat direct fetching as the narrower, lower-level path. Direct fetching is supported but discouraged for general agent use unless you explicitly want that control.
