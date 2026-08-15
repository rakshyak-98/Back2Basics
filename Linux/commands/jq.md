[[Commands]] [[awk]] [[curl]] [[Authentication command]] [[Scripting]]

# jq

> jq is a JSON filter for the shell — select, reshape, and print without writing a script.

## Interview Relevance
API/ops staple: path walks, `select`, `-r` for shell, and why whole-document load matters on big logs.

## Sources
- [jq Manual](https://jqlang.github.io/jq/manual/) — deep-dive
- [jq(1)](https://manpages.debian.org/jq) — overview

## Core Definition
`jq` parses JSON from stdin or a file, applies a filter expression, and prints results. Default pretty-prints; `-r` emits raw strings; `-c` compact/NDJSON-friendly lines; `-e` fails on false/null for scripts.

## Key Concepts
- **`.` / `.a.b`:** Identity / nested field walk.
- **`.[]` / `.[0]`:** Iterate array / index.
- **`select(...)` / `map(...)`:** Filter and transform.
- **`-r` / `-c` / `-e`:** Raw strings, compact, exit status for automation.
- **Streaming:** Default loads whole doc; `--stream` or line-oriented JSON for huge inputs.

## Technical Details

```bash
jq '.' file.json
curl -s https://api.example.com/v1/item | jq .

jq '.name' file.json
jq '.user.email' file.json
jq '.[0]' file.json
jq '.[] | .id' file.json

jq 'map(select(.status == "ok"))' file.json
jq '{id: .id, name: .name}' file.json
jq 'map({(.id): .name}) | add' file.json

jq 'keys' file.json
jq 'length' file.json
jq 'del(.secret)' file.json

jq -r '.token' auth.json
jq -c '.[]' big.json
jq -e '.ok == true' resp.json
```

| Pattern | Job |
|---------|-----|
| `select(.k=="v")` | Filter |
| `group_by(.k)` | Bucket |
| `sort_by(.k)` | Order |
| `to_entries` / `from_entries` | Object ↔ key/value array |
| `has("k")` | Key exists? |

| Symptom | Check | Fix |
|---------|-------|-----|
| `parse error` | Not JSON (HTML/error) | `head`; fix URL/headers |
| `null` everywhere | Wrong path / case | `jq 'keys'`; walk with `.` |
| Quotes break shell | Output used in bash | `jq -r` |
| Huge memory | Whole-file load | `--stream` or NDJSON lines |
| Exit 0 on miss | Default null success | `jq -e` |

## Real-World Applications
Extracting tokens from auth responses, filtering Kubernetes JSON, and shaping CI API payloads before the next pipeline step.

## Pros/Cons or Trade-offs
- **Pro:** Precise JSON surgery in pipes; great with `curl`.
- **Con:** Memory-hungry on giant documents; learning curve for complex filters.
- **Trade-off:** `map(select)` vs `.[] | select` stream shapes differ.

## Comparison
vs [[awk]]/[[grep]]: text/columns vs structured JSON. vs `yq`: YAML/TOML cousins. vs Python: use Python when transforms become programs.

## Mistakes to Avoid
- Comparing `"10"` and `10` without `tonumber`.
- Using jq on multi-GB logs without streaming/line mode.
- Forgetting `-e` in scripts that must fail on missing fields.
