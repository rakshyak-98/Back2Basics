[[commands]]

# Check all locations for a specific unit

> Check all locations for a specific unit — /etc/systemd/system/ # Administrator-created units (highest priority)

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Debugging]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

```bash
systemctl cat <service name>; # Find all unit files for a service.
systemctl show -p FragmentPath <service name>;
```
> [!INFO]
> Unit files location (Priority Order)
```bash
1. /etc/systemd/system/          # Administrator-created units (highest priority)
2. /run/systemd/system/          # Runtime units
3. /lib/systemd/system/          # Distribution packages (lowest priority)
4. /usr/lib/systemd/system/      # Alternative distribution location
1. ~/.config/systemd/user/       # User-specific units
2. /etc/systemd/user/           # Administrator-provided user units
3. /usr/lib/systemd/user/       # Distribution user units
find /etc/systemd /run/systemd /lib/systemd /usr/lib/systemd -name "nginx.service" 2>/dev/null
```

## Standard config / commands

…

## Debugging

```bash
systemctl list-units --failed;
```
```bash
systemctl list-dependencies <service name>; ## list dependencies of a service.
systemctl list-dependencies --reverse nginx.service; # list what depends on this service.
```

```bash
systemctl show -p Wants,Requires,After,Before <service name>;
```

```bash
systemd-analyze critical-chain <service name>;
```

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
