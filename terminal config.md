
**List installed fonts**

```bash
fc-list :spacing=100 family; # instal installed fonts
```

using gsetting

```bash
gsettings set org.gnome.desktop.default-applications.terminal exec 'alacritty'
```


enable disable shell behaviour options

```bash
set -o vi;
set -o emac;
```

|Option|Purpose|
|---|---|
|`errexit` (`-e`)|Exit script immediately if a command fails|
|`nounset` (`-u`)|Error when using an undefined variable|
|`pipefail`|Pipeline fails if any command fails|
|`xtrace` (`-x`)|Print commands before executing (debugging)|
|`verbose` (`-v`)|Print shell input lines as read|
|`noclobber` (`-C`)|Prevent overwriting existing files using `>`|
|`monitor` (`-m`)|Enable job control|
|`history`|Enable command history|