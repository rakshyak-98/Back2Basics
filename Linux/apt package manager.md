- Advance packing tool
```bash
apt install iputils-ping;
apt install dnsutils; # nslookup command packages
apt install iproute2; # ip command packages
apt-get install procps htop; # ps and top command packages.
apt install net-tools; # netstat etc.
apt install telnet;

apt-get install build-essential; # install C in system and gcc

apt-get install lvm2; # logical volume packages, pvdisplay.
apt-cache search; # search the cache in the system with package name.
apt-get show package_name; # search without internet connection, from the cache.
```

> [!NOTE]
> `apt list | grep <package name>` means that the package is available in the Ubuntu repositories, but it does not mean it's installed on your system.

```bash
dpkg -l | grep <package name>;
apt list --installed | grep <package name>;
```

```bash
apt-cache rdepends <pkg name>;
```

## Inspect package details 

```bash
apt-mark showmanual;
apt-mark showauto;
apt-mark showhold;
```

```bash
# list manually installed packages
comm -23 <(apt-mark showmanual | sort -u) <(gzip -dc /var/log/installer/initial-status.gz | sed -n 's/^Package: //p' | sort -u)
```

#### basic packages

```bash
apt install shadow; # include useradd ... packages.
```
see the package log file `/var/log/dpkg.log`

```bash
apt show <package name>
apt search <package name> # 
apt depends <package name>
apt-cache pkgnames; # list all the installed packages in system.
apt-get install -f; # fix broken package.

apt list --upgradable --all-versions;
apt-mark unhold [package name];


# download the gpg public key
curl -fsSL <https://download.docker.com/linux/ubuntu/gpg> | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
# sign and update the sourc list
echo \\
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] <https://download.docker.com/linux/ubuntu> \\
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \\
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Held packages - refers to packages in a package management system (apt) that have been marked as being held back and will not be upgraded or installed automatically.

- happen for conflicts with other packages, or package being considered too risky to upgrade.
- can check which packages are being held back by running the command
