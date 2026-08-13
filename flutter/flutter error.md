[[flutter]]

# flutter error

> flutter error — try flutter pub outdated for more information.

---

## How it works

```text
Try `flutter pub outdated` for more information.
Launching lib/main.dart on motorola edge 50 fusion in debug mode...
FAILURE: Build failed with an exception.
* What went wrong:
Value '/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home' given for org.gradle.java.home Gradle property is invalid (Java home supplied is invalid)
* Try:
Running Gradle task 'assembleDebug'...                           1,099ms
```
- installed at macOS location `/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home`
- you are on linux ubuntu, Gradle cannot start JVM
Why people add this:
- multiple JDK versions installed
- Android Studio using different JDK
- lock project to specific Java version


---


## Steps

1. …


## Verification

```bash
# …
```


## Rollback

1. …


## Related

[[flutter]]

## Sources

- [Wikipedia — flutter error](https://en.wikipedia.org/wiki/flutter_error)
