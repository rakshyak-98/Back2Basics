
## Git commit conflicts

Git three way merge: merge strategy that combines changes from two diverged branches by comparing their two branch tips with their common ancestor (merge base).

> Git uses these three versions, the common ancestor, the current branch, and incoming branch to determine which changes to combine automatically and which required conflict resolution.

- Base : the common ancestor commit from which both developers changes orginated.
- Ours : the version in the branch you are merging into.
- Theirs : the version in the branch you are merging.

> Git detects that both branches (originated branch from common ancestor commit) changed the same part of the file differently

git commit hash : Git uses commit ancestry to identify the common ancestor and determine which chnages need to merged.

```bash
git rev-list [options] <revision> 
git rev-list main; # reverse chronological order
```
- `<revision>` can be a branch, tag, commit hash, or another git reference.

```bash
git rev-list main..stage
```
- Lists commits reachable from `stage` that are not reachable from main.

> This is useful when you want to identify the commits that exist on your feature branch but have not been incorporated into `main`.

```bash
git rev-list main -- <directory>/
```
- to list commits that changed files in the backend directory.

### Counting
```bash
git rev-list --count HEAD #total commits on current branch
git rev-list --count main..feature # how many commits feature is ahead of
git rev-list --left-right --count main...feature
```
- `--left-right --count` is a quick way to see how far a branch has diverged from another.

```bash
git rev-list HEAD -- <file path>; # commits that thouched a file
git rev-list --reverse HEAD # oldest first
git rev-list -1 HEAD -- <file path>; # last commit that touched a file
```