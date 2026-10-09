```bash
git log --oneline -- <file path>; # Show only those commit which this file is tracked changes.

git log --all -- path/to/file

git log -S 'your_code_here' --all --oneline -- path/to/file

# view code hunk commits
git log -S 'func calculateTotal' --all --oneline -- internal/calculator.go

# view commit author name
git log --all --format="%H | %an | %s" -G 'your_code_pattern' -- path/to/file
```


- ZIP the files as they exist int that commit
```bash
git archive --format=zip --output=departure-date-extension-fix.zip b7f790c \
  src/modules/pms/reservation-modification/room-move/room-move.service.ts \
  src/modules/pms/reservation-modification/room-type-modify/room-type-modify.service.ts \
  src/modules/pms/reservation-modification/stay-modify/stay-modify.service.ts
```

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

### interactive patch mode

```bash
git add -p <file>;

git add -p; ## Entire repo
git reset -p; # Unstage hunks
```

```text
Stage this hunk [y,n,q,a,d,s,e,?]?
- `y` → stage this hunk
- `n` → skip
- `a` → stage this + all remaining
- `d` → skip this + all remaining
- `q` → quit

### Hunk manipulation (important)

- `s` → split hunk into smaller parts
- `e` → manually edit patch (fine-grained control)

```

## Git commit conflicts

Git three way merge
- Base : the common ancestor commit from which both developers changes orginated.
- Ours : the version in the branch you are merging into.
- Theirs : the version in the branch you are merging.

> Git detects that both branches (originated branch from common ancestor commit) changed the same part of the file differently

git commit hash : Git uses commit ancestry to identify the common ancestor and determine which chnages need to merged.