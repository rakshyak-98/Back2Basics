[[React]] [[bundler]] [[NodeJS]] [[SWC]]

# Metro Bundler

> React Native's default JavaScript bundler — fast dev iteration via incremental transforms, not webpack-style whole-graph rebuilds.

## Mental model

Metro sits between your RN source tree and the native runtime (Hermes/JSC). Unlike general web bundlers optimized for browser chunks, Metro optimizes for **mobile dev loops**: watch files, transform on demand, serve over the dev server to the app.

```
App requests bundle          Metro dev server
        │                           │
        │  GET /index.bundle        │
        └──────────────────────────►│ resolve graph (lazy)
                                    │ Babel/SWC transform per file
                                    │ cache in metro-cache
                                    ◄── single bundle (dev) or split (prod)
```

Key concepts:
- **Transformer** — Babel (default) or experimental SWC; applies RN preset, Flow/TS, inline requires.
- **Resolver** — `node_modules` + platform extensions (`.ios.js`, `.android.js`, `.native.js`).
- **Serializer** — outputs the bundle string the native side loads.
- **Cache** — file-system cache keyed by transform inputs; stale cache = weird runtime errors.

## Standard config / commands

### CLI (via React Native)

```bash
# Start dev server (usually via react-native CLI)
npx react-native start

# Reset cache after dependency / Babel config changes
npx react-native start --reset-cache

# Production bundle (CI / release)
npx react-native bundle \
  --platform android \
  --dev false \
  --entry-file index.js \
  --bundle-output android/app/src/main/assets/index.android.bundle \
  --assets-dest android/app/src/main/res/
```

### `metro.config.js` (project root)

```js
const { getDefaultConfig, mergeConfig } = require('@react-native/metro-config');

const config = {
  transformer: {
    // inlineRequires: true is often default in RN — defers require() for startup
    getTransformOptions: async () => ({
      transform: { experimentalImportSupport: false, inlineRequires: true },
    }),
  },
  resolver: {
    // alias monorepo packages
    extraNodeModules: {
      '@shared': require('path').resolve(__dirname, '../packages/shared'),
    },
    sourceExts: ['js', 'jsx', 'ts', 'tsx', 'json'],
  },
};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);
```

### Monorepo / symlinks

```js
// metro.config.js — watch hoisted packages
const path = require('path');
const config = {
  watchFolders: [path.resolve(__dirname, '../packages')],
  resolver: {
    nodeModulesPaths: [
      path.resolve(__dirname, 'node_modules'),
      path.resolve(__dirname, '../node_modules'),
    ],
  },
};
```

### Environment variables

```bash
# .env consumed via react-native-config or babel-plugin — not Metro itself
# Metro respects NODE_ENV for dev vs prod transforms
NODE_ENV=production npx react-native bundle ...
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Red screen "Unable to resolve module" | Path, typo, missing `npm install`, wrong `main` in package | Fix import; add to `resolver.extraNodeModules`; reinstall pods on iOS |
| Works after `--reset-cache` only | Stale metro-cache or Babel plugin change | `npx react-native start --reset-cache`; delete `/tmp/metro-*` |
| "TransformError" / syntax error | Babel preset missing for TS/JSX | Ensure `@react-native/babel-preset`; check `babel.config.js` |
| Monorepo package not found | Metro not watching workspace | Add `watchFolders` + `nodeModulesPaths` |
| Huge bundle / slow startup | No inline requires; importing entire libraries | Enable `inlineRequires`; use direct imports (`lodash/map` not `lodash`) |
| Hermes bytecode issues | Wrong Hermes compiler version vs RN version | Align RN + Hermes versions; rebuild release bundle |
| Asset not in APK/IPA | Missing `--assets-dest` on bundle command | Re-run `react-native bundle` with assets path |
| Different behavior iOS vs Android | Platform-specific file not picked up | Use `.ios.js` / `.android.js` suffixes |

## Gotchas

> [!WARNING]
> **Cache lies** — after upgrading RN, Babel plugins, or `metro.config.js`, always `--reset-cache`. Symptom: old code runs, new code never appears.

> [!WARNING]
> **Symlinks in monorepos** — Metro does not follow symlinks like webpack unless `watchFolders` is configured; "module not found" in CI but works locally often means path config drift.

> [!WARNING]
> **Native modules ≠ JS bundle** — fixing Metro doesn't fix missing `pod install` / Gradle linking for native RN modules.

> [!WARNING]
> **Expo vs bare** — Expo wraps Metro with its own config; merging custom `metro.config.js` requires `expo/metro-config` merge pattern.

## When NOT to use

- **Web-only React (Vite/webpack)** — Metro is RN-specific; don't force it for SPA builds.
- **Replacing Babel blindly with SWC** — RN toolchain assumptions (inline requires, Flow) may break; test on both platforms.
- **Custom bundler for simple RN app** — default Metro + reset-cache solves 95% of cases; only eject config for monorepos, aliases, or asset pipelines.

## Related

[[bundler]] [[React]] [[SWC]] [[NodeJS]] [[source map]]
