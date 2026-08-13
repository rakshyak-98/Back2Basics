[[apache]]

# apache configurations

> apache configurations — if you are using something else like /var/www/myproject/public, make sure it's set correctly.

---

## How it works

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


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |


## Gotchas

> [!WARNING]
> …


## Related

[[apache]]

## Sources

- [Wikipedia — apache configurations](https://en.wikipedia.org/wiki/apache_configurations)
