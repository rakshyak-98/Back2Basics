```bash
apt-cache policy <package name>; # view the installation status and priority of a specific package across all configured repositories.
```

- It is the best tool for debugging why a specific version of a program is (or isn't) being installed.
- **Installed:** The version currently on your system (or `(none)`).
- **Candidate:** The version APT _wants_ to install next.
- **Version Table:** A list of every version available in your `/etc/apt/sources.list`, sorted by their "Pin Priority."

```bash
sudo apt full-upgrade;

sudo apt install software-properties-common;
apt-mark showmanual; # show, set and unset verious settings for a package.
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

|Criteria|**Manually Installed**|**Automatically Installed**|
|---|---|---|
|**Definition**|Explicitly installed by the user|Installed as dependencies for other packages|
|**Tracking**|`apt-mark showmanual`|`apt-mark showauto`|
|**Removal Behavior**|Not removed unless explicitly removed|Auto-removed when no longer needed (`apt autoremove`)|
|**Install Command**|`apt install <pkg>`|Installed _with_ another package (not directly)|
|**Uninstallation**|Safe from auto-removal|Can be auto-removed if orphaned|
|**Marking**|Can be marked with `apt-mark manual`|Can be marked with `apt-mark auto`|
|**Purpose**|Intended usage by user|Support/requirement for other packages|

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


## package architecture

```text
deb [arch=amd64 signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/ubuntu jammy nginx
```

- mention the `arch`

```bash
dpkg --print-foreign-architectures; # list secondary CPU architectures
dpkg --print-architectures; # see primary architecture your OS was installed with
```

[`distro-info-data`](https://github.com/deepin-community/distro-info-data)
- the `distro-info` package provides centralised lists of code-names and release history for the supported distributions (Currently: Debian and Ubuntu)

## advance package tool (apt)

`apt show [package name]` this will show the package info `apt show [package name] -a` this will only show the package description.

### difference between `apt remove` and `apt purge`

apt remove just removes the binaries of a package. it leaves residue configuration files. apt purge removes everything related to a package including the configuration files.
