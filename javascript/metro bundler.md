[[React]] [[bundler]] [[NodeJS]] [[SWC]] [[source map]]

# Metro Bundler

> React Native's default JavaScript bundler — fast dev iteration via incremental transforms, not webpack-style whole-graph rebuilds.

## Interview Relevance

Interviewers probe **Metro Bundler** to see if you understand what it does operationally and when it is the wrong tool — not just the definition.

## Sources

- [Metro — Concepts](https://metrobundler.dev/docs/concepts/) — deep-dive
- [Wikipedia — metro bundler](https://en.wikipedia.org/wiki/metro_bundler) — overview

## Core Definition

Metro sits between your RN source tree and the native runtime (Hermes/JSC). Unlike general web bundlers optimized for browser chunks, Metro optimizes for **mobile development loops**: watch files, transform on demand, serve over the development server to the application.

## Key Concepts

- Metro sits between your RN source tree and the native runtime (Hermes/JSC). Unlike general web bundlers optimized for browser chunks, Metro optimizes for **mobile development lo…
- Key concepts: - **Transformer** — Babel (default) or experimental SWC; applies RN preset, Flow/TS, inline requires. - **Resolver** — `node_modules` + platform extensions (`.ios.…

## Technical Details

Metro sits between your RN source tree and the native runtime (Hermes/JSC). Unlike general web bundlers optimized for browser chunks, Metro optimizes for **mobile development loops**: watch files, transform on demand, serve over the development server to the application.

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

## Real-World Applications

In production APIs and tooling, **metro bundler** shows up whenever teams ship Node/JS services. Concrete failure signals to rehearse: **Cache lies** — after upgrading RN, Babel plugins, or `metro.config.js`, always `--reset-cache`. Symptom: old code runs, new code never appears; **Symlinks in monorepos** — Metro does not follow symlinks like webpack unless `watchFolders` is configured; "module not found" in CI but works locally often means path config drift.

## Pros/Cons or Trade-offs

- **Pro:** Solves the job described above when used in the right layer (React Native's default JavaScript bundler — fast dev iteration via incremental t…).
- **Con / when not:** **Web-only React (Vite/webpack)** — Metro is RN-specific; don't force it for SPA builds.
- **Con / when not:** **Replacing Babel blindly with SWC** — RN toolchain assumptions (inline requires, Flow) may break; test on both platforms.
- **Con / when not:** **Custom bundler for simple RN application** — default Metro + reset-cache solves 95% of cases; only eject configuration for monorepos, aliases, or asset pipelines.

## Comparison

vs [[React]]: know when each applies — do not treat them as interchangeable. vs [[bundler]]: know when each applies — do not treat them as interchangeable. vs [[SWC]]: know when each applies — do not treat them as interchangeable.

## Mistakes to Avoid

- **Cache lies** — after upgrading RN, Babel plugins, or `metro.config.js`, always `--reset-cache`. Symptom: old code runs, new code never appears.
- **Symlinks in monorepos** — Metro does not follow symlinks like webpack unless `watchFolders` is configured; "module not found" in CI but works locally often means path config drift.
- **Native modules ≠ JS bundle** — fixing Metro doesn't fix missing `pod install` / Gradle linking for native RN modules.
- **Expo vs bare** — Expo wraps Metro with its own config; merging custom `metro.config.js` requires `expo/metro-config` merge pattern.
- **Red screen "Unable to resolve module":** check Path, typo, missing `npm install`, wrong `main` in package; fix: Fix import; add to `resolver.extraNodeModules`; reinstall pods on iOS
- **Works after `--reset-cache` only:** check Stale metro-cache or Babel plugin change; fix: `npx react-native start --reset-cache`; delete `/tmp/metro-*`
- **"TransformError" / syntax error:** check Babel preset missing for TS/JSX; fix: Ensure `@react-native/babel-preset`; check `babel.config.js`
- **Monorepo package not found:** check Metro not watching workspace; fix: Add `watchFolders` + `nodeModulesPaths`
- **Huge bundle / slow startup:** check No inline requires; importing entire libraries; fix: Enable `inlineRequires`; use direct imports (`lodash/map` not `lodash`)
- **Hermes bytecode issues:** check Wrong Hermes compiler version vs RN version; fix: Align RN + Hermes versions; rebuild release bundle
