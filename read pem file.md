```shell
openssl x500 -in file.pem -text -noout; # certificate
openssl rsa -in file.pem -text -noout; # private key
openssl req -in file.pem -text -noout; # CSR
```
