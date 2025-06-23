### Verify gpg key
```bash
# 1. Extract the fingure print
gpg --no-default-keyring --keyring /usr/share/keyrings/nginx.gpg --fingerprint; 

# 2. Download official key for comparision
curl -fsSL https://repo.com/gpg_signing.key | gpg --with-fingerprint;

```

#### Compare the binary hash
```bash
gpg --no-default-keyring --keyring /usr/share/keyrings/nginx.gpg --export > localkey.gpg
curl -fsSL https://nginx.org/keys/nginx_signing.key -o officialkey.gpg
gpg --dearmor officialkey.gpg
diff -s localkey.gpg officialkey.gpg.gpg
```

```bash
# [ configure key ]
gpgconf --list-dir
gpg --refresh-keys

# [ list keys ]
gpg --list-keys # pulic keys
gpg --list-secret-keys # private keys
gpg --list-secret-keys --keyid-format=long

# [ export keys ]
gpg --export-secret-keys -a KEY_ID > my_private_key.asc; # -a ASCII-armored
gpg --export -a KEY_ID > my_public_key.asc
# -o stdout to location
gpg --export -o public.asc <user ID>
gpg --export-secret-keys -o private.asc <user ID>

# [ edit key ]
gpg --edit-key; # init intrective terminal

# [ verification ]
gpg --verify "signature file"; # verify signature
gpg --detach-sign "file.txt"; # create a detach sign to verify.
gpg --check-trustdb
gpg --firgerprint <key id>;
```

### Generate new keys
```sh
# [ generate new keys ]
gpg --gen-key # asymmetric
gpg --gen-random 32
gpg --import "file"; # import gpg public key from a file.
```

### Encryption
```bash
# [ encryption ]
gpg --sign -u user@example.com mydocument.txt
gpg -e binary_publickey file.asc
gpg --encrypt plain.txt
gpg --encrypt --recipient recipient_name --output "enc.gpg" "file"

# -c symmetric
# -e asymetric
gpg --armor -c -o encrypted.asc "youfile.txt"
gpg --armor -e -o encrypted.asc -r "recipient" "yourfile.txt."

# [ decryption ]
gpg -da binary_publickey.asc
gpg --decrypt plain.gpg
```

```bash
# [ sign ]
gpg --clear-sign "file.txt"; # create new file with clear redable format

# sign with armor representation
gpg --armor -s -o signed.asc "yourfile.txt"
```
- GNU Privacy Guard, used for encryption and digital signature operations.

ASCII-armor : feature to type of encryption called Pretty Good Privacy (PGP). and `.asc` file extension.

`--armore` represents an ASCII-armored representation of data.

```bash

# encrypt file using the public key save as ASCII-armored format.
gpg --armor \\
--output encrypted.txt.asc \\
--encrypt --recipient "username" plaintext.txt;
```

GPG - GNU Privacy Guard, tool is a native security tool for encrypting files. It is a tool to provide digital encryption and signing services using the OpenPGP standard.

openpgp standard - is the most widely used email encryption standard. It is defined by the OpenPGP working group of the Internet Engineering Task Force (IETF)

- is describes the format and methods needed to read, check, generate, and write, conforming encrypted messages, keys, and signatures.

### armor (ASCII-armored-format)
- process of encoding binary data, such as cryptographic keys or messages, into a human-readable text format. 
- This text format is designed to be easily exchanged and shared in contexts where binary data might not be appropriate (e.g.,emails, forums).

## Dearmor Dearmor (or *dearmor*) 
- process of decoding ASCII-armored data back into its *original binary format*. 
- This is done when you want to use the original binary data for cryptographic operations or other purposes.

recipient : specifies the recipient public key or email address
- refers to the individual or entity for whom you are encrypting a message or a file.
- to ensure intended recipient can decrypt and read the content.

### remove all trace of gpg keys

```bash
gpg --delete-secret-keys "key_id"
gpg --delete-keys "key_id"

rm -rf ~/.gnupg/ # gpg stores your keys in files in directory
```

> [!INFO]
>  After your key pair is generated, you may want to create a revocation certificate. the owner of a cryptographic key pair to declare that their public key should no longer be used for encryption, decryption, or digital signatures. Essentially, it revokes the validity of the associated public key.

```bash
gpg --gen-revoke <ID>
```

### edit key

```bash
gpg --edit-key; # init intrective terminal
```

management operations. Some common commands include:

- `adduid`: Add a new user ID to the key.
- `revuid`: Revoke a user ID.
- `expire`: Change the expiration date of the key.
- `revkey`: Revoke the entire key.
- `trust`: Change the trust level assigned to the key.
- `uid`: Select a specific user ID for editing.
- `check`: Check the key for consistency and correctness.

