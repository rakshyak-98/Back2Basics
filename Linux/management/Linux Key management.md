
# generate private key

```bash
openssl genpkey -algorithm RSA -out private_key.pem -aes256 # with pass phrase

openssl genpkey -algorithm RSA -out private_key.pem # without pass phrase

openssl ecparam -name secp256k1 -genkey -noout -out private_key.pem
```

## Generate CSR

```bash
openssl req -new -newkey rsa:2048 -nodes -keyout private.pem -out .csr

```

## verify certificate

```bash
openssl verify -CAfile /path/to/your/chain.crt /home/rakshyak/build/csr.crt

openssl req -text -noout -verify -in <csr.crt>;

openssl rsa -in <private.key> -check; # to check made with rsa algo.

openssl req -inform DER -in csr.der -out csr.pem -outform pem;

opemssl rsa -in private.der -out private.pem -outform pem;
```

SHA256 key fingerprints or SHA256 hash, or checksum are used to verify the authenticity and integrity of cryptographic keys.

- ref
[https://www.freecodecamp.org/news/the-ultimate-guide-to-ssh-setting-up-ssh-keys/](https://www.freecodecamp.org/news/the-ultimate-guide-to-ssh-setting-up-ssh-keys/)

[https://www.youtube.com/watch?v=33dEcCKGBO4](https://www.youtube.com/watch?v=33dEcCKGBO4)


you need different ssh key to pull from different git repository.

```bash
ssh-keygen -t rsa -b 4096 -C 'comment'; # generate public and private key. 
ssh-add id_rsa;
ssh-keygen -lf <filename>; # get the fingureprint of the key private/public.
```
t - type of algorithm
b - bits size
C - comment

> [!NOTE] fixed-length string of characters, typically represented in hexadecimal format.
