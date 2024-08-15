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