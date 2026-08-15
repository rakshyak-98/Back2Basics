[[Configuration]] [[nginx using unix socket]] [[Nginx internals]] [[TCP]] [[UDP]]

# Nginx Stream (L4 TCP/UDP Proxy)

> Layer-4 proxy in the `stream {}` context — forward bytes (TCP/UDP), optional TLS passthrough via SNI preread; no HTTP header parsing.

## Interview Relevance

Distinguishes L7 `http {}` reverse proxy from L4 stream proxying — when to TCP-proxy Postgres, SNI-route TLS, or refuse HTTP-only features in stream.

## Sources

- [nginx.org — ngx_stream_core_module](https://nginx.org/en/docs/stream/ngx_stream_core_module.html) — deep-dive
- [nginx.org — ngx_stream_ssl_preread_module](https://nginx.org/en/docs/stream/ngx_stream_ssl_preread_module.html) — deep-dive
- [nginx.org — TCP and UDP Load Balancing](https://docs.nginx.com/nginx/admin-guide/load-balancer/tcp-udp-load-balancer/) — overview

## Core Definition

The Nginx stream module proxies TCP and UDP at OSI layer 4: it does not interpret HTTP; it forwards connections (and optionally peeks at TLS SNI) to upstreams.

## Key Concepts

- **`stream {}` sibling of `http {}`:** Not nested inside `http`.
- **TCP/UDP proxy:** Database, custom TCP protocols, DNS-like UDP forwarders.
- **TLS passthrough:** `ssl_preread` + `map $ssl_preread_server_name` without terminating TLS.
- **Passive health only (OSS):** `max_fails` — no HTTP `/health` active checks in open-source stream.

## Technical Details

```
Client ──TCP──► Nginx:5432 ──TCP──► PostgreSQL:5432   (TCP proxy)
Client ──TLS──► Nginx:443  ──plain──► backend:8080     (TLS passthrough / SNI routing)
```

`ngx_stream_js_module` adds JS hooks for stream logic (optional; not default OSS).

### TCP proxy (PostgreSQL)

```nginx
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

### TLS passthrough (SNI routing)

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

Requires stream compiled in (`nginx -V 2>&1 | grep stream`).

### UDP sketch

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
ss -tlnp | grep nginx
ss -ulnp | grep nginx
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Connection refused on stream port | `ss`; `nginx -T` stream block | Enable stream; fix listen; SELinux stream connect |
| TLS routes wrong backend | `openssl s_client … -servername` | Fix SNI map; client must send SNI |
| Idle disconnects | `proxy_timeout` too low | Raise for long-lived DB/WS-over-stream |
| Works in HTTP, not stream | Wrong context | `stream {}` is not inside `http {}` |

## Real-World Applications

TCP proxy Postgres through a bastion Nginx; SNI-based multiplexing of several TLS services on :443 without decrypting.

## Pros/Cons or Trade-offs

- **Pro:** Simple, fast L4 fan-in without HTTP overhead.
- **Con:** No `proxy_set_header`, `limit_req`, or `try_files` — L7 features stay in `http {}`.
- **Con:** Rich L7 policies may need HAProxy, Envoy, or a cloud LB instead.

## Comparison

- vs `http { proxy_pass }`: use HTTP block for header-based routing; stream for raw TCP/UDP.
- vs [[nginx using unix socket]]: unix sockets are a local upstream transport; stream is the L4 server context.

## Mistakes to Avoid

- Putting HTTP directives inside `stream {}`.
- Expecting active HTTP health checks from OSS stream.
- Forgetting custom stream access_log formats when debugging opaque byte proxies.
