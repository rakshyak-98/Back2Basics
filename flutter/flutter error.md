```text
Try `flutter pub outdated` for more information.
Launching lib/main.dart on motorola edge 50 fusion in debug mode...

FAILURE: Build failed with an exception.

* What went wrong:
Value '/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home' given for org.gradle.java.home Gradle property is invalid (Java home supplied is invalid)

* Try:
> Run with --stacktrace option to get the stack trace.
> Run with --info or --debug option to get more log output.
> Run with --scan to get full insights.
> Get more help at https://help.gradle.org.
Running Gradle task 'assembleDebug'...                           1,099ms

```
- installed at macOS location `/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home`
- you are on linux ubuntu, Gradle cannot start JVM

Why people add this:
- multiple JDK versions installed
- Android Studio using different JDK
- lock project to specific Java version

