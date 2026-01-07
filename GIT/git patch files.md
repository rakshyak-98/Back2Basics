```bash
git format-patch -N; # Patch from multiple commit;
git format-patch <base>..<head>;

git format-patch -1 <commit_sha>;
```

- Apply patch

```bash
git am <patch file>;
git am --abort;
git am --skip;
```