`systemd, 1` the system-wide systemd
PID `1` is the main system initialization process: It starts when Linux boots and manages **system-level services**, such as:

These services generally run independently of a particular logged-in user.
```txt
systemd
├── nginx
├── sshd
├── redis
├── docker
├── cron
└── ...
```

`systemd --user` your user's systemd, This is a **per-user service manager.**
- it belongs specifically to your linux user session
- This is **service manager dedicated to one user's environment.**
"Don't manage the entire machine. Mange services belonging to this particular user's session."

[[user-level process]] `systemd --user` become the parent

**Why `systemctl` is trying to connect to bus**
`systemctl` is not itself the service manager. It's a client that talks to systemd.

```txt
your terminal
     │
     │ systemctl --user status nginx
     ↓
  systemctl
     │
     │ communicate through D-Bus
     ↓
systemd --user
     │
     ↓
 user services
```

**D-Bus** is an IPC mechanism - Inter Process Communication. It allows one process to communicate with another process.

When you execute the `systemctl --user status nginx` it effectively says
"I need to ask the systemd instance belonging to this user for the status of `nginx`"
Is therefore need to find and connect to the **user's D-Bus/systemd communication endpoint**

**Why connection refused?**
`systemctl --user` doesn't simply search the process tree and talk to PID `2587`. It needs the appropriate **user D-Bus environment/socket.**

If that communication endpoint isn't available or isn't exposed in your current shell environment, you can get:
```txt
Failed to connect to bus: Connection refused
```
A very common cause is that your current shell doesn't have the expected user-session environment variables, particularly:
```bash
echo $DBUS_SESSION_BUS_ADDRESS
echo $XDG_RUNTIME_DIR
```

```bash
loginctl
systemctl --user status
```

**one more important point: nginx probably isn't a user service**
```bash
systemctl status nginx
```

`systemctl` "A command sends requests to a `systemd` manager over D-Bus."

Your Connection refused is happening the **second path**, before `systemd` can even answer your request.
