[[javascript engine]] [[polyfills]] [[React build]] [[Security/Asymmetrical Encryption]] [[NodeJS]] [[web workers]] [[ServiceWorker]]

# WebAssembly (Wasm)

> WebAssembly (Wasm) — rust/C/... → wasm-pack / emscripten → .wasm module

## Interview Relevance

Interviewers probe **WebAssembly (Wasm)** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [WebAssembly — Concepts](https://webassembly.org/docs/wasm-or-asmjs/) — overview
- [MDN — WebAssembly](https://developer.mozilla.org/en-US/docs/WebAssembly) — deep-dive
- [Wikipedia — wasm](https://en.wikipedia.org/wiki/wasm) — overview

## Core Definition

Wasm runs in the same **agent** as JS with:

## Key Concepts

- Wasm runs in the same **agent** as JS with:
- **Linear memory** (ArrayBuffer view) - **Table** of function refs - **No GC objects** (until Wasm GC proposal wider adoption)
- Typical uses: crypto, codecs, image/audio processing, game physics, porting legacy libs — **not** a full DOM/UI replacement.

## Technical Details

```txt
Rust/C/...  →  wasm-pack / emscripten  →  .wasm module
Browser     →  WebAssembly.instantiate  →  linear memory + exported functions
JS glue     →  call wasm.add(a,b), pass TypedArrays
```

Wasm runs in the same **agent** as JS with:

- **Linear memory** (ArrayBuffer view)
- **Table** of function refs
- **No GC objects** (until Wasm GC proposal wider adoption)

Typical uses: crypto, codecs, image/audio processing, game physics, porting legacy libs — **not** a full DOM/UI replacement.

```txt
JS (UI, network)  ←→  Wasm (hot loop, crypto kernel)
```

### Load module (browser)

```javascript
const imports = { env: { log: (n) => console.log(n) } };
const { instance } = await WebAssembly.instantiateStreaming(
  fetch("/pkg/crypto_bg.wasm"),
  imports
);
const result = instance.exports.encrypt_bytes(ptr, len);
```

### Rust + wasm-pack

```bash
wasm-pack build --target web
```

```javascript
import init, { encrypt } from "./pkg/crypto.js";
await init();
encrypt(data);
```

### Vite / bundler

Place `.wasm` in `public/` or use plugins; set correct MIME `application/wasm`.

### Node.js

```javascript
import { readFile } from "node:fs/promises";
const wasm = await WebAssembly.compile(await readFile("add.wasm"));
const { instance } = await WebAssembly.instantiate(wasm, {});
```

## Real-World Applications

In production APIs and tooling, **wasm** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **"Wasm hides secrets"** — client-side crypto keys are still extractable; use Wasm for performance, not trust boundary alone ([[Security/Asymmetrical Encryption]]); **Copy overhead JS ↔ Wasm** — batch work on large TypedArrays; minimize boundary calls.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (WebAssembly (Wasm) — rust/C/... → wasm-pack / emscripten → .wasm module).
- **Con / when not:** **Simple CRUD UI** — JS is faster to ship and debug.
- **Con / when not:** **Full application rewrite in C++** — poor DOM/styling story; use Wasm for hot paths only.
- **Con / when not:** **When Web Crypto API suffices** — native `crypto.subtle` before bundling Rust crypto.

## Comparison

vs [[javascript engine]]: know when each applies — do not treat them as interchangeable. vs [[polyfills]]: know when each applies — do not treat them as interchangeable. vs [[React build]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **"Wasm hides secrets"** — client-side crypto keys are still extractable; use Wasm for performance, not trust boundary alone ([[Security/Asymmetrical Encryption]]).
- **Copy overhead JS ↔ Wasm** — batch work on large TypedArrays; minimize boundary calls.
- **`CompileError`:** check Wrong MIME / corrupt file; fix: Server `application/wasm`; rebuild
- **Memory grow fail:** check Linear memory max; fix: `memory.grow` pages; tune allocator
- **DOM access from Wasm:** check Not allowed; fix: Bridge through JS exports
- **Huge download:** check Debug build; fix: `wasm-opt -Oz`; release profile
- **CORS on wasm fetch:** check Cross-origin module; fix: Same-origin or CORS headers
- **iOS older Safari:** check SIMD/threads unsupported; fix: Feature detect; scalar fallback
