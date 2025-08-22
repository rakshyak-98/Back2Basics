## Understanding Phased Updates
- Ubuntu uses phased updates to distribute package upgrades incrementally, reducing the risk of widespread issues if a new package version has bugs.
- When a package is in the phasing process, it may not be immediately available to all users, even after running `sudo apt update`

> [!INFO]
- To install these deferred updates, you can either wait for the phasing to complete or bypass it to install the updates immediately.

> [!NOTE]
> Verify that the package are deferred due to phasing
```bash
apt-cache policy <package name>;
```
- Look for a line like (phased X%) under the Version table for each package. The percentage indicates the rollout progress. If phasing is confirmed, proceed to bypass it.