[gnu error codes](https://www.gnu.org/software/libc/manual/html_node/Error-Codes.html)

[remove prompt for default key-rings password on login](https://askubuntu.com/questions/867/how-can-i-stop-being-prompted-to-unlock-the-default-keyring-on-boot)

> In bash, the variable `$1` refers to the first command-line argument passed to the script or function

```bash
apt install iputils-ping
apt install dnsutils; # nslookup command packages
apt install iproute2; # ip command packages
apt-get install procps htop; # ps and top command packages.
apt install net-tools; # netstat etc.
apt install telnet;

apt-get install build-essential; # install C in system and gcc

apt-get install lvm2; # logical volume packages, pvdisplay.
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
# reset terminal keybindings
dconf reset -f /org/gnome/terminal/legacy/keybindings/
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

```bash
gsettings set org.freedesktop.ibus.panel.emoji hotkey '@as []'
```

# Update to latest Linux desktop

```bash
lsb_release -a; # check latest stable release

# steps:
# 1 : change the prompt=normal at /etc/update-manager/release-upgrades
# 2 : change prompt=lts to prompt=normal;
sudo do-release-upgrades;
```

## STDIN, STDOUT, STDERR

# system boot timeout config in window 11

win + i > system > about > system protection > advanced > startup and recovery (settings)

ps - process status: report a snapshot of the current processes status.

- options 1 (UNIX) , 2 (BSD) , 3 (GNU)
- process id, parent process id.
- `top` can be used to see the threads running on the system.

`sudo make install` : you are telling the system to execute the instructions in the make-file with administrative privileges, which will build the software and then install it on the system. `make` this is a tool that reads a set of instructions in a make-file and builds the software according to those instructions.

## Exit codes

In Linux and Unix-like systems, exit codes (also known as exit statuses or return codes) are numeric values returned by a command or a program to indicate the outcome of its execution. A value of 0 typically indicates success, while non-zero values indicate various types of errors or abnormal conditions.

Here are some common exit codes along with their meanings:

- **0**: Success
- **1**: General error
- **2**: Misuse of shell builtins
- **126**: Command invoked cannot execute (permission issue or not an executable)
- **127**: Command not found
- **128**: Invalid argument to exit
- **128 + N**: Fatal error signal "N" (e.g., 128 + 9 = 137 indicates a SIGKILL)
- **130**: Script terminated by Control-C
- **137**: Process terminated by Control-C (128 + 9)
- **139**: Segmentation fault (invalid memory reference)
- **143**: Process terminated by Control-C (128 + 15)
- **255**: Exit status out of range or undefined

> Note: you have already run the `./configure` command to set up the build environment.

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
find [path] -maxdepth 2 -mindepth 2 -type [d|f|l] -name [sourcename] -delete.
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

## files 
[command] | tee filename;
find ./ -name '*.txt'
stat [filename]; # to see more info on the file.

# find modified within last 30 days in directory and subdirectory.
find /home -mtime -30; 
find [path] -type f -name [file name];

# find all empty directory.
find [directory] -type d -empty;

# find directory and subdirectory owned by root
find [directory] -user root;

# fix broken grub config
sudo apt-get install --reinstall ubuntu-desktop;
```

tee - command is used to redirect the output of a command to a file, while still displaying it on the terminal. It is named after the T-splitter used in plumbing, which splits water into two directions.

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

pts - pseudo terminal slave.

tty - teletypewriter.

pts - first terminal pseudo terminal slave window. A pair of virtual terminal devices that allow a terminal emulator gnome-terminal to communicate with a program as if it were a terminal.

The master end of a pseudo terminal is connected to the terminal emulator, where a slave end is connected to the program. The slave end is identified by a device name that begins with `pts/` followed by a number that identifies the specific pseudo terminal.

> `pts` notation is specified to Unix-like systems, and may not be used on other operating systems.

SPID - system process id. Identify the process internally. Used to track the process across different terminal sessions.

STAT - stands for status.

- D - Uninterruptible sleep (usually input or output).
- R - running or run-able
- S - interruptible sleep (waiting for an event to complete)
- T - stopped, either by a job control signal or because it is being traced.
- Z - defunct (zombie) process, terminated but not reaped by its parent.

BSD - Berkeley Software Distribution at Curlie.

tty column - display the terminal device associated with a process.

### sha bang

directive meaning - an official or authoritative instruction.

- involving the management or guidance of operations.

shebang is the character sequence consisting of the characters `#!` when a text file with a shebang is used as if it is an executable in a Unix operating system, the program loader mechanism parses the rest of the file’s initial line as an interpreter directive. The loader executes the specified interpreter program, parsing to it as an argument using the path that was initially used when attempting to run the script, so that the program may use the file as input data.

### kill process

`pgrep -l -u $USER` list the process and get the process id, user `kill` command to kill the process.

```bash
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

`apt-cache search` - search the cache in the system with package name and little description and `apt-get show` - search without internet connection, the specified package from the cache and show the all information of the package.

### installing new software

`apt` using this will get the data from the local cache and `apt-get` will get the data from source repository.

get the binary file (it is compiled version package)

get the zip and compile and run the compiled version.

main - maintained by conicol

universal - maintained by communinity

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

# GNU Privacy Guard

```bash
# [ configure key ]
gpgconf --list-dir
gpg --refresh-keys

# [ generate new keys ]
gpg --gen-key # asymmetric
gpg --gen-random 32
gpg --import "file"; # import gpg public key from a file.

# [ list keys ]
gpg --list-keys # pulic keys
gpg --list-secret-keys # private keys

# [ export keys ]
gpg --export-secret-keys -a KEY_ID > my_private_key.asc; # -a ASCII-armored
gpg --export -a KEY_ID > my_public_key.asc
# -o stdout to location
gpg --export -o public.asc <user ID>
gpg --export-secret-keys -o private.asc <user ID>

# [ edit key ]
gpg --edit-key; # init intrective terminal

# [ verification ]
gpg --verify "signature file"; # verify signature
gpg --detach-sign "file.txt"; # create a detach sign to verify.
gpg --check-trustdb
gpg --firgerprint <key id>;
```

```bash
# [ encryption ]
gpg --sign -u user@example.com mydocument.txt
gpg -e binary_publickey file.asc
gpg --encrypt plain.txt
gpg --encrypt --recipient recipient_name --output "enc.gpg" "file"

# -c symmetric
# -e asymetric
gpg --armor -c -o encrypted.asc "youfile.txt"
gpg --armor -e -o encrypted.asc -r "recipient" "yourfile.txt."

# [ decryption ]
gpg -da binary_publickey.asc
gpg --decrypt plain.gpg
```

```bash
# [ sign ]
gpg --clear-sign "file.txt"; # create new file with clear redable format

# sign with armor representation
gpg --armor -s -o signed.asc "yourfile.txt"
```

GNU Privacy Guard, used for encryption and digital signature operations.

ASCII-armor : feature to type of encryption called Pretty Good Privacy (PGP). and `.asc` file extension.

`--armore` represents an ASCII-armored representation of data.

```bash

# encrypt file using the public key save as ASCII-armored format.
gpg --armor \\
--output encrypted.txt.asc \\
--encrypt --recipient "username" plaintext.txt;
```

GPG or gpg - GNU Privacy Guard, tool is a native security tool for encrypting files. It is a tool to provide digital encryption and signing services using the OpenPGP standard.

openpgp standard - is the most widely used email encryption standard. It is defined by the OpenPGP working group of the Internet Engineering Task Force (IETF)

- is describes the format and methods needed to read, check, generate, and write, conforming encrypted messages, keys, and signatures.

### armor

(ASCII-armored-format)

**Armor**: "Armor" refers to the process of encoding binary data, such as cryptographic keys or messages, into a human-readable text format. This text format is designed to be easily exchanged and shared in contexts where binary data might not be appropriate (e.g.,emails, forums).

**Dearmor**: "Dearmor" (or "dearmor") is the process of decoding ASCII-armored data back into its original binary format. This is done when you want to use the original binary data for cryptographic operations or other purposes.

recipient : specifies the recipient public key or email address

- refers to the individual or entity for whom you are encrypting a message or a file.
- to ensure intended recipient can decrypt and read the content.

### remove all trace of gpg keys

```bash
gpg --delete-secret-keys "key_id"
gpg --delete-keys "key_id"

rm -rf ~/.gnupg/ # gpg stores your keys in files in directory
```

After your key pair is generated, you may want to create a revocation certificate. the owner of a cryptographic key pair to declare that their public key should no longer be used for encryption, decryption, or digital signatures. Essentially, it revokes the validity of the associated public key.

```bash
gpg --gen-revoke <ID>
```

### edit key

```bash
gpg --edit-key; # init intrective terminal
```

management operations. Some common commands include:

- `adduid`: Add a new user ID to the key.
- `revuid`: Revoke a user ID.
- `expire`: Change the expiration date of the key.
- `revkey`: Revoke the entire key.
- `trust`: Change the trust level assigned to the key.
- `uid`: Select a specific user ID for editing.
- `check`: Check the key for consistency and correctness.

# BSD

BSD stands for Berkeley Software Distribution. It is a version of the Unix operating system developed at the University of California, Berkeley.

- release in 1970s
- broadly refer to the family of operating system that are derived from the original BSD code-base. Example MacOS, base of BSD version called Darwin,
- FreeBSD, NetBSD, OpenBSD operating system. These systems are known for stability, security, and portability.

### standard output

`>` - used to redirect standard out.

```bash
# STDOUT
command [option] > [output file]
```

```bash
Hit: # comparing metadata with remote site.
Get: # fetching new, improved version from remote site.
Ign: # a non-critical error occured.
Err: # a critical error occured.
```

when `apt-get update` is verifies if the same update indexes need downloading, if not it does not download the same updated indexes again.

- `Hit` - means apt checked the timestamps on package list ( `Release` or `InRelease` file), those match and there are no changes (compare with `/var/lib/apt/lists` ).
- `Ign` - means there are no changes in the `pdiff` index file (in-release file), it wont bother downloading it again, Ignore.
- `Get` - means apt checked the timestamps on package list, there were changes and will be downloaded.

## tee

```bash
some_command 2>&1 | tee output.log
echo "New data" | tee -a existing_file.txt
echo "Hello, world!" | tee file1.txt file2.txt
ls -l | tee directory_listing.txt
```

- **Viewing Output While Saving**: Sometimes, you may want to view the output of a command in real-time while saving it to a file for future reference. `tee` allows you to do this by displaying the output on the terminal while writing it to a file.

## tar

```bash
zip -r archive.zip source_dir -x "excluded_dir/*"
unzip -l archive.zip; # see inside .zip archive
```

```bash
tar -xvf myarchive.tar --wildcards '*.txt'
tar -tf <"file name">; # see inside .tar archive
```

`ctrl + g` : show current line status

`shift + g` : go to end of the file.

## sed

```bash
sed '/pattern_to_delete/d' filename
sed -n '/pattern_to_print/p' filename
sed '2,5s/old_string/new_string/g' filename

# replace
sed -i 's/,/;/g' your_file.txt

sed = filename | sed 'N;s/\\n/: /' # print line number
sed '/^$/d' filename # remove empty line from file
echo "Hello, World!" | sed 'y/aeiou/AEIOU/' # use transliteration

# insert and append
sed '/pattern_to_insert_before/i\\text to insert' filename
sed '/pattern_to_insert_after/a\\text to append' filename

sed -i.bak 's/old_string/new_string/g' filename

# multiple operation
sed -e 's/old_string/new_string/g' -e '/pattern_to_insert_after/a\\text to append' filename
```

```bash
# use different delimiters
sed 's|/path/to/replace|/new/path|g' filename
```

# uwsgi

```bash
uwsgi --ini uwsgi.ini
```

uWSGI acts as a bridge between your web application and the web server (like Nginx or Apache). It takes care of communication, request handling, and process management.

- You configure uWSGI using a configuration file (often named `uwsgi.ini`). This file contains settings like the application entry point, the number of worker processes, and more.
- uWSGI operates using a master-worker model. The master process manages the worker processes that actually handle incoming requests. Each worker is essentially an instance of your application.

# GDB : The GNU Project Debugger

[GDB](https://www.sourceware.org/gdb/) : allows you to see what is going on inside another program while it executed, or what another program was doing at the moment it crashed.

- programs might be executing on the same machine as GDB, on another machine, or on a simulator.
- can run on UNIX and Microsoft Windows, macOS.