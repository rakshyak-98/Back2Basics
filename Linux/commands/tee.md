[[commands]] [[Bash/Bash syntax]] [[visudo]]

# tee

> Splits a pipe — writes the same bytes to a file and still passes them downstream (and to the screen).

```txt
        tee ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Classic shell footgun: `sudo cmd > /etc/file` fails because the shell opens t…

## Sources
- [man tee](https://man7.org/linux/man-pages/man1/tee.1.html) — deep-dive
- [Wikipedia — tee (command)](https://en.wikipedia.org/wiki/Tee_(command)) — overview

## Key Concepts
- **Save + continue:** `cmd | tee log | next` keeps the pipeline alive.
- **`-a` append:** default overwrites like `>`.
- **`sudo tee`:** elevates the write side when the producer runs as a normal user.
- **Fan-out:** one stream to many files: `tee a.txt b.txt`.

## Technical Details
```txt
command ──► tee file.log ──► next | stage
              └── also writes file.log
```

```bash
ls -la | tee listing.txt
docker logs myapp 2>&1 | tee docker.log | grep ERROR
journalctl -f | tee -a journal-backup.log
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf >/dev/null
echo "Hello" | tee a.txt b.txt c.txt
curl -s https://api.example.com | tee /dev/stderr | jq .
```

| What you want | Command shape |
|---------------|---------------|
| Save + continue pipeline | `cmd \| tee log \| next` |
| Root-owned destination | `cmd \| sudo tee /etc/file` |
| Quiet screen, only file | `cmd \| tee file >/dev/null` |

| Symptom | Check | Fix |
|---------|-------|-----|
| Permission denied on `/etc/...` | Used `sudo cmd > file` | `cmd \| sudo tee file` |
| Log truncated | Missing `-a` | `tee -a` |
| Pipeline exits early | SIGPIPE | Ensure consumers read; or put `tee` last |

## Mistakes to Avoid
- **Mistake:** `sudo cmd > /root/file` — the redirect is not root
- **Mistake:** Truncating incident logs by forgetting `-a`

## Pros/Cons or Trade-offs
- **Pro:** Keeps interactive visibility while logging.
- **Con:** Duplicates bytes to disk — wrong for huge binary streams or structured production logging.

## Comparison
- vs `>` / `>>`: those only write; tee also passes data along.
- vs application loggers: prefer real logging in long-running services.


### Use cases
- Incident capture (`journalctl -f | tee -a`), writing resolv.conf/sysctl witho…
