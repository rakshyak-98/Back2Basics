Fast Common Gateway Interface -> binary protocol that improves upon the original CGI by providing a high-performance, language-agnostic way for web servers to interface with external applications for generating dynamic content.
- Process that handles dynamic content generation (like php, python etc.) and communicates with web servers (like Nginx) via the FastCGI protocol.

> [!NOTE]
> FastCGI runs the application as [[persistent processes]] (often called workers or daemons) separate from the web server. These processes stay alive and handle multiple requests over time.
> The web server communicates with the fastCGI application via a persistent connection (usually TCP socket or Unix domain socket), using a binary protocol for efficiency.

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

## Step-by step how FastCGI works

1. Startup -> the FastCGI application processes are started separetly (manually or via a manager). They listen on a socket
2. Client Request -> Browser sends HTTP request to the web server (e.g., Nginx, Apache).
3. Web Server Forwards Request -> the server recognizes the request needs dynamic processing (based on file extension, location, etc.) and sends it to the FastCGI backend via the persistent connection.
4. Protocol Communication -> data is sent in [[records]] (binary packets) that include
	1. Request Id (to multiple requests over one connection).
	2. Parameters (like environment variables in CGI).
	3. Stdin (POST data)
	4. The application processes the request and sends back stdout (response body) and headers.
5. Role Management -> FastCGI supports roles like **Responder** (most common, for generating responses). **Authorizer** (for authentication,) and **Filter** (for modifying input/output).
6. Response -> The web server receives the output, adds any necessary headers if needed, and sends it back to the client.
7. Reuse -> The FastCGI process remains running, ready for the next request (possibly from a different client).

> [!INFO]
> - While FastCGI is still widely used (especially for PHP), newer alternatives like [[uwsgi]]  [[scgi]] or embedded runtimes (mod_php, Node.js or containerized apps) exists. However PHP-FPM remains dominant for PHP on high performance setups like Nginx.