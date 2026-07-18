[[git]]

```bash
git merge-tree $(git merge-base target-branch source-branch) target-branch source-branch;
git merge <source-branch> --no-commit --no-ff; # dry-run merge
```
