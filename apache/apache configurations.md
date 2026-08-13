[[apache]]

# apache configurations

> apache configurations — if you are using something else like /var/www/myproject/public, make sure it's set correctly.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** apache configurations — if you are using something else like /var/www/myproject/public, make sure it's set correctly.

```bash
sudo a2enmod rewrite;
sudo systemctl restart apache2;
```
```bash
cat /etc/apache2/envvars; # see here for apache group and user.
export APACHE_RUN_USER=www-data
export APACHE_RUN_GROUP=www-data
```


---

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[apache]]
