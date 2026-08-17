[[SSH authentication]] [[ssh login]] [[ssh allow local system with key]] [[sshd config]]

# ssh agent

> `ssh-agent` holds decrypted private keys in memory so you type the key passphrase once per session instead of on every SSH connection.

```txt
        ssh agent ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask how the agent relates to encrypted-at-rest keys, `IdentityFi…

## Sources
- [OpenSSH — ssh-agent](https://man.openbsd.org/ssh-agent) — deep-dive
- [OpenSSH — ssh-add](https://man.openbsd.org/ssh-add) — overview

## Key Concepts
- **Passphrase once:** keys stay encrypted on disk; agent holds unlocked material in memory.
- **Per-host identity:** `~/.ssh/config` `IdentityFile` selects which key to offer.
- **Forwarding risk:** `ForwardAgent yes` lets a compromised jump host use your keys.
- **Lifecycle:** start agent → `ssh-add` → list/remove → kill when done.

## Technical Details
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh-add -l
ssh-add -d ~/.ssh/id_ed25519    # remove one key
kill $SSH_AGENT_PID             # stop agent
```

- Define which key to use per host in `~/.ssh/config` (for example `IdentityFil…

| Symptom | Check | Fix |
|---------|-------|-----|
| Could not open a connection to your authentication agent | Agent not running | Start `ssh-agent`; `eval` in shell |
| Permission denied still | Wrong key not loaded | `ssh-add -l`; add correct `IdentityFile` |
| Passphrase asked every time | Agent not started in login shell | Add agent start to shell profile or desktop keyring |
| Agent forwards in untrusted host | `ForwardAgent yes` | Disable except jump hosts you trust |

## Mistakes to Avoid
- **Mistake:** Enabling agent forwarding into untrusted servers
- **Mistake:** Assuming the agent replaces correct `authorized_keys` setup on t…
- **Mistake:** Leaving unnecessary keys loaded in shared/CI environments

## Pros/Cons or Trade-offs
- **Pro:** Usable strong passphrases without constant prompts.
- **Con:** Decrypted keys sit in memory — lock the screen when away.
- **Con:** Forwarding expands the trust boundary to every hop.

## Comparison
- vs typing passphrase each time: agent is better UX; hardware keys (FIDO/sk) raise the bar further.
- vs pageant/keychain: same job on other platforms — still do not forward blindly.


### Use cases
- Daily developer SSH to many hosts, GitHub/GitLab key unlock once per day, and…

- **Example:** Unlock `id_ed25519` once with `ssh-add`
