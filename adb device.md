## Setup Unauthorized device

```bash
adb devices;
adb logcat; # view logs
```

```bash
lsusb; # find vendor iD
```

```text
Bus 002 Device 005: ID 04e8:6860 Samsung Electronics
```
- `04e8` vendor id

```bash
sudo vi /etc/udev/rules.d/51-android.rules;
```

```text
SUBSYSTEM=="usb", ATTR{idVendor}=="04e8", MODE="0666", GROUP="plugdev"
```
- replace the vendor id

```bash
sudo chmod a+r /etc/udev/rules.d/51-android.rules;
sudo udevadm control --reload-rules;
sudo udevadm trigger;

sudo usermod -aG plugdev $USER;
```

```bash
adb kill-server;
adb start-server;
adb devices;
```

```
```text
Expected result: 0123456789ABCDEF    device
```