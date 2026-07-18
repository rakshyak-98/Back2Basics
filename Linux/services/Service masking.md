sometime disabling is not enough. Masking a service makes it impossible to start
```sh
systemctl mask bluetooth.service;
systemctl unmask bluetooth.service;
```
- `mask` create  a symlink to `/dev/null` effectively blocking the service 
