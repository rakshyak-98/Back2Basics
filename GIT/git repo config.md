```shell
gpg --full-generate-key; # generate gpg key
gpg --list-secret-keys --keyid-format=long;
gpg --armor --export <your email>; # export your public key
```

```shell
git config --get commit.gpgsign;
git log --show-signature;
```
#### Configure git to use GPG key
```shell
git config user.signingkey <gpg key>;
git config commit.gpgsign true; # enable auto-sign
git config tag.gpgsign; # enable auto sign for tags
```

```shell
git commit -S -m <commit message>; # if auto-sign is not eanble
```

#### SSH
```shell
git conifg gpg.format ssh;
git config user.signingkey <path to ssh .pub file>;
```
