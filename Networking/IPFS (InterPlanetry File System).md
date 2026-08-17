[[Networking]] [[P2P (Peer-to-Peer)]] [[Data transfer communication channels]]

# IPFS (InterPlanetary File System)

> IPFS finds files by content hash (CID), not by server URL — peers share blocks like a P2P CDN.

```txt
        IPFS (InterPlaneta ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers contrast **content addressing** (CID) with location addressing (…

## Sources
- [IPFS Docs — Concepts](https://docs.ipfs.tech/concepts/) — deep-dive
- [IPFS Docs — Content Identifiers (CID)](https://docs.ipfs.tech/concepts/content-addressing/) — deep-dive
- [Wikipedia — InterPlanetary File System](https://en.wikipedia.org/wiki/InterPlanetary_File_System) — overview

## Key Concepts
- **Core:** IPFS (InterPlanetary File System) is a peer-to-peer content-addressed storage…

## Technical Details
```txt
File → chunk → hash each block → root CID
                │
                ├─ store / pin on nodes
                └─ retrieve by CID (DHT + peers)
```

- How a fetch works:

1. **Split** — file becomes blocks; each gets a hash.
2. **Name** — root CID identifies the whole DAG.
3. **Find** — DHT / peer discovery → nodes that have the blocks.
4. **Get** — pull blocks from nearest peers; verify hashes.

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

| Symptom | Check | Fix |
|---------|-------|-----|
| `ipfs cat` hangs | No providers / daemon down | `ipfs daemon`; pin on a durable node or pinning service |
| Gateway 404 / timeout | Content never pinned / GC’d | Re-add + pin; don’t rely on one upload |
| Wrong file for CID | You mutated then re-used old CID | New bytes ⇒ new CID — update links |
| Slow first fetch | Cold DHT / far peers | Warm cache; use a closer gateway or co-located pin |
| Can’t reach private data | Published on public network | Encrypt payload; or private IPFS / permissioned store |

## Mistakes to Avoid
- **Mistake:** Assuming upload equals durable storage
- **Mistake:** Treating CID as secrecy
- **Mistake:** Trusting HTTP gateways blindly
- **Mistake:** Using raw CIDs for “latest” mutable APIs
- **Mistake:** Expecting easy delete-on-request compliance once data is widely …

## Pros/Cons or Trade-offs
- **Pro:** Integrity by construction — hash mismatch means wrong or corrupted data.
- **Con:** Availability needs pins — upload alone is not forever.
- **Con:** DHT lookup and peer fetch can be slow vs object storage + CDN.

## Comparison
- vs HTTP URL / S3: location addressing (host + path); IPFS addresses content (CID).
- vs [[P2P (Peer-to-Peer)]] CDNs: IPFS is content-addressed block sharing
- vs IPNS: CIDs are immutable; IPNS adds mutable pointers carefully on top.


### Use cases
- Decentralized websites, NFT metadata, and mirror archives publish immutable b…

- **Example:** A team uploads a whitepaper once, pins it on a pinning service, …
