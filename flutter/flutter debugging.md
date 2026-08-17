[[flutter cli]] [[flutter error]] [[dart]] [[android/adb device]] [[Descriptive/DAP (Debug Adapter Protocol)]]

# Flutter debugging

> Watch the Dart VM, Flutter tool, and platform bridges (`adb`, iOS tools) while an app runs — find jank, crashes, and layout bugs.





## Interview Relevance
Interviewers care that you can name the processes in a debug session, when hot reload fails, and how you profile frame jank vs logic bugs.

## Sources
- [Flutter — Debugging Flutter apps](https://docs.flutter.dev/testing/debugging) — deep-dive
- [Flutter — DevTools](https://docs.flutter.dev/tools/devtools) — overview

## Key Concepts
- **Hot reload:** inject updated Dart into the running isolate → keeps state; fails on enum/native/const shape changes.
- **Hot restart / full restart:** reset isolate or rebuild native shell → needed when reload cannot apply.
- **VM service:** debug protocol endpoint for breakpoints, inspect, DevTools → what IDEs attach to.
- **Frontend server:** incremental Dart compiler during `flutter run` → feeds hot reload.
- **Platform bridge:** `adb` / Xcode tools talk to the device → install, logcat, port forward.

## Technical Details
Typical process map during `flutter run` on Android:

| Process | Role |
|---------|------|
| `dart` / Flutter tool | Orchestrates build + attach |
| Dart frontend server | Incremental compile |
| App isolate + VM service | Your code + debug protocol |
| `adb` | Device install, logs, reverse ports |

```bash
flutter run -d <DEVICE_ID>
flutter logs -d <DEVICE_ID>
flutter attach -d <DEVICE_ID>

# Open DevTools from the run session URL, or:
dart devtools
```

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Hot reload no-op | Native / const / enum changed | Hot restart or full restart |
| Breakpoints unbound | Wrong isolate / release build | Debug mode; re-attach |
| Blank after attach | App not paused at VM service | Relaunch with `flutter run` |
| Android logs missing | Wrong device / USB auth | `adb devices`; accept RSA prompt |

## Real-World Applications
Use DevTools timeline for jank, widget inspector for layout, and `flutter logs` when the IDE console truncates.

**Example:** List scrolls at 40 fps in debug — confirm with `--profile` before rewriting widgets.

## Pros/Cons or Trade-offs
- **Pro:** Hot reload keeps UI state while iterating.
- **Con:** Debug JIT hides release jank — always verify with profile/release.

## Comparison
- vs [[flutter error]]: debugging is live inspection; error notes are build/runtime failure catalogs.
- vs native Android Studio debugger: Flutter path goes through Dart VM service first, then platform tools.

## Mistakes to Avoid
- Trusting debug-only timings for production SLAs.
- Fighting hot reload after a native plugin change — full restart instead.
- Debugging without `flutter doctor` when the toolchain is half-broken.
