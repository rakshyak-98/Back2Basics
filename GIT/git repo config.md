[[GIT]]

# git repo config

> git repo config — know what it does, how to configure it, and how it fails in production.

```txt
        git repo config ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** Repo config interviews cover local vs global settings, and what belongs in co…

## Sources
- [Pro Git book](https://git-scm.com/book/en/v2) — deep-dive
- [Git reference documentation](https://git-scm.com/docs) — overview

## Key Concepts
```shell
gpg --full-generate-key; # generate gpg key
gpg --list-secret-keys --keyid-format=long;
gpg --armor --export <your email>; # export your public key
```
```shell
git config --get commit.gpgsign;
git log --show-signature;
```
#### Configure git to use GPG key
```shell
git config user.signingkey <gpg key>;
git config commit.gpgsign true; # enable auto-sign
git config tag.gpgsign; # enable auto sign for tags
```
```shell
- **Note:** git commit -S -m <commit message>; # if auto-sign is not eanble
```
#### SSH
```shell
git conifg gpg.format ssh;
git config user.signingkey <path to ssh .pub file>;
```

## Technical Details
```bash
git config --local user.email "you@company.com"
git config --local core.hooksPath .githooks
git config --list --local
```

## Mistakes to Avoid
> [!WARNING]
> Repository config in `.git/config` overrides global `~/.gitconfig` for the same keys.

| Symptom | Check | Fix |
|---------|-------|-----|
| Wrong identity on commits | Local versus global config | `git config --show-origin user.email` |
| Hooks not running | `core.hooksPath` unset | Set path; ensure scripts are executable |
| Line ending chaos on Windows | `core.autocrlf` mismatch | Align team policy; add `.gitattributes` |

## Pros/Cons or Trade-offs
- Do not store secrets in repository config
