[[Package Manager]] [[system service unit files]] [[supervisorctl]] [[Setup Non-Login user from Running process]] [[apt package manager]]

# Linux application management

> How you install, run, upgrade, and supervise a service on a host — packages or images, plus systemd (or another process manager).

## Interview Relevance

Lifecycle story: artifact → non-root user → unit with Restart → health check → journal — and avoid dual supervisors.

## Sources

- [systemd.service(5)](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) — deep-dive
- [12-Factor App — Logs](https://12factor.net/logs) — overview

## Key Concepts

- **Unit defines runtime:** `ExecStart`, `User=`, `Restart=`.
- **Config vs data:** `/etc` vs `/var` so upgrades don’t wipe state.
- **Health ≠ listen:** probe readiness, not only bind success.
- **One supervisor:** systemd *or* Supervisor/Docker restart — not both fighting.

## Technical Details

```txt
artifact (deb/oci/bin) → User=myapp → systemd unit
                              │
                         journald + metrics
```

```bash
sudo apt-get install myapp
sudo systemctl enable --now myapp
systemctl status myapp --no-pager
journalctl -u myapp -f
curl -fsS localhost:8080/healthz
```

| Knob | Why it matters |
|------|----------------|
| `Restart=on-failure` | Survive crashes |
| `EnvironmentFile=` | Config/secrets injection |

| Symptom | Check | Fix |
|---------|-------|-----|
| Won’t start | `status` + journal | Fix ExecStart/env/perms |
| Port in use | `ss -lntp` | Stop old process; fix unit |
| Works manually not as service | cwd/env/user | Match unit environment |
| Upgrade broke config | Diff `/etc` | Restore; migrate schema |

## Real-World Applications

Deploy an API deb: package installs binary + unit, runs as `User=app`, logs to journal, `/healthz` gates the load balancer.

## Pros/Cons or Trade-offs

- **Pro:** Clear host-local lifecycle with audit-friendly units.
- **Con:** Multi-tenant SaaS usually wants an orchestrator, not ad-hoc host services.

## Comparison

- vs [[supervisorctl]]: legacy Python supervisor vs native systemd.
- vs Kubernetes: node-local app management vs cluster scheduling.

## Mistakes to Avoid

- Running as root “just to work” instead of fixing permissions.
- Running systemd and supervisord for the same process.
- Marking healthy on port open alone.
