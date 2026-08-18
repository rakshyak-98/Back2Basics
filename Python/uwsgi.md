[[Python]]

# User web server gateway interface

> User web server gateway interface — uWSGI acts as a bridge between your web application and the web server (like Nginx or Apache). It takes care of…

## Mental model

**Say it in one breath:** User web server gateway interface — uWSGI acts as a bridge between your web application and the web server (like Nginx or Apache). It takes care of…

```bash
uwsgi --ini uwsgi.ini
```
uWSGI acts as a bridge between your web application and the web server (like Nginx or Apache). It takes care of communication, request handling, and process management.
- You configure uWSGI using a configuration file (often named `uwsgi.ini`). This file contains settings like the application entry point, the number of worker processes, and more.
- uWSGI operates using a master-worker model. The master process manages the worker processes that actually handle incoming requests. Each worker is essentially an instance of your application.

## Related

[[Python]]
