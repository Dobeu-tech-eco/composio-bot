# CLI integration: Composio (Rube) MCP

Use the same Composio-backed MCP server (Rube) in **claude-code**, **gemini-cli**, and **codex**. Rube URL: `https://rube.app/mcp`. Auth is often in-chat OAuth; some setups use a bearer token from [rube.app](https://rube.app) → Use Rube → MCP URL → Generate token.

---

## Claude Code

1. Add Rube MCP in Claude Code (paste the “Generate MCP URL” command from [Composio + Claude Code](https://composio.dev/toolkits/composio/framework/claude-code); it typically adds `https://rube.app/mcp`).
2. In Claude Code, run `/mcp` and complete the Rube/Composio auth flow.
3. Run `/mcp` again to confirm; then use Composio tools via Rube.

No `COMPOSIO_API_KEY` needed in Claude Code when using Rube; Rube handles connection after sign-in.

---

## Gemini CLI

Gemini CLI uses `settings.json` and supports **Streamable HTTP** via `httpUrl`.

1. Locate your Gemini CLI `settings.json` (project or user-level; see [Gemini CLI MCP docs](https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html)).
2. Add Rube under `mcpServers`:

```json
{
  "mcpServers": {
    "rube": {
      "httpUrl": "https://rube.app/mcp"
    }
  }
}
```

If Rube requires a bearer token, set it in an env var (e.g. `RUBE_BEARER_TOKEN`) and add auth per gemini-cli’s schema (e.g. `headers` or the documented env-based auth for HTTP MCP).

3. Restart/reload Gemini CLI and verify tools (e.g. ask it to use a Composio app).

---

## Codex

Codex uses **Streamable HTTP** and stores MCP config in:

- **Windows:** `%USERPROFILE%\.codex\config.toml`
- **macOS/Linux:** `~/.codex/config.toml`

CLI and VS Code extension share this file. You can also use Codex UI: **Settings (gear) → MCP Servers → Add server → Streamable HTTP**.

1. Open `config.toml` and add:

```toml
[mcp_servers.rube]
url = "https://rube.app/mcp"
enabled = true
```

If Rube requires a bearer token:

```toml
[mcp_servers.rube]
url = "https://rube.app/mcp"
bearer_token_env_var = "RUBE_BEARER_TOKEN"
enabled = true
```

Set `RUBE_BEARER_TOKEN` in your environment (or in `.env` and load it before starting Codex).

2. Save and restart Codex; verify with `/mcp` (or MCP list in the UI).

---

## Summary

| CLI         | Config location              | Rube URL             |
|------------|------------------------------|----------------------|
| Claude Code| In-app (Generate MCP URL)    | `https://rube.app/mcp` |
| Gemini CLI | `settings.json` → `mcpServers.rube` | `httpUrl`: `https://rube.app/mcp` |
| Codex      | `~/.codex/config.toml`       | `url = "https://rube.app/mcp"` |

One Rube MCP endpoint gives all three CLIs access to the same Composio tools (500+ apps).
