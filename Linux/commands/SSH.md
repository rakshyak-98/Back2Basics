Server policy (`/etc/ssh/sshd_config`): [[sshd config]]

```shell
ssh -F <config file> -G <Host>; # print final resolved configurations for that host
ssh user@host; # connect to remote host using default key
ssh -p 2222 user@host; # connect with specific port
ssh-copy-id user@host; # copy public key to a remote server
```

```shell
nc -zv host 22; # check ssh port availability
ssh -T user@host;
```

## Remote port forwarding

```bash

# Make local port 3000 accessible on remote port 8080
ssh -R 8080:localhost:3000 user@root;

```

### Debug wrong key/user/port

```bash
ssh -F <config file> -G <host>;
```
- verify which `IdentityFile` is used
- check config inheritance (Host*, wildcard)

### List Current ssh connections

```bash
who; # show who is logged on.
```

### How `ssh-keyscan` fetches SSH host keys
`ssh-kyscan` works by initiating a raw ssh handshake with the remote server just long enough to capture its public host key, then disconnects.
- TCP connect to server on port 22 (or customer with -p).
- Sends SSH protocol version exchange.
- Receives server's public host key's RSA, ED25519.
- Prints key's in OpenSSH `known_hosts` format.

> [!NOTE] Does not authenticate or complete full SSH logins

> [!INFO] You must manually verify the fingerprint from a trusted source before trusting.

#### Why `ssh-keyscan` alone is not secure?
- it trusts whatever host responds on the IP/hostname and port.
- if a attacker is spoofing the server [[MITM]], `ssh-keyscan` will still show their key.
- So, if you blindly save that key (to `known_hosts`) you've now trusting a potentially fake server.
[github official fingerprint](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints)

### Validate ssh key

```sh
ssh-keyscan github.com | tee tmp_key;
ssh-keygen -lf <public key>; # print fingerprint + bits.
ssh-keygen -yf <private key>; # prints public key if valid.

ssh-keygen -i <private key> -v user@host; # verify connectivity.

```
[]()
- verify the fingerprint manually before trusting.

```sh
ssh-keygen -F github.com
```
- this tells you the line number of GitHub's key from `~/.ssh/known_hosts`.
- find all the entries of for a host.

### Why this works

- SSH servers must send their public key early in handshake (to prove identity).
- that key is not secret - it's how clients verify they're talking to the correct server.
- `ssh-keyscan` captures just that.

### Difference between `ssh-keyscan` and `ssh-keygen`

- `ssh-keyscan` fetch a remote server's host key. You want to get a host's key without connecting fully.
- `ssh-keygen` inspect/verify key fingerprint. You want to view fingerprint of local key file (your own SSH keys) or a `known_hosts` entry.

# Understanding the SSH encryption and  Connection process

[post link](https://www.digitalocean.com/community/tutorials/understanding-the-ssh-encryption-and-connection-process)

- ssh key pairs begins after the symmetric encryption has been established.
- client-server model to authenticate two parties and encrypt the data.
- the client is responsible for beginning the initial [[TCP]] handshake with the server.
- ssh connection is established in two separate stages
	- first is to agree upon and establish encryption to protect future communication.
	- second to authenticate the user and discover whether access to the server should be granted.
- server provides its public host key, which the client can use to check whether this was the intended host.
	- both parties negotiate a session key using a version of the [Diffie-Hellman algorithm](), combining their own private data with public data from the other system to arrive at an identical secret session key.
	- session key will be used to encrypt the entire session.
	- public and private key pairs used for this part of the procedure are completely separate from the SSH keys used to authenticate a client to the server.

## Understand Symmetric Encryption, Asymmetric Encryption and Hashes

- **Symmetric** — same key to encrypt and decrypt ([[symmetric encryption]]).
- **Asymmetric** — key pair; used mainly to prove identity, not to encrypt the whole session ([[Asymmetric Encryption]]).
- The server picks the first cipher both sides support.
- SSH uses asymmetric crypto first to agree on a symmetric session key (Diffie-Hellman + temporary key pairs).

### SSH key pairs

- Client creates a key pair and puts the **public** key on the server.
- After the session is encrypted, the client must still **authenticate**.
- Server sends a challenge encrypted with the client's public key.
- Client decrypts with its private key to prove it owns the key.
- Server then opens the user's shell environment.

## Hashing

- SSH uses [[Cryptographic hashing]] for integrity checks.
- Each packet after encryption includes a **MAC** (Message Authentication Code).
- MAC = hash of (shared secret + sequence number + message body).
- MAC sits outside the encrypted payload, at the end of the packet.
- Encrypt first, then compute the MAC.
