To run a specific command on container restart, you should configure the `ENTRYPOINT` or `CMD` block in the `Dockerfile`
- `ENTRYPOINT` : used to define the main command or process that always runs in the container. It cannot be overridden at runtime unless specifically done with `docker run --entrypoint`
- `CMD` : Used to provide default arguments to the `ENTRYPOINT` or to specify the command if no `ENTRYPOINT` is defined. Can be overridden at runtime with `docker urn <image> <command>`

## Docker layered filesystem
- Docker uses a layered filesystem (also called Union Filesystem or UnionFS) to store images and containers in a very efficient, smart way. This is one of the core reasons Docker is fast, lightweight, and save disk space.

 > [!NOTE]
 > Every like in your Dockerfile creates a new layer

```dockerfile
FROM ubuntu:22.04           → Layer 1 (base image)
RUN apt update              → Layer 2
RUN apt install python3     → Layer 3
COPY . /app                 → Layer 4
CMD ["python3", "/app/main.py"] → Layer 5
```

### Types of Union Filesystem Docker uses (Behind the scenes)

Docker supports multiple drivers (you usually don't change this unless needed)

```bash
docker info --format '{{.Driveri}'
```

|Storage Driver|Filesystem|Most Common Use Case|
|---|---|---|
|overlay2|overlayfs|Default on modern Linux (recommended)|
|aufs|AUFS|Older Ubuntu/Debian|
|btrfs, zfs|Native|When you use those filesystems|
|fuse-overlayfs|For rootless|Rootless Docker/Podman|