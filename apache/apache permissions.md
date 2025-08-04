```bash
sudo a2enmod rewrite;

sudo systemctl restart apache2;
```

```bash
cat /etc/apache2/envvars; # see here for apache group and user.

export APACHE_RUN_USER=www-data
export APACHE_RUN_GROUP=www-data
```

> [!NOTE] 
> change the user and group of the files so `apache2` can access those files. Otherwise you will get permission error.
```bash
sudo chown -R www-data:www-data /path/to/folder
sudo chmod -R 755 /path/to/folder

sudo chown -R www-data:www-data /var/lib/php/sessions
sudo chown -R www-data:www-data /var/www/html/your-project-folder

```

> [!NOTE]
> Check your Apache config file `/etc/apache2/sites-enabled/000-default.conf`
```txt
DocumentRoot /var/www/html
```
- if you are using something else like `/var/www/myproject/public`, make sure it's set correctly.

> [!NOTE]
> missing `.htaccess` or Rewrite Rules
> - if you are using `Codelgniter`  `Laravel` or another framework, a missing `.htaccess` can cause routes to break. 
