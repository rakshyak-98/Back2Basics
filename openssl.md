```shell
openssl genpkey -algorithm RSA -out privatekey.pem -aes256; # generate private key
openssl rsa -in privatekey.pem -pubout -out public.key 
	
openssl req -key privatekey.pem -new -out request.csr; # create CSR
openssl x509 -req -days 365 -in request.csr -signkey private.key -out certificate.crt; # self signed certificate
```

```shell
openssl req -in request.csr -text -noout;
openssl x509 -in certificate.crt -text -noout;
```

```shell
openssl x509 -in certificate.cert -notout -subject;
openssl x509 -in certificate.cert -noout -issuer;
openssl x509 -in certificate.crt -noout -fingerprint;
```

```shell
openssl verify -CAfile ca_bunle.crt certificate.crt;
```