
```bash
git log -p <path to file>; # show the sommit history for that specific file with patches (changes/edits)
```


```bash
git show --name-only --pretty="" <commit>;
git diff --name-only --cached;
```

### View logs between two commits

```bash
git log <commit 1>..<commin 2>; # dot is mendaroty
git log -p <commit 1>..<commit 2>;
```
