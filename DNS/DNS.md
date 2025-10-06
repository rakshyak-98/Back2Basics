- DNS run on UDP, the client sends a single request message and the server respond with a single response message.
- A DNS message is encapsulated in a UDP packet.
- DNS can also use [[TCP]], for large queries or responses that exceed the maximum size allowed by UDP.

## DNS subdomain name

### Root server
- first step in resolving human-readable host names into IP address.
- answers other requests by returning a list of authoritative name servers for appropriate top-level domains.
- there are 13 sets of root servers distributed worldwide. Labeled with a letter from A to M.
- operated by different organizations.
- DNS is broken into different zones.
- a 2-byte length field is prepend to each DNS message so that the server or client can tell which part of the byte stream is which message.