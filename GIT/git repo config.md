[[GIT]]

# git repo config

> git repo config — know what it does, how to configure it, and how it fails in production.

## Mental model

**Say it in one breath:** git repository configuration — know what it does, how to configure it, and how it fails in production.

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
git commit -S -m <commit message>; # if auto-sign is not eanble
```
#### SSH
```shell
git conifg gpg.format ssh;
git config user.signingkey <path to ssh .pub file>;
```

## Standard config / commands

```bash
git config --local user.email "you@company.com"
git config --local core.hooksPath .githooks
git config --list --local
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Wrong identity on commits | Local versus global config | `git config --show-origin user.email` |
| Hooks not running | `core.hooksPath` unset | Set path; ensure scripts are executable |
| Line ending chaos on Windows | `core.autocrlf` mismatch | Align team policy; add `.gitattributes` |

## Gotchas

> [!WARNING]
> Repository config in `.git/config` overrides global `~/.gitconfig` for the same keys.

## When NOT to use

- Do not store secrets in repository config — use environment variables or a secret manager.

## Related

[[GIT]]
