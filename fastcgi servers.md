- Process that handles dynamic content generation (like php, python etc.) and communicates with web servers (like Nginx) via the FastCGI protocol.


> [!INFO]
> - web servers like Nginx cannot interpret PHP directly. So, they forward requests to a FastCGI server (like PHP-FPM).

### **How it works:**
1. **Nginx** receives a `.php` request.
2. It **forwards** it to `php-fpm` via FastCGI.
3. `php-fpm` **executes PHP**, returns result to Nginx.
4. Nginx **returns** the final response to the client.

```nginx
location ~ \.php$ {
    include fastcgi_params;
    fastcgi_pass unix:/run/php/php7.4-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
}

```