```bash
sudo a2enmod rewrite;
```
- enables the Apache module named `mod_rewrite`.
- `mod_rewrite` is a built-in Apache module that allows rewriting requested URLs on the fly.
- it commonly used to convert clean URLs like `/blog/post-title` into actual internal file paths like `index.php?post=post-title`.
- it was likely disabled by default on your system, which is common for Apache installs.

> [!INFO]
> Internally this command add a symbolic like for `rewrite.load` from `/etc/apache2/mods-available` into `/etc/apache2/mods-enabled/`. This tells Apache to load the `rewrite_module` at runtime.

> [!WARNING]
>  Without both steps, rewrite rules in `.htaccess` would not work and URLs like `/login` or `/user/123` would return `Not Found` unless the file physically existed.
