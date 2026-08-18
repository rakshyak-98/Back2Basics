[[commands]] [[awk]] [[curl]]

# jq

> jq is a JSON filter for the shell — select, reshape, and print without writing a script.

## Mental model

**Say it in one breath:** feed JSON in, write a filter that walks paths like `.users[].id`, get JSON (or raw text) out.

```txt
stdin / file.json  ──►  jq 'filter'  ──►  stdout
         .          path
         .[]        each array element
         select()   keep matching objects
         -r         raw strings (no quotes)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **`.`** | Identity / pretty-print | “`jq .` formats the blob.” |
| --- | --- | --- |
| **`.a.b`** | Nested field | “Dot path is the object walk.” |
| **`.[]` / `.[0]`** | All / first array items | “Iterate with `.[]`, index with `.[0]`.” |
| **`select(...)`** | Keep if true | “Filter objects before mapping.” |
| **`map(...)`** | Transform each | “Map over arrays; `map_values` for objects.” |
| **`-r` / `-c`** | Raw / compact | “`-r` for shell; `-c` for one line per object.” |

## Standard config / commands

```bash
# Read / pretty
jq '.' file.json
curl -s https://api.example.com/v1/item | jq .

# Paths
jq '.name' file.json
jq '.user.email' file.json
jq '.[0]' file.json
jq '.[] | .id' file.json

# Filter / reshape
jq 'map(select(.status == "ok"))' file.json
jq '{id: .id, name: .name}' file.json
jq 'map({(.id): .name}) | add' file.json

# Keys / size / delete
jq 'keys' file.json
jq 'length' file.json
jq 'del(.secret)' file.json

# Script-friendly
jq -r '.token' auth.json          # no quotes
jq -c '.[]' big.json              # NDJSON-ish compact lines
jq -e '.ok == true' resp.json     # exit 1 if false/null
```

| Pattern | Job |
| --- | --- |
| `select(.k=="v")` | Filter |
| `group_by(.k)` | Bucket |
| `sort_by(.k)` | Order |
| `to_entries` / `from_entries` | Object ↔ key/value array |
| `has("k")` | Key exists? |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| `parse error` | Not JSON (HTML/error page) | `head`; fix `curl` URL/headers |
| `null` everywhere | Wrong path / case | `jq 'keys'`; walk with `.` |
| Quotes break shell | Output used in bash | `jq -r` |
| Huge memory | Whole-file load | Stream with `--stream` or split NDJSON |
| Exit 0 on miss | Default null is success | `jq -e` for scripts |
| Multiple top-level values | NDJSON | `jq -c .` per line or `jq -s` to slurp |

## Gotchas

> [!WARNING]
> **`jq` loads the whole document** (unless `--stream`) — multi‑GB logs need line-oriented JSON.

> [!WARNING]
> **`select` vs `map(select)`** — on an array, `map(select(...))` keeps structure; bare `select` after `.[]` emits a stream.

> [!WARNING]
> **Numbers vs strings** — `"10" != 10`. Use `tonumber` / `tostring` explicitly.

## When NOT to use

- **Line/column text logs** — [[awk]] / [[grep]].
- **YAML/TOML configs** — `yq` / dedicated parsers.
- **Mutating a DB** — jq is a transform tool, not storage.

## Related

[[awk]] [[curl]] [[commands]] [[Authentication command]]
