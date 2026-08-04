# Vault INDEX — Fast Retrieval

> Start here under pressure. Each link is meant to be **operational**, not encyclopedic.
> Note format: [[NOTES_STANDARD]]

---

## On-call / debug first

| Symptom / need | Go to |
|----------------|-------|
| EMFILE / “too many open files” | [[file descriptors]] · [[ss]] |
| Disk “saved” but data gone after crash | [[fsync]] · [[WAL (Write-Ahead Log)]] · [[ACID]] |
| Process killed, no clear app error | [[OOM (Linux Out Of Memory)]] · [[Linux cgroup]] |
| TCP weirdness / half-open / listen state | [[ss]] · [[half-open connections]] · [[Epoll]] |
| DNS not resolving / wrong answer | [[DNS]] · [[dig]] · [[DNS zone]] |
| SSH auth fails / wrong key | [[ssh agent]] · [[SSH authentication]] · [[ssh allow local system with key]] |
| Nginx 502/504/499 | [[Configuration]] · [[nginx using unix socket]] |
| Container won’t start / compose drift | [[Docker compose]] · [[docker cli]] · [[Docker Runtime Security]] |
| Pod CrashLoop / not Ready | [[Pods]] · [[kubectl]] · [[ingress]] |
| Create / apply a Pod manifest | [[kubectl pod creation]] · [[Pods]] · [[kubectl]] |
| Certbot / TLS renew fail | [[certbot error]] · [[TLS (Transport Layer Security)]] · [[ACME server]] |
| Terraform state lock / drift | [[Terraform workflow]] · [[Terraform CLI]] · [[variable file]] |
| Redis latency / OOM / eviction | [[redis-cli]] · [[redis installation]] |
| Slow query / missing index | [[covering index]] · [[mysql index]] · [[Data access patterns]] |
| Postgres `inconsistent types deduced for parameter $n` | [[postgres/postgres parameter type error]] |
| TLS not yet valid / JWT expired / clock skew | [[NTP sync]] · [[date]] · [[TLS (Transport Layer Security)]] |

---

## Domain hubs

### OS & Linux
- Kernel I/O path: [[file descriptors]] · [[Epoll]] · [[fsync]] · [[Buffer cache]] · [[multiple levels of buffering]]
- Window / display: [[i3 Window Manager Starter Guide]] · [[wayland]] · [[WM_CLASS]]
- Process/memory: [[Linux Process Theory]] · [[context switching]] · [[OOM (Linux Out Of Memory)]] · [[mutexes]] · [[non-blocking]]
- Observability: [[eBPF]] · [[top]] · [[journalctl]] · [[systemctl]]
- Time: [[NTP sync]] · [[date]]
- Boot/disk: [[MBR]] · [[inittramfs]] · [[file mount]]

### Networking & DNS
- [[routing table]] · [[BGP]] · [[half-open connections]] · [[connection chrun]] · [[webSocket]]
- [[DNS]] · [[DNS zone]] · [[mDNS]] · [[name server]] · [[public resolver]]

### Containers & orchestration
- [[Docker compose]] · [[docker file]] · [[docker container]] · [[Docker Runtime Security]]
- [[Pods]] · [[kubectl]] · [[Kubernetes services]] · [[ingress]] · [[Cilium]]

### IaC
- [[terraform]] · [[Terraform workflow]] · [[Terraform setup]] · [[variable file]] · [[Terraform CLI]]

### AWS
- [[AWS Networking]] · [[Elastic IP]] · [[Security group]] · [[Route53]] · [[aws STS (Security Token Service)]] · [[IAM]] · [[AWS EC2]] · [[AWS ECR]] · [[AWS Lambda]]

### Data stores
- Semantics: [[ACID]] · [[BASE]] · [[WAL (Write-Ahead Log)]] · [[OLTP]] · [[OLAP]]
- MySQL/Postgres: [[mysql]] · [[covering index]] · [[connection pooling]] · [[psql essential]]
- Redis: [[redis-cli]] · [[redis installation]]
- Mongo: [[WiredTiger storage engine]] · [[MongoDB]]

### Security & access
- [[SSH authentication]] · [[ssh agent]] · [[JWT authentication]] · [[CORS (Cross Origin Request Sharing)]]
- [[TLS (Transport Layer Security)]] · [[single-sign-on (SSO)]] · [[IDOR]]

### Protocols & APIs
- [[gRPC]] · [[SMTP]] · [[MQTT]] · [[HTTP module]]

### Software architecture
- [[Multi-tier and Layered Architecture]] · [[presentation layer]] · [[Service Layer]] · [[frontend layered architecture]] · [[Orchestration layer]]

### Design patterns (apply in projects)
- Hub / principles: [[Design pattern]]
- Creational: [[Design pattern/Factory Method]] · [[Design pattern/Creation pattern/Abstract Factory]] · [[Design pattern/Builder]] · [[Design pattern/Singleton]]
- Structural: [[Design pattern/Adapter]] · [[Design pattern/Bridge]] · [[Design pattern/Decorator]] · [[Design pattern/Facade]] · [[Design pattern/Proxy]]
- Behavioral: [[Design pattern/Strategy pattern]] · [[Design pattern/Chain of Responsibility]] · [[Design pattern/Template Method]] · [[Design pattern/Observer]] · [[Design pattern/Command]] · [[Design pattern/State]] · [[Design pattern/Mediator]] · [[Design pattern/Memento]] · [[Design pattern/Dependency Injection]]

### Git / delivery
- [[git error]] · [[git rebase]] · [[git ssh config]] · [[git worktree]]
- Deploy CLIs: [[Deployment/render cli]] · [[Deployment/vercel cli]] · [[Deployment/vercel deployment]] · [[Netlify/Netlify deployment]]

---

## Quality ceiling (copy these patterns)

| Note | Why copy it |
|------|-------------|
| [[Terraform workflow]] | Mental model + command loop + book-backed |
| [[variable file]] | Typed configs + precedence + warnings |
| [[Configuration]] (Nginx) | Real production configs |
| [[gRPC]] | Deadlines, interceptors, failure thinking |
| [[routing table]] | Short + high-signal gotcha |
| [[ssh agent]] | Multi-key reality + systemd unit |

---

## Empty / stub policy

1. Fill if on-call relevant (P0/P1 in [[NOTES_STANDARD]]).
2. Merge duplicates into one canonical note; leave a stub redirect with `→ [[Canonical]]`.
3. Delete only if the title has no engineering value (prefer redirect).
