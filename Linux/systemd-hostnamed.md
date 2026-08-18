[[systemd]] [[systemctl]] [[D-Bus]]

# systemd-hostnamed

> systemd-hostnamed is the daemon behind `hostnamectl` — static/pretty/transient hostname via D-Bus.

## Mental model

**Say it in one breath:** `hostnamectl` → D-Bus → hostnamed; `/etc/hostname` is what survives reboot.

```txt
hostnamectl ──D-Bus──► systemd-hostnamed
                              │
                              ├─ /etc/hostname (static)
                              └─ kernel utsname (runtime)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **static hostname** | `/etc/hostname` | “What comes back after reboot.” |
| --- | --- | --- |
| **pretty hostname** | Human display name | “Can have spaces — not for DNS.” |
| **transient** | Runtime-only | “DHCP/cloud may set it.” |
| **hostnamectl** | CLI front-end | “Prefer over hand-editing files.” |
| **chassis** | desktop/server/vm | “Hint for UI/power policy.” |

## Standard config / commands

```bash
hostnamectl
sudo hostnamectl set-hostname api-prod-01
sudo hostnamectl set-hostname "API Prod 01" --pretty
cat /etc/hostname
hostname -f
systemctl status systemd-hostnamed
```

| Knob | Why it matters |

| `set-hostname` | Updates static + runtime |
| --- | --- |
| `--pretty` | UI label only |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Name reverts after reboot | cloud-init / DHCP | Pin in cloud-init; stop overwrite |
| hostnamectl fails | hostnamed down | `systemctl status systemd-hostnamed` |
| Apps see old name | Cache / hosts | Restart app; fix `/etc/hosts` |
| FQDN wrong | `/etc/hosts` | Align IP ↔ hostname entries |

## Gotchas

> [!WARNING]
> **Pretty ≠ DNS** — never put spaces in the static hostname.

> [!WARNING]
> **Cloud images** often rewrite hostname every boot via cloud-init.

## When NOT to use

- **DNS search domains** — that’s resolved/NetworkManager.
- **Container/pod names** — namespace-local; hostnamed won’t rename a pod.

## Related

[[systemd]] [[systemctl]] [[D-Bus]] [[NTP sync]]
