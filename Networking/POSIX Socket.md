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

## OS socket bind

In computer networking `bind()` is a system call used to associate a specific network address (IP address) and a port number with a socket.

When you care a socket (using the `socket()` system call), it exists in a "nameless" state. It has no identity on the network. The `bind()` function gives that socket an identity so that other computers or processes know exactly where to send data.

> OS Socket binding is the process of assigning a specific transport layer address, consisting of an IP address and a port number, to a socket file descriptor.

this operation enables an application to control exactly which network interface and port it listens on or communicates from.

## Functional Mechanics

When a socket is created, it exists state without a network identity. Binding attaches it to local system's networking stack:
- server-side -> The `bind()` system call is required to associate a socket with a specific port, allowing the OS to route incoming packets destined for that port to the application.
- Client-side -> Binding is typically optional. If omitted, the OS performs an implicit (ephemeral) binding to an available port when the connection is initiated.