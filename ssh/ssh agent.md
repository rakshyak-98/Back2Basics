[[ssh]]

# ssh agent

> ssh agent — background process that holds decrypted private keys in memory so you type the key passphrase once per login session.

---

## Mental model

**Say it in one breath:** You run `ssh-agent`, load keys with `ssh-add`, and every `ssh` connection reuses those decrypted keys until you log out or kill the agent.

`ssh-agent` stores private keys in memory after you unlock them with `ssh-add`. The keys stay encrypted on disk; only the agent process holds the decrypted material for outgoing SSH connections.

Define which key to use per host in `~/.ssh/config` (for example `IdentityFile ~/.ssh/id_ed25519_github` under `Host github.com`).

---

## Standard config / commands

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh-add -l
ssh-add -d ~/.ssh/id_ed25519    # remove one key
kill $SSH_AGENT_PID             # stop agent
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Could not open a connection to your authentication agent | Agent not running | Start `ssh-agent`; `eval` in shell |
| Permission denied still | Wrong key not loaded | `ssh-add -l`; add correct `IdentityFile` |
| Passphrase asked every time | Agent not started in login shell | Add agent start to shell profile or desktop keyring |
| Agent forwards in untrusted host | `ForwardAgent yes` | Disable agent forwarding except jump hosts you trust |

---

## Gotchas

> [!WARNING]
> Keys in the agent are **decrypted in memory** — lock screen when away from the machine.

---

## When NOT to use

- Do not run ssh-agent forwarding into untrusted servers.

---

## Related

[[ssh]]
