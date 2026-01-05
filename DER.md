Distinguished Encoding Rules Format

- DER is a binary encoding format and is the underlying structure that PEM wraps in Base64.


Conversion commands 

```bash
# Pem -> DER
openssl x509 -in cert.pem -outform der -out cert.der

# DER -> PEM
openssl x509 -inform der -in cert.der -out cert.pem
```

> [!NOTE]
> Use PEM when you need human-readable portable text files (most)