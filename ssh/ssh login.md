```bash
ssh user@server.example.com
```
1. TCP Connection -> Your client connects to the server on port 22.
2. Protocol Negotiation -> They agree on which encryption/authentication algorithm to use.
3. Key Exchange -> They establish a shared secret for encrypting everything.
4. Server Authentication -> You verify you're talking to the real server.
5. Client Authentication -> The server verifies you are who you say you are.
6. Secure Session Established -> Encrypted communication tunnel is read.

**Generate Key Pair (Private + Public)**
```bash
ssh-keygen -t ed25519 -C "you@example.com"
```
- private keys stays with you, the server needs to know who it should trust so, you copy your public key `~/.ssh/authorized_key` of your account on the server.

> [!INFO]
- Now, the server knows: "If someone claims to be Alice, I'll challenge them using this specific public key. If they can prove ownership of the private key, I'll let them in."

**You can approximate this process on the command line without SSH itself**
```bash
# Generate keys (RSA)
openssl genpkey -algorithm RSA -out private.pem -pkeyopt rsa_keygen_bits:2048;
openssl rsa -in private.pem -pubout -out public.pem;
```

```bash
# Create a challenge message
echo "IAmARandomSring123456" > challenge.txt;
```

```bash
# Sign the challenge with your private key
openssl dgst -sha256 -sign private.pem -out signature.bin challenge.txt;
```

```bash
# Verify with the public key
openssl dgst -sha256 -verify public.pem signature.bin challenge.txt;
```

> [!INFO]
> - Only someone with the private key can produce a valid signature
> - Anyone with the public key can check_signature, but they can't forge them.
> - The server never needs to see or store your private key.
> - Replay attacks are foiled because each challenge is random and temporary.
