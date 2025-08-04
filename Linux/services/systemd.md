is dependent upon what init daemon is used by your Linux server.
- before you do any service management, be sure determine the init daemon.

> [!INFO] If you do not have the strings command on your Linux system, you can install it via the binutils packages.
> Your Linux server’s primary job is to offer services.

### How do you start suspend daemon?

### What if you have a special program you want to start on your server?

### How do you get it to start at boot time?

# Understanding the Linux inti Deamon
services, also called daemon, is a running program or a process that provide a particular function.

> [!INFO] init daemon: is the first process to be started by the kernel on the Linux server.
- init daemon has a parent process ID (PPID) of 0, and a PID of 1.
- Once started, init is responsible for spawning (launching) process configured to be started at the server’s boot time, such as the login shell (getty or migetty process).
- the two original Linux init daemons were BSD init and SysVinit.

Int addition, as new services came along, the classic init daemon had to deal with starting more and more services. Thus, the entire system initialization process be less efficient and ultimately slower.

- the modern init daemons have attempted to solve the problems of inefficient system boots and non-static environment. Two of these init daemon are _Upstart_ and `systemd`.

> [!INFO] In order to properly manage your services, you need to know which init daemon your server has
>  - do your lunux distribution and version appear in the preceding list of _Upstart_ adopters? Then your Linux init daemon is the _Upstart_ init daemon.
>  - Try searching your Linux distribution’s init daemon for clues, using the strings and the grep commands.

```bash
sudo strings /sbin/init | grep -i systemd
```

A run-level is a categorization number that determines what services are started and what services are stopped.

## Standard Linux Run-levels

Runlevels are primarily used for managing the system’s state during different phases, such as booting, single-user mode, or normal operation.

system administrators can switch between these targets to change thee system’s operational state.

- the default target is usually multi-user target or graphical target
- run level provide a way to control which services are running or stopped, depending on the desired system behavior.
- the ubuntu distribution, for example, offers run-levels 0-6, but run-levels 2-5 start that same services

> [!INFO] The only run-levels that should be used in the `/etc/inittab` file are 2 through 5. The other run-levels could cause problems.

On a freshly booted Linux server, the current run-level number should be the same as the default run-level number in the `/etc/rc.d/rc#.d` directory

An `/etc/rc.d/rc#.d` directory exists for all of the standard Linux run-levels. Each one contains scripts to start and stop services for its particular run-level.

```bash
ls -d /etc/rc.d/rc?.d
```

the files in the are not scripts, but instead symbolic links to scripts in the `/etc/rc.d/init.d` . Thus, there is no need to have multiple copies of particular scripts.

---

the primary difference between the classics and Upstart is the handling of stopping and starting services. The SysVinit daemon was created to operate in a static environment.

The Upstart init daemon was created to operate inn a flexible and ever-changing environment.

with SysVinit, services are stopped and started based upon runlevels.

> the upstart init daemon is not concerned with runlevels but with system events.

- events are what determine when services are stopped and or started.
- an event is a Linux server occurrence that trigger a needed system state change, which is communicated to the Upstart init deamon.

Example of system events:

- the server boots up.
- the init command is used.
- A USB device is plugged into the server.

An upstart job can be either a task or a service.

- a task performs a limited duty, complete its work, and then returns to a waiting state.
- a service, on the other hand, is a long running program that never finishes its work or self-terminates, but instead stays in a running state.
- A daemon is an example of an Upstart service job.

> events are either communicated to the Upstart init daemon or they are created by the upstart daemon, this is called emitted event.

<aside> 💡 To change the default run-level on an Ubuntu distribution that uses Upstart, edit `/etc/init/rcsysinit.conf` and change the line `env DEFAULT_RUNLEVEL=#` where # to 2 to 5,

</aside>

# Understanding systemd init

System initialization time is reduced by systemd because it starts fewer services and starts them in a parallel manner.

- In addition, systemd can handle a fluid environment because it supervices all the processes on the entire Linux server.

## Learning systemd basics

the systemd is also concerned with runlevels, but they are called target units.

- Units are focus of the systemd.
- A unit is a group consisting of a name, type, and configuration file and is focused on a particular service or action.

the eight systemd units types are:

1. automount
2. device
3. mount
4. path
5. service
6. snapshot
7. socket
8. target

<aside> 💡 The two primary systemd units you need to concerned with for dealing with service are service units and target units.

</aside>

A service unit : is for managing daemons on your Linux server

A target unit : is simply a group of other units.

sysinit is used for starting up services at system initialization.

```bash
systemctl list-units | grep .service
```

- the Linux system unit configuration files are located in the `/lib/systemd/system` and `/etc/systemd/system` directories

<aside> 💡 the static is slightly confusing. It stands for “statically enabled” and it means that the unit is enabled by default and cannot be disabled, even by root.

</aside>

---

The basic service unit configuration file has the following options:

- Description : this is a free-form description (comment line) of the service.
- After : this setting configures ordering. In other words, it lists which units should be activated before this service is started.
- Environment File : the service’s configuration file.
- ExecStart : the command used to start this service.
- ExecReload : the command used to reload this service.
- WantedBy : this identifies what target unit this service belongs to.

```bash
# view the various units a target unit will active
systemctl show --property "wants" multi-user.target;
```

---

A target unit has both wants and requirements, called Requires.

A _Wants_ means that all the units listed are triggered to activate (start). if they fail or cannot be started, no problem.

A _Requires_ means that all the units listed are triggered to activate. if they fail or cannot be started, the entire unit (group of units) is deactivated.

---

## Target units

Description : this is just a free-form description of the target

Requires : then the listed target unit will also be activated. if the listed target unit is deactivated or fails, the the parent will be deactivated.

- if their are no After and Before options, then both the parent and listed target unit will activate simultaneously

Conflicts : this setting avoids conflicts in service. Starting parent target unit will stop the listed targets and services and vice-versa.

After : this setting configures ordering. In other words, it determines which units should be activated before starting this service.

AllowIsolate : this option is a Boolean setting of yes or no.

- if set to yes, then this target unit is activated along with its dependencies and all other are deactivated.

ExecStart : this command starts the service.

ExecReload : this command reloads the service.

Alias : with this command, systemd will create a symbolic link from the target unit names.

---

Reloading a service is different from restarting a service. When you reload a service, the service it self is not stopped. Only the service’s configuration files are loaded again.

# Configuring Persistent services

A persistent service is one that is started at server boot time.

- using the _enable_ option on the systemctl command will set a service to always start at boot ( be persistent ).
- The _enable_ option simply creates a few symbolic links.

You can use _disable_ option on the systemctl command to keep a service from starting at boot.

- However it does not immediately stop the service you need to use the stop option discussed in the section
- the disable option simply removes a few files via the preferred method of the systemctl command.

## Configure a Default runlevel or target unit

simply edit the `/etc/inittab` file using the editor and change the 5 run level to 2,3,4, Do not use the run levels 0 or 6 in this file! This would cause your server to either halt or reboot when it is started up.

- some uses this file, where other uses `/etc/init/rc-sysint.conf` file.

# Adding new or Customized Services

1. create a new or customized service script file.
2. Move the new or customized service script to the proper location for SysVinit management.
3. Add the service to a specific runlevel(s).

<aside> 💡 if you are creating a new script, you will need to make sure you handle all the various options you want the service command to accept for your service, such as _start, stop, restart_ and so on.

</aside>

- once you created a script move it to proper location `/etc/rc.d/init.d`
- the final step is needed only if you want the service to be persistent at certain runlevels.
    - you must create symbolic link for every runlevel at which you want the service to be persistent.
    - check each run-levels directory you want service to start on
    - determine what the appropriate _S number_ should be for your service.
- once you have made the symbolic links, test that your new or modified service will work as expected before performing a server reboot.

The Upstart service job configuration files are located in the `/etc/init` directory, These files are plain text only.

```bash
# cat cron.conf
# cron - regular background program processing daemon
descripton "regular background program processing daemon"

start on runlevel [2345]
stop on runlevel [!2345]

expect fork
respawn

exec cron
```

- the expect : this particular stanza is rather important, the _expect_ fork syntax will allow Upstart to track this daemon and any of its child process (forks).
- respawn : the stanza here tells Upstart to restart this service should it ever be terminated via a means outside of its normal stop on.

```bash
man upstart-events
```

### Adding new services to systemd init

1. Create a new or customized service configuration
2. move the new or customized service configuration unit file
3. add the service to a specific target unit’s wants if you want to have the new or customized service start automatically with other services.

make copy from `/lib/systemd/system`

```bash
[unit]
Description=My new Service

[service]
ExecStart=/usr/bin/my_new_service

```
- there are two potential locations to store service configurations unit files.

> [!INFO]
> - `/ect/systemd/system` : used to store customized local service configuration unit files
> - files in this location are not overwritten by software installations or upgrades
>

> [!INFO]
> - files here are used by the system _event_ if there is a file of the same name in the `/lib.systemd/system` directory
> - Notice that in this directory, the files are symbolic links pointing to service unit configuration
> - `/lib/systemd/system` : store system service configuration unit files
> - files in this location are overwritten by software installations and upgrades.
> - files here are used by the system only if there is not a file of the same name in the `/etc/systemd/system` directory.

<aside> 💡 When you create a new or customized service, in order for the change to take effect without a server reboot, you will need to issue a special command

</aside>

```bash
systemctl daemon-reload
```

- to add a new _service unit_ to _target unit_ you need to create a symbolic link.

```bash
ln -s /etc/systemd/system/my_new_service \\
/etc/systemd/system/multi-user.target.wants/my_new_service.service
```

<aside> 💡 If you want to change the `*systemd target unit`* of a service you will need to change the symbolic link to point to a new target want directory location.

</aside>

- use the -sf command option to force any current symbolic link too be broken and the new designated symbolic like to be enforced.