[[Concurrent modification]]

ETag/if-Match implements optimistic concurrency control, preventing lost updates when multiple clients read and modify the same resource concurrently.

ETag (response header)
Server returns a version identifier for the resource's current state

```txt
GET /channels/42
200 OK
ETag: "a1b2c3d4"
{ "id": 42, "name": "channel1", "bitrate": "6000k" }
```

The Etag is typically a has of the resource content, a version counter, or a last-modified timestamp encoded as an opaque string. It changes whenever the resource changes.

If-Match (request header)
Client sends back the ETag it last read when submitting an update, telling the server **"only apply this update if the resource is still in the state I last saw"**

```txt
PUT /channels/42
If-Match: "a1b2c3d4"
{ "id": 42, "name": "channel1", "bitrate": "8000k" }
```

**Server behavior**
- Current ETag matches `If-Match` -> apply update, return new resource + new ETag.
- Current ETag does not match (resource changed since client read it) -> reject with `412 Precondition Failed`. **Client must re-fetch and retry**.

## Implementation

Server side needs:
- A version field or content hash stored with the resource (e.g., a `version` integer column incremented on each write, or hash of serialized state).
- Compare `If-Match` header value against current stored version before applying any mutation, inside the same transaction as the write.