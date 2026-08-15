[[mysql connection]] [[mysql]] [[Configuration]] [[mysql user]]

# mysql ssl connection

> Encrypt the MySQL wire protocol with TLS — protect credentials and data in transit; required on most cloud-managed instances.

## Interview Relevance
Security-minded interviews ask `ssl-mode` levels and why `REQUIRED` without identity checks is weaker than `VERIFY_IDENTITY`.

## Sources
- [Encrypted Connections](https://dev.mysql.com/doc/refman/en/using-encrypted-connections.html) — deep-dive
- [CREATE USER SSL options](https://dev.mysql.com/doc/refman/en/create-user.html) — overview

## Key Concepts
- **Client ssl-mode ladder:** DISABLED → PREFERRED → REQUIRED → VERIFY_CA → VERIFY_IDENTITY.
- **Server requirement:** `ALTER USER … REQUIRE SSL` (or X509) enforces per account.
- **CA trust:** Managed services publish CA bundles — pin them.
- **Hostname verification:** Stops trusting a valid cert for the wrong host.

## Technical Details
```bash
mysql -h rds.example.com -u app -p --ssl-mode=VERIFY_IDENTITY \
  --ssl-ca=/etc/ssl/certs/rds-ca.pem
```

| Mode | Behavior |
|------|----------|
| `DISABLED` | Plaintext |
| `PREFERRED` | TLS if server supports |
| `REQUIRED` | TLS mandatory |
| `VERIFY_IDENTITY` | TLS + hostname verification |

```sql
ALTER USER 'app'@'%' REQUIRE SSL;
```

## Real-World Applications
All app pools to RDS/Cloud SQL use TLS with CA verification; break-glass admin sessions too.

## Pros/Cons or Trade-offs
- **Pro:** Confidentiality on untrusted networks; compliance checkbox that actually matters.
- **Con:** Cert rotation and CA bundle updates become operational work.
- **Trade-off:** `REQUIRED` alone vs full identity verification.

## Comparison
vs application-level encryption: TLS protects the pipe; column encryption protects data at rest from the DB operator — different threats.

## Mistakes to Avoid
- `PREFERRED` in production and silently falling back to plaintext.
- Skipping hostname verification against public CAs.
- Embedding expired CA files in container images.
