# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A Composio.dev integration hub and documentation repo for connecting AI coding CLIs (claude-code, gemini-cli, codex) and agent SDKs (Claude, OpenAI, Gemini) to 500+ apps via Composio's MCP server (Rube).

This is **not** an application with source code — it's a configuration, documentation, and SDK dependency repo.

## Key Dependencies

- `@anthropic-ai/claude-agent-sdk` — Claude Agent SDK
- `@composio/claude-agent-sdk` — Composio's Claude Agent SDK integration
- `@composio/core` — Composio core library

Install: `npm install`

## Environment Setup

Copy `.env.example` to `.env` and set:
- `COMPOSIO_API_KEY` — from [platform.composio.dev](https://platform.composio.dev) → Settings
- `USER_ID` — stable identifier for Composio sessions
- `RUBE_BEARER_TOKEN` (optional) — for Rube MCP with CLIs

## Architecture

### MCP Integration Layer

All three CLIs connect to the same endpoint: `https://rube.app/mcp` (Rube MCP server). Rube handles Composio auth and exposes meta tools that dynamically discover and execute 20,000+ app tools.

**Agent tool flow:** Search tools → Manage connections (if needed) → Execute tool(s)

### CLI Config Locations

| CLI | Config |
|-----|--------|
| Claude Code | In-app (`/mcp` command) |
| Gemini CLI | `settings.json` → `mcpServers.rube.httpUrl` |
| Codex | `~/.codex/config.toml` → `[mcp_servers.rube]` |

### Composio Project Config

`.composio/project.json` contains the Composio org/project IDs for this workspace. Do not modify manually.

## Documentation

- `docs/cli-integration.md` — How to add Rube MCP to each CLI
- `docs/composio-mcp-tools-and-skills.md` — Meta tool reference, terminology, best practices
- `docs/composio-direct-tools-vs-sessions.md` — When to use sessions vs direct tool fetching
- `docs/coding-agent-usecase.md` — GitHub issue-to-PR workflow with 4-path decision table

## Composio MCP Meta Tools (Quick Reference)

The 7 confirmed meta tools available through the `user-composio` MCP server:

| Tool | Purpose |
|------|---------|
| `COMPOSIO_SEARCH_TOOLS` | Discover tools for a use case; returns schemas, connection status, execution plan, and `session_id` |
| `COMPOSIO_GET_TOOL_SCHEMAS` | Fetch full input schemas when SEARCH returned only a `schemaRef` |
| `COMPOSIO_MANAGE_CONNECTIONS` | Check or create app connections; returns auth URL if needed |
| `COMPOSIO_WAIT_FOR_CONNECTIONS` | Poll until auth reaches ACTIVE/FAILED after showing an auth link |
| `COMPOSIO_MULTI_EXECUTE_TOOL` | Execute 1-50 tools in parallel; only for independent, schema-compliant calls |
| `COMPOSIO_REMOTE_BASH_TOOL` | Run bash in a remote sandbox for simple file/data processing |
| `COMPOSIO_REMOTE_WORKBENCH` | Run Python in a persistent remote Jupyter sandbox for bulk ops and large data |

**Canonical order:** Search -> Schemas (if needed) -> Connections (if needed) -> Wait -> Execute -> Workbench/Bash (if needed)

**Critical:** Always carry `session_id` from SEARCH_TOOLS into every subsequent meta tool call.

## Personal Skill Packs

Composio skills are installed in both Cursor and Claude Code:
- **Cursor:** `~/.cursor/skills/composio-*` (8 skills)
- **Claude Code:** `~/.claude/skills/composio-*` (8 skills)
- **Slash command:** `/composio` triggers the full workflow in Claude Code

## SDK Example

`example_agent.py` — Claude Agent SDK + Composio coding agent (uses env vars, `permission_mode="default"`). See `README.md` for setup.
