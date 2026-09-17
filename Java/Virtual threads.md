They were introduced in **Java 21** as a major part of Project Loom.

> How can a Java application handle a very large number of concurrent, mostly-blocking tasks without needing an equally large number of OS threads?

```java
Thread thread = new Thread(() -> {
	// work
})
thread.start(); // creates a platform thread
```
The JVM typically maps that Java thread to an OS thread. **OS threads are relatively expensive.**

"A **Platform thread** is a traditional Java thread that is backed by an operating system thread." The traditional `Thread` model.

- Traditional Java servers typically use a bounded thread pool:
```txt
			HTTP Requests
						↓
┌─────────────────────┐
│   Thread Pool       │
│                     │
│ T1 T2 T3 ... T100   │
└─────────────────────┘
						↓
			 Database
```
Maybe you have 100 worker threads serving thousands of incoming requests.
- If each request require a platform thread, That's expensive in terms of memory and OS scheduling. So traditionally Java application use a thread pool, Only 100 requests execute concurrently; the others wait for a thread.

> Platform threads are still the actual execution resources underneath virtual threads.

For CPU-bound work, the number of platform/carrier threads are available CPU cores still matter.

Virtual threads mainly give you a much cheaper way to represent **large numbers of concurrent tasks,** particularly tasks that spend significant time waiting on I/O.

"A platform thread is a JVM-managed Java thread that is backed by on OS thread, whereas a virtual thread is a lightweight JVM-managed thread that can be multiplexed over platform threads."

When a **virtual thread blocks on an operation that the JVM can suspend,**
> The virtual thread becomes parked/waiting, and its carrier platform thread is freed to run another virtual thread.


```java
Thread.startVirtualThread(() -> {
	User user = userRepository.findById(10L); // DB Call
	System.out.println(user);
})
```

With a traditional platform thread:
```txt
Platform Thread
      │
      ↓
  DB request
      │
      │ WAIT
      ↓
OS thread is occupied
```

> The DB query still needs execution somewhere. Virtual threads don't eliminate that. They eliminate the need to keep a **Java/OS Thread occupied while waiting for the database's response.**

Starting/Executing a DB operation
```java
User user = repository.findById(10L);
```

```txt
Virtual Thread
     │
     │ 1. execute Java/JDBC code
     ↓
JDBC Driver
     │
     │ 2. send SQL over network
     ↓
Operating System / Socket
     │
     ↓
Database
```

At this point, the database is doing the actual query execution. The Java application **doesn't execute the SQL query itself.**

```txt
Your JVM                         Database

JDBC driver                      DB engine
     │                               │
     │──── SQL request ─────────────→│
     │                               │
     │                         execute query
     │                               │
     │                               │
     │←──── result bytes ────────────│
```
The virtual thread only needs CPU execution for the parts where **your Java application is actually doing work.**
During the waiting period, there's no reason to keep the carrier OS thread dedicated to that virtual thread.

**How does the JVM know when the DB responds?**
This is where the OS networking subsystem comes in. The database connection is ultimately communication through a network socket. The JVM can ask the operating system to wait for the Socket to become ready. Modern Java networking APIs can cooperate with the JVM's virtual-thread scheduler.

**Connection vs Thread**

```txt
100 virtual threads
       ↓
HikariCP
       ↓
10 database connections
```
Only 10 can actually have a database connection simultaneously

```txt
VT1  → connection 1 → DB query
VT2  → connection 2 → DB query
...
VT10 → connection 10 → DB query

VT11 → waiting for Hikari connection
VT12 → waiting for Hikari connection
```
Virtual threads don't create more database capacity. They make the **application-side waiting/concurrency much cheaper.**

"The database executes the query. The virtual thread mainly waits for the I/O result, and that waiting period is what the JVM can suspend without trying up a carrier thread."

**Virtual Threads scale well with blocking I/O**
```java
byte[] response = socketInputStream.read();
```

With a traditional platform thread, you'd think of it as:
```txt
Platform Thread
      │
      ▼
socket.read()
      │
      ▼
OS says: "no data yet"
      │
      ▼
THREAD BLOCKS
      │
      └── OS thread remains occupied waiting
```
with a virtual thread, the JVM tries to avoid occupying the carrier thread during that wait.

A virtual thread isn't directly an OS thread. Virtual thread is running on a carrier thread.

```txt
Virtual Thread A
		 │
		 ▼
 Carrier Thread
		 │
		 ▼
	OS Thread
```
The JVM mounts Virtual Thread A onto a carrier when A needs CPU execution.

**The socket read reaches the JDK networking layer** The important part is that modern JDK blocking socket operations are integrated with the JVM's virtual-thread machinery. The JDK doesn't need to keep the carrier thread sitting there doing nothing. Instead it can arrange for the socket to be monitored for readiness and **part the virtual thread.**

**Who watches the socket?** This is where the OS networking mechanism comes in, On Linux, the underlying mechanism is typically based around `epoll`.

```txt
┌──────────────────────┐
│       Database       │
│                      │
│ executes SQL         │
└──────────┬───────────┘
					 │
		 TCP response
					 │
					 ▼
		┌─────────────┐
		│ OS socket   │
		└──────┬──────┘
					 │
					 ▼
			 epoll
					 │
		"socket readable"
					 │
					 ▼
		┌─────────────┐
		│     JVM     │
		│             │
		│ unpark VT A │
		└──────┬──────┘
					 │
					 ▼
		Virtual Thread A
```
The OS can efficiently monitor many sockets. It doesn't required one OS thread per socket.

**Database finishes the query** Meanwhile, **the database server is doing the actual SQL execution.**

```sql
SELECT * FROM orders WHERE customer_id = 123; 
```
The Java application doesn't spend 500 ms executing that SQL.

**Response arrives**
Eventually the DB sends the result:
```txt
Database
   │
   │ TCP response
   ▼
OS socket
   │
   ▼
epoll detects readable data
   │
   ▼
JVM/JDK
   │
   ▼
Virtual Thread A becomes RUNNABLE
```
The JVM scheduler can then mount A onto **any available carrier.** It doesn't necessarily have to be the same carrier
```txt
Before:

Carrier #1
   └── VT A
        ↓
      socket.read()
        ↓
      PARKED


After:

Carrier #1
   └── VT B

Carrier #2
   └── VT A
        ↓
      process DB response
```

**Virtual threads make the application-side waiting cheap. They do not make the database operation cheap.**

Even through you can have thousands of virtual threads, **the database is still constrained by those 50 connections and by the DB's own capacity.**

Scalability depends on the I/O operation being compatible with virtual-thread parking. Certain native/blocking operations can **pin a virtual thread to its carrier,** which defeats some of the benefit. Modern JDK networking APIs are specifically designed to cooperate with virtual threads.