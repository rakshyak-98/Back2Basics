[[MCP/MCP Client]] [[Descriptive/vscode]] [[Protocol/MQTT]]

# MCP (Model Context Protocol)

> Open protocol for AI clients to discover and call tools, read resources, and exchange prompts with servers — USB-C for LLM integrations.

## Mental model

An **MCP host** (Cursor, Claude Desktop) runs **MCP clients** that connect to **MCP servers** over stdio, SSE, or streamable HTTP. Servers expose **tools** (functions), **resources** (readable URIs), and **prompts**. The model requests a tool call; the client executes it on the server and returns structured results.

```
Host (IDE) → MCP Client ↔ transport ↔ MCP Server (git, DB, browser, …)
```

Spec evolves — streamable HTTP supersedes early SSE-only patterns for remote servers.

## Standard config / commands

### Cursor-style server config (conceptual)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"]
    }
  }
}
```

### Server responsibilities

| Surface | Example |
|---------|---------|
| Tools | `query_database`, `create_issue` |
| Resources | `file:///README.md`, logs URI |
| Prompts | Reusable prompt templates |

### Transport options

| Transport | Use case |
|-----------|----------|
| stdio | Local subprocess (default for CLI servers) |
| Streamable HTTP | Remote/shared server, auth at edge |
| SSE (legacy) | Older deployments; migrate when possible |

Reference: [MCP specification](https://modelcontextprotocol.io/) · [Streamable HTTP PR](https://github.com/modelcontextprotocol/specification/pull/206)

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Server not listed | Config JSON syntax | Validate; restart host |
| Tool call timeout | Server logs | Increase timeout; fix blocking I/O |
| Auth errors (remote) | OAuth/API key | `mcp_auth` flow in host; rotate creds |
| Schema mismatch | Tool input schema | Align server tool definition with client expectations |
| stdio garbled output | println debug on stdout | Log to stderr only in MCP servers |

## Gotchas

> [!WARNING]
> **MCP server = arbitrary code execution** — only install trusted servers; review tool permissions.
>
> **Secrets in server env** — same discipline as CI secrets; don't log tool args with tokens.
>
> **Spec drift** — pin server version; hosts update faster than servers.

## When NOT to use

- Don't build MCP for a one-off script you'd run once in terminal — shell script is simpler.
- Don't expose production DB write tools without authz layer and audit logging.

## Related

[[MCP/MCP Client]] [[NodeJS/CLI]] [[Descriptive/vscode]]
