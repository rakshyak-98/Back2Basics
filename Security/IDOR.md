[[Security]] [[JWT authentication]] [[CORS (Cross Origin Request Sharing)]] [[cross-site scripting]]

# IDOR (Insecure Direct Object Reference)

> **Authorization bug**: client supplies object id (URL/body); server checks authentication but **not ownership** — attacker swaps id and reads/writes someone else's data. Includes auto-increment enumeration.

## Mental model

IDOR is a **broken access control** pattern, not a separate protocol attack. AuthN proves *who you are*; missing AuthZ check lets any logged-in user access `GET /api/orders/12345` by iterating ids.

```
Attacker (user A) ──► GET /invoice/1001 ──► 200 + victim data
                              │
                              └── server checked login, not invoice.owner == A
```

**Auto-increment IDs** make enumeration trivial; **UUIDs alone don't fix IDOR** — they only reduce scanning convenience.

## Standard config / commands

### Secure pattern (server-side)

```python
# BAD — trusts client-supplied id only
invoice = db.get(request.args['id'])

# GOOD — scope query to principal
invoice = db.get(id=request.args['id'], tenant_id=current_user.tenant_id)
if not invoice:
    return 404  # don't 403 leak existence across tenants
```

### Checklist for APIs

| Control | Implementation |
|---------|----------------|
| AuthZ on every object read/write | Policy: `resource.owner_id == user.id` or RBAC/ABAC |
| Indirect references | Opaque tokens mapping to internal id server-side |
| Tenant isolation | `tenant_id` in **every** query (row-level) |
| Mass assignment | Don't bind `user_id` from client body on create |
| GraphQL | Field-level auth; no unscoped node fetch by global id |

### HTTP / framework

```javascript
// Express — never trust params alone
app.get('/files/:id', requireAuth, async (req, res) => {
  const file = await File.findOne({ _id: req.params.id, userId: req.user.id });
  if (!file) return res.sendStatus(404);
  res.json(file);
});
```

### Testing (quick)

- Two test users A/B; capture A's resource id; replay as B → must **404/403**.
- Burp Autorize / custom script on sequential ids (staging only).

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Bug bounty "access other user's order" | Handler fetches by id only | Add ownership predicate; integration test |
| "Random UUID still leaked" | BOLA in microservice trust | Service-to-service authz; don't trust caller's user id header without signature |
| Admin panel sees all (by design?) | Missing role check on `/admin/*` | Separate admin role + audit log |
| Signed URL shared too wide | Presigned URL long TTL, no object binding | Short TTL; least privilege key |
| GraphQL `node(id:)` global ID | Decoded id bypasses parent scoping | Auth resolver per type |

## Gotchas

> [!WARNING]
> **404 vs 403** — cross-tenant prefer **404** to avoid confirming object exists (policy-dependent).

> [!WARNING]
> **UUID in JWT sub ≠ object authz** — still verify resource belongs to subject.

> [!WARNING]
> **Microservices**: gateway checked auth but internal service trusts `X-User-Id` header — forgeable without mTLS/signed internal token.

> [!WARNING]
> **Export/backup endpoints** — bulk CSV without row filter = mass IDOR.

## When NOT to use

- **Confusing with CSRF/XSS** — IDOR is missing server AuthZ; CSRF is unwanted action; XSS is script injection ([[cross-site scripting]], [[XSRF (cross-site request forgery)]]).
- **Rate limiting as fix** — slows enumeration, doesn't fix authorization.

## Related

[[Security]] · [[JWT authentication]] · [[CORS (Cross Origin Request Sharing)]] · [[DNS rebinding]] · [[cross-site scripting]]
