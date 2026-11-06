
## Inspect commit
```bash
git show --stat <commit-hash>;
git show --name-only <commit-hash>;
git show --no-patch <commit-hash>;
``` > [!INFO]
> patch -> a patch is a text-based representation of changes (diffs) between files, usually between commits or working states. It's used to share, review, or apply changes.
```bash
git format-path -1 <commit-hash>; # create patch

git apply --check <patch-file>; # dry run before applying.
#  - you can apply or import it into another repo or branch.
git apply <patch-file>; # apply the changes to your working directory.
# - you still need to commit manually.

git am <patch-file>; # apply and create original commit.
```

### Heads
- `HEAD~1` -> (Ancestor Chains) used to go back a specific number of generations along the first-parent history. 
- `HEAD^1` -> (Specific Parents) Most commits have only one parent, but a merge commit has two or more parents. Goes to the tip of the merged branch.

> [!INFO]
> When you need to inspect the code that was brought into your branch via a merge.

> used to refer to order commits relative to your current `HEAD` position. While they often point to the exact same commit in a simple, linear history, they behave very differently when you encounter **merge commits**.
