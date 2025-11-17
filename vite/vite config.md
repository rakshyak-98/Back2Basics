```bash
vite --config my-config.js;
```

> [!NOTE]
> Environment Variables _are_ automatically loaded later and exposed to application code via `import.meta.env` (with the default `VITE_` prefix filter)

## ModuleRunner
- A module runner is instantiated in the target runtime.
- In dev mode, vite serves modules directly (ESM in browser). But Sometimes you need to execute a module inside Node:
	- Server Side Rendering (SSR).
	- Testing (Vitest).
	- Running plugins that need evaluation.
The ModuleRunner provides this execution environment.

> [!NOTE]
> module runner doesn't support CJS in config files, but external CJS packages should work as usual.

```js
/** @type {import('vite').UserConfig} */
export default {
	// ...
}
```
Since vite ships with TypeScript typings, you can leverage your IDE's intellisense with jsdoc type hints.

Alternative you can use the `defineConfig` helper which should provide intellisense without the need for jsdoc annotations
```js
import { defineConfig } from "vite";
export default defineConifg({
	// ..
})
```

### Conditional Config
```js
export default defineConfig(({ command, mode, isSsrBuild, isPreview }) => {
  if (command === 'serve') {
    return {
      // dev specific config
    }
  } else {
    // command === 'build'
    return {
      // build specific config
    }
  }
})
```

## Vite allowed host error

[server-allowed-hosts](https://vite.dev/config/server-options#server-allowedhosts)

```js
```