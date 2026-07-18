## Open remote file

```bash
zed ssh://<user>@<ip>/<file path>;

```

### Ignore all the eslint rules

```json
{
  "languages": {
    "JavaScript": {
      "language_servers": ["!eslint"]
    },
    "TypeScript": {
      "language_servers": ["!eslint"]
    }
  }
}
```
