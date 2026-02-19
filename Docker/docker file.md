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

- docker file must begin with `FROM` (specifies the parent image). The `FROM` instruction initializes a new build stage and sets the Base image for subsequent instructions. Each `FROM` instruction clears any state created by previous instructions.
- Optionally a name can be given to a build stage by adding `AS name` to the `FROM` instructions.
- docker runs instruction synchronously.
- The `CMD` command represents an argument list for the `ENTRYPOINT`.

`FROM` can appear multiple times within a single `dockerfile` .

```docker
ARG  CODE_VERSION=latest
FROM base:${CODE_VERSION}
CMD  /code/run-app

FROM extras:${CODE_VERSION}
CMD  /code/run-extras
```

```bash
FROM [--platform=<platform>] <image> [AS <name>]
FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]
FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]
```

RUN

```bash
RUN /bin/bash -c 'source $HOME/.bashrc; \\
echo $HOME'
RUN /bin/bash -c 'source $HOME/.bashrc; echo $HOME'
RUN ["/bin/bash", "-c", "echo hello"]
```

```python
### reducing the image files

#dockerfile.prod
#build stage
FROM node:14.16.0-alipine3.13 as <label>
WORKDIR /app
COPY package*.josn ./
RUN num install
COPY . .
RUN npm run build

#stage 2
FROM <webserver> # nginx:1.12-alipine as production stage
RUN addgroup app && adduser -S -G app app
RUN mkdir /app && chown app:app /app
USER app
WORKDIR /app
COPY --from=build-stage /app/build /usr/share/nginx/html
EXPOSE 80
ENTRYPOINT ['nginx', '-g', 'demon off;'] #from nginx doc
```

```toml
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
BindsTo=containerd.service
After=network-online.target firewalld.service containerd.service
Wants=network-online.target
Requires=docker.socket

[Service]
Type=notify
# the default is not to use systemd for cgroups because the delegate issues still
# exists and systemd currently does not support the cgroup feature set required
# for containers run by docker
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
ExecReload=/bin/kill -s HUP $MAINPID
TimeoutSec=0
RestartSec=2
Restart=always

# Note that StartLimit* options were moved from "Service" to "Unit" in systemd 229.
# Both the old, and new location are accepted by systemd 229 and up, so using the old location
# to make them work for either version of systemd.
StartLimitBurst=3

# Note that StartLimitInterval was renamed to StartLimitIntervalSec in systemd 230.
# Both the old, and new name are accepted by systemd 230 and up, so using the old name to make
# this option work for either version of systemd.
StartLimitInterval=60s

# Having non-zero Limit*s causes performance problems due to accounting overhead
# in the kernel. We recommend using cgroups to do container-local accounting.
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity

# Comment TasksMax if your systemd version does not supports it.
# Only systemd 226 and above support this option.
TasksMax=infinity

# set delegate yes so that systemd does not reset the cgroups of docker containers
Delegate=yes

# kill only the docker process, not all processes in the cgroup
KillMode=process

[Install]
WantedBy=multi-user.target
```