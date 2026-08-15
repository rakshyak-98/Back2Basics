[[flutter build]] [[flutter debugging]] [[dart]] [[android]]

# Flutter CLI

> Terminal front door to the Flutter SDK — create projects, run on devices, switch channels, and inspect logs.

## Interview Relevance

Interviewers want channel vs release cadence, debug (JIT) vs release (AOT), and the day-to-day commands you use to ship and debug.

## Sources

- [Flutter — Using the Flutter CLI](https://docs.flutter.dev/reference/flutter-cli) — deep-dive
- [Flutter — Flutter channels](https://docs.flutter.dev/install/upgrade#switching-flutter-channels) — overview

## Key Concepts

- **Channel:** release stream (`stable`, `beta`, `dev`, `master`) → pick stability vs newest APIs.
- **`flutter create`:** scaffolds platform folders + `lib/main.dart` → consistent project layout.
- **`flutter run`:** debug session with JIT + hot reload → fastest iteration on device/emulator.
- **`flutter attach`:** reconnect the tool to an already-running app → useful after detach or from IDE.
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

## Real-World Applications

Daily mobile work: create app → `flutter devices` → `flutter run` → fix with hot reload → `flutter build appbundle` for Play.

**Example:** A teammate on `master` breaks CI; pin the team to `stable` and document `flutter channel` in the README.

## Pros/Cons or Trade-offs

- **Pro:** One CLI covers create, run, analyze, build, and doctor.
- **Con:** Channel upgrades can move Gradle/Xcode expectations — budget a sync day after `flutter upgrade`.

## Comparison

- vs IDE Run button: CLI is scriptable for CI; IDE is faster for breakpoint UX — see [[flutter debugging]].
- vs `dart` CLI: Flutter wraps Dart plus platform tooling (Gradle, Xcode, web).

## Mistakes to Avoid

- Shipping from `master`/`dev` without a rollback plan — prefer `stable` for production apps.
- Assuming `flutter run` performance equals release — profile with `--profile` / `--release`.
- Ignoring `flutter doctor` when devices or toolchains vanish after OS updates.
