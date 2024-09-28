- is one of the agreed-upon methods a [[web server]] can use to negotiate credentials, such as username and password, with a user's [[web browser]].
- used to confirm identity of a user before sending sensitive information, such as online banking transaction history.

### How it works
- It applies a [[hash function]] to the username and password before sending them over the network.

> [!INFO] basic access authentication uses the easily reversible [[Base64]] encoding instead of hashing, making it non-secure unless in conjunction with [[TLS]]

also read
[digest access authentication](https://en.wikipedia.org/wiki/Digest_access_authentication)
