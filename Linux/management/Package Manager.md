```shell
sudo apt install software-properties-common;
```
- package is installed because it provides the `add-apt-repository` command, which is needed to manage third-part repositories.
- It enables managing PPA (Personal Package Archives) and other external `source.list`.
- Ensure dependency resolution and package management stability.

> [!INFO] Since some package are not available in Ubuntu's default repository, we need to add third party repository, which requires `software-properties-common` package to be installed.

```shell
sudo add-apt-repository ppa:<repository name>;
```

```shell
ls /etc/apt/source.list.d/; # list configured ppa pacakge repository
grep -rhE '^dep' /etc/apt/source.list.d/
```


###  auto updates 
```bash
sudo apt install unattended-upgrades;

sudo dpkg-reconfigure --priority=low unattended-upgrades;
```