[[flutter build]] [[flutter debugging]] [[dart]] [[android]]

# Flutter CLI

> Terminal front door to the Flutter SDK — create projects, run on devices, switch channels, and inspect logs.

```txt
        Flutter CLI ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers want channel vs release cadence, debug (JIT) vs release (AOT), a…

## Sources
- [Flutter — Using the Flutter CLI](https://docs.flutter.dev/reference/flutter-cli) — deep-dive
- [Flutter — Flutter channels](https://docs.flutter.dev/install/upgrade#switching-flutter-channels) — overview

## Key Concepts
- **Channel:** release stream (`stable`, `beta`, `dev`, `master`) → pick stability vs newest…
- **`flutter create`:** scaffolds platform folders + `lib/main.dart` → consistent project layout.
- **`flutter run`:** debug session with JIT + hot reload → fastest iteration on device/emulator.
- **`flutter attach`:** reconnect the tool to an already-running app → useful after detach or from ID…
- **Device target (`-d`):** pick emulator, USB device, or chrome → multi-device workflows.

## Technical Details
```bash
flutter channel                 # show current + available
flutter channel stable
flutter upgrade

flutter create my_app
flutter devices
flutter run -d <DEVICE_ID>
flutter attach -d <DEVICE_ID>
flutter install -d <DEVICE_ID>
flutter logs -d <DEVICE_ID>

flutter pub get
flutter analyze
flutter test
flutter bash-completion         # shell completion (where supported)
```

| Mode | Compilation | Use |
|------|-------------|-----|
| `flutter run` (debug) | JIT | Hot reload, asserts |
| `--profile` | AOT + tracing | Perf work |
| `--release` / `flutter build` | AOT optimized | Ship / smoke-test release |

## Mistakes to Avoid
- **Mistake:** Shipping from `master`/`dev` without a rollback plan
- **Mistake:** Assuming `flutter run` performance equals release
- **Mistake:** Ignoring `flutter doctor` when devices or toolchains vanish afte…

## Pros/Cons or Trade-offs
- **Pro:** One CLI covers create, run, analyze, build, and doctor.
- **Con:** Channel upgrades can move Gradle/Xcode expectations — budget a sync day after `flutter upgrade`.

## Comparison
- vs IDE Run button: CLI is scriptable for CI; IDE is faster for breakpoint UX
- vs `dart` CLI: Flutter wraps Dart plus platform tooling (Gradle, Xcode, web).


### Use cases
- Daily mobile work: create app → `flutter devices` → `flutter run` → fix with …

- **Example:** A teammate on `master` breaks CI
