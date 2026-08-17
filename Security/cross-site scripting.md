[[content security policy]] [[SOP (Same-Origin Policy)]] [[IDOR]] [[response header]] [[XSRF (cross-site request forgery)]] [[JWT authentication]]

# Cross-site scripting (XSS)

> Injection of executable script into a page another user's browser will run — steals sessions, defaces UI, exfiltrates data.

```txt
        Cross-site scripti ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Must-know web vuln: stored/reflected/DOM XSS, output encoding, and why CSP is…

## Sources
- [OWASP — Cross Site Scripting](https://owasp.org/www-community/attacks/xss/) — overview
- [OWASP — XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) — deep-dive

## Key Concepts
XSS = attacker's JS runs in **victim origin** context:

```txt
- **Note:** Stored: attacker saves <script> in DB → served to all viewers
Reflected: ?q=<script> in URL → echoed in response
- **Note:** DOM: client JS writes location.hash to innerHTML unsafely
```

- **Note:** Browser same-origin rules then grant access to **cookies**, **localStorage**,…

Defense layers:
- **Note:** 1. **Output encoding** — context-specific (HTML, attr, JS, URL)
- **Note:** 2. **CSP** — [[content security policy]] restrict script sources
3. **HttpOnly cookies** — JS can't read session cookie
4. **Framework defaults** — React/Vue escape text nodes


- **Core:** XSS injects executable script into a page another user's browser will run

## Technical Details
### CSP header (primary HTTP control)

```http
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'self'
```

### Nginx + secure cookies

```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self'" always;
# App sets: Set-Cookie: sid=...; HttpOnly; Secure; SameSite=Lax
```

### Safe patterns (JS)

```javascript
// BAD: element.innerHTML = userInput;
// GOOD:
element.textContent = userInput;
// or DOMPurify.sanitize(html) if HTML required
```

### Test reflection

```bash
curl -s 'https://app.example/search?q=%3Cscript%3Ealert(1)%3C/script%3E' | grep script
```

- **Why HttpOnly:** even if XSS exists, exfiltrating session cookie is harder (…

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Reported script popup | Reproduce URL/param | Encode output; CSP; sanitize HTML |
| Session hijack spike | New script in stored fields | Audit DB content; WAF temporary |
| CSP breaks legit feature | Console violations | Nonce/hash; narrow allowlist |
| Markdown/HTML renderer XSS | Allowlist tags | Use safe parser; no raw HTML pass-through |

## Mistakes to Avoid
- **Mistake:** `dangerouslySetInnerHTML` — name is accurate
- **Mistake:** JSON is not HTML-safe
- **Mistake:** CSP bypass via JSONP/old plugins
- **Mistake:** DOM XSS in SPA routers — `document.write`, `location` to sink

## Pros/Cons or Trade-offs
- **Pro:** Clear attack classes (stored/reflected/DOM) map to concrete defenses.
- **Con:** Don't rely on **WAF alone** — fix source encoding. Don't disable CSP globally for one widget — isolate vendor subdomain.

## Comparison
- vs [[XSRF (cross-site request forgery)]]: XSS runs attacker script in the victim origin
- vs [[content security policy]]: CSP is defense-in-depth after encoding.


### Use cases
- Stored XSS in a comment field steals session cookies unless output is encoded…
