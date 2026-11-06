
## Add notes to the commit
```bash
git notes add -m 'Message';
git notes remove <commit-hash>;

git push origin refs/notes/* ; #pushes updated notes state (including removal);
git notes show [<commit>]; # show the commit notes;
```

```bash
git fetch origin refs/notes/*:refs/notes/*; # fetch remotes notes explicitly.

git log origin/your-branch -1 --format=%H; # Get latest commit of remote branch.
git log origin/your-branch --show-notes;
```
