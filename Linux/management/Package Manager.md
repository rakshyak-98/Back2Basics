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

```bash
Hit: # comparing metadata with remote site.
Get: # fetching new, improved version from remote site.
Ign: # a non-critical error occured.
Err: # a critical error occured.
```

when `apt-get update` is verifies if the same update indexes need downloading, if not it does not download the same updated indexes again.

- `Hit` - means apt checked the timestamps on package list ( `Release` or `InRelease` file), those match and there are no changes (compare with `/var/lib/apt/lists` ).
- `Ign` - means there are no changes in the `pdiff` index file (in-release file), it wont bother downloading it again, Ignore.
- `Get` - means apt checked the timestamps on package list, there were changes and will be downloaded.
### standard output
- used to redirect standard out.

```bash
# STDOUT
command [option] > [output file]
```
