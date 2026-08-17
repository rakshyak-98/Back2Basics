[[SSH authentication]] [[ssh allow local system with key]] [[sshd config]] [[ssh agent]] [[ssh private network]]

# ssh login

> An SSH login is a TCP session to port 22 that negotiates crypto, verifies the host, authenticates you (usually with a key), then opens an encrypted shell or command channel.





## Interview Relevance
Interviewers walk the handshake steps and triage `Permission denied (publickey)` versus connection refused versus “too many authentication failures.”

## Sources
- [RFC 4253 — SSH Transport Layer Protocol](https://datatracker.ietf.org/doc/html/rfc4253) — deep-dive
- [RFC 4252 — SSH Authentication Protocol](https://datatracker.ietf.org/doc/html/rfc4252) — overview
- [OpenSSH — ssh](https://man.openbsd.org/ssh) — overview

## Recall Cues
- Why do interviewers care about Interviewers walk the handshake steps and triage `Permission denied (publickey)` versus connection refused versus “too many authentication failures.”?
- What is step 1: TCP connection to port 22?
- What is step 2: Protocol negotiation — algorithms?
- What is step 3: Key exchange — shared secret for the session?
- What is step 4: Server authentication — verify host key?
- What is step 6: Secure session — encrypted shell/command channel?
- What mistake is **Enabling password authentication on internet-facing servers when keys work**?
- What mistake is **Ignoring host-key change warnings**?

## Technical Details
```bash
ssh user@server.example.com
ssh-keygen -t ed25519 -C "you@example.com"
# private key stays local; public key → ~/.ssh/authorized_keys on server
```

1. TCP connection to port 22.
2. Protocol negotiation — algorithms.
3. Key exchange — shared secret for the session.
4. Server authentication — verify host key.
5. Client authentication — password or [[SSH authentication]] publickey.
6. Secure session — encrypted shell/command channel.

```bash
ssh user@host
ssh -i ~/.ssh/id_ed25519 user@host
ssh -p 2222 user@host
ssh -J jump@bastion user@internal
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Connection refused | sshd down; wrong port | `ss -tlnp \| grep 22`; check firewall |
| Permission denied (publickey) | Key not on server | Install public key in `~/.ssh/authorized_keys` |
| Too many authentication failures | Client offers too many keys | `IdentitiesOnly yes` in `~/.ssh/config` |
| Hangs after banner | DNS reverse lookup delay | Server `UseDNS no` |

## Mistakes to Avoid
- Enabling password authentication on internet-facing servers when keys work.
- Ignoring host-key change warnings.
- Offering dozens of keys until the server hits `MaxAuthTries`.

## Comparison
- vs VPN-only access: SSH can be the jump; VPN can replace public SSH exposure.
- vs serial/console: console saves you when sshd config locks you out.

## Real-World Applications
Interactive admin shells, `ProxyJump` into private networks ([[ssh private network]]), and non-interactive deploy commands.

**Example:** `ssh -J jump@bastion user@internal` logs into an RFC1918 host without exposing port 22 publicly.

## Pros/Cons or Trade-offs
- **Pro:** Encrypted, authenticated remote access with mature tooling.
- **Con:** Internet-facing password auth is a constant attack surface — prefer keys.
- **Con:** Mis-managed known_hosts / host-key changes cause scary but correct warnings.
