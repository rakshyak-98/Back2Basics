```text
    at Object.<anonymous> (/home/mihir/Desktop/playground/script.cjs:19:9)
    at Module._compile (node:internal/modules/cjs/loader:1730:14)
    at Object..js (node:internal/modules/cjs/loader:1895:10)
    at Module.load (node:internal/modules/cjs/loader:1465:32)
    at Function._load (node:internal/modules/cjs/loader:1282:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:235:24)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:170:5)
    at node:internal/main/run_main_module:36:49

```

Top frame -> the real place where the error happened

---

```text
at Module._compile (node:internal/modules/cjs/loader:1730:14)
```
- The is NodeJS internal code that compiles our `.cjs` file into executable JavaScript.
- It is calling your top-level code -> which is why your error appeared inside `<anonymous>`

---

```text
at Object..js (node:internal/modules/cjs/loader:1895:10)
at Module.load (node:internal/modules/cjs/loader:1465:32)
at Function._load (node:internal/modules/cjs/loader:1282:12)
```

- The three frames are Node's CommonJS module loader pipeline
	- `Object...js` -> the loader for `.js` / `.cjs` files
	- `Module.load` -> actually loads the file from disk
	- `Function._load` -> the public-ish API that `require()` uses internally
