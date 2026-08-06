[[Python]]

# User web server gateway interface

> One-line: what / why for **User web server gateway interface** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

```bash
uwsgi --ini uwsgi.ini
```
uWSGI acts as a bridge between your web application and the web server (like Nginx or Apache). It takes care of communication, request handling, and process management.
- You configure uWSGI using a configuration file (often named `uwsgi.ini`). This file contains settings like the application entry point, the number of worker processes, and more.
- uWSGI operates using a master-worker model. The master process manages the worker processes that actually handle incoming requests. Each worker is essentially an instance of your application.

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
