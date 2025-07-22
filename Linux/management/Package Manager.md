```shell
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

### Source list file config
```txt
deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/debian jammy nginx
```
- `deb` -> this is a binary package source (as opposed to `deb-src` for source code).
- `[signed-by=...]` -> custom gpg key used to verify the authenticity of packages.
- 'http://' -> URL of the APT repository (from package org).
- `jammy` -> code name for Ubuntu 22.04 (APT uses Debian-style naming).
- `nginx` -> the distribution/component (like `main`, `contrib`)  here it is nginx specific pacakge.

> [!INFO]
> `main` component -> sub folder under distribution `/dists/jammy/main/binary-amd64/`
> when you run `apt update` APT tries to download
```bash
https://my.repo.com/apt/dists/jammy/Release
https://my.repo.com/apt/dists/jammy/main/binary-amd64/Packages.gz
```
- `jammy` to select the `dists/<distribution>` folder
- `main` (component) to pick which subfolder(s) to load packages from

> [!NOTE]
> APT does not "determine" these — **you must specify both**, and the server must have a matching structure under `/dists`. 


## package architecture
```text
deb [arch=amd64 signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/ubuntu jammy nginx
```
- mention the `arch`

```bash
dpkg --print-foreign-architectures;
dpkg --print-architectures;
```