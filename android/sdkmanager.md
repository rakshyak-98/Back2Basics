[[android]] [[Docker compose]] [[kubectl]]

# sdkmanager

> Android SDK command-line package manager — install platforms, build-tools, NDK in **headless CI** without Android Studio.

---

## Mental model

```txt
sdkmanager  →  reads SDK root ($ANDROID_HOME)
            →  downloads packages from Google Maven/SDK repo
            →  writes licenses + package metadata under cmdline-tools/
```

**SDK layout (modern):**

```txt
$ANDROID_HOME/
  cmdline-tools/latest/bin/sdkmanager
  platforms/android-34/
  build-tools/34.0.0/
  platform-tools/          # adb, fastboot
  licenses/                # must accept for CI
```

**Gradle** consumes `compileSdk`, `buildToolsVersion`, NDK version from `build.gradle` — CI must pre-install matching packages or builds fail before compile.

---

## Standard config / commands

### Install cmdline-tools (CI base image)

```bash
export ANDROID_HOME=/opt/android-sdk
export PATH="$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools"

# Download commandlinetools-linux-*.zip from developer.android.com
mkdir -p "$ANDROID_HOME/cmdline-tools"
unzip commandlinetools-linux-*.zip -d /tmp
mv /tmp/cmdline-tools "$ANDROID_HOME/cmdline-tools/latest"
```

### Accept licenses (non-interactive)

```bash
yes | sdkmanager --licenses
# Or pipe pre-accepted hashes in regulated CI (document in vault policy)
```

### Install packages (typical CI set)

```bash
sdkmanager --install \
  "platform-tools" \
  "platforms;android-34" \
  "build-tools;34.0.0" \
  "cmdline-tools;latest"

# NDK (when native code / React Native / Flutter)
sdkmanager --install "ndk;26.1.10909125"
```

### List / update

```bash
sdkmanager --list              # available + installed
sdkmanager --list_installed
sdkmanager --update            # upgrade installed (pin in CI instead)
```

### Gradle alignment

```gradle
// app/build.gradle
android {
  compileSdk 34
  buildToolsVersion "34.0.0"
  ndkVersion "26.1.10909125"
}
```

### GitHub Actions pattern

```yaml
- uses: android-actions/setup-android@v3
- run: sdkmanager --install "platforms;android-34" "build-tools;34.0.0"
```

### Docker CI snippet

```dockerfile
ENV ANDROID_HOME=/opt/android-sdk
RUN yes | sdkmanager --licenses && \
    sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Failed to install ... license not accepted` | `licenses/` dir | `yes \| sdkmanager --licenses` |
| `SDK location not found` | `ANDROID_HOME`, `local.properties` | Set env; `sdk.dir=` in local.properties |
| Gradle: compileSdk not found | `--list_installed` | Install matching `platforms;android-XX` |
| NDK build fails version mismatch | `ndkVersion` in Gradle vs installed | `sdkmanager --install "ndk;..."` exact version |
| `Warning: Still waiting for package manager` | Stale lock / parallel jobs | Single sdkmanager process; clear `.android` locks |
| Network fail in CI | Proxy / Google repo | Mirror or cache SDK tarball; retry with timeout |

---

## Gotchas

> [!WARNING]
> **Unpinned `--update` in CI** — non-reproducible builds; pin platform + build-tools versions in pipeline YAML.

> [!WARNING]
> **Old `tools/bin/sdkmanager`** — deprecated; use `cmdline-tools/latest/bin`.

> [!WARNING]
> **JDK version** — AGP 8+ requires JDK 17; sdkmanager itself needs working Java on PATH.

> [!WARNING]
> **Huge SDK footprint** — cache `$ANDROID_HOME` in CI; don't re-download platforms every job.

---

## When NOT to use

- **Local dev with Android Studio** — Studio SDK Manager UI is easier; same packages underneath.
- **iOS builds** — Xcode / `xcodebuild`, not sdkmanager.
- **Installing arbitrary APKs on device** — `adb install`, not sdkmanager.

---

## Related

[[android]] · [[Docker compose]] · [[docker cli]] · [[Terraform workflow]]
