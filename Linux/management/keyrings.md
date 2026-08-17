[[source list file]] [[gpg]] [[apt package manager]] [[Linux Key management]] [[FileManagement/source list file]]

# keyrings

> APT keyrings hold the OpenPGP keys that verify repository metadata — modern path is `/usr/share/keyrings` + `signed-by=`.





## Interview Relevance
Expect deprecation of `apt-key`, per-repo `signed-by`, and how to fix `NO_PUBKEY` / `EXPKEYSIG`.

## Sources
- [Debian wiki — SecureApt](https://wiki.debian.org/SecureApt) — deep-dive
- [Ubuntu — Third-party repositories](https://help.ubuntu.com/community/ThirdPartyRepositories) — overview

## Key Concepts
- **Scoped trust:** `signed-by=` limits a key to one repo.
- **dearmor:** ASCII armored key → binary `.gpg` for APT.
- **One keyring per vendor:** blast-radius control.
- **Permissions:** root-owned `644` so users cannot swap trust anchors.

## Technical Details
```txt
vendor.asc ──gpg --dearmor──► /usr/share/keyrings/vendor.gpg
                                      ▲
sources.list.d → deb [signed-by=…] …
```

```bash
curl -fsSL https://example.com/key.asc | \
  sudo gpg --dearmor -o /usr/share/keyrings/example.gpg
echo 'deb [signed-by=/usr/share/keyrings/example.gpg] https://example.com/apt stable main' \
  | sudo tee /etc/apt/sources.list.d/example.list
sudo apt-get update
gpg --no-default-keyring --keyring /usr/share/keyrings/example.gpg --list-keys
```

| Symptom | Check | Fix |
|---------|-------|-----|
| NO_PUBKEY | Path / key id | Install correct keyring |
| EXPKEYSIG | Expired | Update vendor key |
| apt-key warnings | Legacy | Migrate to signed-by |
| Wrong key trusted globally | apt-key ring | Remove global trust; scoped signed-by |

## Real-World Applications
Add a vendor APT repo for a database or Kubernetes package with a dedicated keyring file instead of the old trusted.gpg grab-bag.

## Pros/Cons or Trade-offs
- **Pro:** Per-repo trust reduces cross-repo forgery blast radius.
- **Con:** More files to manage; fingerprint verification still required out-of-band.

## Comparison
- vs [[Linux Key management]]: APT trust anchors vs broader secret/key tooling.
- vs language package trust (npm/pip): separate from APT keyrings.

## Mistakes to Avoid
- Using deprecated `apt-key add`.
- Fetching keys over plain HTTP without fingerprint checks.
- World-writable keyring paths.
