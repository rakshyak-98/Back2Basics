[[runtime]] [[interpreter]] [[linker]] [[assembly language]]

# Runtime Environment

> The libraries, VM, and OS services present when your binary runs on a target machine — must exist on every deployment host or be bundled with the app.

---

## Mental model

**Build-time environment** (headers, compiler) ≠ **runtime environment** (what executes):

```txt
Dev laptop                    Production node
──────────                    ───────────────
gcc, headers, debug symbols   libc.so, libssl, JVM, Node, /dev, cgroups
         │                              ▲
         └── artifact (jar, binary) ─────┘
```

Components:
- **Dynamic linker** (`ld.so`) + shared libs (`libc`, `libstdc++`)
- **Language VM** (JVM, .NET, V8 for Node, BEAM)
- **OS interface** — syscalls, [[file descriptors]], [[Linux cgroup]] limits
- **Config/env** — `PATH`, `LD_LIBRARY_PATH`, `JAVA_HOME`, timezone, DNS

**"Works on my machine"** = runtime mismatch (glibc version, missing `.so`, wrong Node LTS).

---

## Standard config / commands

### Inspect binary runtime deps

```bash
ldd ./myapp                    # shared libraries
readelf -d ./myapp | grep NEEDED
file ./myapp                   # interpreter path (e.g. /lib64/ld-linux-x86-64.so.2)

# Java
java -version
jar tf app.jar | head

# Node
node -p "process.version"
which node
```

### Reproduce prod runtime in container

```dockerfile
FROM debian:bookworm-slim
COPY myapp /usr/local/bin/
RUN ldd /usr/local/bin/myapp | grep "not found" && exit 1 || true
```

```bash
docker run --rm myimage ldd /usr/local/bin/myapp
```

### glibc compatibility (common break)

```bash
ldd --version
# Build on older glibc or static-link musl for wide portability
```

**Why containers:** ship a known runtime filesystem root — not just the binary.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `./app: No such file` (binary exists) | Missing dynamic linker | Install correct libc or use musl static build |
| `version GLIBC_X.XX not found` | Newer build, older host | Build on oldest target distro; manylinux wheel |
| JVM `UnsupportedClassVersionError` | JDK compile > JRE run | Align `-target` and runtime JDK |
| Node native module ABI error | Module compiled for different Node | Rebuild with `npm rebuild`; pin Node version |

---

## Gotchas

> [!WARNING]
> **`LD_LIBRARY_PATH` in prod** — fragile; prefer RPATH or container image. Wrong order → wrong OpenSSL → mysterious TLS failures.

> [!WARNING]
> **Alpine (musl) vs Debian (glibc)** — prebuilt binaries often glibc-only.

> [!WARNING]
> **Orchestrator injects runtime** — sidecars change localhost, certs, and env; app must read config not hardcoded paths.

---

## When NOT to use

Don't bundle an entire VM for every microservice if a **static binary or distroless** image with pinned deps suffices — balance reproducibility vs image size.

---

## Related

[[runtime]] [[interpreter]] [[linker]] [[Docker]] [[Linux]]
