A `FastCGI server` is a long-running process that handles dynamic content generation (lik php, python etc.) and communicates with web servers (like Nginx) via the FastCGI protocol.

> [!INFO]
> - web servers like Nginx cannot interpret PHP directly. So, they forward requests to a FastCGI server (like PHP-FPM).

### **How it works:**
1. **Nginx** receives a `.php` request.
2. It **forwards** it to `php-fpm` via FastCGI.
3. `php-fpm` **executes PHP**, returns result to Nginx.
4. Nginx **returns** the final response to the client.