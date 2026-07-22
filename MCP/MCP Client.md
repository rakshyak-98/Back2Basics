[[MCP]] [[webSocket]] [[JWT authentication]] [[gRPC]]

# MCP Client

> Model Context Protocol client ops — how Cursor and tooling hosts discover, auth, invoke, and debug MCP servers — **MCP spec (Anthropic ecosystem)**.

---

## Mental model

An **MCP client** (Cursor, Claude Desktop, custom SDK host) connects to one or more **MCP servers** that expose **tools**, **resources**, and **prompts** over a transport. The LLM never talks to your server directly — the client mediates capability discovery and tool calls.

```txt
┌──────────────┐   JSON-RPC    ┌──────────────┐   SQL/API   ┌──────────┐
│  MCP Client  │ ◄───────────► │  MCP Server  │ ──────────► │ Backend  │
│  (Cursor)    │  stdio/HTTP   │  (postgres,  │             │          │
└──────┬───────┘               │   github…)   │             └──────────┘
       │                       └──────────────┘
       ▼
   LLM selects tool → client calls server → result injected into context
```

| Surface | Client responsibility |
|---------|----------------------|
| **tools/list** | Cache schema; show model what exists |
| **tools/call** | Validate args; enforce timeouts; redact secrets in logs |
| **resources/read** | Fetch file/DB rows into context window |
| **prompts/get** | Template expansion for repeatable workflows |
| **auth** | OAuth/API keys — client stores tokens, not the model |

**Transport:** `stdio` (local subprocess — most Cursor servers), `SSE/HTTP` (remote), streamable HTTP (spec evolution — see [[MCP]]).

---

## Standard config / commands

### Cursor MCP config (`~/.cursor/mcp.json` or project `.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"],
      "env": {}
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_TOKEN}"
      }
    }
  }
}
```

### Client-side invocation flow (SDK mental model)

```txt
1. initialize → negotiate protocol version + capabilities
2. tools/list → [{ name, description, inputSchema }]
3. (model turn) → tools/call { name, arguments }
4. server executes → { content: [{ type: "text", text: "..." }], isError?: bool }
5. client attaches result to conversation; may truncate large payloads
```

### Debugging local server

```shell
# Run server manually — same command as mcp.json
npx -y @modelcontextprotocol/server-filesystem /tmp

# Inspect stderr (stdio transport uses stdout for protocol; logs go stderr)
MCP_DEBUG=1 npx -y @modelcontextprotocol/server-postgres "$DATABASE_URL"

# Verify tool schema
# Cursor: GetMcpTools / MCP panel — or use @modelcontextprotocol/inspector
npx @modelcontextprotocol/inspector npx -y @modelcontextprotocol/server-filesystem /tmp
```

### Timeouts and limits (host settings)

```txt
Tool call timeout:     30–120s default — override for long migrations
Max result size:     truncate + offer pagination resource
Concurrent calls:    serialize if server isn't thread-safe
Retry:               idempotent reads yes; writes no blind retry
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Server not listed in Cursor | MCP settings → logs; JSON syntax | Fix `mcp.json`; restart Cursor |
| `needsAuth` / 401 | Server status; OAuth flow | Run `mcp_auth`; refresh token |
| Tool call hangs | Server stderr; backend connectivity | Timeout; fix DB URL / VPN |
| `command not found` | `which npx`; PATH in GUI app | Absolute path to node/npx in config |
| Empty tool list | Server startup crash on import | Run command manually; fix env vars |
| Works in CLI, not Cursor | Cursor inherits different env | Put secrets in `env` block, not shell profile |
| Protocol version error | Client vs server version skew | Update server package or pin version |

```shell
# macOS/Linux: GUI apps often lack your shell PATH
# Use full paths:
"command": "/usr/local/bin/npx"
```

---

## Gotchas

> [!WARNING]
> **Secrets in args** — connection strings in `mcp.json` sit on disk. Prefer env vars; never commit tokens.

> [!WARNING]
> **stdio stdout pollution** — any `console.log` to stdout corrupts JSON-RPC. Log to stderr only in servers.

> [!WARNING]
> **Non-idempotent tools** — model may retry. Design `deploy_prod` with confirmation or idempotency keys.

> [!WARNING]
> **Context bloat** — `resources/read` on large files fills the window. Client should summarize or slice.

> [!WARNING]
> **Tool schema too vague** — model passes wrong types. Tight `inputSchema` with enums and required fields.

> [!WARNING]
> **Parallel tool calls** — two writes racing. Document side effects; use server-side locking.

---

## When NOT to use

- **Simple static docs** — link the doc; don't wrap in MCP.
- **High-QPS automation** — use direct API/SDK; MCP adds LLM mediation overhead.
- **Untrusted servers** — MCP server runs with host privileges; audit before adding.

---

## Related

[[MCP]] [[webSocket]] [[gRPC]] [[expressjs]] [[JWT authentication]]
