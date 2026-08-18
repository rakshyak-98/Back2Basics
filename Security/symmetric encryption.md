[[symmetric encryption]] [[SSH]]

# Symmetric encryption

> Same key encrypts and decrypts. Also called a **shared secret** or **secret key**.

## Mental model

- One key for both sides.
- Both parties must end up with the same key without sending the secret in plain text.
- A **key exchange** (e.g. Diffie-Hellman) uses public + private values so each side computes the same key independently.

## Where it is used

- **SSH** encrypts the whole session with a symmetric key after setup.
- Password auth still runs inside that encrypted channel.
- Bulk data (files, TLS traffic) uses symmetric crypto because it is fast.

## Related

[[Asymmetric Encryption]] · [[SSH]] · [[TLS (Transport Layer Security)]]
