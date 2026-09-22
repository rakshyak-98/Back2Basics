The application uses a **programming interface (API)** exposed by the OS, not an interface that the application implements itself.

```txt
Your Application
      │
      │ calls socket API
      ▼
Operating System
      │
      ├── Socket implementation
      ├── TCP implementation
      ├── IP implementation
      └── Network driver
      │
      ▼
Network hardware
```

**Programming API/contract**
```txt
socket()
bind()
listen()
accept()
connect()
send()
recv()
close()
```
- the application uses this interface. It does not implement it.

**Socket has two related meanings in networking discussions**, which makes the terminology confusing.
**Socket API** the interface exposed by the OS to applications.
**Socket** the actual **OS-manged communication endpoint** created when the application calls `socket()`.