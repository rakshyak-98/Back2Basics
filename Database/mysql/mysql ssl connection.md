[[mysql connection]] [[mysql]] [[Configuration]]

# mysql ssl connection

> Encrypting the MySQL wire protocol with TLS—protects credentials and data in transit; required for many cloud-managed instances.

## Client connect

```bash
mysql -h rds.example.com -u app -p --ssl-mode=VERIFY_IDENTITY \
  --ssl-ca=/etc/ssl/certs/rds-ca.pem
```

## Modes (`ssl-mode`)

| Mode | Behavior |
|------|----------|
| `DISABLED` | Plaintext |
| `PREFERRED` | TLS if server supports (default in some clients) |
| `REQUIRED` | TLS mandatory |
| `VERIFY_IDENTITY` | TLS + hostname verification |

## Server side

Require SSL per user:

```sql
ALTER USER 'app'@'%' REQUIRE SSL;
```

## Sources

- MySQL Reference Manual — [Using Encrypted Connections](https://dev.mysql.com/doc/refman/en/using-encrypted-connections.html)
- MySQL Reference Manual — [CREATE USER SSL Options](https://dev.mysql.com/doc/refman/en/create-user.html)
