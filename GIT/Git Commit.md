```bash
git log --follow --oneline -- <file path>; # show which commits include a given file
git log --diff-filter=D --oneline -- <file path> 
git log --diff-filter=A --oneline -- <file path>
git log --all -- path/to/file # Search across all branch

git log -S 'your_code_here' --all --oneline -- path/to/file

# view code hunk commits
git log -S 'func calculateTotal' --all --oneline -- <file path> 

# view commit author name
git log --all --format="%H | %an | %s" -G 'your_code_pattern' -- path/to/file

git log --author=<author-name> --diff-filter=A --name-status
```

## Author based filters
```bash
git log <branch-name> --format="%h %an" | sort -u
git log --author=<author-name>;
```

- ZIP the files as they exist int that commit
```bash
git archive --format=zip --output=departure-date-extension-fix.zip b7f790c \
  src/modules/pms/reservation-modification/room-move/room-move.service.ts \
  src/modules/pms/reservation-modification/room-type-modify/room-type-modify.service.ts \
  src/modules/pms/reservation-modification/stay-modify/stay-modify.service.ts
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
