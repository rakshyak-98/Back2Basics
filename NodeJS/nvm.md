[[NodeJS]] [[CLI]] [[node command]] [[Node.js run as a non-privileged user]]

# nvm (Node Version Manager)

> One-line: per-user Node version switching via shell hooks — install multiple runtimes; pin version per project with `.nvmrc`; fix PATH before systemd/cron runs node.

## Mental model

nvm installs Node versions under `~/.nvm/versions/node/` and **replaces `node`/`npm` on PATH** when you `nvm use`. Shell startup sources `nvm.sh` to define the `nvm` function — non-interactive contexts (cron, systemd, `sudo`) often **don't load nvm**, so `node` is missing or wrong version.

```
shell login → source ~/.nvm/nvm.sh
       │
nvm install 22 → ~/.nvm/versions/node/v22.x/bin/node
       │
nvm use        → PATH points at selected version
       │
cd project     → auto `nvm use` if .nvmrc + shell hook enabled
```

## Standard config / commands

### Install & default version

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
# restart shell, then:
nvm install --lts
nvm alias default lts/*
node -v
```

### Project pin (`.nvmrc`)

```bash
echo "22.16.0" > .nvmrc
nvm use          # reads .nvmrc
nvm install      # install if missing
```

### Shell auto-switch (optional in ~/.zshrc)

```bash
# loads nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

### Run under different user (systemd/cron)

```bash
sudo -u appuser -H bash -lc 'cd /app && nvm use && node server.js'
# -l = login shell so nvm loads; -c = command
```

### Fish shell

```bash
nvm install lts
set -Ux NVM_DIR $HOME/.nvm
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `curl: Permission denied` writing cache | `~/.nvm/.cache` ownership | `sudo chown -R $USER:$USER ~/.nvm`; reinstall curl if needed |
| `node: command not found` in cron/systemd | Non-login shell | Full path: `~/.nvm/versions/node/v22/bin/node` or source nvm in unit |
| Wrong Node in IDE terminal | Integrated terminal not login shell | `.nvmrc` + direnv; or set `terminal.integrated.inheritEnv` |
| `npm` global packages missing after upgrade | Globals per version | Reinstall globals; use `npx` or project-local deps |
| Version mismatch vs `engines` | `node -v` vs package.json | `nvm install`; enable `engine-strict` in `.npmrc` |
| Slow shell startup | nvm in every subshell | Lazy-load nvm plugin (zsh) or use fnm/mise |

## Gotchas

> [!WARNING]
> **`sudo` resets environment** — `sudo node` uses system Node, not nvm's; use `sudo -u user -H bash -lc 'nvm use && …'`.

> [!WARNING]
> **CI should not rely on nvm** — use `actions/setup-node`, Docker base image, or `mise`/`fnm` with explicit version.

> [!WARNING]
> **Cache dir permissions** — failed downloads leave corrupt partial files; clear `~/.nvm/.cache` after fixing perms.

## When NOT to use

- **Production containers** — bake Node version into Dockerfile; no nvm in image.
- **System-wide Node for all users** — use distro packages or NodeSource with apt pinning.
- **Windows native** — use nvm-windows or fnm; bash nvm is Unix-oriented.

## Related

[[node command]] [[node package json]] [[CLI]] [[Node.js run as a non-privileged user]] [[Deployment/vercel deployment]]
