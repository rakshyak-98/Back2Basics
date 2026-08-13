[[Descriptive]] [[blockchain property]] [[Etherium]]

# Blockchain

> A blockchain is a linked, append-only ledger of blocks — useful when many parties need a shared history without one admin DB.

---

## How it works

```txt
tx → mempool → block(n) hashes block(n-1) → network consensus
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Block** | Batch of txs + header | “Links via parent hash.” |
| **Consensus** | Who may append | “PoW/PoS/permissioned.” |
| **Finality** | When tx is settled | “Probabilistic vs hard finality.” |
| **Smart contract** | On-chain program | “Ethereum VM example.” |

---


## Configuration and commands

```bash
# ethereum sketch
cast block latest
cast tx <hash>
```

| Knob | Why it matters |
|------|----------------|
| Fee / gas | Inclusion priority |
| Confirmations | Reorg risk |
| Chain id | Replay protection |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Tx stuck | gas / nonce | Bump fee; fix nonce |
| Wrong network | chain id / RPC | Point wallet to right chain |
| Reorged tx | shallow confirmations | Wait deeper finality |
| Contract revert | traces | Read error; fix calldata |

---


## Gotchas

> [!WARNING]
> **Immutable mistakes** — bad contract deploys are forever (unless upgrade pattern).

> [!WARNING]
> **Blockchain ≠ free database** — cost, latency, and privacy differ from Postgres.

---


## When not to use

- **Ordinary CRUD apps** — a database is enough.
- **Needs delete/GDPR erase of history** — poor fit for public ledgers.


## Related

[[blockchain property]] [[Etherium]] [[symmetrical encryption]]

## Sources

- [Wikipedia — Blockchain](https://en.wikipedia.org/wiki/Blockchain)
