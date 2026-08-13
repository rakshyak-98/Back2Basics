[[ssh]]

# SSH authentication

> SSH authentication — decrypting the signed challenge with the public key.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** SSH authentication — decrypting the signed challenge with the public key.

#### The verification process involves:
- **Decrypting** the signed challenge with the public key.
- Checking if the result matches the original challenge sent by the server.
- If the signature matches, it proves the client has the corresponding private key
### How Key Authentication Works in SSH (Verification of Signature by Server)
SSH key-based authentication is built on **public-key cryptography**, which allows for secure, passwordless authentication. The core idea is that the client proves its identity to the server by signing a challenge with its private key, and the server verifies the signature using the client's public key.
Here’s how the **key authentication process** works step-by-step:

## Standard config / commands

```bash
ssh -v user@host                 # verbose auth debug
ssh-keygen -lf ~/.ssh/id_ed25519.pub
cat ~/.ssh/authorized_keys
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Publickey denied | Key not in authorized_keys | Match `.pub` fingerprint on server |
| Wrong signature algorithm | Old server; new key type | Use ed25519 or rsa-sha2; check server `PubkeyAcceptedAlgorithms` |
| Keyboard-interactive loop | PAM or 2FA module | Complete second factor; check server logs |
| Certificate expired | SSH certificate auth | Re-sign host/user cert with CA |

---

## Gotchas

> [!WARNING]
> Server chooses allowed methods — client cannot force publickey if the server disables it.

---

## When NOT to use

- Do not share private keys between users or machines.


---

## Related

[[ssh]]
