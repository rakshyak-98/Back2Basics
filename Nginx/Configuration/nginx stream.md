[[Nginx]] [[Configuration]] [[nginx using unix socket]]

# Nginx Stream (L4 TCP/UDP Proxy)

> One-line: `stream {}` module proxies raw TCP/UDP — use for databases, MQTT, TLS passthrough, or non-HTTP protocols; separate from `http {}`.

## Mental model

The **stream** context operates at OSI layer 4. Nginx does not parse HTTP headers — it forwards bytes between client and upstream. Two common patterns:

```
Client ──TCP──► Nginx:5432 ──TCP──► PostgreSQL:5432   (TCP proxy)
Client ──TLS──► Nginx:443  ──plain──► backend:8080     (TLS passthrough / SNI routing)
```

`ngx_stream_js_module` adds JavaScript hooks for stream-layer logic (SNI inspection, routing) — optional, not in default OSS build.

---

## Standard config / commands

### TCP proxy (PostgreSQL example)

```nginx
# /etc/nginx/nginx.conf — top level, sibling to http {}
stream {
    upstream postgres {
        server 10.0.1.10:5432;
        server 10.0.1.11:5432 backup;
    }

    server {
        listen 5432;
        proxy_pass postgres;
        proxy_connect_timeout 5s;
        proxy_timeout 300s;
    }
}
```

### TLS passthrough (SNI-based routing)

```nginx
stream {
    map $ssl_preread_server_name $backend {
        api.example.com   backend_api;
        db.example.com    backend_db;
        default           backend_default;
    }

    upstream backend_api  { server 127.0.0.1:8443; }
    upstream backend_db   { server 127.0.0.1:5432; }
    upstream backend_default { server 127.0.0.1:8080; }

    server {
        listen 443;
        ssl_preread on;
        proxy_pass $backend;
    }
}
```

Requires `stream` module compiled in (`nginx -V 2>&1 | grep stream`).

### UDP (DNS forwarder sketch)

```nginx
stream {
    server {
        listen 53 udp;
        proxy_pass 8.8.8.8:53;
        proxy_timeout 5s;
    }
}
```

```bash
sudo nginx -t && sudo systemctl reload nginx
ss -tlnp | grep nginx    # TCP listeners
ss -ulnp | grep nginx    # UDP listeners
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Connection refused on stream port | `ss -tlnp \| grep :PORT`; `nginx -T \| grep -A5 stream` | Enable stream block; fix listen address; SELinux `http_port_t` won't apply — check `stream_connect` |
| TLS passthrough routes wrong backend | `openssl s_client -connect host:443 -servername api.example.com` | Fix `$ssl_preread_server_name` map; client must send SNI |
| Idle disconnects | `proxy_timeout` too low | Raise for long-lived connections (DB, WebSocket over stream) |
| Works in HTTP block, not stream | Wrong context | `stream {}` is **not** inside `http {}` |

---

## Gotchas

> [!WARNING]
> **No HTTP directives in stream:** `proxy_set_header`, `limit_req`, `try_files` — all invalid. Layer-4 only.

> [!WARNING]
> **Health checks:** OSS stream has passive upstream only (`max_fails`). No HTTP `/health` probe — use external checker or nginx-plus.

> [!WARNING]
> **Logging:** Default access log format is binary-ish; enable `stream` access_log with custom format for debugging.

---

## When NOT to use

- **HTTP reverse proxy** — use `http {}` + `proxy_pass`; stream loses header-based routing (except SNI preread).
- **Application-aware load balancing** — use HAProxy, Envoy, or cloud LB for rich L7 policies.

---

## Related

[[Configuration]] [[nginx using unix socket]] [[Nginx internals]]
