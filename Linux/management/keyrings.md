[[management]] [[source list file]] [[gpg]] [[apt package manager]]

# keyrings

> APT keyrings hold the OpenPGP keys that verify repository metadata — modern path is files under `/usr/share/keyrings` + `signed-by=`.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** download vendor key → store dearmored in keyrings dir → point the sources line at it with `signed-by`.

```txt
vendor.asc ──gpg --dearmor──► /usr/share/keyrings/vendor.gpg
                                      ▲
sources.list.d → deb [signed-by=…] …
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **keyring file** | Binary keyring | “Not `apt-key add` anymore.” |
| **signed-by** | Per-repo trust | “Limits key blast radius.” |
| **dearmor** | ASCII → binary | “APT wants `.gpg` binary.” |
| **NO_PUBKEY** | Missing key | “Install/fix keyring path.” |
| **expired key** | Vendor rotated | “Fetch new key; keep old briefly.” |

---

## Standard config / commands

```bash
curl -fsSL https://example.com/key.asc | \
  sudo gpg --dearmor -o /usr/share/keyrings/example.gpg
echo 'deb [signed-by=/usr/share/keyrings/example.gpg] https://example.com/apt stable main' \
  | sudo tee /etc/apt/sources.list.d/example.list
sudo apt-get update
# inspect
gpg --no-default-keyring --keyring /usr/share/keyrings/example.gpg --list-keys
```

| Knob | Why it matters |
|------|----------------|
| Mode `644` root-owned | Prevent user swap of trust anchors |
| One keyring per vendor | Blast-radius control |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| NO_PUBKEY | Path / key id | Install correct keyring |
| EXPKEYSIG | Expired | Update vendor key |
| apt-key warnings | Legacy | Migrate to signed-by |
| Wrong key trusted globally | apt-key ring | Remove global trust; scoped signed-by |

---

## Gotchas

> [!WARNING]
> **`apt-key` is deprecated** — keys in the trusted.gpg grab-bag over-trust.

> [!WARNING]
> **HTTP without TLS for keys** — verify fingerprints out-of-band.

---

## When NOT to use

- **Internal debs only** — use a signed internal mirror, still with keyrings.
- **Language packages** — npm/pip trust is separate from APT keyrings.

---

## Related

[[source list file]] [[apt config]] [[gpg]] [[Linux Key management]]
