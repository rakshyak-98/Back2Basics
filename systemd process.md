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
