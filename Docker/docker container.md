
```bash
docker run [OPTIONS] image_name[:tag];
```

```bash
docker run hello-world;

docker run -it --rm ubuntu bash; # interactive terminal, remove when stopped
docker run -d --name my-nginx -p 8080:80 nginx:latest;

docker run -d -e MYSQL_ROOT_PASSWORD=secret123 --name mydb mysql:8.0;
```

```bash
docker run -it -v $(pwd):/app python:3.11 bash; # Mount current directory into container
```

```bash
docker create --name my-container -p 9000:80 nginx; # Create container (but don't start it).
docker start my-container;
docker start -ai my-container; # start and attach terminal
```

## Snap shot a container

```bash
# Basic (recommended)
docker commit my-dev-container my-snapshot:2026-01-20

# Or with more metadata (very useful)
docker commit \
  --author "Rakshyak <you@email.com>" \
  --message "Snapshot after installing nodejs + custom config" \
  my-dev-container \
  myproject/snapshot:debug-20260120

```

Backup entire image with layers/history. Saves image to `.tar` (good for transfer to another machine)

```bash
docker save -o backup.tar image:tag
```

Restore from export tar

```bash
docker import container.tar newimage:flat;
```

## Run container with working director

```text
docker run [options] \
  -w /path/inside/container \
  image-name \
  your-command [args]
```

```bash
docker run -it -w /app ubuntu:24.04 bash;
```
- start with interactive bash shell
- Working directory is `/app` (created automatically if missing)
- `-it` interactive + pseudo-TTY