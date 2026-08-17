[[Database]] [[Vector database]]

# GridFS

> MongoDB specification for storing files larger than the 16 MB BSON document limit by chunking binary data across `fs.files` and `fs.chunks` collections.





## Interview Relevance
GridFS tests whether you know BSON size limits and when object storage beats putting blobs in the database. Interviewers want chunk metadata layout and a clear “use S3/GCS instead” decision.

## Sources
- [MongoDB Documentation — GridFS](https://www.mongodb.com/docs/manual/core/gridfs/) — deep-dive

## Key Concepts
- **16 MB BSON limit:** single documents cannot hold large files → GridFS chunks them.
- **Two collections:** `fs.files` metadata + `fs.chunks` binary segments (default 255 KB).
- **Streaming I/O:** read/write without loading the whole file into memory.

## Technical Details
```txt
fs.files   — metadata (filename, length, uploadDate, contentType)
fs.chunks  — binary segments (default 255 KB) keyed by files_id + n
```

When to use:

- Large blobs inside MongoDB when object storage (S3, GCS) is not available
- Streaming reads/writes without loading entire file into memory

When not to use:

- General-purpose CDN assets — use object storage + CDN
- Relational reporting on file metadata — model metadata in SQL, bytes in object store

## Real-World Applications
Legacy Mongo-centric apps storing user uploads without an object store. Example: a medical imaging prototype streams DICOM blobs via GridFS until the team migrates bytes to S3 and keeps only metadata in MongoDB.

## Pros/Cons or Trade-offs
- **Pro:** Stays inside MongoDB operationally; supports streaming large files past the BSON limit.
- **Con:** Worse CDN story, backup size, and operational cost than object storage for most product assets.

## Comparison
vs object storage (S3/GCS): object stores are the default for CDN-facing blobs; GridFS is a MongoDB-native fallback. vs [[Vector database]]: unrelated—vectors store embeddings for similarity; GridFS stores opaque file bytes.

## Mistakes to Avoid
- Using GridFS as a general CDN origin for static assets.
- Loading entire multi-GB files into application memory instead of streaming chunks.
- Expecting relational join/reporting ergonomics over chunk collections without a metadata model.
