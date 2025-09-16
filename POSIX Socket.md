## Overview
- **Definition**: Standardized API (POSIX) for inter-process & network communication using sockets.  
- **Origin**: Based on BSD sockets, adopted by POSIX for portability.  
- **Key Idea**: Socket = file descriptor → usable with `read()`, `write()`, `close()`.  
- **Uses**: TCP/UDP networking, IPC (Unix domain sockets), raw packet access.

---

## Core Functions
1. **Socket Lifecycle**
   - `socket()` → create endpoint.
   - `bind()` → assign local address/port.
   - `listen()` → mark socket as server/passive.
   - `accept()` → accept client connection.
   - `connect()` → initiate connection (client).
   - `close()` → release socket.

2. **Data Transfer**
   - `send()`, `recv()` → stream-based (TCP).
   - `sendto()`, `recvfrom()` → datagram-based (UDP).
   - `read()`, `write()` → also usable since socket is a fd.

3. **Control**
   - `setsockopt()`, `getsockopt()` → configure options.
   - `select()`, `poll()`, `epoll/kqueue` → multiplexing.

---

## Data Structures
- `struct sockaddr` → generic address container.
- `struct sockaddr_in` → IPv4 address.
- `struct sockaddr_in6` → IPv6 address.
- `struct sockaddr_un` → Unix domain address.
- `struct msghdr`, `struct iovec` → scatter/gather I/O.

---

## Client vs Server Workflow
**Client**
1. `socket()`
2. `connect()`
3. `send()/recv()`
4. `close()`

**Server**
1. `socket()`
2. `bind()`
3. `listen()`
4. `accept()`
5. `send()/recv()`
6. `close()`

---

## Properties
- Protocol families: `AF_INET`, `AF_INET6`, `AF_UNIX`, `AF_PACKET`.
- Blocking & non-blocking modes supported.
- Errors follow `errno`.
- Extensible for new protocols.

---

## Common Edge Cases
- `EADDRINUSE` → port already bound.
- `EAGAIN` / `EWOULDBLOCK` → non-blocking socket operations.
- **Partial send/recv** → loop until all data processed.
- **SIGPIPE** → writing to closed socket (use `MSG_NOSIGNAL` or ignore).
- IPv6 dual-stack behavior → `IPV6_V6ONLY` option.
