- login shell is the first shell session that a user interacts with after logging into a system, and it typically reads specific configuration files to set up the environment.
- it is the first process executed with your user ID when you log into an interactive session, such as via a terminal or SSH. 
- it is responsible for setting up user environment by reading configuration file like `/etc/profile` and `~/.bash_profile` or `~/.profile` for Bash, or similar files for other shells.

```bash
bash --login -c 'env'; # View environment variables or aliases that are set in a login shell
```