[[mysql]] [[mysql Privileges]] [[mysql connection]] [[mysql ssl connection]]

# mysql user

> MySQL accounts are `user`@`host` pairs with an auth plugin and grants — apply least privilege for apps and humans.

```txt
        mysql user ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Expect create-user + grant examples, plugin differences (`caching_sha2_passwo…

## Sources
- [CREATE USER](https://dev.mysql.com/doc/refman/en/create-user.html) — deep-dive
- [Account Management](https://dev.mysql.com/doc/refman/en/account-management.html) — overview

## Key Concepts
- **Identity = user + host:** Same username, different hosts, different accounts.
- **Auth plugins:** `caching_sha2_password` (MySQL 8 default), legacy `mysql_native_password`.
- **Grants:** Separate from identity — see [[mysql Privileges]].
- **TLS requirements:** Can be part of the account definition ([[mysql ssl connection]]).

## Technical Details
```sql
CREATE USER 'app'@'10.%' IDENTIFIED BY 'strong-password' REQUIRE SSL;
GRANT SELECT, INSERT, UPDATE, DELETE ON myapp.* TO 'app'@'10.%';

SELECT user, host, plugin FROM mysql.user;
SHOW GRANTS FOR 'app'@'10.%';
```

## Mistakes to Avoid
- **Mistake:** Application connections as `root`@`%`
- **Mistake:** Wildcard hosts with powerful grants on the public internet
- **Mistake:** Leaving unused accounts enabled after offboarding

## Pros/Cons or Trade-offs
- **Pro:** Host scoping limits stolen-password usefulness off-network.
- **Con:** Many `user`@`host` variants clutter audits if unmanaged.
- **Trade-off:** Shared app user vs per-service users (blast radius vs operational overhead).

## Comparison
- vs [[psql user]]: PostgreSQL roles unify users/groups


### Use cases
- Per-environment app users restricted to VPC CIDRs
