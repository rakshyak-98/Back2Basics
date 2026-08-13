[[vite]]

# vite error

> vite error — the issue is now 100% clear: you are running npm run build, which executes npx vite build, but npx is still trying to

---

## How it works

The issue is now 100% clear: **you are running npm run build**, which executes `npx vite build`, but **`npx` is still trying to use the broken `./node_modules/.bin/vite` script that has no execute permission**.
This is the classic “Permission denied” bug that hits almost everyone at least once (especially on WSL, Git-cloned repos, or when node_modules was copied from another machine).
### Exact Diagnosis from Your Output
```text
sh: 1: vite: Permission denied
```


---


## Steps

1. …


## Verification

```bash
# …
```


## Rollback

1. …


## Related

[[vite]]

## Sources

- [Wikipedia — vite error](https://en.wikipedia.org/wiki/vite_error)
