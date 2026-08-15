[[flutter cli]] [[android]] [[dart/dart functions]] [[Nginx]]

# Flutter build and release

> Compile Dart to shippable artifacts — debug uses JIT; profile/release use AOT (`libapp.so`, IPA, or web JS/Wasm).

## Interview Relevance

Interviewers want the debug/profile/release matrix, Android App Bundle vs APK, signing, and why obfuscation needs retained symbols.

## Sources

- [Flutter — Build and release an Android app](https://docs.flutter.dev/deployment/android) — deep-dive
- [Flutter — Build and release modes](https://docs.flutter.dev/testing/build-modes) — overview

## Key Concepts

- **Debug:** JIT + VM service → hot reload; slowest, asserts on.
- **Profile:** AOT + tracing → performance work without full debug overhead.
- **Release:** AOT, tree-shaken, asserts off → what you ship.
- **Signing:** Android keystore / iOS provisioning → store identity; losing the keystore blocks updates for that app id.
- **Obfuscation + symbols:** rename Dart symbols; keep `--split-debug-info` for readable crashes.

## Technical Details

```
Dart source ──► kernel / AOT ──► libapp.so (mobile) or js/wasm (web)
                 ├── debug: JIT + VM service
                 ├── profile: AOT + tracing
                 └── release: optimized AOT
```

```bash
flutter pub get && flutter analyze && flutter test
flutter run                      # debug
flutter run --profile
flutter build appbundle --release \
  --obfuscate --split-debug-info=build/debug-info
flutter build apk --release --split-per-abi
flutter build ios --release
flutter build web --release
flutter clean && flutter pub get
```

**android/key.properties** (gitignored) + `keytool` once for the upload keystore. Version in `pubspec.yaml`: `1.2.0+42` (name + monotonic build number).

| Symptom | Check | Fix |
|---------|-------|-----|
| Release crash, debug OK | Obfuscation | Retain/upload symbol files |
| Signing failed | Alias/password/path | Fix `key.properties` |
| Huge APK | Fat ABI | `--split-per-abi` or AAB |
| `versionCode` rejected | Non-monotonic `+N` | Bump build number |
| Hot reload after native change | Plugins / enums | Full restart |

## Real-World Applications

CI: test → build AAB with obfuscation → upload artifact + symbols to Play / crash reporter.

**Example:** Play rejects a rebuild because `+41` was reused — bump to `+42` in `pubspec.yaml`.

## Pros/Cons or Trade-offs

- **Pro:** AAB lets Play deliver ABI splits; smaller downloads.
- **Con:** Obfuscation without symbols makes production crashes unreadable.

## Comparison

- vs [[flutter cli]] `run`: local iteration; `build` produces store artifacts.
- vs native Android release: Flutter still rides Gradle/Xcode; you own both Dart and platform configs.

## Mistakes to Avoid

- Committing keystores or `key.properties`.
- Judging jank from debug builds.
- Shipping without uploading obfuscation symbols.
