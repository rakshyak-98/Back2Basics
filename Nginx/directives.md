[[How does directive work#try_files]]

# directives

> directives — server — defines a virtual server

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** directives is infra/security tooling — least privilege, clear config, observable failures.


server ->  defines a **virtual server**
- group all config block for a domain/port.
listen -> defines which IP/PORT this server listens on.
server_name ->
- is how Nginx decides which `server {...}` block should handle an incoming request.
root -> sets the base directory for serving static files.
index -> defines the default file to serve when a directory is requested.
location -> defines how to handle requests for a path
proxy_pass -> forwards requests to another server (reverse proxy).
proxy_set_header -> passes extra headers to the backend.
- Often used for `Host` `X-Real-IP` `X-Forward-For`
error_page -> defines a custom page for specific error codes.
- example `error_page 404 /custom_404.html;`
upstream -> defines a group of backend servers for load balancing.
gzip & gzip_types -> enable compression for responses.
```nginx
server {
	gzip on;
	gzip_types text/plain application/json;
}
```
auth_basic / auth_basic_user_file -> Enables HTTP basic authentication

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **directives** | Core idea of this note | “I can explain directives without jargon.” |
| **least privilege** | Only needed access | “Grant the smallest role that works.” |
| **secret** | Password/key/token | “Secrets out of git; rotate them.” |
| **observability** | metrics/logs/traces | “You can’t fix what you can’t see.” |

---

## Standard config / commands

```bash
# status
# check version, auth, and recent changes
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Auth fail | clock / creds / IAM | Sync time; fix policy |
| TLS error | cert chain / SNI | Fix certs and CA bundle |
| Deploy down | rollback / health | Roll back; check probes |

---

## Gotchas

> [!WARNING]
> Never commit long-lived secrets.

---

## When NOT to use

- Don’t build custom infra when managed services meet the SLO.

---

## Related

[[How does directive work#try_files]]
