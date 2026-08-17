[[Descriptive]] [[web capabilities]] [[JWT authentication]] [[IDOR]] [[TLS (Transport Layer Security)]] [[marketplace application]]

# Ethereum (filename Etherium.md)

> Programmable blockchain: accounts hold state; transactions pay **gas** to mutate it — **Ethereum Yellow Paper** + **Mastering Ethereum** for SE integration context.

```txt
        Ethereum (filename ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Ethereum questions cover smart contracts, gas, and why chain data differs fro…

## Sources
- [MDN Web Docs](https://developer.mozilla.org/) — overview

## Key Concepts
```txt
┌─────────────┐     signed tx      ┌──────────────┐
│ EOA (wallet)│ ─────────────────► │ EVM block    │
│ or Contract │     + gas fee      │ state trie   │
└─────────────┘                    └──────────────┘
```

**Account types:**
- **EOA:** (externally owned): private key controls; nonce + ETH balance
- **Contract:** : code + storage; no private key; invoked by tx or other contracts

- **Note:** **Transaction:** nonce, gas limit, max fee / priority fee (EIP-1559), value, …

- **Note:** **Gas:** metered computation + storage

- **Note:** **Layers SEs touch:** RPC nodes (JSON-RPC), wallets (MetaMask, WalletConnect)…

## Technical Details
### JSON-RPC (read-only via node provider)

```bash
# Balance (wei)
curl -s $ETH_RPC -X POST -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getBalance","params":["0xADDR","latest"],"id":1}'

# Call contract (eth_call — no state change)
# eth_sendRawTransaction — signed tx broadcast
```

### ethers.js (app integration)

```javascript
import { JsonRpcProvider, Wallet, Contract, parseEther } from 'ethers';

const provider = new JsonRpcProvider(process.env.ETH_RPC);
const balance = await provider.getBalance('0x...');

const wallet = new Wallet(process.env.PRIVATE_KEY, provider);
const tx = await wallet.sendTransaction({
  to: '0x...',
  value: parseEther('0.01'),
});
await tx.wait(1); // 1 confirmation
```

### Gas estimation pattern

```javascript
const gas = await contract.method.estimateGas(args);
const fee = await provider.getFeeData();
const tx = await contract.method(args, {
  gasLimit: gas * 120n / 100n,  // 20% headroom
  maxFeePerGas: fee.maxFeePerGas,
  maxPriorityFeePerGas: fee.maxPriorityFeePerGas,
});
```

### Event indexing (backend)

```javascript
// Prefer indexer (The Graph, subsquid) over scanning all blocks in app
contract.on('Transfer', (from, to, value, event) => {
  // unreliable for prod — use confirmed logs + reorg handling
});
const logs = await contract.queryFilter(filter, fromBlock, toBlock);
```

### Units

```txt
1 ETH = 10¹⁸ wei
gwei = 10⁹ wei (fee display)
```

## Mistakes to Avoid
> [!WARNING]
> **Reorgs:** treat as final only after N confirmations; backend must unwind indexed state on reorg.

> [!WARNING]
> **Private keys in app servers** — hot wallet only; HSM/KMS/MPC for treasury; never log mnemonics.

> [!WARNING]
> **Integer money:** use bigint / decimal libs; JS `Number` loses wei precision.

> [!WARNING]
> **Approvals (ERC-20)** — users grant contract spend limit; audit infinite approve UX.

> [!WARNING]
> **L2 bridge latency** — "Ethereum" UX may be L2; withdrawals have challenge periods on rollups.

| Symptom | Check | Fix |
|---------|-------|-----|
| `insufficient funds for gas` | ETH balance on payer EOA | Fund hot wallet; gas tank pattern |
| Tx stuck pending | `eth_getTransactionByHash` | Bump fee (EIP-1559 replacement); nonce gap audit |
| `nonce too low` | Pending tx queue | Serialize signer; track nonce in DB |
| Revert with no message | Custom errors (Solidity 0.8.4+) | Simulate with `eth_call`; decode `error.data` |
| Wrong network (chainId) | `wallet_switchEthereumChain` | Enforce chainId in signed tx (EIP-1559) |
| Indexer behind chain tip | Block lag metric | Delay UI confirmation count; handle reorgs > 1 block |
| Rate limit on public RPC | 429 from provider | Paid node; self-hosted geth/erigon; batch requests |

## Pros/Cons or Trade-offs
- **Centralized ledger sufficient**
- **High-frequency micro-payments**
- **Private enterprise data on-chain**
