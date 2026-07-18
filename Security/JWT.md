[jwt alg algorithms](https://datatracker.ietf.org/doc/html/rfc7518#section-3.1)

| **Part**         | **Name** | **Purpose**                                                                                                                                      |
| ---------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1. Header**    | `xxxxx`  | Contains metadata. Usually defines the type (`JWT`) and the hashing algorithm used (like `HS256`).                                               |
| **2. Payload**   | `yyyyy`  | Contains the "claims" or data you passed in (e.g., `userId`). This is where the session info lives.                                              |
| **3. Signature** | `zzzzz`  | The security guard. It is a hash of the (Header + Payload + Secret). If anything in the first two parts changes, this signature becomes invalid. |

> [!WARNING]
> **Trusting Claims Before Verification:** Reading a claim and performing an action (like deleting a database record) before the `jwt.verify()` function has finished. You must verify the signature _first_, otherwise, the "claim" is just a pinky-promise from the client.

- Signed token can verify the integrity of the claims contained withing it, while encrypted tokens hide those claims.
- JWT rely on a single key. If that key is compromised, the entire system is at risk.
- You con't push message to all clients, and you can't manage clients from the server side.
- JWT does not inherently support broadcasting messages to all clients.
- With JWT the server cannot directly manage or control clients once they are authenticated.
- JWT are stateless, meaning that after a token is issued, the server does not retain any session information.
 
 > [!NOTE]  >  - Revoking access or managing client states must be handled differently, often requiring additional mechanisms (token blacklisting or database checks). >  - until the token expires the client retains access, which could pose security risks.

Each JWT is typically associated with a specific user or session, meaning that messages must be sent individually to each client rather than as a group.
- You run an online journal. You want everyone to read and comment on only one document, not on any others. Tokens could allow this.

[JWT workflow](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics#section-4.12)
- `POST/login` -> get access token + refresh token cookie.
- user `access_token` to call `GET /` API.
- On expiry, `POST /refresh` -> gets new tokens.
- Try reusing old refresh token -> get `403 Forbidden`.


### JWT options

```js
jwt.sign(payload, secret, { expiresIn: '10m' })   // 10 minutes
jwt.sign(payload, secret, { expiresIn: '1d' })    // 1 day
jwt.sign(payload, secret, { expiresIn: 3600 })    // seconds
```

- exp = iat + duration


claim -> is essentially a piece of information asserted about a subject (usually a user). If you think of a JWT as a digital ID card, the claims are the specific fields on that card, like "Name", "Date of Birth", or "Clearance level".

- It is called a "claim" because the token is claiming something is true. It only becomes 'fact' to the server once the digital signature is verified to prove the token hasn't been tampered with.

```js
const jwt = require('jsonwebtoken');

const payload = {
  // Registered Claims (Standardized)
  sub: "1234567890", // Subject (User ID)
  name: "John Doe",
  iat: 1516239022,

  // Public/Private Claims (Custom)
  "https://example.com/is_admin": true,
  "role": "editor"
};

const token = jwt.sign(payload, 'your-256-bit-secret');
```

> [!NOTE]
> **Conflicting Custom Claims** -> Using generic keys like `id` or `role` in a system that integrates multiple services. If Service A thinks `role` is a string and Service B thinks `role` is an array, your code will crash. This is why many pros use URNs (like `urn:example:role`) for custom claims.