[[Docker]]

# commit changes in the container to new image.

> commit changes in the container to new image. — OCI - Open Container Initiative. OCI runtime is a specification for running containerised applications.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

```bash
docker commit <container id> <new-image-name>;
docker port <container id>; # test docker port
```
OCI - Open Container Initiative. OCI runtime is a specification for running containerised applications.
- specifies the runtime behavior of containers.
- manage the lifecycle of containers, including starting, stopping, and removing containers.
- provides a way to configure the resources that are available to a container, such as CPU, memory, and network resources.
```bash
docker ps --format "{{.Names}}\\t {{.Ports}}"
docker inspect --format='{{json .NetworkSettings.Ports}}' mycontainer
```
> [!NOTE]
> Keep in mind that even if a port is exposed in a container, it may not be accessible from outside the host machine if the container is not connected to the host network or if the firewall is blocking traffic to that port.

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
