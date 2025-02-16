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
