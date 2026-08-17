[[Operating System]] [[Runtime Environment]] [[interpreter]] [[OS program]] [[Heap memory]] [[linker]] [[file descriptors]]

# Runtime

> Runtime is the active phase when a program executes — and colloquially the libraries/services that phase depends on, distinct from compile/link time.

```txt
        Runtime ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Compile-time vs runtime errors

## Sources
- [Wikipedia — Runtime system](https://en.wikipedia.org/wiki/Runtime_system) — overview
- Bryant & O’Hallaron, *Computer Systems* — deep-dive

## Key Concepts
- **Compile/link time:** source → objects ([[linker]]) → image.
- **Runtime phase:** CPU executes; allocator serves [[Heap memory]]; I/O uses [[file descriptors]].
- **Runtime system:** GC, JIT, stdlib services ([[Runtime Environment]]).
- **Managed languages:** [[interpreter]]/JIT inside the runtime.

## Technical Details
- “Runtime error” vs “compile error” separates logic after launch from syntax/t…
- The loaded [[OS program]] plus its [[Runtime Environment]] define behavior.

## Mistakes to Avoid
- **Mistake:** Ambiguous docs that mix “runtime” (phase) with “runtime” (produc…
- **Mistake:** Blaming the OS for missing language runtime packages in an image
- **Mistake:** Ignoring runtime initialization cost in cold-start platforms

## Pros/Cons or Trade-offs
- **Rich runtimes:** productivity and safety nets; memory/complexity cost.
- **Minimal runtimes:** smaller attack surface; more app responsibility.
- **Trade-off:** interpret/JIT flexibility vs AOT predictability.

## Comparison
- vs [[Runtime Environment]]: environment is the supporting machinery
- vs compile time: before vs during execution.


### Use cases
- Language version managers, container images shipping a runtime, and diagnosin…
