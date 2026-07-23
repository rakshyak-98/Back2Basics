[[flutter]] [[android]] [[dart/dart functions]]

# Flutter build and release

> Compile Dart to native ARM/x64 binaries and platform bundles — debug fast, profile jank, release with obfuscation, signing, and store-ready artifacts.

## Mental model

```
Dart source ──► kernel / AOT compiler ──► libapp.so (mobile) or js/wasm (web)
                      │
                      ├── debug: JIT + VM service (hot reload)
                      ├── profile: AOT + tracing
                      └── release: AOT optimized, tree-shaken, no asserts
```

Platform shells:
- **Android** — Gradle wraps `flutter build apk/appbundle`; signing via keystore.
- **iOS** — Xcode archive; provisioning profiles + App Store Connect.
- **Web** — `flutter build web` → CanvasKit or skwasm renderer.

## Standard config / commands

### Day-to-day

```bash
flutter pub get
flutter analyze
flutter test

flutter run                    # debug on device/emulator
flutter run --profile          # performance profiling
flutter run --release          # local release smoke test
```

### Android release

```bash
# App Bundle (Play Store preferred)
flutter build appbundle --release \
  --obfuscate --split-debug-info=build/debug-info

# APK (side-load / legacy)
flutter build apk --release --split-per-abi
```

**android/key.properties** (gitignored)

```properties
storePassword=***
keyPassword=***
keyAlias=upload
storeFile=/home/user/upload-keystore.jks
```

**Generate keystore (once)**

```bash
keytool -genkey -v \
  -keystore ~/upload-keystore.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias upload
```

**android/app/build.gradle** — reference signing config; `minSdk`, `targetSdk`, `versionCode`/`versionName` from `pubspec.yaml`:

```yaml
# pubspec.yaml
version: 1.2.0+42   # name+build number
```

### iOS release

```bash
flutter build ios --release
# Open ios/Runner.xcworkspace → Product → Archive → Distribute
```

### Web

```bash
flutter build web --release --web-renderer canvaskit
# Serve build/web/ via CDN or [[Nginx]]
```

### Obfuscation and symbols

```bash
flutter build appbundle --obfuscate --split-debug-info=build/symbols
# Upload symbols to Play Console / Sentry for readable crash stacks
```

### Clean when builds lie

```bash
flutter clean && flutter pub get
cd android && ./gradlew clean && cd ..
```

### CI sketch

```yaml
- run: flutter test
- run: flutter build appbundle --release --obfuscate --split-debug-info=symbols
- uses: upload-artifact # .aab + symbols/
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Hot reload doesn't apply | Native code / const / enum changed | Hot restart; full restart |
| Release crash, debug OK | Obfuscation renamed symbol | `--split-debug-info`; retain mapping |
| Gradle / SDK errors | JDK, AGP, compileSdk mismatch | Align `android/build.gradle` with Flutter docs for version |
| Signing failed | Wrong alias/password | Verify `key.properties`; path to keystore |
| iOS provisioning | Cert expired | Regenerate in Apple Developer portal |
| Huge APK | Single ABI fat apk | `--split-per-abi` or use AAB |
| Web blank screen | Base href / renderer | `--base-href /app/`; check console for wasm errors |
| `versionCode` rejected | Monotonic build number | Bump `+N` in pubspec |

## Gotchas

> [!WARNING]
> **Never commit keystore or key.properties** — use CI secrets; losing keystore = can't update app id on Play.

> [!WARNING]
> **Debug performance ≠ release** — profile with `--profile` or `--release`; debug JIT masks jank.

> [!WARNING]
> **Tree shaking removes unused icons/fonts** — declare assets in `pubspec.yaml` explicitly.

> [!WARNING]
> **Plugin native bumps** — after `flutter upgrade`, run pod install / gradle sync; stale pods cause link errors.

## When NOT to use

- **Shipping debug builds** — larger, slower, asserts enabled.
- **Obfuscation without symbol backup** — crash reports become useless.
- **Manual APK for Play Store** — prefer **AAB** for dynamic delivery.

## Related

[[flutter]] [[android]] [[dart/dart functions]] [[Release cycle]] [[Nginx]]
