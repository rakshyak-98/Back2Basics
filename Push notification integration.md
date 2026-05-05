APNs certificate is Apple's way of authenticating your backend server to send push notification to ISO devices.
- It proves to Apple that your server is legitimate and authorized to send notification for your app. Without it, Apple won't deliver your push notification.


> [!INFO]
> You don't directly handle the certificate in your Flutter code
> - Firebase Cloud Messaging (FCM) handles IOS certificates for you behind the scenes.
> - Is using APNs directly, your backend engineer manages the certificate and authentication.