[[Database]] [[Vector database]]

# GridFS

> MongoDB specification for storing files larger than the 16 MB BSON document limit by chunking binary data across `fs.files` and `fs.chunks` collections.

## Structure

```txt
fs.files   — metadata (filename, length, uploadDate, contentType)
fs.chunks  — binary segments (default 255 KB) keyed by files_id + n
```

## When to use

- Large blobs inside MongoDB when object storage (S3, GCS) is not available
- Streaming reads/writes without loading entire file into memory

## When not to use

- General-purpose CDN assets — use object storage + CDN
- Relational reporting on file metadata — model metadata in SQL, bytes in object store

## Sources

- MongoDB Documentation — [GridFS](https://www.mongodb.com/docs/manual/core/gridfs/)
