[[PHP-FPM]] [[php]] [[apache modules]] [[Nginx]]

# PHP errors

> Triage blank pages, 502s, and bind failures — separate “web server cannot listen,” “FPM socket mismatch,” and “PHP threw inside the worker.”





## Interview Relevance
Interviewers watch your first commands: `ss`, service status, socket path alignment, then logs — not random restarts.

## Sources
- [PHP — Error Handling](https://www.php.net/manual/en/book.errorfunc.php) — overview
- [Nginx docs](https://nginx.org/en/docs/) — overview

## Key Concepts
- **Port bind errors:** “no listening sockets” / address in use → Apache/Nginx conflict on 80/443.
- **502 Bad Gateway:** front door up, upstream FPM down or wrong socket.
- **500 from PHP:** worker ran; app/log has the exception (often with `display_errors=Off`).
- **CLI vs FPM:** different ini files → “works in CLI” is not proof.

## Technical Details
```bash
sudo ss -tlnp | grep -E ':80|:443'
sudo systemctl status apache2 nginx php*-fpm
sudo php-fpm8.2 -t
sudo tail -f /var/log/php8.2-fpm.log /var/log/nginx/error.log
```

Nginx and pool must agree:

```nginx
fastcgi_pass unix:/run/php/php8.2-fpm.sock;
```

```ini
listen = /run/php/php8.2-fpm.sock
```

| Symptom | Check | Fix |
|---------|-------|-----|
| No listening sockets | `ss`, competing service | Free 80/443; one front server |
| 502 | FPM status + socket | Restart FPM; align paths |
| Blank page | App/FPM log | Log errors; fix exception |
| Socket permission denied | owner/group/mode | Match `www-data` and Nginx user |

## Real-World Applications
After PHP upgrades, sockets rename (`php8.2` → `php8.3`) — update Nginx and reload both sides.

**Example:** Apache left enabled beside Nginx — bind failure on reboot; disable the unused service.

## Pros/Cons or Trade-offs
- **Pro:** Logs + socket model make failures localizable.
- **Con:** Multiple logs (Nginx, FPM, app) — look at the right one first.

## Comparison
- vs [[PHP-FPM]] tuning: errors note is triage; FPM note is pool design.
- vs Apache `mod_php`: fewer socket issues, worse isolation for modern apps.

## Mistakes to Avoid
- Restarting Nginx only when FPM is dead.
- Enabling `display_errors` on production to “debug.”
- Editing CLI `php.ini` and expecting the site to change.
