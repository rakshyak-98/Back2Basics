
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