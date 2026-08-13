[[Networking]] [[P2P (Peer-to-Peer)]]

# IPFS (InterPlanetary File System)

> IPFS finds files by content hash (CID), not by server URL — peers share blocks like a P2P CDN.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** You ask for a CID; the network finds whoever has those blocks and streams them to you.

```txt
File → chunk → hash each block → root CID
                │
                ├─ store / pin on nodes
                └─ retrieve by CID (DHT + peers)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **CID** (content ID) | Hash naming the bytes | “Same content → same CID; change bytes → new CID.” |
| **Content addressing** | Locate by hash, not hostname | “URL is where; CID is what.” |
| **Pin** | Keep blocks from GC | “Unpinned data can vanish when nodes leave.” |
| **Gateway** | HTTP front to IPFS | “Browsers hit `ipfs.io/ipfs/<CID>` without a local node.” |
| **DHT** | Map CID → providers | “Lookup finds who has the blocks.” |

### How a fetch works (4 steps)

1. **Split** — file becomes blocks; each gets a hash.
2. **Name** — root CID identifies the whole DAG.
3. **Find** — DHT / peer discovery → nodes that have the blocks.
4. **Get** — pull blocks from nearest peers; verify hashes.

---

## Standard config / commands

```bash
# Install / start a local node (Kubo)
ipfs init
ipfs daemon

# Add and pin
ipfs add ./report.pdf          # prints CID
ipfs pin add <CID>

# Fetch
ipfs cat <CID> > report.pdf
ipfs get <CID>

# Via public gateway (no local daemon)
curl -L "https://ipfs.io/ipfs/<CID>" -o report.pdf
```

| Knob | Why it matters |
|------|----------------|
| Pin / remote pin | Persistence — free peers are not a backup |
| Gateway vs local | Gateways are convenient; you trust their availability |
| Private swarm | Don’t put secrets on public IPFS without encryption |
| Garbage collection | Unpinned blocks disappear under disk pressure |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `ipfs cat` hangs | No providers / daemon down | `ipfs daemon`; pin on a durable node or pinning service |
| Gateway 404 / timeout | Content never pinned / GC’d | Re-add + pin; don’t rely on one upload |
| Wrong file for CID | You mutated then re-used old CID | New bytes ⇒ new CID — update links |
| Slow first fetch | Cold DHT / far peers | Warm cache; use a closer gateway or co-located pin |
| Can’t reach private data | Published on public network | Encrypt payload; or private IPFS / permissioned store |

---

## Gotchas

> [!WARNING]
> **Upload ≠ forever** — without a pin (yours or a service), content can disappear.

> [!WARNING]
> **CID is integrity, not secrecy** — anyone with the CID can fetch public data.

> [!WARNING]
> **Gateway trust** — HTTP gateways can lie or go down; verify CID when it matters.

---

## When NOT to use

- **Mutable “latest” APIs** — use object storage + CDN, or IPNS carefully; raw CIDs are immutable.
- **Low-latency interactive apps** — DHT lookup is not a Redis round-trip.
- **Compliance / delete-on-request** — global copies are hard to erase; prefer controlled storage.

---

## Related

[[Networking]] [[P2P (Peer-to-Peer)]] [[Data transfer communication channels]]
