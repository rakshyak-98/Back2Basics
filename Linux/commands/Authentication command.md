## ssh
```bash
ssh-keyscan <hostname>;
ssh-keyscan -p <port> <hostname>; # if SSH is running on a non-default port
ssh-add -l
ssh-keygen -R remote-host; # remove a host key
ssh-keyscan remote-host >> ~/.ssh/known_hosts; # manually add a host key
```
- you can add the output to your `known_hosts file
### Verify SSH keys
```bash
ssh-copy-id user@remote-host;
ssh -v <hostname>; # verify ssh key
```
- add your public key to the remote host's `~/.ssh/authorized_keys` file
### How does SSH uses `known_hosts`?
- used by SSH client to verify the identity of the remote host.
- it stores the public host keys of previously connected servers to prevent **man-in-the-middle-attacks**.
```bash
ssh user@remote-host; # Found no entry for the host
# you receive a prompt
# the server public host key is added to your known_hosts file.
```
- On subsequent connections, SSH client check the remote host's key against the entry in `known_hosts`.

> [!INFO] SSH uses the public key from the `known_hosts` file to ensure the server's authenticity.

each line in `known_hosts` contains
```text
hostname algorithm public-key
```

## gnupg

```sh
sudo apt install gnupg;
```

```sh
gpg --full-gen-key; # generate new set of keys
gpg --list-secrets-key --keyid-format=long;

gpg --armor --export <key id>; # export public key
gpg --armor --export-secret-keys <key id>; # export private key
```

### gnupg git config
```sh
git config --global user.signingkey <key>;
git config --global commit.gpgsign true;
```

```sh
git commit -S -m 'signed commit';
git log --show-signature;
```