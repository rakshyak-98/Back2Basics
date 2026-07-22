[[NodeJS/open api specification]] [[ExpressJS/express error handler]] [[Security/JWT authentication]] [[Messaging/Web hooks]]

# Postman

> API client + collection runner + Newman CLI for CI — design, debug, and regression-test HTTP APIs — **Postman docs + contract testing in pipelines**.

## Mental model

Postman wraps HTTP: environments hold variables (`{{baseUrl}}`), collections group requests, tests run **JavaScript assertions** on responses. **Newman** runs the same collections headless in CI.

```
Collection
 ├── Request (method, URL, headers, body)
 ├── Pre-request script (sign JWT, set timestamp)
 ├── Tests (pm.test assertions)
 └── Environment (dev/stage/prod variables)

Local GUI ──export──► Newman in CI ──► JUnit/HTML report
```

| Piece | Role |
|-------|------|
| **Workspace** | Team sharing, forks |
| **Collection** | Versioned API test suite |
| **Environment** | Secrets + base URLs per stage |
| **Monitor** | Scheduled cloud runs (paid tiers) |

## Standard config / commands

### Install CLI (Linux)

```bash
curl -o- "https://dl-cli.pstmn.io/install/linux64.sh" | sh
postman --version
```

### Login (API key for cloud sync / Newman cloud)

```bash
postman login --with-api-key "$POSTMAN_API_KEY"
```

### Run collection locally

```bash
postman collection run ./collections/users.postman_collection.json \
  -e ./envs/staging.postman_environment.json \
  --reporters cli,junit \
  --reporter-junit-export results.xml
```

### Newman (npm — common in CI)

```bash
npm i -g newman
newman run collection.json -e staging.json --bail
```

### Lint OpenAPI-linked collection

```bash
postman api lint   # validates against linked API definition
```

### Example test script (in request **Tests** tab)

```javascript
pm.test('status 200', () => pm.response.to.have.status(200));
const json = pm.response.json();
pm.test('has id', () => pm.expect(json.id).to.be.a('string'));
pm.environment.set('lastUserId', json.id);
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `401` in CI, works in GUI | Missing env vars | Pass `-e` file; secrets in CI vault |
| Flaky tests on timestamps | Hard-coded dates | Use `pm.variables.replaceIn('{{$timestamp}}')` |
| SSL errors Newman | Corporate MITM cert | `NODE_EXTRA_CA_CERTS` or `--insecure` (dev only) |
| Collection run order wrong | Data dependencies | Use collection folders + explicit sequence |
| `postman login` fails | Typo in command | Correct: `postman login` (not `postman loging`) |

## Gotchas

> [!WARNING]
> Commit **environment templates** with empty secrets — never commit filled env JSON with prod API keys.

- **Pre-request vs test** timing — OAuth token refresh belongs in pre-request script.
- **Collection v2.1 vs OpenAPI import** — re-import may overwrite manual test edits.
- **Rate limits** — parallel Newman runs can DDoS your staging API; use `--delay-request`.

## When NOT to use

- Load testing at scale — use k6, Locust, or Gatling.
- Long-lived gRPC streaming — use grpcurl or dedicated clients (Postman supports gRPC but lighter tooling exists).

## Related

[[NodeJS/open api specification]] [[Security/JWT authentication]] [[ExpressJS/express error handler]] [[DevOps/Jenkins]]
