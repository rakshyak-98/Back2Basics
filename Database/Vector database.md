[[Database]] [[GIN]] [[OLTP]] [[Data access patterns]] [[SQL/postgres]] [[BASE]] [[ACID]]

# Vector database

> Storage and indexes built for approximate nearest-neighbor search over high-dimensional embeddings — complements, not replaces, the authoritative [[OLTP]] row store.





## Interview Relevance
Interviewers ask how RAG/search fits beside a system of record, ANN index trade-offs (HNSW vs IVF), and rebuild/consistency stories. Signal: vectors are a derived index; users and money stay in transactional tables.

## Sources
- Johnson, J., Douze, M., Jégou, H., "Billion-scale similarity search with GPUs" (FAISS) — deep-dive
- [pgvector](https://github.com/pgvector/pgvector) — deep-dive
- [Pinecone docs — vector database concepts](https://docs.pinecone.io/guides/get-started/concepts) — overview
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 2 (specialized indexes) — overview
- [Wikipedia — Nearest neighbor search](https://en.wikipedia.org/wiki/Nearest_neighbor_search) — overview

## Core Definition
A vector database (or vector index) stores embedding vectors and answers “top-k most similar to query vector **q**” by cosine, L2, or inner product — usually approximately, for speed at scale.

## Key Concepts
- **Embedding:** fixed-length float vector from a model (text, image, audio).
- **ANN (approximate nearest neighbor):** trade exactness for latency and recall targets.
- **HNSW:** graph-based ANN — fast queries, memory-heavy.
- **IVF / quantization:** inverted lists + coarse codes — scales with disk-friendly layouts.
- **Source of truth:** keep entities in PostgreSQL/MySQL; rebuild or sync vectors as derived data ([[BASE]]-friendly).

## Technical Details
Problem shape: given **q**, return top-k by similarity — semantic search, recommendations, RAG retrieval.

```txt
OLTP (users, docs, orders) ──► embed text ──► vector index
         │                           ▲
         │                      query embedding
         └── authoritative IDs / ACLs / money
```

| Index family | Strength | Cost |
|--------------|----------|------|
| **HNSW** | Low latency, high recall | RAM |
| **IVF + PQ** | Large corpora | Tuning nprobe / recall |
| **pgvector** | Same transaction boundary as SQL (small–medium) | Not a billion-scale specialist |

Operational notes:

- Filter by metadata (tenant, ACL) before or during ANN — security is not “nearest neighbor alone.”
- Version embeddings when models change; plan full reindex.
- Measure recall@k and p99 latency under realistic filters.

## Real-World Applications
Support bot: embed knowledge articles into pgvector or Qdrant; store article rows and permissions in PostgreSQL; retrieve top-k chunks then generate an answer. Product search: hybrid lexical + vector ranking with filters for in-stock SKUs from [[OLTP]].

## Pros/Cons or Trade-offs
- **Pro:** Semantic recall that keyword indexes miss; specialized ANN performance.
- **Con:** Approximate results; model drift; dual-write / sync complexity.
- **Trade-off:** In-engine (pgvector) simplicity vs dedicated vector service scale.

## Comparison
vs [[OLTP]]: transactional correctness and joins vs similarity search. vs [[GIN]] / full-text: inverted indexes for tokens; vectors for dense semantic space. vs [[OLAP]]: analytics aggregates history; vectors retrieve similar items — different question shape.

## Mistakes to Avoid
- Using the vector store as the only copy of user or payment data.
- Ignoring metadata filters — leaking other tenants’ nearest neighbors.
- Expecting exact k-NN at web scale without naming the recall trade-off.
- Changing embedding models without a reindex plan.
