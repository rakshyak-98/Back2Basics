view DNS server configurations

```shell
cat /etc/resolv.conf;
resolvectl status;
nmvli dev show | grep DNS;
ip route show;
route -n;
route print;
route -n get default;
tracert google.com;
netstat -nr;
```

```shell
```