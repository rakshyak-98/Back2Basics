[[management]] [[Package Manager]] [[system service unit files]] [[supervisorctl]]

# Linux application management

> Application management on Linux is how you install, run, upgrade, and supervise a service — packages or images, plus systemd (or a process manager).

## Mental model

**Say it in one breath:** ship artifacts → run under a dedicated user → unit with restart/limits → logs + health checks.

```txt
artifact (deb/oci/bin) → User=myapp → systemd unit
                              │
                         journald + metrics
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **unit** | How it runs | “ExecStart + Restart + User.” |
| --- | --- | --- |
| **config vs data** | `/etc` vs `/var` | “Separate so upgrades don’t wipe state.” |
| **health check** | Ready/live | “Don’t mark healthy on listen alone.” |
| **rollback** | Prior version | “Keep n-1 artifacts.” |
| **12-factor logs** | stdout/err | “Let journald/collectors ship.” |

## Standard config / commands

```bash
sudo apt-get install myapp
# or: deploy binary to /usr/local/bin
sudo systemctl enable --now myapp
systemctl status myapp --no-pager
journalctl -u myapp -f
curl -fsS localhost:8080/healthz
```

| Knob | Why it matters |

| `Restart=on-failure` | Survive crashes |
| --- | --- |
| `EnvironmentFile=` | Secrets/config injection |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Won’t start | `status` + journal | Fix ExecStart/env/perms |
| Port in use | `ss -lntp` | Stop old process; fix unit |
| Works manually not as service | cwd/env/user | Match unit environment |
| Upgrade broke config | Diff `/etc` | Restore; migrate schema |

## Gotchas

> [!WARNING]
> **Running as root “just to work”** — fix permissions instead.

> [!WARNING]
> **Two supervisors** (systemd + supervisord + docker restart) fight each other.

## When NOT to use

- **One-shot CLI tools** — no service needed.
- **Multi-tenant SaaS** — prefer k8s/orchestrator over ad-hoc host services.

## Related

[[system service unit files]] [[Package Manager]] [[supervisorctl]] [[Setup Non-Login user from Running process]]
