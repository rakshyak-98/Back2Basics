```bash
dpkg -l | grep tzdata
ls -la /usr/share/zoneinfo/
```

**You should have directories such as:**
```txt
/usr/share/zoneinfo/Asia/
/usr/share/zoneinfo/Europe/
/usr/share/zoneinfo/America/
/usr/share/zoneinfo/UTC
```

```bash
sudo timedatectl set-timezone Asia/Kolkata; # If tzdata is missing or damaged
```