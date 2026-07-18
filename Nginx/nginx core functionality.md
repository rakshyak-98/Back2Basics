
`accept_mutex`

When `accept_mutex` disabled
- All workers processes get simultaneously notified about a new incoming connection.
- the race to call `accept()` on the shared listen socket.
- Only one of them actually gets the connection.
- The others get `EAGAIN` (or similar) and go back to sleep.
This is called **thundering herd** problem (or wake-up storm).


## What really happens step by step (when accept_mutex is off)

1. A new client connects → kernel puts the connection into the listen queue
2. Kernel sends a signal / wakes up **all** worker processes that are currently doing epoll_wait() (or equivalent) on the listen socket
3. All (e.g. 8–32) workers wake up **at almost the same time**
4. All workers call accept() on the same listen socket in a race
5. **Only one** worker succeeds and gets the new connection
6. All other workers get accept() returning **-1** with `errno = EAGAIN (or EWOULDBLOCK)`
7. Those workers go back to sleep (`epoll_wait` again)
8. The winning worker handles the connection normally


## How to view and monitor the kernel's connection listen queue

also called backlog or SYN queue on linux system
- the queue where incoming TCP connections wait before an application (like nginx) calls `accept()`.

- Listen backlog -> maximum queue size set by the application (`listen 128;` in nginx).
- Current queued connections -> how many are waiting right now (SYN queue + incomplete queue).
- When the queue is full -> kernel drops new connections (you see `SYN_RECV` drops in stats).

```bash
ss -tln; # current listen sockets + Recv-Q (queued connections)
ss -ltnp; # process, see which process own the socket.
ss -ltn state syn-recv; # Only connections in SYN_RECV state (waiting in queue) Debugging backlog overflow

netstat -ltn; # Classic alternative (similar to ss)
# - Look for:
# - TcpExtListenDrops — connections dropped because queue was full
# - TcpExtListenOverflows — similar (old kernels)

tcpdump -i any port 80 -nn; # See SYN packets ariving (and if they get RST where queue full) Real time traffic + drops

```

```bash
sysctl net.core.somaxconn; # max possible backlog. default 4096
```