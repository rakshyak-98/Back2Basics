#### Change the lib compiler

> Edit `tsconfig.json` → `compilerOptions.lib`. Lists which built-in JS APIs TypeScript knows about (DOM, ES2020, etc.).

### tsconfig cannot find `@types`

> If `@types/foo` is installed but TypeScript still errors, set `typeRoots` or `types` in `tsconfig.json` so it knows where to look.

`tsBuildInfoFile` in `tsconfig.json`:
- Where TypeScript saves incremental build cache.
- Speeds up the next compile by reusing what changed last time.
- Set the path if you want the cache file somewhere specific.

> [!INFO] by compilation information is stored in a file named `.tsbuildinfo` in the same directory as the `tsconfig.json` file.

