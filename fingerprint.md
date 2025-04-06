a fingerprint is a short, unique hash of a server's public SSH key.
- used to identify and verify a server's key.
- easier to check than the full key.
- protects against man-in-the-middle [[MITM]] attacks

> [!INFO] default hash `MD5`  
> - you can change to `SHA256`

```sh
ssh-keygen -l -f ssh_host_ed25519_key.pub;

ssh-keygen -E sha256 -l -f <pubkey>; # change default hash to SHA256
```