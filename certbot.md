```bash
sudo apt install python3-certbot-nginx; # if using Nginx
sudo apt install python3-certbot-apache; # if using apache 
```

Generate certificate
```bash
# Certbot only configure HTTPS, but you may be asked whether you want HTTP traffic redirected to HTTPS.
sudo certbot --nginx -d <domain name> -d <secondary domain name>;

# --redirect
sudo certbot --nginx --redirect -d <domain name> -d <secondary domain name>;
```

**"Explicitly request redirect"** means telling Certbot: Alter enabling HTTPS, automatically redirect anyone who visits the HTTP version of the website to the HTTPS version.