[[apache]]

# apache configurations

> apache configurations — if you are using something else like /var/www/myproject/public, make sure it's set correctly.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** apache configurations — plain job, how I run it, how I know it’s broken.


```bash
sudo a2enmod rewrite;
sudo systemctl restart apache2;
```
```bash
cat /etc/apache2/envvars; # see here for apache group and user.
export APACHE_RUN_USER=www-data
export APACHE_RUN_GROUP=www-data
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **apache configurations** | Core idea of this note | “I can explain apache configurations without jargon.” |
| **mental model** | How it works in one line | “Explain it without jargon first.” |
| **failure mode** | How it breaks | “Say what you check first.” |

---

## Standard config / commands

```bash
# reproduce with minimal input
# compare working vs broken env
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Unexpected result | inputs / versions | Reproduce minimal case |
| Works on one machine | env drift | Diff config and versions |
| Silent failure | logs / metrics | Add checks and alerts |

---

## Gotchas

> [!WARNING]
> Prefer simple words you can say in an interview.

---

## When NOT to use

- Skip it when a simpler existing tool already fits.

---

## Related

[[apache]]
