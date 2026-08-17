[[Apache CLI]] [[INDEX]]

# apache CLI

> Apache HTTP Server CLI — modules, sites, and configtest.

---

## Apache CLI

From [[Apache CLI]].

```bash
sudo a2enmod rewrite ssl headers proxy proxy_http
sudo a2ensite myapp.conf
sudo apache2ctl configtest
sudo systemctl reload apache2

apache2ctl -M          # loaded modules
apache2ctl -S          # vhost map
```
