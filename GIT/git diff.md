```bash
git diff --name-only;
git diff --cached --name-only;
git diff main.. --name-only;
git diff --name-status;
```

```bash
git diff --stat
git diff --shortstat
```

```bash
git diff --cached;
git diff --staged;
git diff HEAD;
git diff HEAD~1 HEAD;
git diff main...HEAD;
git diff main..feature;
```

```bash
git diff v1.2.3 v1.3.0 --name-only;
git diff abc123..def456;
git diff --since="2 days ago" --name-only;
```

### Filter by path/pattern

```bash
git diff -- src/;
git diff -- '*.js' '*.ts' '*.tsx';

git diff -- . ':!node_modules';
git diff --diff-filter=R --name-only;
```

## Ignore some kind of changes

```bash
# Ignore whitespace-only changes
git diff -w
# or
git diff --ignore-space-change
# or
git diff --ignore-all-space

# Ignore blank lines
git diff --ignore-blank-lines

# Treat all whitespace as equal
git diff --ignore-space-at-eol

# Ignore changes in indentation
git diff --ignore-cr-at-eol
```
