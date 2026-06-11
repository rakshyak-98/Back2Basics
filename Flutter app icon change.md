Instructions for replacing the default Flutter launcher icon with the green recycling trash icon (`WasteManagement.png`).

## Prerequisites

- Flutter SDK installed and working
- Source image: `WasteManagement.png` at the repo root (`EquipTrack/WasteManagement.png`)
- Recommended: square PNG, ideally **1024x1024** (minimum **512x512**)

## Scope

This procedure updates launcher icons for:
- Android
- iOS
- Web (PWA icons)
- Windows
- macOS
Optional follow-ups cover login screen branding and web manifest theme colors.

## Step 1: Place the source icon in the Flutter project

```bash

cd WasteManagement

mkdir -p assets/icon

cp ../WasteManagement.png assets/icon/app_icon.png

```
Use the filename `app_icon.png` to match the EquipTrack-app convention.

## Step 2: Update `pubspec.yaml`

File: `WasteManagement/pubspec.yaml`

### 2a. Add dev dependency

Under `dev_dependencies`, add:
```yaml

flutter_launcher_icons: ^0.14.3

```

### 2b. Add launcher icon configuration

After `dev_dependencies` (same level as `flutter:`), add:
```yaml

flutter_launcher_icons:
android: true
ios: true
web:
generate: true
windows:
generate: true
macos:
generate: true
image_path: assets/icon/app_icon.png
remove_alpha_ios: true

```

### 2c. Register asset for in-app use (optional)

If you also want the icon on the login screen, under the `flutter:` section add:

```yaml

assets:
- assets/icon/app_icon.png

```

## Step 3: Generate platform icons

```bash

cd WasteManagement
flutter pub get
dart run flutter_launcher_icons

```
Expected output: a success message listing generated icons per platform.

### Files that should change

| Platform | Path                                                    |
| -------- | ------------------------------------------------------- |
| Android  | `android/app/src/main/res/mipmap-*/ic_launcher.png`     |
| iOS      | `ios/Runner/Assets.xcassets/AppIcon.appiconset/*.png`   |
| Web      | `web/icons/Icon-*.png`                                  |
| Windows  | `windows/runner/resources/app_icon.ico`                 |
| macOS    | `macos/Runner/Assets.xcassets/AppIcon.appiconset/*.png` |

## Step 4: Rebuild and verify

```bash
flutter clean
flutter pub get
flutter run

```

On a device or emulator:
1. Uninstall any existing WasteManagement build (icons do not always refresh on upgrade).
2. Install the new build.
3. Confirm the home screen or app drawer shows the green recycling icon.

For a release APK:

```bash
flutter build apk --release

```

## Step 5: Login screen branding (optional)

File: `lib/screens/login_screen.dart`
Replace the placeholder `Icons.recycling_rounded` block (around lines 156-168) with:
```dart
ClipRRect(
	borderRadius: BorderRadius.circular(16),
		child: Image.asset(
		'assets/icon/app_icon.png',
		width: 56,
		height: 56,
		fit: BoxFit.cover,
	),
),

```
Requires Step 2c (`assets` entry in `pubspec.yaml`).

## Step 6: Web manifest theme colors (optional)

File: `web/manifest.json`
Change `background_color` and `theme_color` from `#0175C2` to a green that matches the icon, for example `#1B5E20`.
Also update `web/index.html` if the `theme-color` meta tag still uses blue.

## Verification checklist

- [ ] `assets/icon/app_icon.png` exists in the WasteManagement project
- [ ] `flutter_launcher_icons` is listed in `dev_dependencies`
- [ ] `flutter_launcher_icons` config block is present with correct `image_path`
- [ ] `dart run flutter_launcher_icons` completed without errors
- [ ] Android `ic_launcher.png` files updated (not default Flutter blue)
- [ ] App reinstalled and launcher icon visible on device
- [ ] (Optional) Login screen shows PNG instead of Material icon
- [ ] (Optional) Web manifest colors match green branding

## Troubleshooting

| Issue                                   | Action                                                                        |
| --------------------------------------- | ----------------------------------------------------------------------------- |
| Old icon still shown                    | Uninstall the app completely, then reinstall                                  |
| `dart run flutter_launcher_icons` fails | Run `flutter pub get` first; confirm `image_path` file exists                 |
| iOS build warns about alpha channel     | `remove_alpha_ios: true` is already set; re-run the generator                 |
| Blurry icon on device                   | Use a higher-resolution source image (1024x1024)                              |
| Login image not found                   | Confirm `assets:` entry in `pubspec.yaml` and path `assets/icon/app_icon.png` |
