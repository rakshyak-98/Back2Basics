[[MCP]] [[JWT authentication]] [[webSocket]]

# MCP Client

> Host-side MCP operations — discover servers, authenticate, list tools/resources/prompts, invoke calls with timeouts, and debug failures.

```txt
        MCP Client ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Platform reviews: client mediates the LLM (model never speaks raw to your …

## Sources
- [MCP — Clients](https://modelcontextprotocol.io/docs/concepts/architecture) — deep-dive
- [Cursor — MCP docs](https://docs.cursor.com/) — overview

## Key Concepts
- **Mediation:** LLM selects a tool → client validates/calls server → result returns to contex…
- **tools/list & tools/call:** schema discovery + invocation.
- **resources/read & prompts/get:** context and templates.
- **Auth:** OAuth/API keys stored by the client, not the model.

## Technical Details
```txt
MCP Client ←JSON-RPC→ MCP Server → Backend API/DB
LLM picks tool → client executes → result to model
```

- Cursor-style config (`~/.cursor/mcp.json` or project `.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_TOKEN}" }
    }
  }
}
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Server missing | JSON config | Validate; restart host |
| Timeouts | Server logs | Fix blocking I/O; raise timeout |
| Auth errors | Token/OAuth | Re-auth; rotate secrets |
| Garbled stdio | Debug prints on stdout | Log to stderr only |

## Mistakes to Avoid
- **Mistake:** Passing unsanitized tool output straight into shell commands
- **Mistake:** Putting long-lived tokens in world-readable config without env i…
- **Mistake:** Using stdio servers that spam stdout with logs

## Pros/Cons or Trade-offs
- **Pro:** One host can juggle many specialized servers.
- **Con:** Debugging spans host logs + server logs + transport.

## Comparison
- vs [[MCP]]: protocol vs operator checklist on the client.
- vs IDE extensions: MCP is model-facing capabilities, not only UI plugins.


### Use cases
- Cursor connects to postgres/github servers so agents can query schema and ope…

- **Example:** Tool schema mismatch after server upgrade
