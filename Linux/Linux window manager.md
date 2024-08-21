```bash
alsamixer; # manage volume
xbacklight; # manage brightness
nmcli; # manage network
links; #
```
### Application management
- this configuration specifies that Ranger should be launched in a terminal. new file in the `.local/share/applications/ranger.desktop`
```bash
[Desktop Entry]
Name=Ranger
Exec=kitty -e ranger %F
Type=Application
Terminal=true
MimeType=inode/directory;
```

> [!NOTE] after creating the `.desktop` file, need to update the MIME type to associate directories with Ranger.

```bash
xdg-mime default ranger.desktop inode/directory; # update MIME type

xdg-mime query default inode/directory; # confirm
```

### Display manager
```bash
sudo dpkg-reconfigure gdm3;
sudo apt-get install --reinstall gdm3;
sudo journalctl -xe;
sudo systemctl daemon-reload; # reload systemd daemon to apply tha changes;
```

- configure: `/etc/systemd/system/` or `/usr/lib/systemd/system/` if it doesn't exist, you may need to reinstall the `gdm3` package.

- this configuration ensures that `gdm3` is started when the `graphical.target` is reached and that it is also aliased as `display-manager.service`
```bash
[Install]
Alias=display-manager.service
WantedBy=graphical.target
```

## Window manager

### Wayland Enable
```bash
# /etc/gdm3/custom.conf
WaylandEnable=true
```

Xorg is a full featured X server that was originally designed for UNIX and UNIX-like operating systems running on Intel x86 hardware.

### X server
is a display server for UNIX like operating systems, including Linux.

- provide framework for graphical user interface by mapping graphical elements such as windows, applications, and input devices.
- facilitates the communication between the hardware and the software.
- default display server for Linux.

### Wayland
display server protocol and architecture designed as a replacement for x11.

- starting with Ubuntu 17.10 there has been experimental support for wayland.
- user can choose wayland as the session type during the login screen.

### I3
```bash
i3-msg exit; # exit from current login session.
i3-config-wizard; # re-generate default i3 config file
```

- configure PAM(Plugable Authentication Module): Ensure that your PAM configuration includes the necessary lines to unlock the key-ring. 
- `/etc/pam.conf` and `/etc/pam.d/<desktop manager>` this should include `auth required pam_gnome_keyring.so` line.