- Signed token can verify the integrity of the claims contained withing it, while encrypted tokens hide those claims.
- JWT rely on a single key. If that key is compromised, the entire system is at risk.
- You con't push message to all clients, and you can't manage clients from the server side.
- JWT does not inherently support broadcasting messages to all clients.
- With JWT the server cannot directly manage or control clients once they are authenticated.
- JWT are stateless, meaning that after a token is issued, the server does not retain any session information.

> [!NOTE] 
>  - Revoking access or managing client states must be handled differently, often requiring additional mechanisms (token blacklisting or database checks).
>  - until the token expires the client retains access, which could pose security risks.

Each JWT is typically associated with a specific user or session, meaning that messages must be sent individually to each client rather than as a group.
- You run an online journal. You want everyone to read and comment on only one document, not on any others. Tokens could allow this.

[JWT workflow](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics#section-4.12)
- `POST/login` -> get access token + refresh token cookie.
- user `access_token` to call `GET /` API.
- On expiry, `POST /refresh` -> gets new tokens.
- Try reusing old refresh token -> get `403 Forbidden`.
