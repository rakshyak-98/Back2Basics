[[sdkmanager]] [[flutter debugging]] [[Linux/commands/SSH]]

# adb device

> Android Debug Bridge talks to phones/emulators — list devices, install APKs, forward ports, and stream logs for development.

```txt
        adb device ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Mobile interviews expect `adb devices`, authorization prompts, and logcat/`in…

## Sources
- [Android — adb](https://developer.android.com/tools/adb) — deep-dive

## Key Concepts
- **adb server/client:** local server mediates device connections.
- **Device state:** `device`, `unauthorized`, `offline`.
- **Install/debug:** push APKs, reverse ports for dev servers.
- **logcat:** device logs filtered by tag/pid.

## Technical Details
```bash
adb devices
adb install -r app.apk
adb logcat
adb reverse tcp:8080 tcp:8080
adb shell
```

| State | Meaning |
|-------|---------|
| `unauthorized` | Accept RSA prompt on phone |
| `offline` | Cable/driver glitch — replug/restart adb |
| `device` | Ready |

```bash
adb kill-server && adb start-server
```

## Mistakes to Avoid
- **Mistake:** Ignoring `unauthorized` and blaming Flutter
- **Mistake:** Multiple adb versions on PATH fighting each other
- **Mistake:** Leaving `adb tcpip` debugging open on untrusted networks

## Pros/Cons or Trade-offs
- **Pro:** Universal Android tooling entry point.
- **Con:** USB drivers/cables and authorization UX cause flaky setups.

## Comparison
- vs Xcode devices window: same role on iOS with different tools.
- vs [[sdkmanager]]: sdkmanager installs platform tools; adb uses them.


### Use cases
- Flutter/React Native debugging on a physical Pixel: `adb devices` must show `…

- **Example:** Emulator listed but app installs to the wrong target
