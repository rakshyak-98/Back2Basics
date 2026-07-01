TFTP is a **simple file transfer protocol** that transfers files over a network using UDP instead of TCP. It is designed for environments where devices need to download or upload files with minimal protocol overhead.

**Why TFTP exists**
some devices (routers, switches, IP phone, embedded systems, PXE boot clients) have:
- Very little memory
- Limited CPU
- No operating system yet

They only need to:
- Download a boot image
- Upload/download configuration files
- Update firemware

A full-featured protocol like [[ftp]] is unnecessarily complex.

```txt
Client
   |
RRQ / WRQ
   |
UDP Port 69
   |
TFTP Server
```

Read Request (RRQ) (client downloads a file)

```txt
Client
   |
RRQ "boot.img"
   |
Server
   |
DATA Block 1
   |
ACK 1
   |
DATA Block 2
   |
ACK 2
   |
```

Write Request (WRQ)

```txt
Client
   |
WRQ "config.txt"
   |
Server
   |
ACK 0
   |
DATA Block 1
   |
ACK 1
   |
```

> [!INFO]
> **Reliability**
>
> Although UDP is unreliable, TFTP adds reliability by:
> 
> - Numbering each data block
> - Requiring an ACK for every block
> - Retransmitting a block if its ACK is not received before a timeout