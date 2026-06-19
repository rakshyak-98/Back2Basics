APNs certificate is Apple's way of authenticating your backend server to send push notification to ISO devices.
- It proves to Apple that your server is legitimate and authorized to send notification for your app. Without it, Apple won't deliver your push notification.


> [!INFO]
> You don't directly handle the certificate in your Flutter code
> - Firebase Cloud Messaging (FCM) handles IOS certificates for you behind the scenes.
> - Is using APNs directly, your backend engineer manages the certificate and authentication.

> [!WARNING]
> `google-service.json` -> is Firebase's Android config file. It tells your app which Firebase project it belongs to and wires up Google Services at build time. Required for push notification service.

- Without `google-service.json` `Firebase.initializeApp()` usually fails on Android, so you won't get FCM tokens, push notification or device registration after login.

## What the file contains

It’s generated in the [Firebase Console](https://console.firebase.google.com/) when you register your Android app. It includes things like:

- Project ID and Project number
- Application ID (`com.hotelmate.hkApp` — must match `applicationId` in Gradle)
- API keys and mobile SDK app ID
- Config for FCM and other enabled Firebase services

At build time, the `com.google.gms.google-services` plugin reads this file and generates the Android resources Firebase SDKs expect.