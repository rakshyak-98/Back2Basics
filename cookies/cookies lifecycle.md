
**Cookies types**
- Session -> deleted when tab/session ends
- Persistent -> stored until expiration
- Host-only -> not shared with subdomains

**Storage rules**
- Stored per domain + path scope
- Public suffix protection (cannot set `.com` etc)
- Attributes control visibility/security

`Path` -> Which routes auto-send this cookie
`Domain` -> Which subdomains can access it
`Max-Age/Expires` -> Defines **persistence**
`HttpOnly` -> JavaScript **cannot** read it
`Secure` -> Only over **HTTPS**
`SameSite` -> Controls cross-site sending
`Priority` -> Browser eviction order

**Automatic sending in requests**
- Browser checks domain + path + security flag
- If matched -> adds to `Cookie:` request header

`SameSite=Lax/strict` -> blocks many cross-site sends (CSRF defence).
`HttpOnly` -> protects from [[XSS cookie]]

**Phases**: `Client Request → Server Response (Set-Cookie) → Client Stores → Subsequent Requests → Server Reads → Expiry / Manual Deletion`

---
## 1. **Creation (Server → Client)**
### Server sets a cookie:
- **HTTP Header**:
```
Set-Cookie: sessionId=abc123; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=3600
```

### Lifecycle Impact:
- Sent in the **HTTP response** from server to browser.
- Browser **parses and stores** this in its cookie jar **if**:
	- Domain & Path match
	- Not blocked by `HttpOnly`, `Secure`, `SameSite` conditions
	
---

## 2. **Storage (Client Side)**
### Browser stores cookies:
- **In-memory** (session cookie)
- Or **on-disk** (persistent cookie)  

> [!NOTE]
> Controlled by: `Max-Age=<seconds>` or `Expires=<date>`

### Edge Cases:
- No `Max-Age` or `Expires` ⇒ destroyed on browser close
- Cookies per domain: 180–300 max (~4KB each)

---

## 3. **Transmission (Client → Server)**
### Automatic sending by browser:
- On every **request** matching the domain/path:
```
Cookie: sessionId=abc123
```
### Constraints:
- `Secure`: only sent over HTTPS
- `HttpOnly`: JS cannot access via `document.cookie`
- `SameSite`:
	- `Lax`: sends on top-level GETs
	- `Strict`: only same-origin
	- `None`: sent on cross-site _if Secure_

---

## 4. **Usage (Server Side)**
### Server reads cookies:
- From the `Cookie:` header
- In Node.js/Express (example):
```js
req.cookies['sessionId']
```

### Validations (common use cases):
- Auth tokens
- Preferences
- CSRF tokens

---

## 5. **Updating / Deleting**
### Update:
- Re-`Set-Cookie:` with same name, new value
### Delete:
- Set cookie with `Max-Age=0` or `Expires=Past`
```http
Set-Cookie: sessionId=; Max-Age=0; Path=/
```

---

## 6. **Access Control**

| Method         | Can JS Access         | Sent with Requests | Notes                            |
| -------------- | --------------------- | ------------------ | -------------------------------- |
| `HttpOnly`     | ❌                     | ✅                  | secure, cannot be stolen via XSS |
| Non-`HttpOnly` | ✅ (`document.cookie`) | ✅                  | useful for preferences           |

---

## 7. **Client-Side Manual Cookie Control**
```js
document.cookie = "theme=dark; Max-Age=3600; Path=/";
```
- Cannot set `HttpOnly`, `Secure`, `SameSite` via JS
- JS can read only non-`HttpOnly`

---

## 8. **Common Gotchas**
> [!NOTE]
> CORS must allow credentials: 
> - Frontend: `fetch(url, { credentials: "include" })` 
> - Server: `Access-Control-Allow-Credentials: true`

- Cross-site cookies require `SameSite=None; Secure`
- Domain mismatch (subdomain issues)
- Clock skew can affect expiry

---

## Cookie Flow Summary
```text
Client  ─────────▶  Server
        [Request w/ no cookie]

Client  ◀─────────  Server
        [Set-Cookie: sessionId=abc123]

Client stores sessionId=abc123

Client  ─────────▶  Server
        [Cookie: sessionId=abc123]

Server uses cookie data for auth/state
```
