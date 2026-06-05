AOT (Ahead-of-Time Compilation)

```bash
flutter bash-completion;
flutter create <DIRECTORY>; # Creates a new project
flutter install -d <DEVICE ID>; # Install flutter app on an attached device.
flutter logs; # SHow log output fo running flutter apps.
```

```bash
flutter run; # Users JIT (Just-In-Time) compilation
flutter attach -d <DEVICE ID>;
```

## Channel

A channel is a release stream of the Flutter SDK. Each channel receives updates at different speeds and stability levels.

> [!INFO]
> Flutter channels are official Flutter SDK repository.

```bash
flutter channel; # list channel
flutter channel beta; # switch channel
```