[[Linux]] [[apt package manager]] [[APT policy]] [[gpg]] [[source list file]]

# apt config

> apt config is the file layout that steers repos, pins, and keys — sources, preferences, apt.conf snippets, keyrings.

## Mental model

**Say it in one breath:** lists say *where* packages come from; preferences say *which version wins*; keyrings say *whom we trust*; apt.conf.d tweaks *behavior*.

```txt
/etc/apt/sources.list(+.d)     → repositories
/etc/apt/preferences(+.d)      → pinning ([[APT policy]])
/etc/apt/keyrings + signed-by= → trust (modern)
/etc/apt/apt.conf.d/           → proxies, retries, recommends
/var/lib/apt/lists/            → cached indexes
/var/cache/apt/archives/       → downloaded .debs
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **`sources.list.d`** | Drop-in repo files | “Vendor packages ship one file each.” |
| --- | --- | --- |
| **`signed-by=`** | Per-repo key | “Safer than a global trusted keyring.” |
| **`preferences.d`** | Pins | “Keep prod on a known candidate.” |
| **Hit/Get/Err** | update line status | “Err stops trust; Ign is often harmless.” |
| **`apt-config dump`** | Effective settings | “See what snippets actually applied.” |

## Standard config / commands

| Path | Purpose |
| --- | --- |
| `/etc/apt/sources.list` | Primary repos |
| `/etc/apt/sources.list.d/` | Extra `.list` / `.sources` |
| `/etc/apt/preferences.d/` | Pinning |
| `/etc/apt/apt.conf.d/` | Behavior snippets |
| `/etc/apt/auth.conf.d/` | Private repo creds |
| `/etc/apt/keyrings/` | Binary keys for `signed-by=` |
| `/var/lib/apt/lists/` | Metadata cache |
| `/var/cache/apt/archives/` | `.deb` cache |

```bash
apt-config dump | less
ls /etc/apt/sources.list.d/
ls /etc/apt/apt.conf.d/
sudo apt update
sudo apt clean          # clear archives
sudo apt autoclean
```

## update output lexicon

| Prefix | Meaning | Action |
| --- | --- | --- |
| **Hit:** | Cache still current | OK |
| **Get:** | Downloading fresh lists | OK |
| **Ign:** | Nothing useful / skip | Usually OK |
| **Err:** | Fetch/auth failed | Fix URL/key/network |
| **W:** | Warning | Often unsigned/hash — investigate |
| **E:** | Fatal | Blocks install until fixed |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `Err:` 404 | Codename / path | Align suite with `/etc/os-release` |
| Signature errors | keyrings + `signed-by` | [[gpg]] dearmor into keyrings |
| Proxy needed | Environment / apt.conf | `Acquire::http::Proxy` in apt.conf.d |
| Stale packages | Old lists | `apt update`; check clock (TLS) |
| Mysterious pin | preferences.d | `apt policy pkg` |

## Gotchas

> [!WARNING]
> **Two files defining the same repo** — duplicate sources cause noisy updates and confusion; keep one.

> [!WARNING]
> **Credentials in sources.list URLs** — prefer `auth.conf.d` so `ps` and backups don’t leak passwords.

> [!WARNING]
> **Deleting `/var/lib/apt/lists` is fine** — next `apt update` rebuilds; don’t delete dpkg databases.

## When NOT to use

- **One-off local `.deb`** — `apt install ./file.deb` / `dpkg -i` then `-f install`.
- **Snaps/flatpaks** — different stores.
- **Container FROM scratch without apt** — distroless has no package manager.

## Related

[[apt package manager]] [[APT policy]] [[gpg]] [[source list file]] [[Linux]]
