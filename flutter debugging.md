
### Process description

| Process           | Purpose                                           |
| ----------------- | ------------------------------------------------- |
| `dart:dartdev_ao` | Dart CLI launcher (`dart` command infrastructure) |
| `dart:flutter_to` | Flutter tool (`flutter run`, `flutter build`)     |
| `adb`             | Android Debug Bridge command                      |
| `dart:dartdev_ao` | Another Dart CLI helper process                   |
| `adb`             | Another ADB invocation                            |
| `dart:frontend_s` | Dart frontend server (compiler)                   |
