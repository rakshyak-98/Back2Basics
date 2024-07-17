```bash
# switch contianer image without deleting the container.
docker commit <container_id> <new container name>
docker run -d --name <new_container_name> --volumes-from <old_container_name> <new_image_name>

```