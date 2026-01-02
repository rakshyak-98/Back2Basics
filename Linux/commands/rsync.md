```bash
rsync -av --progress src/ dest/
rsync -av src/ user@host:/path/; # remote
rsync -avz src/ user@host:/path/; # compress
```

```bash
rsync -av -e "ssh -i ~/.ssh/key" src/ user@host:/path/; # ssh key
```

```bash
rsync -av --exclude node_modules src/ dest/
```

> [!INFO]
> A plain copy (e.g., `scp` or `cp -r`) always transfers full files, even if only a tiny part changed → wasteful for large files or frequent syncs.