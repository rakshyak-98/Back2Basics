```bash
alsamixer; # manage volume
xbacklight; # manage brightness
nmcli; # manage network
links; #
```

### Application management

```bash
lsb-release -a; # check your ubuntu version

sudo apt udpate;
sudo apt upgrade -y;
```

```bash
# Install git, curl, wget, build essentials
sudo apt install -y \
  git \
  curl \
  wget \
  build-essential \
  software-properties-common \
  apt-transport-https
	
```

```bash
mkdir -p ~/applications
mkdir -p ~/.local/bin
mkdir -p ~/.local/share/applications

echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bsahrc
source ~/.bashrc

```

```bash
cd ~/applications
git clone <repository-url> <app-name>
# OR
wget <download-url> -O <app-name>.tar.gz
tar -xzf <app-name>.tar.gz
cd <app-name>

```

## Create systemd service for auto-start

```bash
cat > ~/.config/systemd/user/my-app.service;

```

```ini
[Unit]
Description=My Application After=network.target

[Service]
Type=simple User=$USER WorkingDirectory=%h/applications/my-app ExecStart=/home/$USER/.nvm/versions/node/v18.x.x/bin/node /home/$USER/applications/my-app/index.js Restart=on-failure RestartSec=10 [Install] WantedBy=default.target EOF
```

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

---
### Bluetooth connectivity
- `ControllerMode = bredr` to `/etc/bluetooth/main.conf`

> [!INFO]
> `ControllerMode` -> is a BlueZ configuration (usually set in `main.conf`)

```vi
[General]
ControllerMode = dual    # or le, or bredr
```

- Then restart Bluetooth
```bash
sudo service bluetooth restart;
sudo btmgmt info; # BlueZ tool 
```