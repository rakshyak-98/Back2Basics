[[npm]] [[npm script]] [[node error]] [[Runtime Errors]] [[node environment configuration]]

# npm error

> Common failure modes when npm or a script it launches dies — peer conflicts, lifecycle failures, and Node/V8 heap limits during builds.

```txt
        npm error ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers care less about memorizing messages and more about triage: read …

## Sources
- [npm Docs — common errors](https://docs.npmjs.com/common-errors) — overview
- [Node.js — `--max-old-space-size`](https://nodejs.org/api/cli.html#--max-old-space-sizesize-in-megabytes) — deep-dive
- [Baseline — browser mapping package](https://www.npmjs.com/package/baseline-browser-mapping) — overview

## Key Concepts
- **Installer vs script:** `ERESOLVE` / fetch failures are install-time; `ELIFECYCLE` means a script exi…
- **Peer / tree conflicts:** see [[npm]] — fix ranges before relying on `--legacy-peer-deps`.
- **Heap limit:** Node caps the V8 old-space size so one process cannot eat all RAM → large web…
- **Stale tooling data:** packages like `baseline-browser-mapping` warn when embedded browser-support t…
- **Exit codes:** non-zero from scripts fails continuous integration


- **Core:** “npm error” usually means either the *installer* could not build a valid tree…

## Technical Details
- **Stale Baseline data warning:** 

```text
[baseline-browser-mapping] The data in this module is over two months old.
… update: npm i baseline-browser-mapping@latest -D
```

- **JavaScript heap out of memory:** 

```text
FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
```

```bash
NODE_OPTIONS="--max-old-space-size=4096" npm run build
```

- What happens:

```text
npm run build
  → starts Node
    → V8 heap grows to configured max
      → allocation fails when the graph/build retains too much
```

| Symptom | Check | Fix |
|---------|-------|-----|
| `ERESOLVE` | Peer ranges | Align versions; see [[npm]] |
| `ELIFECYCLE` | Child stderr above | Fix the tool error, not npm itself |
| Heap OOM on build | Bundle size / parallelism | Raise heap *or* split build; find leaks |
| `EACCES` global install | Permissions | Prefer nvm/fnm; avoid `sudo npm` |
| Network `ETIMEDOUT` | Registry / proxy | Mirror, retry, check corporate proxy |

## Mistakes to Avoid
- **Mistake:** Only reading the last `npm ERR!` line
- **Mistake:** Setting a huge heap globally instead of fixing an unbounded cach…
- **Mistake:** Committing `--legacy-peer-deps` as the long-term answer to every…

## Pros/Cons or Trade-offs
- **Pro:** Raising the heap unblocks legitimate large compiles quickly.
- **Con:** A higher heap hides leaks and can thrash the machine — measure before normalizing large limits.
- **Con:** Suppressing peer errors with flags hides real incompatibilities.

## Comparison
- vs [[pnpm logs]]: same triage idea — capture verbose output; different package manager.
- vs [[Runtime Errors]]: application exceptions at runtime


### Use cases
- Debugging failed pipelines: distinguish “dependency tree broken” from “TypeSc…

- **Example:** A CI build OOMs on a large TypeScript project
