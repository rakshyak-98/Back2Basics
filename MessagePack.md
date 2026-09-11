Binary serialisation format used to convert structured data objects, arrays, string, numbers, booleans into a compact sequence of bytes so it can be stored or transmitted efficiently.

```txt
Application data
      ↓
 MessagePack encoder
      ↓
    bytes
      ↓
      Network / Disk
      ↓
 MessagePack decoder
      ↓
Application data
```

```json
{
	"id": 42,
	"name": "Alice",
	"active": true
}
```
JSON represents this as text
```txt
{"id":42,"name":"Alice","active":true}
```
MessagePack stores the same logical structure as **binary bytes**
```binary
83 A2 69 64 2A A4 6E 61 6D 65 A5 41 6C 69 63 65 A6 61 63 74 69 76 65 C3
```
- MessagePack is not actually an encoding of JSON. JSON and MessagePack are two different serialisation formats that can represent similar data.

MessagePack represents the same information as **binary bytes**.

> MessagePack is a binary serialisation format for JSON-like structured data. Often described as binary-JSON

**"MessagePack is a compact binary serialisation format designed to represent structured data similar to JSON, but in binary form.**

"In particular, since they don't prescribe a schema, they need to include all the object field names within the encoded data."