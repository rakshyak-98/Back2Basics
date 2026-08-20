[[AWS]] [[AWS Lambda]] [[IAM]] [[ARN (Amazon Resource Name)]] [[ALB (Application Load Balancer)]] [[CloudWatch]] [[JWT authentication]]

# API Gateway

> Managed HTTP front door to Lambda (and HTTP proxies) — **HTTP API** (cheaper/simpler) vs **REST API** (full feature set). Auth, throttling, and `lambda:InvokeFunction` permission mistakes dominate outages.

## Mental model

Client hits a **stage** URL → API Gateway applies **auth / throttle / routes** → integration (Lambda proxy, HTTP, AWS service). For Lambda, Gateway needs **resource-based permission** on the function (`lambda:InvokeFunction` for `apigateway.amazonaws.com`).

```
Client ──► API Gateway (stage) ──► Lambda / HTTP
                │
                ├── Authorizer (JWT / Lambda)
                └── Usage plan / throttle
```

| Type | Use when |
|------|----------|
| **HTTP API** | JWT/OIDC, Lambda proxy, lower latency/cost |
| **REST API** | API keys, WAF association legacy features, request validation richness |
| **WebSocket API** | Bidirectional; connection management burden |

vs [[ALB (Application Load Balancer)]]: ALB for VPC fleets / path to EC2/ECS; API Gateway for serverless edge + managed auth/throttle.

## Standard config / commands

### Lambda permission (required)

```bash
aws lambda add-permission \
  --function-name api-handler \
  --statement-id AllowAPIGW \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:REGION:ACCOUNT:APIID/*/*"
```

### Deploy / invoke

```bash
aws apigatewayv2 get-apis
curl -i "https://{api-id}.execute-api.{region}.amazonaws.com/{stage}/health"
```

### Auth patterns

| Pattern | Notes |
|---------|-------|
| JWT authorizer (HTTP API) | Validate issuer/audience at edge |
| Lambda authorizer | Custom; cache policy carefully |
| IAM SigV4 | Service-to-service |
| None + app auth | Only behind CloudFront/WAF with care |

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 403 Missing Authentication Token | Wrong path/method/stage | Exact resource path; trailing slash |
| 500 / Lambda Integration failure | Permission; Lambda error | `add-permission`; check [[CloudWatch]] `/aws/lambda/...` |
| 401/403 authorizer | JWT claims; audience; clock skew | Fix issuer; NTP; authorizer cache TTL |
| Throttled 429 | Stage/account limits; usage plan | Raise limits; backoff |
| CORS preflight fail | OPTIONS route; Gateway CORS config | Configure CORS on HTTP API |
| Timeout | Gateway max 29s integration | Move long work to async SQS |

## Gotchas

> [!WARNING]
> **29-second hard integration timeout** (REST/HTTP) — long jobs must be async.

> [!WARNING]
> **Lambda permission source-arn too wide** (`/*/*`) — tighten to stage/method when possible.

> [!WARNING]
> **REST vs HTTP API** — features and console/CLI (`apigateway` vs `apigatewayv2`) differ; don't mix docs.

> [!WARNING]
> **Stage variables / deploy** — changing config without deploy leaves old stage live.

## When NOT to use

- **Heavy L7 routing to many EC2/ECS services** — ALB (+ path rules).
- **WebSockets at huge scale with sticky brokers** — dedicated connection layer.
- **Public static files** — S3 + CloudFront.

## Related

[[AWS Lambda]] · [[IAM]] · [[ARN (Amazon Resource Name)]] · [[ALB (Application Load Balancer)]] · [[CloudWatch]] · [[JWT authentication]] · [[AWS SQS]] · [[AWS]]
