[[flutter build]] [[android]] [[flutter cli]]

# Flutter app icon change

> Replace the default launcher icon on Android/iOS with your brand assets — mipmaps / AppIcon sets the home-screen image users tap.





## Interview Relevance
Interviewers rarely deep-dive icons, but release hygiene questions expect you to know platform asset locations, density buckets, and that a Flutter rebuild alone does not always refresh launcher caches.

## Sources
- [Flutter — App icons](https://docs.flutter.dev/deployment/android#changing-the-application-launcher-icons) — overview
- [Android — Adaptive icons](https://developer.android.com/develop/ui/views/launch/icon_design_adaptive) — deep-dive

## Recall Cues
- Why do interviewers care about Interviewers rarely deep-dive icons, but release hygiene questions expect you to know platform asset locations, density buckets, and that a Flutter rebuild alone does not always refresh launcher caches?
- What is step 1: Provide a high-res master PNG (e.g. brand mark)?
- What is step 4: Rebuild and reinstall: `flutter build apk` / run on device?
- What mistake is **Only changing `assets/` and expecting the home-screen icon to update**?
- What mistake is **Committing a tiny source image and upscaling — looks soft on xxxhdpi**?
- What mistake is **Forgetting iOS `AppIcon` when Android was updated (or the reverse)**?

## Technical Details
Manual (Android sketch):

1. Provide a high-res master PNG (e.g. brand mark).
2. Generate mipmaps / adaptive layers into `android/app/src/main/res/`.
3. Confirm `AndroidManifest.xml` `android:icon` / `android:roundIcon`.
4. Rebuild and reinstall: `flutter build apk` / run on device.

Common package approach (`pubspec.yaml`):

```yaml
dev_dependencies:
  flutter_launcher_icons: ^0.14.0

flutter_launcher_icons:
  android: true
  ios: true
  image_path: assets/icon/app_icon.png
```

```bash
dart run flutter_launcher_icons
flutter clean && flutter run
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Old icon after rebuild | Install vs overlay | Uninstall app; reinstall |
| Blurry icon | Source resolution | Use ≥1024px master; regenerate densities |
| Android adaptive crop | Safe zone | Keep logo inside adaptive safe area |

## Mistakes to Avoid
- Only changing `assets/` and expecting the home-screen icon to update.
- Committing a tiny source image and upscaling — looks soft on xxxhdpi.
- Forgetting iOS `AppIcon` when Android was updated (or the reverse).

## Comparison
- vs in-app `Image.asset`: UI images are Flutter assets; launcher icons are native resources.
- vs store listing graphics: Play/App Store screenshots/feature graphics are separate from the launcher icon.

## Real-World Applications
White-label or rebrand: one master asset → generate both stores’ icons → verify on a physical launcher, not only the IDE.

**Example:** Shipping a waste-management app — swap default Flutter logo for `WasteManagement.png` via launcher-icons config before Play upload.

## Pros/Cons or Trade-offs
- **Pro:** Codegen packages keep Android/iOS in sync from one file.
- **Con:** Hand-edited mipmaps drift between platforms after the next rebrand.
