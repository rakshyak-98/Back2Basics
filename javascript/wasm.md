[[javascript engine]] [[polyfills]] [[React build]] [[Security/Asymmetrical Encryption]] [[NodeJS]] [[web workers]] [[ServiceWorker]]

# WebAssembly (Wasm)

> WebAssembly (Wasm) — rust/C/... → wasm-pack / emscripten → .wasm module

```txt
        WebAssembly (Wasm) ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe **WebAssembly (Wasm)** to see if you understand what it do…

## Sources
- [WebAssembly — Concepts](https://webassembly.org/docs/wasm-or-asmjs/) — overview
- [MDN — WebAssembly](https://developer.mozilla.org/en-US/docs/WebAssembly) — deep-dive
- [Wikipedia — wasm](https://en.wikipedia.org/wiki/wasm) — overview

## Key Concepts
- **Wasm runs:** Wasm runs in the same **agent** as JS with:
- **Linear memory:** (ArrayBuffer view) - **Table** of function refs - **No GC objects** (until Wa…
- **Typical uses:** Typical uses: crypto, codecs, image/audio processing, game physics, porting l…


- **Core:** Wasm runs in the same **agent** as JS with:

## Technical Details
```txt
Rust/C/...  →  wasm-pack / emscripten  →  .wasm module
Browser     →  WebAssembly.instantiate  →  linear memory + exported functions
JS glue     →  call wasm.add(a,b), pass TypedArrays
```

- Wasm runs in the same **agent** as JS with:

- **Linear memory:** (ArrayBuffer view)
- **Table:** of function refs
- **No GC objects:** (until Wasm GC proposal wider adoption)

- Typical uses: crypto, codecs, image/audio processing, game physics, porting l…

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

- Place `.wasm` in `public/` or use plugins

### Node.js

```javascript
import { readFile } from "node:fs/promises";
const wasm = await WebAssembly.compile(await readFile("add.wasm"));
const { instance } = await WebAssembly.instantiate(wasm, {});
```

## Mistakes to Avoid
- **Mistake:** **"Wasm hides secrets"**
- **Mistake:** **Copy overhead JS ↔ Wasm**
- **Mistake:** **`CompileError`:** check Wrong MIME / corrupt file
- **Mistake:** **Memory grow fail:** check Linear memory max
- **Mistake:** **DOM access from Wasm:** check Not allowed
- **Mistake:** **Huge download:** check Debug build
- **Mistake:** **CORS on wasm fetch:** check Cross-origin module
- **Mistake:** **iOS older Safari:** check SIMD/threads unsupported

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (WebAssembly (Wasm) — rust/C/... → wasm-pack / emscripten → .wasm module).
- **Con / when not:** **Simple CRUD UI** — JS is faster to ship and debug.
- **Con / when not:** **Full application rewrite in C++**
- **Con / when not:** **When Web Crypto API suffices**

## Comparison
- vs [[javascript engine]]: know when each applies


### Use cases
- In production APIs and tooling, **wasm** shows up whenever teams ship Node/JS…
