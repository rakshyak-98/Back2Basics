- a separate data connection is established for transferring files.
- Active Mode: the server connects back to the client to transfer data.
- Passive Mode: the client establishes the data connection to the server, which is often more firewall-friendly
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