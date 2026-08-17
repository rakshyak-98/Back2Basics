[[NodeJS]] [[CLI]] [[node command]] [[Node.js run as a non-privileged user]] [[node package json]] [[Deployment/vercel deployment]]

# nvm (Node Version Manager)

> nvm (Node Version Manager) — nvm installs Node versions under ~/.nvm/versions/node/ and replaces node/npm on PATH when you nvm use. Shell startup sources nvm.sh to define





## Interview Relevance
Interviewers probe **nvm (Node Version Manager)** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources
- [nvm-sh/nvm](https://github.com/nvm-sh/nvm) — deep-dive
- [Wikipedia — nvm](https://en.wikipedia.org/wiki/nvm) — overview

## Core Definition
nvm installs Node versions under `~/.nvm/versions/node/` and **replaces `node`/`npm` on PATH** when you `nvm use`. Shell startup sources `nvm.sh` to define the `nvm` function — non-interactive contexts (cron, systemd, `sudo`) often **don't load nvm**, so `node` is missing or wrong version.

## Key Concepts
- nvm installs Node versions under `~/.nvm/versions/node/` and **replaces `node`/`npm` on PATH** when you `nvm use`. Shell startup sources `nvm.sh` to define the `nvm` function — …

## Technical Details
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

## Real-World Applications
In production APIs and tooling, **nvm** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **`sudo` resets environment** — `sudo node` uses system Node, not nvm's; use `sudo -u user -H bash -lc 'nvm use && …'`; **CI should not rely on nvm** — use `actions/setup-node`, Docker base image, or `mise`/`fnm` with explicit version.

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (nvm (Node Version Manager) — nvm installs Node versions under ~/.nvm/versions/no…).
- **Con / when not:** **Production containers** — bake Node version into Dockerfile; no nvm in image.
- **Con / when not:** **System-wide Node for all users** — use distro packages or NodeSource with apt pinning.
- **Con / when not:** **Windows native** — use nvm-windows or fnm; bash nvm is Unix-oriented.

## Comparison
vs [[CLI]]: know when each applies — do not treat them as interchangeable. vs [[node command]]: know when each applies — do not treat them as interchangeable. vs [[Node.js run as a non-privileged user]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid
- **`sudo` resets environment** — `sudo node` uses system Node, not nvm's; use `sudo -u user -H bash -lc 'nvm use && …'`.
- **CI should not rely on nvm** — use `actions/setup-node`, Docker base image, or `mise`/`fnm` with explicit version.
- **Cache dir permissions** — failed downloads leave corrupt partial files; clear `~/.nvm/.cache` after fixing perms.
- **`curl: Permission denied` writing cache:** check `~/.nvm/.cache` ownership; fix: `sudo chown -R $USER:$USER ~/.nvm`; reinstall curl if needed
- **`node: command not found` in cron/systemd:** check Non-login shell; fix: Full path: `~/.nvm/versions/node/v22/bin/node` or source nvm in unit
- **Wrong Node in IDE terminal:** check Integrated terminal not login shell; fix: `.nvmrc` + direnv; or set `terminal.integrated.inheritEnv`
- **`npm` global packages missing after upgrade:** check Globals per version; fix: Reinstall globals; use `npx` or project-local deps
- **Version mismatch vs `engines`:** check `node -v` vs package.json; fix: `nvm install`; enable `engine-strict` in `.npmrc`
- **Slow shell startup:** check nvm in every subshell; fix: Lazy-load nvm plugin (zsh) or use fnm/mise
