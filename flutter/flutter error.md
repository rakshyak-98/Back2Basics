[[flutter build]] [[Flutter CLI]] [[android]] [[dart]]

# Flutter errors

> Typical Flutter/Android build and runtime failures — wrong JDK path, stale Gradle, and dependency drift — and how to clear them.

```txt
        Flutter errors ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers want a calm triage path: read the first actionable line, check J…

## Sources
- [Flutter — Android setup](https://docs.flutter.dev/get-started/install/linux#android-setup) — overview
- [Gradle — Build Environment](https://docs.gradle.org/current/userguide/build_environment.html) — deep-dive

## Key Concepts
- **First failure line:** Gradle/Flutter often print a long stack
- **`org.gradle.java.home`:** pinned JDK path in Gradle properties → breaks when you change OS or machine.
- **`flutter pub outdated`:** shows dependency drift → useful after upgrade failures.
- **Host vs project JDK:** Android Studio JDK ≠ command-line JDK → CI and laptop can disagree.

## Technical Details
- Common failure: Linux laptop with a macOS JDK path left in Gradle properties:

```text
Value '/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home'
given for org.gradle.java.home Gradle property is invalid
```

- Why it appears: multiple JDKs, Android Studio defaults, or a copied `gradle.p…

```bash
flutter doctor -v
flutter pub outdated
echo "$JAVA_HOME"
# Fix project or user gradle.properties — remove invalid org.gradle.java.home
# or point it at a real JDK 17+ on this machine

flutter clean && flutter pub get
cd android && ./gradlew --stop && ./gradlew clean && cd ..
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Invalid Java home | Path exists on this OS? | Edit `gradle.properties`; set `JAVA_HOME` |
| SDK / compileSdk mismatch | `android/app/build.gradle` | Align with Flutter template for your version |
| Plugin native link errors | After `flutter upgrade` | Clean; refresh pods / Gradle sync |
| Pub resolution fail | Constraints in `pubspec.yaml` | `flutter pub outdated`; relax pins carefully |

## Mistakes to Avoid
- **Mistake:** Committing machine-specific `org.gradle.java.home` paths
- **Mistake:** Running endless `flutter clean` without reading the first Gradle…
- **Mistake:** Mixing JDK 8 with modern Android Gradle Plugin requirements

## Pros/Cons or Trade-offs
- **Pro:** Pinning JDK major version keeps builds reproducible.
- **Con:** Absolute JDK paths in repo properties are not portable across OS/machines.

## Comparison
- vs [[flutter debugging]]: errors here are usually build/config; debugging is runtime/VM.
- vs pure Android Gradle errors: Flutter adds another layer (`flutter` tool + plugins) on top of Gr…


### Use cases
- Onboard a new engineer: `flutter doctor -v` must be green before touching pro…

- **Example:** CI fails after a macOS-only `gradle.properties` commit
