## Configuration manager
```sh
dconf dump /org/gnome/terminal;
dconf load /org/gnome/terminal < <your dconf file>;
```
### Environment configurations
- `XDG_` prefix used to denote a set of environment variables defined by the XDG Base Directory Specification.
- these specification aims to standardize the locations of user-specific files and directories.

```bash
apt-cache rdepends <package name>; # view dependency on packages.
apt-cache rdepends libgtk-3-0;
update-alternatives --config editor; # change the default options for editor
```

```bash
# Prompt

```bash
<<comment
	Text Attributes:
	- 0: Reset all attributes (normal)
	- 1: bold
	- 4: Underline
	- 5: blink
	- 7: reverse video (swap foreground and background colors)
	- 8: concealed (invisible)
	Text colors
	- 30 - 37 (foreground) : set text color (black, red, green yellow, blue, magenta, cyan, white)
- 40 - 47 (background) : set background color...
comment
PS1='\[\e[1;34m\]➜ \W \[\e[1;35m\]$(__git_ps1 " (%s)")\[\e[0m\]\$ ' #my prompt.
```

```bash
set -o vi
set -o emacs
```

### Common installation
```bash
sudo apt install libgtk-3-0 libgtk2.0-0
```

### Application launcher

```bash
sudo cp systemd/appname.service /etc/systemd/system/
sudo chmod +x /etc/systemd/system/appname.service
sudo systemctl daemon-reload.
sudo systemctl start appname

touch ~/.local/share/applications/<app-name>.desktop;
sudo nano [app-name]; # to add configuration.

# change time zone
sudo timedatectl set-timezone Your/Desired/Timezone;
sudo ln -sf /usr/share/zoneinfo/Your/Desired/Timezone /etc/localtime
sudo apt-get install tzdata
dpkg-reconfigure tzdata; # to re collaberate system time zone. 
```

```bash
[Desktop Entry]
Version=1.0 # the version of desktop file.
Type=Application # could be Application, Link or Directory.
Name=Android Studio # appear in the launvher.
Exec="/opt/android-studio/bin/studio.sh" %f # command executed and %f file passed as argument.
Icon=/opt/android-studio/bin/studio.png # used for the launcher icon.
Categories=Development;IDE; # categories in which the application belongs.
Terminal=false # indicates wheter the application run in terminal or not.
StartupNotify=true # enables visual feedback that the application has launced.
StartupWMClass=jetbrains-android-studio # A WM_CLASS property that should match the class name of the application main window.
```

A `.desktop` file is a type of configuration file used in Linux and Unix-like operating systems to create launcher icons of applications. The file contains information about the application, such as its name, location, icon, and command to start the application.

WM_CLASS - x11 windowing systems, the WM_CLASS property is a property of a window that is used to identify the class and instance of an application. The WM_CLASS property is set by the application when it creates its main window and is used by the window manger to apply special settings or rules to the applications (theme or style to all windows of a particular class, to always keep an applications window on top of other windows).

### how to configure a service file

```bash
[unit] # section contains metadata about the service.
Description=My Service

[Service] # section contains the configuration for the service itself.

# directive specifies the path to the executable that starts the service.
ExecStart=/usr/bin/my-service

# directive to configure how the service is restarted after it exits.
Restart=always

# directive used to specify the user account under which the service should run.
User=[local machine user]

[Install] # used to configure how the service is installed on the system.

# directive specifies the target unit this service should be installed to.
WantedBy=multi-user.target
```

### Scheduling config

`/dev/null` delete anything which is navigate to it

```bash
<file path> > /dev/null 
```

```bash
crontab -e; #cronos meaning time, e - edit
```

every row is a new command.

first five columns are for scheduling, and final sixth column is command or script to be run.

follow the pattern. Asterisk means **in every** (originally any). And 5 columns separated by space are in this sequence min(0-59),hours(0-23), date of month, month, day of week.

```bash
15 * * * * echo 'hello world' >> ~/Desktop/sechedule.txt # run in every 15 min
0,15,30 * * * * #single column.
*/15 * */3 * * # run every 15 min in every 3rd day.
59 23 * JAN,DEC SUN # run on every JAN DEC on SUN at 23:59
```

deb: used to install Degian packages on a Debian-based linux distribution.

## update-alternatives

1. `link`: The link is the symbolic link to the alternative you want to manage. This link is typically found in a location like "/etc/alternatives/".
2. `name`: The name is the name of the alternative you are providing. It's a unique identifier used to reference this alternative.
3. `path`: The path is the actual location of the alternative binary or service that you want to set as an option. This should be the path to the binary of the desired alternative.
4. `priority`: The priority is an integer value used to determine the highest priority for an alternative. When you have multiple alternatives, the one with the highest priority value will be chosen as the default.

```bash
sudo update-alternatives --list <"name link">
sudo update-alternatives --remove <"name"> <"path">
sudo update-alternatives --auto <"link">

# Example
sudo update-alternatives --install /usr/bin/java java /path/to/java-version-1/bin/java 100
sudo update-alternatives --install /usr/bin/java java /path/to/java-version-2/bin/java 200
```

## APT repository

When you add a PPA to your system, you are essentially adding a new software repository. This repository contains packages that are not part of the official Ubuntu distribution but have been built and maintained by community members or third-party developers. These packages may include newer versions of software, different configurations, or entirely new applications not available in the official repositories.

- `user` refers to the Launchpad user or team that maintains the PPA.
- `ppa-name` is the name of the PPA itself.

```bash
# interact with source.list.d files.
sudo add-apt-repository -L
sudo apt-get update
```

### source list

- addition list files that specify the package repositories of the APT.
- each file inside the directory `/etc/source.list.d` can contain multiple lines of repository information. These repositories are used to download and install software packages and updates.

```bash
deb [options] <URI> <distribution> <component1> <component2> ...
## deb - indicates that it's binary package repository
## db-src - for source packages.
## [options] - are optional and can specify architecture or other APT parameters.
## <URI> - repository URL.
## <distribution> - release name (focal, bionic, buster).
## <component> - repository section (main, contrib, non-free).
```

## VISUDO

`visudo` is a command-line utility used to safely edit the system's sudoers file `/etc/sudoers`. 
- The sudoers file, typically located at `/etc/sudoers` 
- controls the privileges and permissions for users and groups to execute administrative commands.
- The `sudo` command is used to execute "visudo" with superuser (root) privileges since editing the `sudoers` file requires administrative access.

```bash
# template of sudoers fiel : 
# <user/group>  <host>=(<run as user>:<run as group>) <sepecial>: <commands to allow>
# %group_name - syntax to define group permission
john   ALL=(root)   /usr/bin/apt-get
```

1. `user_or_group`: This field specifies the user or group to whom the rule applies. It can be a specific user (e.g., "john"), a group name (e.g., "%developers"), or the keyword "ALL," representing all users.
2. `host`: This field defines the system or host-names where the rule is valid. It can be the name of a specific host (e.g., "localhost") or the keyword "ALL," indicating the rule applies to all hosts.
3. `(runas_user)`: This optional field specifies the user as whom the command should be run. If omitted, the command is executed as the root user. For example, if you want to allow a user to run a specific command as another user (e.g., "www-data"), you would include "(www-data)" in this field.
4. `commands`: This field contains the commands or command patterns that the user or group is allowed to run. It can be a specific command (e.g., `/usr/bin/apt-get`), a command with wildcard patterns (e.g., `/usr/bin/*`), or the keyword `ALL` allowing the user or group to run any command.

## Window partition types and usage

Here are some common partition types you might encounter when executing the `list partition` command:

1. **Primary Partition**: This is a standard partition that can be used to store data or install an operating system.
2. **Extended Partition**: An extended partition is a special type of primary partition that can be further divided into logical drives. It's used in the Master Boot Record (MBR) partitioning scheme to overcome the limit of four primary partitions.
3. **Logical Partition**: Logical partitions are partitions created within an extended partition. They are used in the MBR partitioning scheme to create more than four partitions on a single disk.
4. **EFI System Partition (ESP)**: This partition contains boot-related files for systems using the Unified Extensible Firmware Interface (UEFI). It's used to boot UEFI-based operating systems.
5. **System Reserved Partition**: This partition contains boot-related files for systems using the Master Boot Record (MBR) partitioning scheme and BIOS boot method.
6. **Recovery Partition**: A recovery partition contains system recovery tools and may also hold a backup copy of the operating system. It's used for system recovery and troubleshooting.
7. **OEM Partition**: An OEM partition might contain tools, drivers, or other data provided by the original equipment manufacturer. It's typically used for system recovery or customization.
8. **Data Partition**: A partition dedicated to storing user data, separate from the operating system and application files.
9. **Unallocated Space**: Unallocated space represents space on the disk that has not been assigned to any partition. It's available for creating new partitions.


## Setup auto-completion

```bash
dpkg -l | grep bash-completion
```

- copy the cli tool auto completion script
- create a file in `/etc/bash_completion.d`

```bash
source /etc/bash_completion;
```

## openssl

### for HTTPS server

```bash
openssl genrsa -out server.key 2048; # gen private key
openssl req -new -key server.key -out server.csr; # gen CSR
# gen self sign certificate
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt;
```

### terminfo
`/usr/share/terminfo` directory is a compiled database that describe the capabilities of various terminals.
- it is used by applications like terminal emulator to communicate with the terminal and take advantage of its specific features.
- entries are organized into sub-directories based on the firs letter of the terminal name (e.g. `/usr/share/terminfo/v` for viewpoint terminals)
#### Usage
- Applications like the terminal emulator use the terminfo database to determine how to control the terminal
- entries in the terminfo database are compiled from source files using the `tic` command.

### Sound
`/etc/asound.conf` ALSA settings file. User level `~/.asoundrc`