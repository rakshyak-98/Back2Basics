[cheat sheet](https://last9.io/blog/linux-commands-cheat-sheet/)
[gnu error codes](https://www.gnu.org/software/libc/manual/html_node/Error-Codes.html)
[remove prompt for default key-rings password on login](https://askubuntu.com/questions/867/how-can-i-stop-being-prompted-to-unlock-the-default-keyring-on-boot)

> [!INFO]
> In bash, the variable `$1` refers to the first command-line argument passed to the script or function

```shell
timedatectl list-timezones;
```

```
# shortcut key
ctrl + r - reverse history
ctrl + a, ctrl + e - move to start of line or end of line.
ctrl + u, ctrl + k - delete text before or after.
ctrl + z - suspend process and to ruseme use fg.
ctrl + d - to close current session terminal.
```

```bash
# reset terminal keybindings dconf reset -f /org/gnome/terminal/legacy/keybindings/
echo $$; # get the PID of bash
show <parameter>; # show the value of a run-time parameter
for i in {0..255}; do printf "\x1b[38;5;${i}mcolour${i}\n"; done # test color support
```

verbose meaning - expressed in more words then needed.

```bash
gio trash # use gio utility trash instead of rm
sed -i.bak 's/old__string/new_string/g' <"file name">
echo $?; # print the last execution exit code.
ls -1 /path/to/directory | wc -l; # count file in a directory.
echo "hello" | tee -a existing_file.txt; # read from standard inputs usually provided from pip line.

# [ move file ]
mv -p "source" "destination"
Update version
time python -c ''
```
time command
- Real time (real) Total elapsed time from start to finish.
- User time (user) CPU time spent in user mode.
- System time (sys) CPU time spend in kernel mode.
```bash
time -p <args>; # POSIX-sompilant output format
time -o <args>; # Redirect output to a file
time -f <args>; # Customize output format
```

### `gsettings` 
	
```bash
gsettings set org.freedesktop.ibus.panel.emoji hotkey '@as []'

gsettings get org.gnome.Terminal.ProfilesList default; # get profile

# theme
gsettings get org.gnome.desktop.interface gtk-theme
gsettings set org.gnome.desktop.interface gtk-theme 'Yaru-dark'
```

```bash
gnome-default-applications-properties
```

```bash
PROFILE_ID=$(gsettings get org.gnome.Terminal.ProfilesList list | grep -o "'[^']*'" | tr -d "'")
gsettings list-recursively "org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:$PROFILE_ID/"
```

```bash
gsettings set "org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:$PROFILE_ID/" use-theme-colors false
gsettings set "org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:$PROFILE_ID/" background-color '#282A36'
gsettings set "org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:$PROFILE_ID/" foreground-color '#F8F8F2'
gsettings set "org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:$PROFILE_ID/" palette "['#000000', '#FF5555', '#50FA7B', '#F1FA8C', '#BD93F9', '#FF79C6', '#8BE9FD', '#BFBFBF', '#4D4D4D', '#FF6E67', '#5AF78E', '#F4F99D', '#CAA9FA', '#FF92D0', '#9AEDFE', '#E6E6E6']"
```

```bash
gsettings set "org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:$PROFILE_ID/" bold-color '#FFFFFF'
gsettings set "org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:$PROFILE_ID/" bold-color-same-as-fg false
```

# Update to latest Linux desktop

```bash
lsb_release -a; # check latest stable release

# steps:
# 1 : change the prompt=normal at /etc/update-manager/release-upgrades
# 2 : change prompt=lts to prompt=normal;
sudo do-release-upgrades;
```

# STDIN, STDOUT, STDERR

# system boot timeout config in window 11

win + i > system > about > system protection > advanced > startup and recovery (settings)

`sudo make install` : you are telling the system to execute the instructions in the make-file with administrative privileges, which will build the software and then install it on the system. `make` this is a tool that reads a set of instructions in a make-file and builds the software according to those instructions.


> [!INFO] you have already run the `./configure` command to set up the build environment.

```bash
date +%y-%m-%d-%H-M%-%s;

echo -e "\\n\\t\\r" # enables interpretation of escape sequence

sudo install -o root -g root -m 0755 [file binary] [absoulte path destination];

service [unit name] [status | restart | stop | start]

## user
sh -c [string command to execute]; # read from string. if there are arguments after the string, they are assigned to the pointional parameters.
sh -i; # the shell is intrective.
sh -s; # read from standard input.

## device
sudo mkfs.vfat /dev/sdb1; # format pandrive.
sudo umount /dev/sdb1; # unmount pandrive.

## file system
cat -n <file name>; # show the line number.
ls */**; # list nested files.
ls -i [filename]; # to see the associated file number (inode).
tail -f [file name] # to follow in the stdout.
cut -d ":" -f1 /etc/passwd;

## firewall
ufw status; # check firewall status.
ufw show; # show firewall current configurations rules.
ufw logging; # show current logging level.
ufw app list;
ufw allow 3000/tcp;
ufw reset;
ufw delete allow;

## system commands
free -h [-m | -g]; # see memory usage.

# disk usage space used by the flles and directories in a directory tree.
du -ch --max-depth=1 --apparent-size --exclude="*.mp3" [directory name];
du -sh; # see disk space -s total disk usage for each specified file.
ls -l;
# disk file system. tmfs -temperory file system.
df -k --local --type=<TYPE 
[ext4 | xfs | ntfs | nfs | tmpfs | fuseblk | cifs | all]
>;
df -a --type=all;
df; # amount of available and used disk space on all mounted file system.

unmount; # unmouunt file system.
mount; # mount file system.

# fix broken grub config
sudo apt-get install --reinstall ubuntu-desktop;
```

`chmod` use to grant user, group and other read, write, and execute permissions, `chmod a-x` execute permission for all users. `x` execute, `w` write, `r` read. `a` all user `u` current user `o` other. `rwx-rw-x` it is in the format `ownerOfFile-groupOfOwner-others`. this can be done with octal 761 ( in binary 111, 110, 001) `rwx` to give permissions.

access the environment variables `echo $ENVIRONMENT_VARIABLE_NAME`.

to add environment variable `export` example- `export PATH=$PATH:$(pwd)` this will add the present working directory.

```bash
chmod -s /bin/bash; # change the login shell for the current user;
```

pager in UNIX - helps the user get the output one page at a time, by getting the rows of the terminal and displaying that many lines.

- a terminal pager, or paging program, is a computer program used to view (not modify) the contents of a text file moving down the file one line or one screen at a time.
- some, but not all, pagers allow movement up a file.
- `less` `more` are a pager program. `-p` for `man` specify which output pager to use.

Btrfs - B-Tree File System. Is the default file system for the operating system and XFS is the default for all others use cases. ex: mongodb.

- write in a new location then link the change in, until the last write, the new changes are not committed.
- COW - copy on write.

# crontab

Cron jobs are particularly useful for automating repetitive or scheduled tasks on a server.

It is denoted by a forward slash (/) followed by a number. This can be useful when you want a job to run at regular intervals within a specified range.
 
```bash
crontab -e
crontab -l
```

```
30 3 * * * /path/to/script.sh

#Run a job every Monday and Wednesday at 3 PM:
0 15 * * 1,3 /path/to/job

#Run a job every 2nd hour:
0 */2 * * * /path/to/command

#Run a job every 30 minute between 9am and 5pm
0,30 9-17 * * * /path/to/job
*/10 9-17 * * * /path/to/script.sh
```

### ln (link)

inode - is a data structure that keeps track of all the files and directories within the Linux or UNIX-based filesystem.

**hard link:** use to create replica as, deleting the linked file will not effect the content.

**soft link:** use to create run source link files, as if the source is removed, it broke the link and loose all the content.

- identified by an integer known as _inode number._ These unique identifier store metadata about each file and directory.

In command is used to create hard links and soft links (system link) for files in Linux.

- hard link - is a file its own, and the file references or points to the exact spot on a hard drive where the inode stores the data.
- soft link - is not a separate file, it points to the name of the original file, rather than to a spot on the hard drive.
- symbolic link - points to another file or folder on Linux or UNIX-based computer, or a connected file system.

### ps1

is one of the few variables used by the shell to generate the prompt.

- PS1 represent the **primary string process.**

### process
```bash
nsenter -t <pid> -m -u -i -n -p /bin/bash
```
- pts - pseudo terminal slave.
 -tty - teletypewriter.
- pts - first terminal pseudo terminal slave window. A pair of virtual terminal devices that allow a terminal emulator gnome-terminal to communicate with a program as if it were a terminal.
- The master end of a pseudo terminal is connected to the terminal emulator, where a slave end is connected to the program. The slave end is identified by a device name that begins with `pts/` followed by a number that identifies the specific pseudo terminal.

> `pts` notation is specified to Unix-like systems, and may not be used on other operating systems.

- SPID - system process id. Identify the process internally. Used to track the process across different terminal sessions.

- STAT - stands for status.
- D - Uninterruptible sleep (usually input or output).
- R - running or run-able
- S - interruptible sleep (waiting for an event to complete)
- T - stopped, either by a job control signal or because it is being traced.
- Z - defunct (zombie) process, terminated but not reaped by its parent.
`tty` column - display the terminal device associated with a process.

### sha bang

directive meaning - an official or authoritative instruction.

- involving the management or guidance of operations.

shebang is the character sequence consisting of the characters `#!` when a text file with a shebang is used as if it is an executable in a Unix operating system, the program loader mechanism parses the rest of the file’s initial line as an interpreter directive. The loader executes the specified interpreter program, parsing to it as an argument using the path that was initially used when attempting to run the script, so that the program may use the file as input data.

### kill process

`pgrep -l -u $USER` list the process and get the process id, user `kill` command to kill the process.

```bash
kill -l; # list all the signal names;
sudo lsof -i -P -n | grep LISTEN
kill -s QUIT [process id]
```

### kill a process by name not pid

`pkill [process name]`

### open ssh client

Ssh - Secure Shell is a program for logging into a remote machine and for executing commands on a remote machine.

`ssh-keygen` - to generate, manages and converts authentication keys.

### systemd

- runs as background process, rather than being under the direct control of an interactive user.

it is a Linux initialization system and service manager that includes features like on -demand starting of demons, mount and auto-mount point maintenance, snapshot support and processes tracking using Linux control groups.

location `/lib/systemd/system/`

### advance package tool (apt)

`apt show [package name]` this will show the package info `apt show [package name] -a` this will only show the package description.

### difference between `apt remove` and `apt purge`

apt remove just removes the binaries of a package. it leaves residue configuration files. apt purge removes everything related to a package including the configuration files.

### user

`$USER` to get the current user set in environment variable. or `user` to get the current user.

# Shell Linux

### bashrc file

a `.bashrc` file is shell script that bash (bourne again shell) runs whenever it is started. Along with setting in the OS, the `.bashrc` helps set the environment variables. Whenever the `.bashrc` is modified the changes is available on the next terminal session.

```bash
source ~/.bashrc; # to restart the .bashrc to detect changes in the file.
```

## bash

[https://cs50.harvard.edu/ap/2020/assets/pdfs/exit_codes.pdf](https://cs50.harvard.edu/ap/2020/assets/pdfs/exit_codes.pdf)

Any non-zero exit code (commonly 1 or -1) conventionally means that there was some sort of error during the program execution that prevented the program from completing successfully.

bash auto complete - bash provides you a way of specifying your keywords, and using them to autocomplete command line arguments for your application.

```bash
echo [print to console]
echo -n [print-in same line]
read [VARIABLE_INPUT]
echo $VARIABLE_INPUT
```

### shell script

-e exit immediately if any command in the script returns a non-zero exit status.

-u treat unset variables as an error and exit immediately.

-x print each command before executing it.

-c tells the shell to execute the commands that follow it.

```bash
/bin/sh -c set -eux; # used to run shell script.
```

shell script - default command-line interpreter Unix-like operating system, including Linux.

### Open source software

`/var/lib/apt/lists`


### installing new software

`apt` using this will get the data from the local cache and `apt-get` will get the data from source repository.

get the binary file (it is compiled version package)

get the zip and compile and run the compiled version.

main - maintained by conicol

universal - maintained by community

### downloading source code

`sudo /etc/apt/source.list` configuration file to look up and download package.

**etc** - editable text configurations.

for install the source code package need `dpkg-dev` . if you install using the source code you loose the ability to track the version of the application. So for the best use the package manager to download and install the package.

### uninstalling package

```bash
apt-get remove <package name>; #  the configuration file still in the system or use the.
sudp apt-get purve <package name>; # this will remove any configuration file with the package.
sudo apt-get autoremove; # remove the archived files.
```

their are archives of the packages (the first time a package get installed it is compressed and saved as archives) in the `/var/cache/apt/archives` - this remains from the packages which are no longer maintained to the repository `sudo apt-get autoclean` or `sudo apt-get clean` (this will delete the downloaded archive files in `var/cache/apt/archive`.

### System commands

```bash
uname;
lscup; #view the cpu information.
lshw; #view the hardware information.
uname -a; #show system information.
```

`uname` to get the system name and `uname -s` print the kernel name of your system `uname -n` - to get the network host-name `uname -v` - to get the kernel version `uname -r` to get kernel release `uname -m` machine hardware name.

### sort command
`tac` command also reverse order. `sort -n <file>` sort the number `-u` - for unique `-r` for reverse `-n` for number . `-k` - search with key (column number)

```bash
sort -f 1;
sort -nr <file name>; #sort by number in reverse.
sort -nrh <file name>; # h - human readable format.
sort -nM <file name>; #M -month.
sort -n; #sort by numeric value.
sort -u; # unique.
```

### make
the Linux make command is used to build and maintain groups of programs and files from the source code. The make command invokes the execution of the make-file. It is a special file that contains the shell commands that we create to maintain the project.

### file permissions
execute permission **x** - is means access go inside (**`cd`**) that group.
the permissions are divided in 3 having 3 places for each group which hold three permission out of (r, w, x) bits. On every first place is reserved for the type of the file.

```bash
touch <executable file>;
echo hello <executable file>;
ls;
chomod og+x+w-r <user>;
```

## Environment variables
```bash
printenv; #print all env variables;
printenv PATH; #print value of pertical value
export DB_NAME=test_db; #only avaliable in current session.
# for storing the varibale permantely, add the variable to the .bashrc file.
echo DB_NAME=test_db >> .bashrc;
```

## tee
```bash
some_command 2>&1 | tee output.log
echo "New data" | tee -a existing_file.txt
echo "Hello, world!" | tee file1.txt file2.txt
ls -l | tee directory_listing.txt
```

- **Viewing Output While Saving**: Sometimes, you may want to view the output of a command in real-time while saving it to a file for future reference. `tee` allows you to do this by displaying the output on the terminal while writing it to a file.

## zip
```bash
zip -e output.zip folder/; # password protect zip.
zip -z output.zip; # add comment to zip folder.
zip -r archive.zip source_dir -x "excluded_dir/*";
```

```sh
zip -r output.zip folder_name1 folder_name2;
```
- `-r` includes sub-folders files

```sh
zip existin.zip file1 file2; # add files to existing zip.
zip -r otuput.zip folder/ -x "*.log" "*.tmp";
```
- `-x` exclude files/patterns

```sh
unzip -l output.zip; # list contents of zip file.
```

```bash
unzip -l archive.zip; # see inside .zip archive
unzip -j <file path to unzip>;
unzip -r archive.zip source_dir -x "excluded_dir/*" "**/dist/*";
```

## tar
```bash
tar -xvf myarchive.tar --wildcards '*.txt'
tar -tf <"file name">; # see inside .tar archive
```

`ctrl + g` : show current line status

`shift + g` : go to end of the file.

## sed
```bash
sed '/pattern_to_delete/d' filename; # delete the line
sed -n '/pattern_to_print/p' filename;
sed '2,5s/old_string/new_string/g' filename;

# replace
sed -i 's/,/;/g' your_file.txt; # inplace change

sed = filename | sed 'N;s/\\n/: /' # print line number
sed '/^$/d' filename # remove empty line from file
echo "Hello, World!" | sed 'y/aeiou/AEIOU/' # use transliteration

# insert and append
sed '/pattern_to_insert_before/i\\text to insert' filename
sed '/pattern_to_insert_after/a\\text to append' filename

sed -i.bak 's/old_string/new_string/g' filename; # create a backup version.

# multiple operation
sed -e 's/old_string/new_string/g' -e '/pattern_to_insert_after/a\\text to append' filename
```
```bash
# use different delimiters
sed 's|/path/to/replace|/new/path|g' filename
```

## ed editor
```bash
ed filename; # open file
# a - Enter insert mode
# . - Exit append mode by thyping period on new line.
# p - print current line
# 1,3p - print specific line numbers.
# 1,$p - print all lines.
# d - delete the current line.
# 1,3d - delete specific lines.
# 1,$s/old/new/g - sustitute text in all lines.
# w - save changes.
# wq - save and quite.
# = - print current line number.
# /example - search example in editor.
# 10 - move to line no. 10.
```

## xrandr
- show information about the display monitor.
```bash
xrandr --output <display> --auto --above <display>;
xrandr --output <display> --off;
xrandr --output <display> --mode <display>;
xrandr --output <display> --auto --same-as <dispaly>
```

## getent
- get entries from Name Service Switch libraries
```bash
getent <serice name>
```

## curl
```bash
curl -O <url>; # save file with original name  
curl --cookie-jar cookies.txt https://example.com; # allow to store and send cookies during requests
curl -x <proxy:port> <url>; # route requests through a proxy
curl --url smtp://smtp.example.com --mail-from sender@example.com --mail-rcpt recipient@example.com -T mail.txt
```

```bash
curl -X <http method> -d "key1=value1&key2=value2" <url> 
curl -X POST -d "key1=value1&key2=value2" https://example.com/endpoint

curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' https://example.com/endpoint

```

#### curl network
```bash
curl ifconfig.me/ip;
curl ifconfig.me/all.json;
curl ifconfig/mime;
curl ifconfig/forwarded;
```

## visudo
- the `/etc/sudoers` file should only be edited using the `visudo` command which ensures the file is edited by one user at a time and performs syntax checks.
- Errors or bad syntax in the `/etc/sudoers` may result in locking out all users.

```bash
<username> <hostname>(user:group) command
# username - specifies the user the rule applies to
# hostname - the machine the rule applies to
# user:group - user and group the rule applies to usually ALL
# command - the command user is allow to run
# NOPASSWD - allow the user to run the specified command without a password

# to allow user john to run the /usr/bin/foo and /usr/bin/bar commands as root witthout a password
john ALL=NOPASSWD: /usr/bin/foo /usr/bin/bar
%sudo	ALL=(ALL:ALL) NOPASSWD:ALL # allow sudo command to run without password
```

## mount
- mounting connects a file system from a storage device (like hard disk, USB or network share) to a directory in the main Linux file system tree. 
- it instructs the operating system that the file system is ready to use and associates it with a particular point in the systems's hierarchy.
```bash
mount; # list all mounted filesystem
mount /dev/sdb1/mnt; # Mount a partition manually
mount -o ro /dev/sdb1/mnt; # read-only mount
mount -o loop file.iso /mnt; # mount an ISO image
mount -t nfs <ip>:/share /mnt; # a network share (NFS)

umount /mnt; # unmount a mounted filesystem
umount -f /mnt;

mount -o remount, rw /mnt; # remount with different options
```

## tr
- used for translating, deleting or compressing characters in text stream. 
- it works with standard input and output.
```bash
grep 'MimeType' /usr/share/applicatoins/eog.desktop | tr ';' '\n';
```

## flock
- command used to implement advisory locks.

## vmstat

vmstat - monitoring system, info about processes, memory, paging, block I/O, traps and CPU activity. Perform dignosing performance issues and understanding system behavior under different workloads.
### xdg-open
- is a command line utility in Linux that opens a file or URL in the user's preferred application. It is part of the XDG [[X Desktop Group]] utilities.
- commonly used in desktop environment such as GNOME, KDE, XFCE

```bash
xdg-open http://www.example.com
xdg-open /path/to/example.pdf
```
- each file type has an associated MIME, When `xdg-open` is run it identifies the MIME type of the file you want to open.
- applications are defined in desktop entry files (usally with a `.desktop` extension) located in directories like `/usr/share/applications`. These files contain metadata about the application, including
	- the name of the application
	- the command to execute it
	- the MIME type it can handle
- `xdg-mime` is used internally by `xdg-open` to query which application is associated with a given MIME type.

#### What is atk-bridge
is a software component that acts as a bridge between the ATK (Accessibility Toolkit)

> [!NOTE] Users may encounter warnings such as "Failed to load module **'atk-bridge'" if the library is missing or not properly configured**

This bridge enables applications that use ATK (such as those built with GTK and other toolkits) to expose their accessibility information to assistive technologies like screen readers, magnifiers and other accessibility tools through the AT-SPI infrastructure.

ATK -> is a toolkit-independent accessibility API, providing a way for applications to describe their user interface elements and events in a standardized way.

ATK-SPI -> is the main accessibility framework on Linux, allowing assistive technologies to interact with applications and retrieve information about their UI.

atk-bridge -> connects these two layers: it translates ATK calls from applications into AT-SPI events and data, making them accessible over D-Bus (the interprocess communication mechanism used by AT-SPI2)
### xdg-mime

```bash
xdg-mime query default <MIME type>
```

- the default applications are store in
	- `~/.config/mimeapps.list`
	- `~/.config/gtk-3.0/setting.ini` (for GTP applications)
## ld
- `ld` is a GNU linker, a part of the GNU binutils package.
- primary role is to link multiple object files (`.o` files), libraries, and other resources into a single executable program or a library.
- linking is a crucial step in the compilation process, where seprate pieces of code and data are combined to form a runnable application.
### key features of ld
- symbolic resolution: combines symbols (like function, names, and global variables) from different object files, resolving references between them.
- relocation's: adjust memory addresses so that the program's code and data are correctly placed in the executable's memory space.
- library linking: incorporates necessary code from libraries (static or shared) into the final executable
- output generation: produces the final output file, such as an executable or a shared library
## busctl - list all the currently active buses (D-Bus services)


## `grep`

```shell
ss -t -a | grep -E '80|443|3000|5000';
lsof -i :443 | grep ESTABLISHED;
```

### The binary analysis tool
`objdump` -> is command line utility used to analyze and disassemble ELF binaries in Linux.
- provides detailed information about executables, object files, and shared libraries.

## **Key Options & Their Use Cases**
### General Information

| Option | Description                                                                    |
| ------ | ------------------------------------------------------------------------------ |
| `-f`   | Displays **file header** information (architecture, format, entry point, etc.) |
| `-x`   | Displays **all headers** (section headers, symbols, program headers)           |
| `-p`   | Shows information about **program headers** (useful for shared libraries)      |
### **Disassembly (Viewing Assembly Code)**

| Option     | Description                                                          |
| ---------- | -------------------------------------------------------------------- |
| `-d`       | Disassemble **only the executable sections** (ignores data sections) |
| `-D`       | Disassemble **everything** (including data sections)                 |
| `-M intel` | Display assembly in **Intel syntax** (default is AT&T syntax)        |
- this shows the assembly instructions of the binary.

```shell
objdump -d -M intel <binary>;
```

### **Inspecting Symbols & Functions**

| Option | Description                                                      |
| ------ | ---------------------------------------------------------------- |
| `-t`   | Displays the **symbol table** (function names, global variables) |
| `-T`   | Shows symbols from **shared libraries**                          |
| `-C`   | Demangles **C++ symbols** (makes them human-readable)<br>        |

```shell
objdump -t <binary> | grep main;
```
- this finds the main function in the symbol table.

### **Inspecting Sections (Memory Layout)**

| Option | Description                                               |
| ------ | --------------------------------------------------------- |
| `-s`   | Display **raw section data** (useful for debugging)       |
| `-h`   | Show **section headers** (helps understand memory layout) |
## `lsof`
lists on its standard output file information about files opened by processes for the following UNIX dialects
