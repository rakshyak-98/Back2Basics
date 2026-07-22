[[javascript engine]] [[polyfills]] [[React build]] [[Security/Asymmetrical Encryption]] [[NodeJS]]

# WebAssembly (Wasm)

> **Portable binary IR** run near-native speed in browser/Node — compile from Rust/C/C++/Go — sandboxed, no direct DOM — **WebAssembly spec**.

---

## Mental model

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `CompileError` | Wrong MIME / corrupt file | Server `application/wasm`; rebuild |
| Memory grow fail | Linear memory max | `memory.grow` pages; tune allocator |
| DOM access from Wasm | Not allowed | Bridge through JS exports |
| Huge download | Debug build | `wasm-opt -Oz`; release profile |
| CORS on wasm fetch | Cross-origin module | Same-origin or CORS headers |
| iOS older Safari | SIMD/threads unsupported | Feature detect; scalar fallback |

---

## Gotchas

> [!WARNING]
> **"Wasm hides secrets"** — client-side crypto keys are still extractable; use Wasm for performance, not trust boundary alone ([[Security/Asymmetrical Encryption]]).

> [!WARNING]
> **Copy overhead JS ↔ Wasm** — batch work on large TypedArrays; minimize boundary calls.

---

## When NOT to use

- **Simple CRUD UI** — JS is faster to ship and debug.
- **Full app rewrite in C++** — poor DOM/styling story; use Wasm for hot paths only.
- **When Web Crypto API suffices** — native `crypto.subtle` before bundling Rust crypto.

---

## Related

[[javascript engine]] · [[web workers]] · [[ServiceWorker]] · [[polyfills]] · [[React build]]
