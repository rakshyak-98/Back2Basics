[[apache]]

# apache configurations

> apache configurations — if you are using something else like /var/www/myproject/public, make sure it's set correctly.

---

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

## Related

[[apache]]
