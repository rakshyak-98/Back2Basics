## Check if a specific port is open on a remote server using its domain name

```bash
nc -zv example.com 80;
nc -zv example.com 22 80 443 3389; # check multiple port at once
nc -zv -w 3 example.com 22; # with timeout 3 seconds
```