[[content security policy]] [[SOP (Same-Origin Policy)]] [[IDOR]] [[response header]]

# Cross-site scripting (XSS)

> Injection of executable script into a page another user's browser will run — steals sessions, defaces UI, exfiltrates data.

---

## Mental model

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Reported script popup | Reproduce URL/param | Encode output; CSP; sanitize HTML |
| Session hijack spike | New script in stored fields | Audit DB content; WAF temporary |
| CSP breaks legit feature | Console violations | Nonce/hash; narrow allowlist |
| Markdown/HTML renderer XSS | Allowlist tags | Use safe parser; no raw HTML pass-through |

---

## Gotchas

> [!WARNING]
> **`dangerouslySetInnerHTML`** — name is accurate.

> [!WARNING]
> **JSON is not HTML-safe** — `</script>` in JSON inside `<script>` breaks out.

> [!WARNING]
> **CSP bypass via JSONP/old plugins** — audit third-party script allowlist.

> [!WARNING]
> **DOM XSS in SPA routers** — `document.write`, `location` to sink.

---

## When NOT to use

Don't rely on **WAF alone** — fix source encoding. Don't disable CSP globally for one widget — isolate vendor subdomain.

---

## Related

[[content security policy]] [[SOP (Same-Origin Policy)]] [[XSRF (cross-site request forgery)]] [[JWT authentication]] [[response header]]
