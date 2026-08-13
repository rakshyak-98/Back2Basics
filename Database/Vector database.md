[[Database]] [[GIN]] [[OLTP]] [[Data access patterns]]

# Vector database

> Storage and indexes optimized for approximate nearest-neighbor search over high-dimensional embeddings—complements, not replaces, authoritative [[OLTP]] row stores.

## Problem shape

Given a query embedding vector **q**, find top-k vectors similar by cosine distance or L2—used in semantic search, recommendations, and RAG pipelines.

## Architecture pattern

```txt
OLTP (users, orders) ──► embed text ──► vector index (Pinecone, pgvector, Qdrant)
                              ▲
                         query embedding
```

Keep **source of truth** in PostgreSQL/MySQL; treat vectors as a derived index that can be rebuilt.

## Index families

- **HNSW** — graph-based ANN; fast queries, memory-heavy
- **IVF** — inverted lists with coarse quantization
- **pgvector** — extension inside PostgreSQL for smaller scale

## Sources

- Johnson, J., Douze, M., Jégou, H., "Billion-scale similarity search with GPUs" (FAISS)
- PostgreSQL pgvector — [https://github.com/pgvector/pgvector](https://github.com/pgvector/pgvector)
- Kleppmann, *DDIA*, Ch. 2 (specialized indexes)
