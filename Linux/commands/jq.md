[[Commands]] [[awk]] [[curl]] [[Authentication command]] [[Scripting]]

# jq

> jq is a JSON filter for the shell — select, reshape, and print without writing a script.

```txt
        jq ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** API/ops staple: path walks, `select`, `-r` for shell, and why whole-document …

## Sources
- [jq Manual](https://jqlang.github.io/jq/manual/) — deep-dive
- [jq(1)](https://manpages.debian.org/jq) — overview

## Key Concepts
- **`.` / `.a.b`:** Identity / nested field walk.
- **`.[]` / `.[0]`:** Iterate array / index.
- **`select(...)` / `map(...)`:** Filter and transform.
- **`-r` / `-c` / `-e`:** Raw strings, compact, exit status for automation.
- **Streaming:** Default loads whole doc; `--stream` or line-oriented JSON for huge inputs.


- **Core:** `jq` parses JSON from stdin or a file, applies a filter expression, and print…

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

## Mistakes to Avoid
- **Mistake:** Comparing `"10"` and `10` without `tonumber`
- **Mistake:** Using jq on multi-GB logs without streaming/line mode
- **Mistake:** Forgetting `-e` in scripts that must fail on missing fields

## Pros/Cons or Trade-offs
- **Pro:** Precise JSON surgery in pipes; great with `curl`.
- **Con:** Memory-hungry on giant documents; learning curve for complex filters.
- **Trade-off:** `map(select)` vs `.[] | select` stream shapes differ.

## Comparison
- vs [[awk]]/[[grep]]: text/columns vs structured JSON


### Use cases
- Extracting tokens from auth responses, filtering Kubernetes JSON, and shaping…
