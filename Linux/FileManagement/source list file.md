[[FileManagement]] [[apt package manager]] [[apt configuration]] [[keyrings]]

# source list file

> An APT sources line tells apt where packages come from — URI, suite, components, and which key verifies them.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** `deb [options] URI suite component…` is one repository; `signed-by=` pins trust.

```txt
deb [arch=amd64 signed-by=/usr/share/keyrings/foo.gpg] https://ex/apt jammy main
 │    options                                           suite          component
 type
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **deb** | Binary packages | “deb-src is source — rare on servers.” |
| **suite** | Codename (jammy) | “Must exist under `/dists/<suite>/`.” |
| **component** | main/universe/… | “Selects which Packages indexes to fetch.” |
| **signed-by** | Keyring path | “Replaces `apt-key add`.” |
| **apt update** | Fetch Release/Packages | “Broken line → update fails.” |

---

## Standard config / commands

```bash
# /etc/apt/sources.list.d/nginx.list
deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
  http://nginx.org/packages/debian bookworm nginx

sudo apt-get update
apt-cache policy nginx
sudo mv /etc/apt/sources.list.d/bad.list{,.disabled}
```

| Knob | Why it matters |
|------|----------------|
| `signed-by=` | Modern trust pin |
| `arch=` | Avoid foreign-arch noise |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `NO_PUBKEY` / signed-by errors | Keyring path | Install keyring; fix path |
| 404 on update | Suite/URI | Match codename; check vendor docs |
| Wrong version | Multiple repos | `apt-cache policy`; pin preferences |
| apt-key warnings | Legacy trust | Migrate to keyrings + signed-by |

---

## Gotchas

> [!WARNING]
> **`trusted=yes`** disables signature checks — never on production.

> [!WARNING]
> **Syntax errors block all updates** — disable a bad `.list` quickly.

---

## When NOT to use

- **One random binary** — prefer vendor packages or a container, not a shady PPA.
- **Air-gapped fleets** — use a local mirror, not one-off list edits.

---

## Related

[[apt package manager]] [[apt configuration]] [[keyrings]] [[Package Manager]]
