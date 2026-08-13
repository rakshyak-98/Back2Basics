<!-- note-strategy: operational -->
[[apache]]

# CGI

> CGI — common Gateway Interface — is a standard protocol that allows a web server to interact with external programs (called CGI scripts or programs) to…

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** CGI — common Gateway Interface — is a standard protocol that allows a web server to interact with external programs (called CGI scripts or programs) to…

Common Gateway Interface -> is a standard protocol that allows a web server to interact with external programs (called CGI scripts or programs) to generate dynamic content, rather than just serving static files.
Process per request -> Each CGI invocation spawns a new process, which is resource-intensive (slow for high traffic). This is why modern alternatives like FastCGI, mod_php, or application servers (Node.js) are preferred.


---

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[apache]]
