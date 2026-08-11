[[Database]] [[BASE]] [[OLAP]] [[OLTP]] [[WAL (Write-Ahead Log)]] [[Data access patterns]] [[GIN]]

# Vector database

> Store embedding vectors and find “nearest” neighbors fast — semantic search, RAG retrieval, recommendations — not row-by-id OLTP.

---

## Mental model

**Say it in one breath:** A vector DB indexes high-dimensional embeddings so approximate nearest-neighbor (ANN) search returns similar items in milliseconds; metadata filters narrow the candidate set.

```txt
Ingest                         Query
──────                         ─────
text/image ──► embedding model ──► vector + metadata
                      │
                      ▼
              durable store + ANN index (HNSW / IVF / DiskANN…)
                      │
query text ──► same model ──► k-NN / range search (+ filters)
```

Many systems separate **write path** (append segments / WAL) from **read path** (immutable index segments). Replication often ships raw data and rebuilds ANN indexes locally (index build is expensive and non-deterministic).

Postgres can do this in-process with **pgvector**; dedicated stores (Milvus, Qdrant, Pinecone, Weaviate, …) optimize ANN + filter + scale-out.

## Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Embedding** | Dense float vector for meaning | “Same model at write and query or neighbors are nonsense.” |
| **ANN** | Approximate nearest neighbor | “We trade a little recall for huge speed vs brute force.” |
| **HNSW** | Graph-based ANN index | “Great recall/latency; RAM-heavy.” |
| **IVF** | Cluster/coarse quantize then search lists | “Tune `nprobe`; cheaper memory, more knob care.” |
| **Metric** | Distance (cosine, L2, IP) | “Metric must match how the model was trained.” |
| **Recall@k** | Fraction of true top-k you return | “Primary quality metric for the index, not just QPS.” |
| **Hybrid search** | Vector + keyword/metadata | “Filter then ANN, or fuse BM25 + vector scores.” |

---

## Standard config / patterns

### Postgres + pgvector (good default for modest scale)

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE chunks (
  id        BIGSERIAL PRIMARY KEY,
  doc_id    BIGINT NOT NULL,
  content   TEXT NOT NULL,
  embedding vector(1536) NOT NULL,
  meta      JSONB
);

-- Cosine distance ops — pick opclass to match metric
CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);

SET hnsw.ef_search = 40;

SELECT id, content, 1 - (embedding <=> $1) AS score
FROM chunks
WHERE meta @> '{"lang":"en"}'
ORDER BY embedding <=> $1
LIMIT 10;
```

### Dedicated vector store checklist

```txt
1. One embedding model + dimension per collection (no silent mix)
2. Distance metric locked to model (cosine vs L2)
3. Metadata indexes for filters (tenant_id, acl, type)
4. Measure Recall@k on a labeled set before tuning QPS
5. Backups include vectors + index rebuild procedure
```

| Knob | Why it matters |
|------|----------------|
| Dimension | Must match model; wrong dim = insert/query failure |
| `ef_search` / `nprobe` | Higher = better recall, more CPU/latency |
| Filter selectivity | Ultra-selective filters can destroy ANN plans |
| Segment compaction | Write amplification vs query freshness |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| “Similar” results look random | Model mismatch; metric mismatch; unnormalized cosine | Same model+version; fix metric; normalize if required |
| High latency after data growth | Index type / `ef_search`; RAM | Raise resources; retune; shard by tenant |
| Good ANN, wrong tenants | Missing filter / ACL in query | Mandatory `tenant_id` predicate; test isolation |
| Insert OK, search empty/stale | Async index build / uncommitted segment | Wait for index ready; check build lag metrics |
| Recall drops after reindex | Different build params | Pin `m`/`ef_construction`; regression test Recall@k |
| Disk/RAM blow-up | HNSW graphs; replicas rebuilding | Cap replicas building at once; consider IVF/DiskANN |

---

## Gotchas

> [!WARNING]
> **Different embedding models are different spaces** — you cannot query ada-002 vectors with a voyage/openai-v3 vector and expect meaning.

> [!WARNING]
> **ANN is approximate** — default knobs can miss true neighbors. Always track Recall@k in staging when you change index settings.

- **Filter-then-search versus search-then-filter** — wrong order tanks recall or scans too much.
- **Re-embedding on model upgrade** — treat as a migration; dual-write or blue/green collections.
- **Not a replacement for [[OLTP]]** — still need a system of record for money, inventory, strong FKs ([[ACID]]).
- **JSONB filters** in PG may want [[GIN]] beside the vector index.

---

## When NOT to use

- **Exact key/value or relational CRUD** — Postgres/MySQL without vectors.
- **Keyword-only search at small scale** — Postgres FTS / Elasticsearch may be enough.
- **Tiny corpora** — brute-force `ORDER BY distance LIMIT k` can beat ANN overhead.

## Related

[[Database]] [[BASE]] [[OLAP]] [[OLTP]] [[Data access patterns]] [[GIN]] [[WAL (Write-Ahead Log)]] [[ACID]] [[Database design]]
