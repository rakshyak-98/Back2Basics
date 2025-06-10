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

**Application-Specific Configuration**: The instance name is typically set by the application itself when it is launched. Many applications allow you to specify the instance name using command-line options. For example, terminals like `gnome-terminal`, `urxvt`, and `termite` can be launched with flags like `--name` or `--class` to define their instance and class names explicitly [i3wm instance](https://bbs.archlinux.org/viewtopic.php?id=259587)

> [!NOTE] after creating the `.desktop` file, need to update the MIME type to associate directories with Ranger.

```bash
xdg-mime default ranger.desktop inode/directory; # update MIME type
xdg-mime query default inode/directory; # confirm
```

```bash
# list all the MIME types from shared-mime-info database
grep -hE '^[^#]' /usr/share/mime/packages/*.xml | grep -oP 'type="\K[^"]+'

```