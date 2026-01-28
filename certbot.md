```bash
certbot plugins
certbot certificates;
sudo apt install certbot python3-certbot-nginx
```

```bash
sudo certbot --nginx -d example.com -d www.example.com; # Get certificate + auto-configure nginx
sudo certbot --apache -d example.com -d www.example.com;
```

```bash
sudo certbot certonly --nginx -d example.com; # Get certificate only (no auto-config).
```

```bash
sudo certbot renew; # Renew all certificate
sudo certbot renew --dry-run;
```