## Inspect commit
```bash
git show --stat <commit-hash>;
git show --name-only <commit-hash>;
git show --no-patch <commit-hash>;
```

> [!INFO]
> patch -> a patch is a text-based representation of changes (diffs) between files, usually between commits or working states. It's used to share, review, or apply changes.
```bash
git format-path -1 <commit-hash>; # create patch

git apply --check <patch-file>; # dry run before applying.
#  - you can apply or import it into another repo or branch.
git apply <patch-file>; # apply the changes to your working directory.
# - you still need to commit manually.

git am <patch-file>; # apply and create original commit.
```

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