## Good practice

- input normalization (trim + lowercase)
- Separate helper for directory existence check
- Rich returned object with metadata
- Propagating original error via `cause` + context properties.
- `stdio: "inherit"` -> useful for seeing real-time output during debugging
- Warning instead of crash on `chmod` failure


## Security Risk – Path Traversal Vulnerability (Critical)

```
const templateDir = path.resolve(__dirname, "app-builds", templateName);
```

**Problem**: templateName comes from the user / caller / external input.

If someone passes:

- templateName = "../../../../etc/passwd"
- templateName = "../../secrets"
- templateName = "..%2F..%2F..%2F"

→ path.resolve() will happily climb out of your project root and give access to **any file on the filesystem** the Node.js process has permission to read.

This is a **classic path traversal vulnerability** — very common in file upload / template systems.

## API

- Security No Auth/Validation -> open write access api. Bloating your DB with malicious data
- Add middleware for auth (JWT) + zod schema validation. Never trust `req.body`.
- Missing body size limits, rate limiting (spam risk).


### Command Injection Vulnerabilities

```javascript
// Line: execFileAsync("rsync", ["-a", "--delete", `${src}/`, `${dest}/`])
```

While `execFile` is safer than `exec`, the `--delete` flag with `rsync` is dangerous. If an attacker controls the source directory, they could delete all files in the destination.

**Recommendation:** Validate that `src` exists and is within expected boundaries before executing.