```bash
stat <filename>;
xdg-mime query default inode/directory; # get the information of file manager

echo $XDG_CURRENT_DESKTOP; # current desktop environment

lsblk; # list block devices

# make custom tmpfs file system
sudo mount -t tmpfs -o size=100M tmpfs <path>;
```

#### Make the mount permanent
- automatically mounted at boot, you can add an entry to `/etc/fstab` file.
```txt
tmpfs <path> tmpfs size=100M 0 0
```

```bash
df -h; #verify the mount
```

### API package lock
- `/var/lib/dpkg/lock` or `/var/lib/apt/lists/lock`
- apt package manager uses lock files to prevent multiple processes from accessing the package database simultaneously.
- when you initiate an upgrade apt creates a lock file at `/var/lib/dpkg/lock` or `/var/lib/apt/lists/lock` This file act as a signal that a package management operation is in progress, preventing other instances of `apt` or `dpkg` from running concurrently.

### mime type
- `/etc/mime.types` 

```bash
gio mime <mime-type>;
```

### block device
 - a type of device file that allows access to storage devices in fixed size blocks.
- block devices area a way for Linux kernel to interact with physical storage devices or simulated devices.
- call block device because they read and write data in fixed-size "blocks" of multiple bytes at a time.
- example of block devices hard devices, SSDs, USB drives, CD-ROMS, and RAM disks
- block device provide random access to data organized in fixed-size blocks.
- the block size must be a multiple of the sector size and a power of 2, not exceeding the page size.
- file-systems are usually stored on block devices.
- when you format a block device, you create a file-system on it.
- the file-system then can be mounted at a specific location in the directory structure, making the storage available to the system.

delegate - authorized to represent others or an elected representative.

`sudo` - the `sudo` program allows a user to start a program with the credentials of another user.

the system administrator has to set up the `/etc/sudoers` file. This can be useful to delegate administrative tasks to another user (without giving the root password).

```bash
cat <"file"> | cut -d "," -f 1-5; # Set delimiter and get the fifleds.
sudo mount -o remount,rw /path/to/filesystem
chmod +u <"filename">; # set uid permission bits.
chmod +t <"finename">; # set sticky bits.
chcon -t 
restorecon ;

find "$new_dir_name" -type f -exec sed -i "s/PLACEHOLDER/$new_dir_name/g" {} \\;
```

```bash
find . -type d -exec touch {}/<filename> \\;
#  \\; end of the -exec command is necessary to terminate the -exec option.
```

[user management](https://www.notion.so/user-management-fcce2450e15c4c1aa8b0ebfad6dd3e25?pvs=21)
uid permission bits : setuid (SUID), setguid (SGID) bits. associated with the user and group ownership of a file or directory.

> [!INFO] cannot change it using the `chmod` command because sockets are a special type of file that doesn't have the execute permission or the ability to set the `setuid` or `setgid` bits.

1. SUID : set on an executable file, it allows the files to be executed with the privileges of the file’s owner, instead of the user who is running the program. Used to give a non-privileged user temporary elevated permission when executing certain program (system utilities).
2. SGID : set on an executable file or a directory, it allows the file or the files created within the directory to inherit the group ownership of the parent directory, rather than the group of the user who created them. Used to maintain group ownership consistency when multiple user work on the same files within a shared directory.

Sticky bits : commonly applied to directories to restrict who can delete or rename files within that directory (Also referred as the _restricted deletion flag_)

- the owner of the directory can delete or rename any file within it.
- users who are not the owner of the directory (even if they have write permission on the directory) can only delete or rename files if they are the owner of the file.
- set on directory like `/tmp` it prevents users from accidentally or maliciously deleting or renaming each other’s files.

```bash
sed -n "5, 10p" filename; # display specific range of lines in a file.

stat [file_name];
stat -L [file_name]; # to follow the symbolic link.

mkdir -p bla/things/sablam
mkdir <"folder">
touch <"file name">
```

### creating files

touch command - is used to create or update the timestamps of a file or directory. Keep in mind that is any of the file names you specify with the `touch` command already exist, their timestamps will be updated rather than creating new files.

```bash
mkdir {jan,feb}{2017,2022} # expands link algebra bracket, 
touch filename{a..z}

ls -Z; # display security context.
ls -sh; # see the size with files names;
ls users-0*
ls l?st.sh
ls l[abdcio]st.sh
ls ??st*; # matches exactly two character.
ls [clst]*
ls [clst][io]?t*
rm *tar*
ls users-[0-9][a-z0-9][0-9]*
ls users-[0-9][!0-9][a-zA-Z]*

touch file{1..3}
touch {jan, feb}{1..3}/file{1..10}.txt
mkdir -p dir1/subdir1/
```

`ls -z` : used in systems that implement Mandatory Access Control (MAC) or Security-Enhanced Linux (SELinux) policies.

- it will list the files and directories in the current directory along with their associated security context labels. These labels provide information about the access controls and permissions for each file or directory based on the security policy enforced by SELinux.

### etc file
`/etc/x11/default-display-manager` set display manager

the `/etc/passwd` file is owned by the root user and must be readable by all the users, If a user ID has a password, then the password field will have and exclamation point, and do not have a password field will have asterisk.

```bash
passwd; # use to change password for the current login user if not admin.
```

the `/etc/passwd` file is used to keep track of every registered user that has access to a system.

the `/etc/passwd` file is a colon-separated file that contains the following information

- username
- x means has a encrypted password (`/etc/shadow`)
- user ID number
- user's group id number
- full name of the user GECOS
- user home directory
- login shell

binary programs : understood by machine directly

text based scripts : understood by human which need to interpret and convert to machine every it is executed.

## install

```bash
sudo install -m 1777 -d /etc/apt/keyrings
```

- `m 1777` sets the permissions to `1777` in octal notation.
    - The leading `1` sets the "sticky bit" which is a special permission.
    - The `777` indicates read, write, and execute permissions for the owner, group, and others.
- The rest of the command remains the same: `d` specifies that the target is a directory, and `/etc/apt/keyrings` is the path to the directory that will be created.

The "sticky bit" (`1` in the `1777` permission mode) has different effects depending on the context. In the case of directories, it is often used to ensure that only the owner of a file within the directory can delete or rename that file, even if others have write permissions on the directory. This can be useful in directories where multiple users are creating and managing files.

## Wildcard

### creating files

touch command - is used to create or update the timestamps of a file or directory. Keep in mind that is any of the file names you specify with the `touch` command already exist, their timestamps will be updated rather than creating new files.

```bash
mkdir {jan,feb}{2017,2022} # expands link algebra bracket, 
touch filename{a..z}

ls -sh; # see the size with files names;
ls users-0*
ls l?st.sh
ls l[abdcio]st.sh
ls ??st*; # matches exactly two character.
ls [clst]*
ls [clst][io]?t*
rm *tar*
ls users-[0-9][a-z0-9][0-9]*
ls users-[0-9][!0-9][a-zA-Z]*

touch file{1..3}
touch {jan, feb}{1..3}/file{1..10}.txt
mkdir -p dir1/subdir1/
```
