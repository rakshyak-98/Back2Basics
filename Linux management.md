[system administration YT](https://www.youtube.com/watch?v=UCr04qIB7uc&t=22578s)

[updating drivers](https://ubuntu.com/server/docs/nvidia-drivers-installation)

[manual config sudoedit](https://www.digitalocean.com/community/tutorials/how-to-edit-the-sudoers-file)

---
atk : Accessibility Toolkit

### system user sudo
system user - individual, or (system) process acting on behalf of an individual, authorized to access a system.

- an individual that is authorized to access information and information system to perform assigned duties.

```bash
# list manually installed packages
comm -23 <(apt-mark showmanual | sort -u) <(gzip -dc /var/log/installer/initial-status.gz | sed -n 's/^Package: //p' | sort -u)
```

### GRUB

```bash
sudo nano /etc/default/grub # change quite splash to nomodeset.
sudo update-grub
sudo dpkg --list | grep -E -i --color  "linux-image|linux-headers"; # list installed kernals.
```

- **Keyring**: In GnuPG, a keyring is a file or database that stores cryptographic keys. There are two primary types of keyrings: "pubring.kbx" for public keys and "secring.gpg" for secret (private) keys.
- **Public Keys**: "pubring.kbx" specifically stores public keys. Public keys are used to verify digital signatures and encrypt data that can only be decrypted by the corresponding private key.
- **Key Database Format**: The "kbx" in "pubring.kbx" stands for KeyBox, which is the format used to store the keys. It's a modern keyring format used by GnuPG and is more efficient and secure than older formats.

## Users

user groups - are used to give several access permissions.

`/etc/passwd` - information about user home directory.

passwords are stored in the `/etc/shadow`

```bash
useradd -m john # create a user john with home directory.
usermod -s /bin/bash john; #setting the shell for the john user.
useradd -d $USER <dir name># set the home directory for the user account.
useradd -g [groupname] [username];
useradd -e [yyyy-mm-dd] [username]; # new user account with expiration date.
useradd -c [comment_for_user] [username]; # set user comment.
```

```bash
w; # show information of current user.
id; # show ids.
pkill -KILL -u $USER; # logout current user.
finger; # info login name, real name, contact.
chsh; # change the default login shell for current user.
chage; # changes the again paramters for a user account. (password expiration).
whoami;
userdel;
useradd;
last; # info about previous user logins.
fuser -all; # process using file.
```

## Apt Package management

#### basic packages
```bash
apt install shadow; # include useradd ... packages.
```
see the package log file `/var/log/dpkg.log`

```bash
apt show <package name>
apt search <package name> # 
apt depends <package name>
apt-cache pkgnames; # list all the installed packages in system.
apt-get install -f; # fix broken package.

apt-mark showhold;
apt list --upgradable --all-versions;
apt-mark unhold [package name];

# download the gpg public key
curl -fsSL <https://download.docker.com/linux/ubuntu/gpg> | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
# sign and update the sourc list
echo \\
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] <https://download.docker.com/linux/ubuntu> \\
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \\
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Held packages - refers to packages in a package management system (apt) that have been marked as being held back and will not be upgraded or installed automatically.

- happen for conflicts with other packages, or package being considered too risky to upgrade.
- can check which packages are being held back by running the command

## configured ports

`etc/services` has all the default used port configurations.

## openssl command

de facto meaning - existing or holding a specified position in fact but not necessarily by legal right.

```json
ls /etc/ssl/certs; # list system ca certificates pre installed.
sudo update-ca-certificates --fresh; # update the CA certificates bundle.
```

### generate an API key pair

```bash
openssl genpkey -algorithm RSA -out private_key.pem
openssl rsa -pubout -in private_key.pem -out public_key.pem

# [ generate fingerprint ]
openssl rsa -pubin -in public_key.pem -outform DER \\
| openssl dgst -sha256 -binary \\
| openssl enc -base64
```

checking certificate validity

```bash
# connect request
openssl s_client -connect redhat.com:443 -brief
openssl s_client -connect redhat.com:443 -brief -time 10

# generate private key
openssl genpkey -algorithm RSA -out private_key.pem -aes256 # with pass phrase
openssl genpkey -algorithm RSA -out private_key.pem # without pass phrase
openssl ecparam -name secp256k1 -genkey -noout -out private_key.pem

# generate CSR
openssl req -new -newkey rsa:2048 -nodes -keyout private.pem -out .csr

# verify certificate
openssl verify -CAfile /path/to/your/chain.crt /home/rakshyak/build/csr.crt

openssl req -text -noout -verify -in [csr.crt];
openssl rsa -in <private.key> -check; # to check made with rsa algo.

openssl req -inform DER -in csr.der -out csr.pem -outform pem;
opemssl rsa -in private.der -out private.pem -outform pem;
```

SHA256 key fingerprints or SHA256 hash, or checksum are used to verify the authenticity and integrity of cryptographic keys.

- ref
    
    [https://www.freecodecamp.org/news/the-ultimate-guide-to-ssh-setting-up-ssh-keys/](https://www.freecodecamp.org/news/the-ultimate-guide-to-ssh-setting-up-ssh-keys/)
    
    [https://www.youtube.com/watch?v=33dEcCKGBO4](https://www.youtube.com/watch?v=33dEcCKGBO4)
    

you need different ssh key to pull from different git repository.

```bash
ssh-keygen -t rsa -b 4096 -C 'comment'; # generate public and private key. 
ssh-add id_rsa;
ssh-keygen -lf [filename]; # get the fingureprint of the key private/public.
```

t - type of algorithm

b - bits size

C - comment

> fixed-length string of characters, typically represented in hexadecimal format.

### Setup SSH config

- create `~/.ssh/config` config directive.

```jsx
Host github-repo
    HostName github.com
    User git
    IdentityFile /path/to/custom/keys/repo_private_key
```

> the username `git` is commonly used. This is because when you clone a repository over SSH, you connect to the `git` user on the GitHub server.

### how to setup public key authentication

```bash
# on window use putty
ssh-keygen -b 4096 
ssh-copy-id [username@ipaddress]
```

[https://linuxhint.com/ssh-keyscan-ubuntu/](https://linuxhint.com/ssh-keyscan-ubuntu/)

```python
ssh-keyscan hostname
ssh-keyscan -p [port] hostname
ssh-keyscan -t [rsa | dsa | ...] hostname
```

### test key

```jsx
ssh -i /path/to/private/key username@hostname
```

> Remember that the `HostName` should be the actual hostname or IP address of the remote host, while the `Host` is a custom name you choose to represent that host in the SSH config file.

## System management

limiting resources - is valuable in environments with multiple users and system performance issues.

- file path - `/etc/security/limits.conf` . Changing the values in the file persist after system reboot.

```bash
jobs;

lsusb; # list USB devices.
sudo sync; # to flush the filesystem buffers, all buffered data to be written to disk.
lspci; # list PCI devices.
lsblk; # disk partitions.
lsof -P -i; # P no port names, i : show ipv[46]
sudo lshw; # list hardware information.
lscpu; # CPU architecture.
df <"-h | -H"> ; # Disk space usage.
top; # real-time resource usage, CPU and memory.
free: # memory usage and availability.
uptime; # system has been running.
hostname; # system's hostname.

dig google.com +short
dig google.com +trace

# [service]
systemctl list-timers;
sudo systemctl list-unit-files --type=service;
sudo systemctl reset-failed [service name];
systemctl; # controls systemd system and service manager.
service; # controls sys services managed by init system.
ps;
top; # show real time system resource usage info.
kill;
shutdown;
reboot;
uname;
poweroff;
df; # info disk space udage on the system.
du; # info disk udage of files dand directories.
lsblk; # info about storage devices and partitions.
mount;
unmount;
lsof; # list open files and process that opened them.

# [network]
iptables -L # Displays the current firewall ruleset.
iptables -F # Flushes (deletes) all firewall rules.
iptables -A # Appends a new rule to the end of the firewall ruleset.
iptables -I # Inserts a new rule at a specific position in the firewall ruleset.
iptables -D # Deletes a specific rule from the firewall ruleset.
iptables -P # Sets the default policy for a chain (ACCEPT, DROP, or REJECT).
iptables -N # Creates a new user-defined chain.
iptables -E # Renames a user-defined chain.
iptables -Z # Resets the packet and byte counters for a chain.
iptables-save # Saves the current firewall ruleset to a file.
iptables-restore # Restores a saved firewall ruleset from a file.

pgrep [name];
pstree -p -u -a; # show -p show pids | -u uid transitions | -a command line argument.

ps aux;
ps [username];
ps -e --forest;

hostnamectl set-hostname [new system name];

sudo -l; # check to see if privileged account on this machine.

ulimit -a; # to check system limits.
```

is an init system. `systemctl` command, is the central management tool for controlling the init system.

units - A unit file is a plain text int-style (a configuration file for computer software that consists of a text-based content with a structure and syntax) file that encodes information about a service, a socket, a device, a mount point, an auto mount point, a swap file or partition, a start-up target, a watched file system path, and supervised by **systemd.**

A unit configuration file whose name ends with `.service` encodes information about a process controlled and supervised by systemd.

```bash
systemctl start [.service]
systemctl status [.service]
systemctl list-unit-files
sysremctl list-unit --type=service
```

## service management

the fundamental purpose of an init system is to initialize the components that must be started after the Linux kernel is booted (`userland` components).

In `systemd` the target of most actions are units, which are resources that `systemd` knows how to manage. Units are categorized by the type of resource they represent and they are defined with files known as unit files. for service management tasks, the target unit will be service units, which have unit files with a suffix of `.service` .

### starting and stopping services

```bash
systemctl start application.service
# or
systemctl start application

systemctl stop application.service
systemctl restart application.service
systemctl reload application.service
systemctl reload-or-restart application.service
```

```bash
sysctl -a; # display all kernel parameters and their current values.
sysctl -w [parameter]=[value]; # set the value of a kernel parameter.
sysctl -p [file]; # reads the specificed file and sets the kernel.
```

sysctl - command in Linux used to modify kernel parameters at runtime. These parameters are stored in the `/proc/sys` directory and can be used to configure various aspects of the system, such as network settings, kernel settings, and more.

- display the current value of a kernel parameter, as well as to change the value of a kernel parameter.
- the changes made `sysctl` are not persistent across reboots, it is a way to configure system behavior on runtime. it is recommended to use `/etc/sysctl.conf` to make persistent across reboot.

### enabling and disabling services

```bash
sudo systemctl enable application.service
```

this will create a symbolic link from the system’s copy of the service file (usually in `/lib/systemd/system` or `/etc/systemd/system` ) into the location on disk where `systemd` looks for auto-start files.

```bash
sudo systemctl disable application.service # this will remove the symbolic link
```

### checking status of service

```bash
sudo systemctl status application.service
```

this will provide you with the service state, the `cgroup` hierarchy, and the first few log lines.

```bash
sudo systemctl is-active application.service; # stdout the state is active or inactive
sudo systemctl is-enabled application.service; # stdout the state is enable or disable
# this will active if it is running properly or failed if an error occured. if the unit was
# intentionally stopped, it may return unknown or inactive.
sudo systemctl is-failed application.service 
```

### system state overview

```bash
systemctl list-units; # show the list of current running services.
# UNIT - systemd unit name
# LOAD - the unit configuration has been parsed by systemd.
# ACTIVE - a summary state about whether the unit is active.
# SUB - this is a lower-level state that indicates more detailed information about the unit.
# DESCRIPTION - a short textual dscription of what the unit does.
```

```bash
systemctl
# only displays units that systemd has attempted to parse and load into memory.
systemctl list-units 
systemctl list-units --all
systemctl list-units --all --state=inactive
systemctl list-units --type=service
systemctl list-unit-files # include those that systemd has not attemoted to load.
#static - means that the unit file does not contain an install section.
```

static units cannot be enabled, this means the unit performs a one-off action or is used only as a dependency of another unit and should not be run by itself.

`systemd` only read units that it thinks it needs, this will not necessarily include all of the available units on the system.

## Firewall

[ufw guid](https://help.ubuntu.com/community/UFW)

## Terminate process

### processes
```bash
echo $$; # represent the current process id
pidof <process>; # get the process id
pidstat -p <pid>; # get the stat of the process
strace -f -p <pid> -o <output file>;
readlink <symbolic link file>;
```

### signals
- **SIGHUP (1):** Hang Up. This signal is often used to instruct daemons to reload their configuration files or restart gracefully. It can also be used to disconnect a process from its controlling terminal.
- `kill -1 PID`
- **SIGINT (2):** Interrupt. This signal is typically generated when you press Ctrl+C in the terminal. It's used to request a process to terminate cleanly.
    ```
    kill -2 PID
    ```
- **SIGQUIT (3):** Quit. This signal is similar to SIGINT but can be used to request a process to terminate and produce a core dump for debugging purposes.
    ```
    kill -3 PID
    ```
- **SIGTERM (15):** Terminate. As mentioned earlier, SIGTERM is used to request a process to terminate gracefully. It allows the process to clean up and release resources.
    
    ```
    kill -15 PID
    ```
    
- **SIGUSR1 (10) and SIGUSR2 (12):** User-defined signals. These signals can be used for custom actions within a process. Their behavior depends on how the process is programmed to respond to them.
    ```
    kill -10 PID # SIGUSR1
    kill -12 PID # SIGUSR2
    ```
    
- **SIGSTOP (19) and SIGCONT (18):** Stop and Continue. SIGSTOP is used to pause a process, and SIGCONT is used to resume it. These signals do not terminate the process but allow you to temporarily halt and restart it.
    
    ```
    kill -19 PID # SIGSTOP
    kill -18 PID # SIGCONT
    ```
    
- **SIGTSTP (20) and SIGTTIN (21) and SIGTTOU (22):** Terminal-related signals. SIGTSTP is sent when you press `Ctrl+z` in the terminal to suspend a process. SIGTTIN and SIGTTOU are used when background and foreground processes attempt to read from or write to the terminal, respectively.
    
    ```bash
    kill -20 PID  # SIGTSTP (Ctrl+Z)
    ```

## Hardware

```bash
# to list available sound cards. If none are listed, 
# it indicates a problem with sound card detection or drivers.
aplay -l;

pacmd; # this command provides control over PulseAudio's configuration.
alsamixer; 
```

### passwd

```bash
passwd -l [user] #lock the user to use login password.
passed -u [user] #unlock user.
echo 'userpassword' | passwd --stdin [user] #read password from standard input.
```

### group

> Password field: Historically, this field stored an encrypted password, but modern systems use an "x" or "*" character to indicate that the encrypted password is stored in the `/etc/gshadow` file.

```bash
id <username>; # to see the groups related to the user with group id.
getent group 1001; # check if group exist.
gorups <username>; # to see the groups of the user without group id.
chgrp [group] [file or directory]; # change the associated group.
usermod -aG [group name] [user name]; # append supplimentary group.
usermod -ag [group name] [user name]; # force group as primary group.
gpasswd -d username groupname; # remove user from the group.
```

- users can be members of multiple supplementary groups, allowing them to share resources and permissions with other users in those groups.

dip - Daemons, system and network management group, is a group on a linux system that is typically used to control access to certain system-level functions and resources.

member of the dip group are typically considered to be privileged user and are granted access to certain system-level commands and files that are not available to regular users.

dip group can give users access to manage and configure system daemon, network interfaces, system logs. Member of this group are also allowed to reboot the system, run system updates.

On Ubuntu systems, the dip group is typically used to control access to the `sudo` command, which allow users to execute commands with superuser privileged. Member of the group dip are allowed to use `sudo` command to perform certain system-level tasks, such as installing software or changing system settings.

samba-share - provides file sharing and print services for computers on a network. It uses the server message block and common internet file system (SMB/CIFS) protocol, so the services created by running samba are available to Linux.

# Managing Process

```bash
ps -ef; # shows all the aunning processes on the system. Parent process, user id.
ps aux; # more detaild information abot each process.
ps -eo pid,user,cmd,%cpu,%mem; #displays a custom output. the command used to start process.
ps -C [process_name]; # info on specific process.
ps -p [process_id]; # info on specific process matches the process id.
ps -eo pid, ppid,%cpu,%mem,cmd;
ps --sort="-rss"
```

```bash
pgrep [appname]; # to see if the bin file is running /*/bin

# [process status commands]
ps $USER; # so current running process.
ps -T; # show process whit tty attached to it.
ps -e; # stands for every process.
ps -P [parent PID]; # to see all the process associated with the parent process.
ps; # to see the threads running on and Ubuntu system.
ps t; # select all the process associated with this terminal.

sleep 3 &; # & to run in the background.
mkdir testDir \\ #line break.

ps -0 ; # user defined format.
ps -Lp [PID]; # to see the threads of a specific process.

pstree -p; # see the threads (with pid).
pstree -p [pid]; # to see specific process tree.
pstree -p -u -a; # commnly combination flag.
pstree -c | -g | -h;
```

### Upgrade system OS version

```python
sudo apt update && sudo apt upgrade -y
sudo apt install update-manager-core
sudo nano /etc/update-manager/realease-upgrades; # change Prompt=never to Prompt=lts
sudo do-release-upgrade
```

## Archive

`gzip`, `pizip`, `bzip`,

tar ball - is a jargon term for a TAR archive - a group of files collected together as one.

GNU tar is an archiving program designed to store multiple files in a single file (an archive), and to manipulate such archives.

-c - create,

-v - verbose

-f - accept files

-j - for `bzip` algo

-z - for `gz` compress data

```bash
tar -c [new.tar] file[1-3].txt # creat a tar without using a compression algo.
zip ourarchive.zip file1.txt file2.txt; # output as stdout and files without extracting them.
tar -czvf ourarchive.tar.gz file[1-3].txt # create tar and compress usign gzip algo.
tar -cjvf ourarchive.tar.bz2 file[1-3].txt # create tar and compress using bzip2 algo.

```

```bash
tar -tf [.tar]; # to inspect .tar.
tar -tvf [.tar];

# extract the archive and avoid overwriting existing files.
tar -xf [tar archive] --no-overwrite-dir; 
```

to know the file format `file` .

`tar -t archive.tar` - to know what inside the tar ball. it list the file inside the tar archive.

`tar -x archive.tar` - to extract into the current path.

POSIX tar archive - also known as a tarball, is a file format used to bundle a st of files together into a single archive file.

POSIX stands for Portable Operating System Interface. defines a set of specifications for how tar archives should be created and formatted.

### compression algo

```bash
$ gzip archive.tar
$ bzip2 archive.tar
```

to unzip

`gunzip` - to unzip the `gaiz` `archive.tar`

### un-ziping in one step

```bash
$ tar -xzvf archive.tar.gz
$ tar -xjvf archive.tar.bz2
unzip <file.zip>
```

# Files

```bash
unlink <"filename">; # number of links, goes to zero the memory is released.
mv <"current path"> <"new path">; # udpate the path.
grep <"string"> <"file path">; # find text as content of a file.
```

file system table : refers to the `/etc/fstab` file, which stands for file system table. is an essential configuration file that contains information about how various file system should be mounted and managed when the system boots.

```bash
find /path/to/search -name filename.txt
find /path/to/search -mtime -N
find /path/to/search -size +10M
find /path/to/search -name filename.txt -delete
find /path/to/search -maxdepth 2 -name "*.txt"
find /path/to/search -name "*.txt" -ls
find /path/to/search -type f -perm 644

# [advance]
find /path/to/search -name "*.txt" -mtime -7
# Find files by combining multiple criteria with OR logic:
find /path/to/search \\( -name "*.txt" -o -name "*.log" \\)

find /path/to/search -name "*.txt" -not -path "/path/to/search/exclude"
find /path/to/search -name "*.txt" -exec command {} \\;
find /path/to/search -name "*.txt" -exec tar czvf archive.tar.gz {} +
```

# Links

```bash
# hard link : link to the memory of the content in the system.
# soft link : link to the registerd path of the source.
ln <"option"> <"target"> <"destination">
```

# Partitions

partition table : is a data structure used in computer storage devices, such as hard drives and SSDs to define the division of the storage space. Each partition within a storage device is like a separate logical drive, with its own file system and data.

MBR : Master Boot Record

GPT : Global unique Identifier Partition Table.

```bash
fdisk -l ; # list the disk partition. Linux partition good.
mkfs ; # see the file system.
tuen2fw -j; # add a journal.
mount; # 
unmount;
blkid; # print the universally unique identifier for a device.
```

## Hardware

```python
lsusb;
lspci -vv;
lsmod;
modeprob -a;
```

## Cat command

```bash
cat > newfile.txt
This is some text.
Press Ctrl+D to save.
```

```bash
cat file.txt file2.txt > combined.txt
cat -n file.txt
cat -v file.txt
cat -A file.txt
tac file.txt
```

```bash
for file in file1.txt file2.txt; do
    echo "File: $file"
    cat $file
done
```

## system commands

PCI: "Peripheral Component Interconnect." It is a standard interface used in computers and servers to connect various hardware components, such as expansion cards, graphics cards, network cards, and other peripheral devices, directly to the motherboard.

PCI allows these components to communicate with the computer's central processing unit (CPU) and memory, enabling them to function as part of the overall system.

**Hot-Plugging**: Some PCI standards, like PCI Express (PCIe), support hot-plugging, which allows you to connect or disconnect devices while the computer is running without requiring a system restart. This feature is particularly useful for servers and systems that need to be operational at all times.

**Configuration**: The PCI interface allows devices to be configured and controlled by software. The computer's operating system communicates with the devices using drivers and manages their resources.

### sync command

When you use a computer, the data that you create or modify is often stored in the computer’s memory (RAM). This is because it is faster to access data from memory then from a hard drive or other storage device.

to make sure that your data is not lost when the power is turned off, the computer writes the data to a storage device (Hard drive) on a regular basis.

the `sync` command is a Linux utility that forces the computer to write all buffered (unwritten) data to the storage device, ensuring that all data is saved before the system is shut down.

by running the `sync` command before shutting down the system, you can be sure that all of your data has been written to the storage device and will not be lost when the power is turned off.

# Setup ssh between two linux instances

```bash
apt install openssh-server;
ssh -i "pem file location" -L 8090:0.0.0.0:8080 "hostname" # port forward
```

`/etc/ssh/sshd_config` You can make various changes in this file, such as changing the default SSH port, disabling root login, or using key-based authentication. After making changes, save and exit the editor.

# Grand Unified Boot loader `grub`

- Bootloader - a program that is responsible for loading the operating system kernel into memory and starting it.

- BIOS boot - Basic Input Output System. A firmware program that is stored on a ROM chip on the motherboard of a computer. When the computer is turned on, the BIOS performs a series of checks and initialization, and then searches for and loads the bootloader.

- kernel initialization - once the kernel is loaded into memory, it performs a series of initialization tasks, such as setting up the device drivers, mounting the root filesystem, and starting the init process.

- init process - the first user-space process that is started by the kernel. It is responsible for starting other system process and services, as well as running the system initialization scripts.

> NOTE: ⚠️In some cases, there might be compatibility issues or conflicts between the default graphics drivers and certain hardware configurations or graphics cards. These issues can lead to problems such as a blank screen, graphical glitches, or an inability to boot properly