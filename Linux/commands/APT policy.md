```shell
apt policy;
```
- `apt policy` command is used to check the installed and available versions of package, along with their priority (pinning) and source repositories.
```shell
apt policy <package name>;
```

> [!INFO] the numbers (500, 100, etc.) represent priority levels that determine which package version is installed. This priorities come from API pinning rules in `/etc/apt/preferences`.

### **Priority Breakdown**

| Priority  | Meaning                                                           |
| --------- | ----------------------------------------------------------------- |
| **100**   | Installed package (from `.deb` or manually added).                |
| **500**   | Default priority for packages from official repositories or PPAs. |
| **990**   | Packages from explicitly defined `APT::Default-Release`.          |
| **1-99**  | Lower priority (used for downgrade protection).                   |
| **>1000** | Forces package installation even if it’s a downgrade.             |
### Example: `apt policy nginx`
```shell
nginx:
  Installed: 1.18.0-0ubuntu1
  Candidate: 1.21.0-1+ubuntu20.04
  Version table:
     1.21.0-1+ubuntu20.04 500
        500 http://ppa.launchpad.net/nginx/stable/ubuntu focal/main amd64 Packages
 *** 1.18.0-0ubuntu1 100
        100 /var/lib/dpkg/status

```
- `1.18.0-0ubuntu1 (100)`: Installed version (lower priority).
- `1.21.0-1+ubuntu20.04 (500)`: Available version from PPA (higher priority).
- Since `500` is higher than `100`, running `sudo apt upgrade nginx` will install `1.21.0-1+ubuntu20.04`.