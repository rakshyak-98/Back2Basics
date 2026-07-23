[[MongoDB]] [[Database]] [[WiredTiger storage engine]]

# GridFS

> One-line: MongoDB's convention for storing files >16MB BSON limit — chunks in `fs.files` + `fs.chunks`; stream in/out; not a general filesystem.

## Mental model

BSON documents cap at **16MB**. GridFS splits a file into **255KB chunks** (default), storing metadata in `fs.files` and binary chunks in `fs.chunks` (default bucket prefix `fs`).

```
Upload stream ──► fs.files (metadata: filename, length, uploadDate)
              └──► fs.chunks { files_id, n, data } × N
```

Drivers expose `openUploadStream` / `openDownloadStream`. GridFS is **not** POSIX — no directories, permissions, or random seek performance like local disk. Use for user uploads, video, backups inside Mongo when you already run it.

## Standard config / commands

### Node.js upload

```javascript
import { MongoClient, GridFSBucket } from 'mongodb';

const bucket = new GridFSBucket(db, { bucketName: 'uploads' });

const uploadStream = bucket.openUploadStream('report.pdf', {
  metadata: { userId: '123', contentType: 'application/pdf' },
});

fs.createReadStream('./report.pdf').pipe(uploadStream);
uploadStream.on('finish', () => console.log(uploadStream.id));
```

### Download

```javascript
const downloadStream = bucket.openDownloadStreamByName('report.pdf');
downloadStream.pipe(res); // Express response
```

### Find metadata

```javascript
const cursor = bucket.find({ 'metadata.userId': '123' });
```

### Delete

```javascript
await bucket.delete(fileId); // removes chunks + file doc
```

### Custom bucket / chunk size

```javascript
new GridFSBucket(db, {
  bucketName: 'media',
  chunkSizeBytes: 1024 * 1024, // 1MB chunks — fewer docs, larger RAM per read
});
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Slow listing | Missing index on `filename` | Index `fs.files.filename`; query by `_id` when possible |
| Orphan chunks after failed upload | Partial upload | Abort stream; delete incomplete file doc; periodic cleanup job |
| 16MB error still | Not using GridFS | Any single **document** field still limited — only file payload is chunked |
| Replica lag on large upload | Many chunk inserts | Increase chunk size; upload off-peak; use S3 for huge media |
| MD5 mismatch (legacy) | Corruption / partial read | Re-upload; verify `length` vs aggregated chunk sizes |
| Memory spike on download | Buffer entire file | Always stream; never `readFile` whole GridFS object |

## Gotchas

> [!WARNING]
> **GridFS ≠ S3** — expensive at TB scale; object storage + CDN is cheaper for static media.

> [!WARNING]
> **No transactions across bucket + collection updates** without multi-doc transaction (replica set required).

> [!WARNING]
> **Renaming** — update `filename` in `fs.files` only; chunks keyed by `_id`.

## When NOT to use

- **Small blobs (< few MB)** — embed `BinData` in document or store URL to S3.
- **Full-text search on binary** — extract text sidecar collection.
- **Need POSIX semantics** — use object storage or NFS.

## Related

[[MongoDB]] [[WiredTiger storage engine]] [[Stream]] [[Database]]
