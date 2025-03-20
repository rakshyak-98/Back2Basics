
```txt
Downloading and installing node v22.14.0... Downloading https://nodejs.org/dist/v22.14.0/node-v22.14.0-linux-x64.tar.xz... Warning: Failed to open the file /home/rakshyak/.nvm/.cache/bin/node-v22.14.0-linux-x64/node-v22.14.0-linux-x64.tar.xz: Warning: Permission denied curl: (23) client returned ERROR on write of 1360 bytes
```
- ensure curl has correct permissions, if `curl` is failing due to permission issues.

```shell
sudo apt install --reinstall curl;

```
