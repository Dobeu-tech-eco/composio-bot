# composio-bot

Composio.dev bot and integration hub for claude-code, gemini-cli, codex, and agent SDKs (Claude, OpenAI, Gemini).

## Composio setup

1. **Account and API key**  
   Create an account at [platform.composio.dev](https://platform.composio.dev) and create an API key in **Settings**. Never commit your API key.

2. **Environment variables**  
   Copy `.env.example` to `.env` and set:
   - `COMPOSIO_API_KEY` — your Composio API key
   - `USER_ID` — stable id for Composio sessions (e.g. `user_1` or your email)
   - Optional: `RUBE_BEARER_TOKEN` if you use Rube MCP with the CLIs (get from [rube.app](https://rube.app) → Use Rube → MCP URL → Generate token)

3. **Composio CLI (global)**  
   From a bash shell (WSL, Git Bash, or macOS/Linux):
   ```bash
   curl -fsSL https://composio.dev/install | bash
   source ~/.bashrc   # or open a new terminal
   composio whoami    # verify (set COMPOSIO_API_KEY first)
   ```
   Docs: [Composio CLI](https://docs.composio.dev/docs/cli).

4. **Rube (optional)**  
   For **claude-code**, **gemini-cli**, and **codex**, you can use Composio via Rube’s MCP server (`https://rube.app/mcp`) so all three share the same tools. See [docs/cli-integration.md](docs/cli-integration.md).

## Env vars by integration

| Integration        | COMPOSIO_API_KEY | USER_ID | Other                    |
|--------------------|------------------|--------|---------------------------|
| Composio CLI       | Yes              | Optional | —                         |
| Claude Code (Rube) | No (auth in app) | —      | —                         |
| Gemini CLI (Rube) | No (auth in app) | —      | Optional bearer token      |
| Codex (Rube)       | No (auth in app) | —      | Optional bearer token      |
| Claude Agent SDK   | Yes              | Yes    | ANTHROPIC_API_KEY         |
| OpenAI Agent SDK   | Yes              | Yes    | OPENAI_API_KEY            |
| Gemini (Google) SDK| Yes              | Yes    | GOOGLE_API_KEY            |

## SDK example

`example_agent.py` is a Claude Agent SDK + Composio coding agent that reads GitHub issues and can open PRs. It uses environment variables (never hardcoded secrets) and `permission_mode="default"` for production safety.

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in your keys
python example_agent.py
```

> **Note:** `script.js` is a legacy sample with hardcoded secrets and a misleading extension (Python code in a .js file). Use `example_agent.py` instead.

## Personal Cursor skills

A pack of 8 Cursor skills for Composio meta tools is installed at `~/.cursor/skills/composio-*`:

| Skill | Covers |
|-------|--------|
| `composio-workflow` | Orchestrator — canonical execution order and decision guide |
| `composio-search-tools` | COMPOSIO_SEARCH_TOOLS |
| `composio-get-tool-schemas` | COMPOSIO_GET_TOOL_SCHEMAS |
| `composio-manage-connections` | COMPOSIO_MANAGE_CONNECTIONS |
| `composio-wait-for-connections` | COMPOSIO_WAIT_FOR_CONNECTIONS |
| `composio-multi-execute` | COMPOSIO_MULTI_EXECUTE_TOOL |
| `composio-remote-workbench` | COMPOSIO_REMOTE_WORKBENCH |
| `composio-remote-bash` | COMPOSIO_REMOTE_BASH_TOOL |

## Docs

- [CLI integration](docs/cli-integration.md) — Add Composio (Rube) MCP to claude-code, gemini-cli, and codex.
- [MCP tools and skills](docs/composio-mcp-tools-and-skills.md) — Meta tool reference and terminology.
- [Direct tools vs sessions](docs/composio-direct-tools-vs-sessions.md) — When to use each mode.
- [Coding agent use case](docs/coding-agent-usecase.md) — GitHub issue-to-PR workflow with decision table.
