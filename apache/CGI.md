[[apache]] [[fastCGI servers]] [[PHP-FPM]] [[Proxy/Reverse Proxy]]

# CGI

> Common Gateway Interface — the web server forks a process per request and talks via environment variables and stdio to generate dynamic responses.

```txt
        CGI ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers use CGI to test whether you understand process-per-request cost …

## Sources
- [RFC 3875 — CGI](https://datatracker.ietf.org/doc/html/rfc3875) — deep-dive
- [Wikipedia — Common Gateway Interface](https://en.wikipedia.org/wiki/Common_Gateway_Interface) — overview

## Key Concepts
- **External program:** script/binary invoked by the server → not just static files.
- **Process per request:** spawn → run → exit → high overhead under load.
- **Env + stdio protocol:** request metadata in environment; body on stdin; response on stdout.
- **Language agnostic:** any executable can be a CGI program.

## Technical Details
```
Client → httpd → fork CGI script → stdout response → client
```

- Classic path: `ScriptAlias` / `cgi-bin`.
- Failure modes: slow forks, permission errors, and scripts that do not emit co…

## Mistakes to Avoid
- **Mistake:** Designing new high-traffic apps on classic CGI
- **Mistake:** Trusting user input in CGI scripts without the same hardening as…
- **Mistake:** Leaving `cgi-bin` writable by the deploy user

## Pros/Cons or Trade-offs
- **Pro:** Simple mental model; easy to drop in a script.
- **Con:** Poor performance and harder connection reuse than FastCGI.

## Comparison
- vs [[fastCGI servers]]: FastCGI keeps workers warm and uses a binary multiplexed protocol.
- vs [[PHP-FPM]]: FPM is a FastCGI process manager specialized for PHP.


### Use cases
- Legacy admin tools and embedded devices still expose CGI

- **Example:** A traffic spike melts a CGI guestbook
