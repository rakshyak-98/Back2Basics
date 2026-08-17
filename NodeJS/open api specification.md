[[expressjs]] [[gRPC]] [[JWT authentication]] [[CORS (Cross Origin Request Sharing)]] [[webhook]]

# OpenAPI specification

> API contract as machine-readable truth — design, codegen, validation, and breaking-change discipline for service engineers — **OpenAPI 3.x**.

```txt
        OpenAPI specificat ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use **OpenAPI specification** to check whether you can explain t…

## Sources
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) — deep-dive
- [Wikipedia — open api specification](https://en.wikipedia.org/wiki/open_api_specification) — overview

## Key Concepts
- **Spec:** Source of truth for routes + models — | **Codegen**
- **Runtime validation:** Reject bad requests at boundary (ajv, express-openapi-validator)


- **Core:** OpenAPI (Swagger) describes **paths, schemas, authentication, and errors** in…

## Technical Details
- OpenAPI (Swagger) describes **paths, schemas, authentication, and errors** in…
- It is the handshake between teams: frontend, backend, QA, and gateway policie…

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

- **Contract-first:** write specification → review → generate stubs → implement.
- **Code-first:** annotate controllers → export specification

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

### Breaking change rules (SE discipline)

| Change | Breaking? | Safe alternative |
|--------|-----------|------------------|
| Remove endpoint/field | **Yes** | Deprecate → sunset header → v2 path |
| Add **required** request field | **Yes** | Optional with default; or new `/v2` |
| Narrow enum / widen type | **Yes** | Add new enum value; new field `statusV2` |
| Add optional response field | No | — |
| Rename field | **Yes** (clients) | Keep old + new during migration |
| Change error shape | Often yes | Version media type or path |

- **Versioning:** prefer URL `/v1` or header `Accept: application/vnd.company.o…
- Don't rely on `info.version` alone — consumers ignore it.

## Mistakes to Avoid
- **Spec drift**::** → docs lie. Treat spec mismatch as build failure
- **Mistake:** **`additionalProperties: false`**
- **Mistake:** **Codegen merge pain**
- **Mistake:** **oneOf/anyOf validation**
- **Mistake:** **OpenAPI ≠ gRPC**
- **Mistake:** **400 "request did not match schema":** check Validator logs
- **Mistake:** **Generated types out of date:** check CI codegen diff
- **Mistake:** **Prod 500, dev fine:** check `validateResponses: true` in prod
- **Mistake:** **Gateway rejects valid JWT:** check `securitySchemes` mismatch
- **Mistake:** **False breaking CI:** check Intentional major bump

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (API contract as machine-readable truth — design, codegen, validation, and breaki…).
- **Con / when not:** **Internal-only service** with one caller and shared mono…
- **Con / when not:** **Streaming / WebSocket-primary APIs**
- **Con / when not:** **Early prototype**

## Comparison
- vs [[expressjs]]: know when each applies


### Use cases
- In production APIs and tooling, **open api specification** shows up whenever …
