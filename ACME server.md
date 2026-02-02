- is the remote server (rub by a Certificate Authority) that Certbot talks to using the ACME protocol.

- Automated Certificate Management Environment
- it's a standardized protocol for automatically getting, renewing, and revoking TLS/SSL certificates.
- ACME client -> the software that asks for certificates.
- ACME server -> the server on the Certificate Authority side that answers those requests

It handles
- Domain ownership validation (via challenges like HTTP-01, DNS-01, TLS-ALPN-01)
- issuing the actual certificate
- Renewal checks
- Revocation (if needed)

## ACME server

|ACME Server|Operator|Free?|Production Trusted?|Default in Certbot?|Notes|
|---|---|---|---|---|---|
|Let's Encrypt production|ISRG / Let's Encrypt|Yes|Yes|Yes (default)|acme-v02.api.letsencrypt.org|
|Let's Encrypt staging|ISRG / Let's Encrypt|Yes|No (for testing)|--staging flag|staging environment to avoid rate limits|
|ZeroSSL|ZeroSSL|Yes (limited)|Yes|Possible via --server|Popular alternative|
|Google Trust Services|Google|Yes|Yes|Possible|Newer public CA|
|Your own private CA|step-ca, Smallstep, Boulder, etc.|Yes (self-hosted)|No (internal only)|--server flag|For internal use|