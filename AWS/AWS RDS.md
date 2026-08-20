[[AWS]] [[AWS Networking]] [[Security group]] [[connection pooling]] [[AWS Secrets Manager]] [[KMS]] [[AWS Billing and cost management]]

# AWS RDS

> Managed relational DB (MySQL, Postgres, MariaDB, SQL Server, Oracle, Aurora) — you manage schema and connections; AWS manages patching, Multi-AZ failover, and backups. **SG + SSL + connection storms** are the production killers.

## Mental model

RDS runs DB engines on managed instances in **your VPC** (private subnets). Endpoint DNS points at the writer (Multi-AZ: standby in another AZ for failover, **not** a read scale-out). **Read replicas** are separate for scale-out. Storage is EBS-backed (or Aurora distributed storage).

```
App ──► RDS Proxy (optional) ──► writer endpoint
                                      │ Multi-AZ sync standby
App ──► reader endpoint(s) ───────────┘ replicas (async)
```

| Feature | Meaning |
|---------|---------|
| **Multi-AZ** | Sync standby; failover minutes; same endpoint |
| **Read replica** | Async copy; separate endpoint; lag possible |
| **Parameter group** | Engine knobs (`max_connections`, SSL) |
| **RDS Proxy** | Connection multiplex for Lambda/spiky apps ([[connection pooling]]) |

## Standard config / commands

### Prod checklist

| Setting | Choice | Why |
|---------|--------|-----|
| Subnet group | Private data tier, ≥2 AZ | No public IP |
| Publicly accessible | No | SG + bastion/SSM only |
| SG | Inbound 5432/3306 from `app-sg` only | Not `0.0.0.0/0` |
| Encryption | Storage encrypted + SSL require | KMS + `sslmode=require` |
| Backup | Retention ≥7; copy snapshots cross-region for DR | PITR |
| Secrets | Master secret in Secrets Manager | Rotation |

```bash
aws rds describe-db-instances --db-instance-identifier app-prod \
  --query 'DBInstances[0].{Endpoint:Endpoint,MultiAZ:MultiAZ,Status:DBInstanceStatus}'

aws rds describe-db-log-files --db-instance-identifier app-prod
```

### SSL

Many engines need CA bundle (`rds-ca-rsa2048-g1`). Postgres: `sslmode=require` or `verify-full`. MySQL: `ssl: 'Amazon RDS'` in node drivers.

### Connection math

```
max_connections ≈ (memory formula) ; app pools × tasks must stay under it
Lambda: prefer RDS Proxy or Data API — one pool per concurrent env explodes
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Connection timed out | SG; subnet route; public flag; NACL | Open from app SG; private path ([[Security group]]) |
| `too many connections` | `SHOW PROCESSLIST` / `pg_stat_activity` | Lower pools; RDS Proxy; kill idle |
| Failover surprise | Multi-AZ event; DNS TTL | Retry with backoff; verify Multi-AZ |
| Replica lag | CW `ReplicaLag` | Reduce load; bigger replica; don't read-your-writes on replica |
| Auth fail after rotate | Secrets Manager rotation mid-deploy | Proxy IAM auth or refresh secret |
| Storage full | CW `FreeStorageSpace` | Autoscale storage; vacuum; archive |
| SSL required errors | Parameter `rds.force_ssl` | Client SSL config |

## Gotchas

> [!WARNING]
> **Multi-AZ ≠ read scaling** — standby does not take reads; use replicas.

> [!WARNING]
> **Publicly accessible + `0.0.0.0/0` SG** — ransomware bait; never for prod.

> [!WARNING]
> **Major version upgrade** — downtime / blue-green; test parameter group compatibility.

> [!WARNING]
> **Stopped instances still bill storage**; auto-restart after 7 days if stopped.

## When NOT to use

- **Key-value / single-digit-ms at huge scale** — consider [[AWS DynamoDB]].
- **Serverless spiky without Proxy** — connection storms; use Proxy or Aurora Serverless v2 carefully.
- **Need full OS / custom kernel modules** — self-managed on EC2 (rare).

## Related

[[AWS Networking]] · [[Security group]] · [[connection pooling]] · [[AWS Secrets Manager]] · [[KMS]] · [[AWS DynamoDB]] · [[AWS Billing and cost management]] · [[AWS]]
