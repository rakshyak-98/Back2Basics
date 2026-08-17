[[MCP Client]] [[Descriptive/vscode]] [[Protocol/MQTT]]

# MCP (Model Context Protocol)

> Open protocol for AI hosts to discover and call tools, read resources, and fetch prompts from servers — “USB-C for LLM integrations.”

```txt
        MCP (Model Context ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers (AI platform) want host/client/server roles, transports (stdio v…

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

## Mistakes to Avoid
- **Mistake:** Installing untrusted servers with broad filesystem/network access
- **Mistake:** Logging secrets from tool args to stdout (stdio servers must kee…
- **Mistake:** Assuming the model “has root” — the client enforces what runs

## Pros/Cons or Trade-offs
- **Pro:** Standardize tool plugins across hosts.
- **Con:** A malicious/buggy server is arbitrary code with your credentials.

## Comparison
- vs raw function-calling APIs: MCP standardizes discovery and transports across apps.
- vs [[MCP Client]]: this note is the protocol; client note is host-side ops.


### Use cases
- IDE agent lists repo files via a filesystem server and opens PRs via a GitHub…

- **Example:** Remote HTTP server behind auth
