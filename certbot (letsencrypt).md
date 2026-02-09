
- Default config and log files path
- Main debug log: `/var/log/letsencrypt/letsencrypt.log`
- Global level conf: `/etc/letsencrypt/cli.ini`
- User level conf `~/.config/letsencrypt/cli.ini`

> [!NOTE]
> You cannot get a public trusted certificate (from Let's Encrypt ACME server).
> - use `staging` environment

```bash
sudo certbot certonly \
  --staging \
  --standalone \
  -d testhotel1.example.com \
  -d testhotel5.example.com \
  --email your@email.com \
  --agree-tos \
  --non-interactive   # optional, if you want to skip prompts
```
- `--standalone` -> Certbot starts its own temporary web server on port 80 (make sure nothing else is using 80).

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

## Renew certificate

```bash
sudo certbot renew; # Renew all certificate
sudo certbot renew --dry-run;
```

```bash
sudo certbot renew --deploy-hook "systemctl reload nginx";
sudo certbot renew --quiet; # For cron
```

## Webroot

- `certbot` needs to prove to let's Encrypt that you really control the domain you're requesting a certificate for.

The `--webroot` plugin is the mechanism that tells `certbot`:
> “Please write those challenge files into this folder on disk → my already-running web server (Apache, Nginx, Caddy, lighttpd, IIS, etc.) will automatically serve them at the correct URL.”
- You specify the folder with `-w` / `--webroot-path`

```bash
sudo certbot certonly \
	--webroot \
  -w /var/www/html          # ← DocumentRoot or public folder
  -d example.com -d www.example.com
```

## HTTP-01 Challenge

- HTTP-01 is the most common ACME challenge for domain validation in Certbot. It proves you control a domain by serving a specific token file (your domain name `-d` and port 80)