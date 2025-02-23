```shell
gpg --full-generate-key; # generate gpg key
gpg --list-secret-keys --keyid-format=long;
gpg --armor --export <your email>; # export your public key
```

#### Configure git to use GPG key
```shell
git config user.signingkey <gpg key>;
git config commit.gpgsign true;
```
