[[Docker CLI]] [[INDEX]]

# Docker CLI

> Docker Engine CLI — build, run, inspect, network, volumes, and compose.

---

## Docker CLI

### Validate Dockerfile

From [[Docker CLI]].

```bash
docker build --check .                    # BuildKit checks (syntax/policy)
docker buildx build --check .             # dry parse without full build
docker run --rm -i hadolint/hadolint < Dockerfile   # lint
```

### Build

From [[Docker CLI]].

```bash
docker build -t myapp:latest .                              # context = cwd
docker build -f docker/Dockerfile -t myapp:1.0.0 .
docker build --no-cache -t myapp:latest .
docker build --build-arg NODE_ENV=production -t myapp:latest .
docker build --target builder -t myapp:builder .
```

### Run

From [[Docker CLI]].

```bash
docker run -d --name myapp -p 3000:3000 myapp:latest
docker run --rm -it myapp:latest /bin/sh    # ephemeral debug shell
docker exec -it myapp /bin/sh               # into running container
```

### Inspect & logs

From [[Docker CLI]].

```bash
docker ps -a
docker logs -f --tail 200 myapp
docker inspect myapp
docker inspect --format '{{json .NetworkSettings.Networks}}' myapp
docker top myapp
docker stats --no-stream
```

### Network

From [[Docker CLI]].

```bash
docker network ls
docker network create app-net
docker run -d --network app-net --name api myapp:latest

docker network disconnect app-net api
docker network connect --alias api-internal app-net api
```

### Volumes

From [[Docker CLI]].

```bash
docker volume create mydata
docker run -v mydata:/var/lib/data myapp:latest
docker run -v /host/path:/container/path:ro myapp:latest   # bind mount

docker volume ls
docker volume inspect mydata
```

### Image transfer

From [[Docker CLI]].

```bash
docker save myapp:latest | gzip > myapp.tar.gz
docker load < myapp.tar.gz
docker tag myapp:latest registry.example.com/myapp:v1
docker push registry.example.com/myapp:v1
```

### Compose plugin

From [[Docker CLI]].

```bash
sudo apt install docker-compose-plugin
docker compose up -d
docker compose logs -f api
docker compose down -v   # -v removes named volumes — careful in production
```

### System maintenance

From [[Docker CLI]].

```bash
docker system df
docker system prune              # stopped containers, dangling images, unused networks
docker system prune -a             # all unused images — aggressive
docker system prune -a --volumes   # includes unused volumes — data loss risk
```
