```bash

sudo useradd -b /bin/bash <user>;
```

```bash
sudo usermod -d <path to home directory> <user>; # upser user record /etc/passwd to point to new home
```

### Copy default Configuration file

```bash
sudo cp -r /etc/skel/. /home/myuser/;
sudo chown -R <user>:<group> <path to home dir>;
```

### Give the user a login shell

> [!INFO]
> If you created the user with --system or without a shell, it might have `/usr/sbin/nologin` or `/bin/false`. For running Node.js apps, a real shell helps (especially for environment setup):

```bash
sudo usermod -s /bin/bash <user>;
```