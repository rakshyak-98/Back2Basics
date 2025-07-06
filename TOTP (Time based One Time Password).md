```js
const otplib = require('otplib');

const secret = otplib.authenticator.generateSecret();
const token = otplib.authenticator.generate(secret);
const isValid = otplib.authenticator.check(userInputCode, secret);

```

### How TOTP Works
1. when a user enables TOTP 2FA:
	- the server generates a random secret (using `base32`)
	- that secret is shown as QR code or string.
	- the user scans it in their TOTP app.
2. Both the server and the app use the same secret and the current timestamp to generate OTPs.
3. At login
	- the user enters a 6-digit TOTP.
	- the server verifies it using the same secret + time window.