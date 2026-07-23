[[expressjs]] [[gRPC]] [[JWT authentication]] [[CORS (Cross Origin Request Sharing)]] [[webhook]]

# OpenAPI specification

> API contract as machine-readable truth — design, codegen, validation, and breaking-change discipline for service engineers — **OpenAPI 3.x**.

---

## Mental model

OpenAPI (Swagger) describes **paths, schemas, auth, and errors** in YAML/JSON. It is the handshake between teams: frontend, backend, QA, and gateway policies all read the same file.

```txt
┌─────────────┐     openapi.yaml      ┌─────────────┐
│ API author  │ ────────────────────► │   Repo CI   │
└─────────────┘                       └──────┬──────┘
                                           │
              ┌────────────────────────────┼────────────────────────────┐
              ▼                            ▼                            ▼
        Server stubs                 Client SDK                   Contract tests
        (validation)                 (TypeScript)                  (Schemathesis)
```

| Artifact | Purpose |
|----------|---------|
| **Spec** | Source of truth for routes + models |
| **Codegen** | Types/clients/servers — never hand-write DTOs twice |
| **Runtime validation** | Reject bad requests at boundary (ajv, express-openapi-validator) |
| **Diff (oasdiff, openapi-diff)** | CI gate on breaking changes |

**Contract-first:** write spec → review → generate stubs → implement. **Code-first:** annotate controllers → export spec — faster to start, drifts unless CI enforces sync.

---

## Standard config / commands

### Minimal spec fragment

```yaml
openapi: 3.0.3
info:
  title: Orders API
  version: 1.2.0
paths:
  /orders/{id}:
    get:
      operationId: getOrder
      parameters:
        - name: id
          in: path
          required: true
          schema: { type: string, format: uuid }
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '404':
          $ref: '#/components/responses/NotFound'
components:
  schemas:
    Order:
      type: object
      required: [id, status]
      properties:
        id: { type: string, format: uuid }
        status: { type: string, enum: [pending, shipped] }
```

### Express + openapi-validator + ajv

```javascript
import express from 'express';
import * as OpenApiValidator from 'express-openapi-validator';

const app = express();
app.use(express.json());

app.use(
  OpenApiValidator.middleware({
    apiSpec: './openapi.yaml',
    validateRequests: true,
    validateResponses: process.env.NODE_ENV !== 'production', // dev only — perf cost
  })
);

app.get('/orders/:id', (req, res) => {
  res.json({ id: req.params.id, status: 'pending' });
});

app.use((err, req, res, next) => {
  res.status(err.status || 500).json({ error: err.message });
});
```

### Codegen (TypeScript client)

```shell
npm i -D @openapitools/openapi-generator-cli
npx openapi-generator-cli generate \
  -i openapi.yaml -g typescript-fetch -o src/generated/api
```

### CI breaking-change check

```shell
npm i -D oasdiff
oasdiff breaking openapi.yaml openapi.main.yaml
# Exit 1 on: removed endpoint, new required field, type change, enum shrink
```

---

## Breaking change rules (SE discipline)

| Change | Breaking? | Safe alternative |
|--------|-----------|------------------|
| Remove endpoint/field | **Yes** | Deprecate → sunset header → v2 path |
| Add **required** request field | **Yes** | Optional with default; or new `/v2` |
| Narrow enum / widen type | **Yes** | Add new enum value; new field `statusV2` |
| Add optional response field | No | — |
| Rename field | **Yes** (clients) | Keep old + new during migration |
| Change error shape | Often yes | Version media type or path |

**Versioning:** prefer URL `/v1` or header `Accept: application/vnd.company.orders.v2+json`. Don't rely on `info.version` alone — consumers ignore it.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 400 "request did not match schema" | Validator logs; compare body vs spec | Spec too strict or client drift — fix spec or client |
| Generated types out of date | CI codegen diff | Regenerate on spec merge; commit generated output |
| Prod 500, dev fine | `validateResponses: true` in prod | Disable response validation in prod |
| Gateway rejects valid JWT | `securitySchemes` mismatch | Align bearer format with [[JWT authentication]] |
| False breaking CI | Intentional major bump | Bump `/v2`, baseline new spec file |

---

## Gotchas

> [!WARNING]
> **Spec drift** — code-first without CI diff → docs lie. Treat spec mismatch as build failure.

> [!WARNING]
> **`additionalProperties: false`** — strict mode breaks forward-compatible clients adding fields. Use intentionally at trust boundaries only.

> [!WARNING]
> **Codegen merge pain** — commit generated code or generate in CI; don't hand-edit generated files.

> [!WARNING]
> **oneOf/anyOf validation** — ajv errors are cryptic. Prefer flat schemas for public APIs.

> [!WARNING]
> **OpenAPI ≠ gRPC** — for high-performance internal RPC, [[gRPC]] + protobuf; expose REST/OpenAPI at edge only.

---

## When NOT to use

- **Internal-only service** with one caller and shared monorepo — protobuf/ts types may suffice.
- **Streaming / WebSocket-primary APIs** — OpenAPI support is awkward; document separately.
- **Early prototype** — don't codegen before shape stabilizes; sketch spec yes, gate no.

---

## Related

[[expressjs]] [[gRPC]] [[webhook]] [[JWT authentication]] [[CORS (Cross Origin Request Sharing)]]
