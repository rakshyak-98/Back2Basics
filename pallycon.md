`pallycon-customdata-v2` -> token is a server-side generated, cryptographically signed authentication string and authorizes your application to request a decryption key from the PallyCon License Server. You do not get this token from the client-side code the library itself; 

**You must implement an authentication flow in your backend to retrieve it.**

### The Authentication Architecture

1. **Application Auth**: Before the player initiates a license request, your app authenticates the user against your own backend (e.g., via a standard OAuth2 or JWT session).
    
2. **Token Generation**: Upon successful user authentication, your backend communicates with the **PallyCon DevConsole API** (or your own internal token service) to generate a valid DRM license token.
    
3. **Token Delivery**: Your backend returns this token to the client app (your Android/Kotlin code).
    
4. **License Request**: Your Android app then injects this token into the `pallycon-customdata-v2` HTTP header when making the request to `[https://license-global.pallycon.com/ri/licenseManager.do](https://license-global.pallycon.com/ri/licenseManager.do)`.

## PallyCon DevConsole API

Access to the PallyCon (now DoveRunner) DevConsole is granted through their official developer portal.

> [!INFO]
> **DevConsole Utilities**: Inside the console, look for the **DRM Tools** or **License Token Generator** section. This provides an interface to input your `Site ID` and `Site Key` (found in your account dashboard) to generate test tokens for specific `Content ID` values.