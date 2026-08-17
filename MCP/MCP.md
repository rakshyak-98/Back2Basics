[[MCP Client]] [[Descriptive/vscode]] [[Protocol/MQTT]]

# MCP (Model Context Protocol)

> Open protocol for AI hosts to discover and call tools, read resources, and fetch prompts from servers — “USB-C for LLM integrations.”





## Interview Relevance
Interviewers (AI platform) want host/client/server roles, transports (stdio vs HTTP), and the security model (tools = code execution).

## Sources
- [MCP specification](https://modelcontextprotocol.io/) — deep-dive
- [MCP — Architecture](https://modelcontextprotocol.io/docs/concepts/architecture) — overview

## Key Concepts
- **Host:** IDE/app (Cursor, Claude Desktop) embedding clients.
- **Client:** session talking to one server.
- **Server:** exposes tools, resources, prompts.
- **Transport:** stdio (local), streamable HTTP/SSE (remote).

## Technical Details
```
Host → MCP Client ↔ transport ↔ MCP Server (git, DB, browser, …)
```

| Surface | Example |
|---------|---------|
| Tools | `query_database`, `create_issue` |
| Resources | `file:///README.md` |
| Prompts | Reusable templates |

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

## Real-World Applications
IDE agent lists repo files via a filesystem server and opens PRs via a GitHub server — model only sees mediated results.

**Example:** Remote HTTP server behind auth — prefer streamable HTTP patterns over legacy-only SSE setups when migrating.

## Pros/Cons or Trade-offs
- **Pro:** Standardize tool plugins across hosts.
- **Con:** A malicious/buggy server is arbitrary code with your credentials.

## Comparison
- vs raw function-calling APIs: MCP standardizes discovery and transports across apps.
- vs [[MCP Client]]: this note is the protocol; client note is host-side ops.

## Mistakes to Avoid
- Installing untrusted servers with broad filesystem/network access.
- Logging secrets from tool args to stdout (stdio servers must keep stdout clean).
- Assuming the model “has root” — the client enforces what runs.
