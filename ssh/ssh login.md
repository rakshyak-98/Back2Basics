[[ssh]]

# Verify with the public key

> Verify with the public key — TCP Connection — Your client connects to the server on port 22.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Verify with the public key — TCP Connection — Your client connects to the server on port 22.

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

## Standard config / commands

```bash
ssh user@host
ssh -i ~/.ssh/id_ed25519 user@host
ssh -p 2222 user@host
ssh -J jump@bastion user@internal
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Connection refused | sshd down; wrong port | `ss -tlnp | grep 22`; check firewall |
| Permission denied (publickey) | Key not on server | Install public key in `~/.ssh/authorized_keys` |
| Too many authentication failures | Client offers too many keys | `IdentitiesOnly yes` in `~/.ssh/config` |
| Hangs after password | DNS reverse lookup delay | Server `UseDNS no` (administrator setting) |

---

## Gotchas

> [!WARNING]
> SSH authenticates **the client key to the server** — username must exist on the server OS.

---

## When NOT to use

- Do not enable password authentication on internet-facing servers if key-based login is available.


---

## Related

[[ssh]]
