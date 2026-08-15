[[Etherium]] [[Descriptive]] [[Security]] [[ACID]]

# Blockchain properties (engineering lens)

> Distributed ledger guarantees for builders — immutability, consensus, and transparency trade off against latency, cost, and privacy; don't treat "on-chain" as magic persistence.

## Interview Relevance

Property questions check immutability, transparency, and what blockchain does not guarantee (correct business logic).

## Sources

- [MDN Web Docs](https://developer.mozilla.org/) — overview
- [Blockchain — Wikipedia](https://en.wikipedia.org/wiki/Blockchain) — overview

## Key Concepts

A blockchain is an **append-only, replicated log** where blocks link via cryptographic hashes. Network nodes agree on ordering through a **consensus** protocol (PoW, PoS, BFT variants).

```
Tx submitted ──► mempool ──► block proposed ──► consensus ──► finalized chain
                              │
                              └── hash links to parent block
```

Properties engineers care about:

| Property | Meaning | Production implication |
|----------|---------|------------------------|
| Immutability | Changing old blocks breaks hash chain | Can't "edit" records — only append corrections |
| Decentralization | No single writer | Slower finality; upgrade coordination hard |
| Transparency | Public chains: all data visible | No PII on-chain without encryption |
| Consensus | Agreement despite faults | CAP: partition behavior varies by chain |
| Finality | Irreversibility delay | Design for reorgs / pending state |
| Smart contracts | Deterministic code on-chain | Bugs are irreversible; audit + upgrade patterns |

## Technical Details

### Integration patterns (off-chain app + chain)

```
┌─────────────┐     RPC/WS      ┌──────────────┐
│  App / API  │ ◄──────────────►│  Node (geth) │
└─────────────┘                 └──────────────┘
       │                                 │
       │ store hashes only               │ full ledger
       ▼                                 ▼
   PostgreSQL                      Blockchain
```

- **Anchor hash on-chain, data off-chain** — store document hash in contract event; blob in S3/IPFS.
- **Wallet/signing** — user keys in HSM/browser wallet; server never holds user seed in production.
- **Idempotency** — tx nonce management; retry with same nonce versus replacement.

### Read contract (Ethereum JSON-RPC)

```js
// ethers.js v6
const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
const contract = new ethers.Contract(address, abi, provider);
const owner = await contract.owner();
const block = await provider.getBlockNumber();
```

### Write with explicit gas / finality wait

```js
const tx = await contract.setStatus(id, 1, { maxFeePerGas, maxPriorityFeePerGas });
const receipt = await tx.wait(2); // wait 2 confirmations — reorg buffer
if (receipt.status !== 1) throw new Error('reverted');
```

### Event indexing (don't scan chain in request path)

```js
contract.on('Transfer', (from, to, value, event) => {
  indexer.queue({ block: event.log.blockNumber, from, to, value: value.toString() });
});
// Production: The Graph, subsquid, or custom indexer + DB
```

### Config checklist

- RPC provider redundancy (primary + fallback).
- Chain ID in tx (`chainId`) — prevent cross-chain replay.
- Monitor reorg depth for your chain.
- Rate-limit public RPC; self-host node for SLA.

## Pros/Cons or Trade-offs

- **CRUD application with trusted operator** — PostgreSQL + audit log is simpler and cheaper.
- **Sub-second latency requirements** — chain finality is seconds to minutes.
- **GDPR right-to-erasure** — conflicts with immutability; keep PII off-chain.

## Mistakes to Avoid

> [!WARNING]
> **Public = world-readable** — emails, KYC, trade secrets don't belong on public L1.

> [!WARNING]
> **Immutability = no hotfix** — deploy proxy upgrade patterns (UUPS/transparent) or accept migration cost.

> [!WARNING]
> **Oracle problem** — on-chain code only sees what oracles feed; bad oracle = bad state.

> [!WARNING]
> **Gas costs spike** — batch operations; L2 rollups for user-facing frequency; don't put ML on-chain.

| Symptom | Check | Fix |
|---------|-------|-----|
| Tx pending forever | Gas too low; nonce gap | Bump fee (EIP-1559); fix nonce sequence |
| Tx succeeded then "undone" | Chain reorg | Wait more confirmations; idempotent handlers |
| Contract call reverts | `eth_call` simulate; decode revert | Fix require conditions; check allowance/balance |
| RPC intermittent | Provider rate limit | Self-host or paid tier; exponential backoff |
| Indexer drift | Missed events during downtime | Backfill from last synced block |
| Wrong network in wallet | `chainId` mismatch | Prompt switch network; validate in backend |
