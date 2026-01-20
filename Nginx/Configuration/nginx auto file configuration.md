	## Requirements for the creating and setup nginx config files, template build files

- Change Ownership of `/var/www/html` (for static files)
- If deploying built sites:
 
```bash
sudo chown -R your-pm2-user:your-pm2-user /var/www/html
sudo chmod -R 755 /var/www/html
```

- For Nginx Configs: Use sudo with Passwordless Commands

- Edit /etc/sudoers (with visudo):

```text
ubuntu ALL=(root) NOPASSWD: /usr/sbin/nginx -t
ubuntu ALL=(root) NOPASSWD: /bin/systemctl reload nginx
ubuntu ALL=(root) NOPASSWD: /bin/cp /tmp/nginx-hotel-example.com.conf /etc/nginx/sites-available/hotel-example.com
ubuntu ALL=(root) NOPASSWD: /bin/ln -sf /etc/nginx/sites-available/hotel-example.com /etc/nginx/sites-enabled/
```
> [!WARNING]
> - In Node.js, use child_process.exec with sudo for only those steps.
> - Temp write config to /tmp first, then sudo copy/symlink/reload.

debug

```bash
sudo -l
```
