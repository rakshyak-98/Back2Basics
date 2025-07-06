[full Stack authentication](https://firtman.github.io/authentication/)

validating user identity, system validation, or a service validation.

Credentials -> identify user on server side.
SSO -> same credential with different web apps.
2FA -> user name and password is 1FA, otp is 2FA.
MFA -> 2 or more factor of authentication.
passkey -> 
OAuth 2.0 -> keep user logged, login with thrid party authentication.
JWT -> format metadata for credentials.
OTP -> receive an one time password. Web OTP.
Public Key Cryptography -> 


Custom AUth -> user/pass, WebAuthn
Identity Providers -> OpenID, SAML2.0, Sign in with (My server won't store any data from you).
Identity As a Service IDaaS ->

### Authentication on the web
#### Risk
- man in the middle attacks, attack through the network.
- key loggers, (install custom keyboard downloaded).
- Easy to guess password. 
- Web Server and DBs attacks.
- phishing and Social Engineering Attacks.

#### HTTP Auth/Logins Forms
- HTTP support basic auth.
- HTTPS -> encryption at the middle not on the server.


## Login Form Flow

Registration
Login
Recover password

-  connect labels for each element
- don't use placeholder as labels
- using html semantics
- one SPAs, form names different for registration and logic forms, password manager don't know on which page you are. 
- one SPAs, use submit form event and submission will be triggered by a pushState (onClick event have problem with password managers). Password manager might won't save the password.
- let the user make the password visible.
- Help password managers with autocomplete HTML attributes.


### Enhanced login form
`autocomplete` -> new-password, or current-password depend on the page is it login page or password recovery page.

> [!INFO] Login form
```html
<input type="email" autocomplete="username" />
<input type="email" autocomplete="current-password" />
```

> [!INFO] Registration form
```html
<input type="email" autocomplete="username" />
<input type="password" autocomplete="new-password" />
```