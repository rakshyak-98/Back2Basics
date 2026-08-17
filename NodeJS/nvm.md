[[NodeJS]] [[NodeJS CLI]] [[NodeJS CLI]] [[Node.js run as a non-privileged user]] [[node package json]] [[Deployment/vercel deployment]]

# nvm (Node Version Manager)

> nvm (Node Version Manager) — nvm installs Node versions under ~/.nvm/versions/node/ and replaces node/npm on PATH when you nvm use. Shell startup sources nvm.sh to define

```txt
        nvm (Node Version  ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe **nvm (Node Version Manager)** to see if you understand wh…

## Sources
- [nvm-sh/nvm](https://github.com/nvm-sh/nvm) — deep-dive
- [Wikipedia — nvm](https://en.wikipedia.org/wiki/nvm) — overview

## Key Concepts
- **nvm installs:** nvm installs Node versions under `~/.nvm/versions/node/` and **replaces `node…


- **Core:** nvm installs Node versions under `~/.nvm/versions/node/` and **replaces `node…

## Technical Details
- nvm installs Node versions under `~/.nvm/versions/node/` and **replaces `node…
- Shell startup sources `nvm.sh` to define the `nvm` function

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

## Mistakes to Avoid
- **Mistake:** **`sudo` resets environment**
- **Mistake:** **CI should not rely on nvm**
- **Mistake:** **Cache dir permissions**
- **Mistake:** **`curl: Permission denied` writing cache:** check `~/.nvm/.cach…
- **Mistake:** **`node: command not found` in cron/systemd:** check Non-login s…
- **Mistake:** **Wrong Node in IDE terminal:** check Integrated terminal not lo…
- **Mistake:** **`npm` global packages missing after upgrade:** check Globals p…
- **Mistake:** **Version mismatch vs `engines`:** check `node -v` vs package.js…
- **Mistake:** **Slow shell startup:** check nvm in every subshell

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (nvm (Node Version Manager) — nvm installs Node versions under ~/.nvm/versions/no…).
- **Con / when not:** **Production containers**
- **Con / when not:** **System-wide Node for all users**
- **Con / when not:** **Windows native**

## Comparison
- vs [[NodeJS CLI]]: know when each applies


### Use cases
- In production APIs and tooling, **nvm** shows up whenever teams ship Node/JS …
