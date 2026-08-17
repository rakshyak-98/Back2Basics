[[content security policy]] [[SOP (Same-Origin Policy)]] [[IDOR]] [[response header]] [[XSRF (cross-site request forgery)]] [[JWT authentication]]

# Cross-site scripting (XSS)

> Injection of executable script into a page another user's browser will run — steals sessions, defaces UI, exfiltrates data.





## Interview Relevance
Must-know web vuln: stored/reflected/DOM XSS, output encoding, and why CSP is defense-in-depth not a substitute for encoding.

## Sources
- [OWASP — Cross Site Scripting](https://owasp.org/www-community/attacks/xss/) — overview
- [OWASP — XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) — deep-dive

## Core Definition
XSS injects executable script into a page another user's browser will run — sessions, DOM, and data are at risk.

## Key Concepts
XSS = attacker's JS runs in **victim origin** context:

```txt
Stored:  attacker saves <script> in DB → served to all viewers
Reflected: ?q=<script> in URL → echoed in response
DOM:     client JS writes location.hash to innerHTML unsafely
```

Browser same-origin rules then grant access to **cookies**, **localStorage**, DOM, and authenticated `fetch`.

Defense layers:
1. **Output encoding** — context-specific (HTML, attr, JS, URL)
2. **CSP** — [[content security policy]] restrict script sources
3. **HttpOnly cookies** — JS can't read session cookie
4. **Framework defaults** — React/Vue escape text nodes

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

**Why HttpOnly:** even if XSS exists, exfiltrating session cookie is harder (not impossible with CSRF combos).

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Reported script popup | Reproduce URL/param | Encode output; CSP; sanitize HTML |
| Session hijack spike | New script in stored fields | Audit DB content; WAF temporary |
| CSP breaks legit feature | Console violations | Nonce/hash; narrow allowlist |
| Markdown/HTML renderer XSS | Allowlist tags | Use safe parser; no raw HTML pass-through |

## Real-World Applications
Stored XSS in a comment field steals session cookies unless output is encoded and CSP blocks inline script.

## Pros/Cons or Trade-offs
- **Pro:** Clear attack classes (stored/reflected/DOM) map to concrete defenses.
- **Con:** Don't rely on **WAF alone** — fix source encoding. Don't disable CSP globally for one widget — isolate vendor subdomain.

## Comparison
- vs [[XSRF (cross-site request forgery)]]: XSS runs attacker script in the victim origin; CSRF forges requests using the victim's cookies.
- vs [[content security policy]]: CSP is defense-in-depth after encoding.

## Mistakes to Avoid
- `dangerouslySetInnerHTML` — name is accurate.
- JSON is not HTML-safe — `</script>` in JSON inside `<script>` breaks out.
- CSP bypass via JSONP/old plugins — audit third-party script allowlist.
- DOM XSS in SPA routers — `document.write`, `location` to sink.
