```shell
docker inspect --format '{{json .NetworkSettings.IPAddress}}' <container_id>
```
#### Installation
```bash
sudo apt install docker-compose-plugin; # install docker compose command as plugin
```

```bash
# switch contianer image without deleting the container.
docker ps -q; # show only container id 
docker commit <container_id> <new container name>
docker run -d --name <new_container_name> --volumes-from <old_container_name> <new_image_name>
```


## Network
```bash
docker netword disconnect <network name>;
docker network connect --alias <alias name> <network name> <container anme>
```

## Volume
- Docker containers are designed to be stateless by nature. These short-lived storage is called the "ephemeral container file system."
- Volumes: docker managed storage option, stored outside the container's File system, allowing data to be persisted across container restarts and removals.
- Bind mounts: Mapping a host machine's directory or file into a container, effectively sharing host's storage with the container.
- tmpfs mounts: In-memory storage, useful for cases where just the persistence of data within the life-cycle of the container is required.
```bash
```
### bind
- When use a bind mount, a file or directory on host machine is mounted into a container. The file or directory is referenced by its absolute path on the host machine.
- when use a volume, a new directory is created within Docker's storage directory on the host machine, and Docker manages that directory's contents.
- Can't use Docker CLI commands to directly manage bind mounts.