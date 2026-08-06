[[Networking]]

# Internal routing

> One-line: what / why for **Internal routing** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

- if you and the target device reside on the same private IP network and you cannot configure your router, you can communicate directly within the network using internal routing.
- identify the Device's Private IP
- On the target device, find its private IP:
- Ensure the program Listens on a Non-Default Port
	- verify that the program you want to communicate with is actively listening on the desired port.
```shell
sudo netstat -tuln | grep <port>
```
- Directly Connect Using the private IP
```shell
curl http://198.168.1.3:5000;
```
- Verify Firewell or Security Settings
	- Ensure the target device allows incoming connections on the specified port:
```shell
sudo ufw allow 5000
```

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
