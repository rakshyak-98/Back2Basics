[[React]] [[bundler]] [[NodeJS]] [[SWC]] [[source map]]

# Metro Bundler

> React Native's default JavaScript bundler — fast dev iteration via incremental transforms, not webpack-style whole-graph rebuilds.

```txt
        Metro Bundler ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe **Metro Bundler** to see if you understand what it does op…

## Sources
- [Metro — Concepts](https://metrobundler.dev/docs/concepts/) — deep-dive
- [Wikipedia — metro bundler](https://en.wikipedia.org/wiki/metro_bundler) — overview

## Key Concepts
- **Metro sits:** Metro sits between your RN source tree and the native runtime (Hermes/JSC)
- **Key concepts:** Key concepts: - **Transformer**


- **Core:** Metro sits between your RN source tree and the native runtime (Hermes/JSC)

## Technical Details
- Metro sits between your RN source tree and the native runtime (Hermes/JSC).
- Unlike general web bundlers optimized for browser chunks, Metro optimizes for…

```
App requests bundle          Metro dev server
        │                           │
        │  GET /index.bundle        │
        └──────────────────────────►│ resolve graph (lazy)
                                    │ Babel/SWC transform per file
                                    │ cache in metro-cache
                                    ◄── single bundle (dev) or split (prod)
```

- Key concepts:

- **Transformer:** — Babel (default) or experimental SWC
- **Resolver:** — `node_modules` + platform extensions (`.ios.js`, `.android.js`, `.native.js…
- **Serializer:** — outputs the bundle string the native side loads.
- **Cache:** — file-system cache keyed by transform inputs

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

## Mistakes to Avoid
- **Mistake:** **Cache lies**
- **Mistake:** **Symlinks in monorepos**
- **Mistake:** **Native modules ≠ JS bundle**
- **Mistake:** **Expo vs bare**
- **Mistake:** **Red screen "Unable to resolve module":** check Path, typo, mis…
- **Mistake:** **Works after `--reset-cache` only:** check Stale metro-cache or…
- **Mistake:** **"TransformError" / syntax error:** check Babel preset missing …
- **Mistake:** **Monorepo package not found:** check Metro not watching workspa…
- **Mistake:** **Huge bundle / slow startup:** check No inline requires
- **Mistake:** **Hermes bytecode issues:** check Wrong Hermes compiler version …

## Pros/Cons or Trade-offs
- **Pro:** Solves the job described above when used in the right layer (React Native's default JavaScript bundler — fast dev iteration via incremental t…).
- **Con / when not:** **Web-only React (Vite/webpack)**
- **Con / when not:** **Replacing Babel blindly with SWC**
- **Con / when not:** **Custom bundler for simple RN application**

## Comparison
- vs [[React]]: know when each applies


### Use cases
- In production APIs and tooling, **metro bundler** shows up whenever teams shi…
