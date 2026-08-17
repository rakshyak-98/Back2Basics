[[adb device]] [[flutter build]] [[Linux/apt package manager]]

# sdkmanager

> Android SDK command-line package manager — install platforms, build-tools, NDK, and other packages without the full Android Studio UI.





## Interview Relevance
CI interviews: headless SDK install, accepting licenses, and pinning `build-tools`/`platforms` versions for reproducible builds.

## Sources
- [Android — sdkmanager](https://developer.android.com/tools/sdkmanager) — deep-dive

## Key Concepts
- **SDK root:** `ANDROID_HOME` / `ANDROID_SDK_ROOT`.
- **Packages:** platforms, build-tools, platform-tools, emulators, NDK.
- **Licenses:** `sdkmanager --licenses` must be accepted in CI.
- **Channel/version pins:** avoid silent skew across agents.

## Technical Details
```bash
sdkmanager --list
sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"
yes | sdkmanager --licenses
```

| Package | Role |
|---------|------|
| platform-tools | `adb`, `fastboot` |
| platforms;android-XX | Compile SDK |
| build-tools;X.Y.Z | aapt/dx/d8 tooling |
| ndk;XX | Native builds |

## Real-World Applications
GitHub Actions runner installs only needed packages instead of full Android Studio.

**Example:** Flutter build fails missing `build-tools` — install the version Gradle requests, not a random older one.

## Pros/Cons or Trade-offs
- **Pro:** Scriptable, minimal images for CI.
- **Con:** Easy to drift if versions are not pinned in docs/CI.

## Comparison
- vs Android Studio SDK UI: same packages; CLI is automatable.
- vs [[adb device]]: sdkmanager installs; adb operates devices.

## Mistakes to Avoid
- Skipping license acceptance in CI.
- Installing every package “just in case” (huge images).
- Mixing multiple SDK roots without fixing environment variables.
