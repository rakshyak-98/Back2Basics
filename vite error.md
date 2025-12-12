The issue is now 100% clear: **you are running npm run build**, which executes `npx vite build`, but **`npx` is still trying to use the broken `./node_modules/.bin/vite` script that has no execute permission**.

This is the classic “Permission denied” bug that hits almost everyone at least once (especially on WSL, Git-cloned repos, or when node_modules was copied from another machine).

### Exact Diagnosis from Your Output

```text
> npx vite build
sh: 1: vite: Permission denied
```

> [!INFO]
> `npx` found vite inside ./node_modules/.bin/, but that file is not marked executable (`-rw-r--r--` instead of `-rwxr-xr-x`).