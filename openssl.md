`/etc/ssl/certs/ca-certificates.crt`
### Generate certificate
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

### Generate self signed certificate
```bash
sudo mkdir -p /etc/nginx/certs;
sudo openssl req -x509 -nodes -days 365 \
	-newkey rsa:2048 \
	-keyout /etc/nginx/certs/shop.localhost.key \
	-out /etc/nginx/certs/shop.localhost.crt
```
- `Common Name (CN)` -> shop.localhost (important).
- others you can skip with Enter.

This gives you 
`/etc/nginx/certs/shop.localhost.crt` (certificate)
`/etc/nginx/certs/shop.localhost.key` (private key)