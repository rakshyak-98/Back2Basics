[[Linux]] [[gsetting]] [[editor configuration]] [[X Desktop Group]]

# Linux configuration

> Linux configuration is scattered on purpose — `/etc` for system, `~/.config` for user, unit drop-ins for services; know which layer wins.

## Mental model

**Say it in one breath:** system files in `/etc`, user XDG in `~/.config`, runtime in `/run`; overrides beat vendors.

```txt
vendor (/usr/lib, /lib) < /etc < drop-ins < runtime
user: ~/.config (XDG) + dconf for GNOME
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **`/etc`** | Host config | “Survives package updates if done right.” |
| --- | --- | --- |
| **drop-in** | Partial override | “systemd `.d/*.conf` pattern.” |
| **XDG** | User config dirs | “`~/.config`, not random dotfiles only.” |
| **dconf** | GNOME binary store | “Use gsettings.” |
| **sysctl** | Kernel knobs | “`/etc/sysctl.d`.” |

## Standard config / commands

```bash
# system
ls /etc/systemd/system
sudo sysctl --system
# user
echo "$XDG_CONFIG_HOME"
ls ~/.config | head
# GNOME
gsettings list-schemas | head
dconf dump /org/gnome/ | head
```

| Knob | Why it matters |

| File vs DB config | Backup/diff story differs |
| --- | --- |
| Permissions on `/etc` | Secrets stay 600 |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Change ignored | Wrong layer / cache | Confirm path; restart service; daemon-reload |
| Lost after upgrade | Edited vendor file | Move to `/etc` drop-in |
| User setting missing | Wrong account | Configure the desktop user, not root |
| Conflict | Two tools edit same key | Pick one source of truth |

## Gotchas

> [!WARNING]
> **Editing files under `/usr`** — upgrades overwrite; use `/etc`.

> [!WARNING]
> **Mixing Ansible and hand edits** without drift detection causes ghosts.

## When NOT to use

- **Ephemeral containers** — bake configuration at image build or inject environment.
- **Secrets in world-readable conf** — use tmpfs/agents/KMS.

## Related

[[etc files]] [[system service unit files]] [[gsetting]] [[sysctl]] [[editor configuration]]
