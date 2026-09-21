- a separate data connection is established for transferring files.
- Active Mode: the server connects back to the client to transfer data. Your router or firewall usually blocks that incoming connection, so transfers hang or fails.
- Passive Mode: the server tells your computer which port to use, and your computer opens the connection to it. Every connection goes out from your side, so it get through routers and firewalls without any setup. 

## Setup ftp server
#### vsftpd
- Very Secure FTP Daemon
- support IPv6 and SSL. virtual users with PAM (pluggable authentication modules).
- vsftpd is the default FTP server in the Ubuntu.
```bash

```

#### virtual user
- A virtual user is a user login which does not exist as a real login on the system in `/etc/passwd`  and `/etc/shadow` file.
- virtual users can be more secure than real user, because a compromised account can only use the FTP server but cannot login to system to use other services such as [[SSH]] or [[SMTP]].