```bash
git branch -vv; # show which remote/branch your local branch is tracking.
```
```txt
* main  abc123 [origin/main] commit message
```

```bash
git config --get branch.$(git branch --show-current).remote
git config --get branch.$(git branch --show-current).merge
```