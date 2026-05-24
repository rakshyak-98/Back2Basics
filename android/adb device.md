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

> [!NOTE]
> `10.0.2.2` -> special alias created by Android Emulator to access host machine localhost.
> - Android emulator runs inside virtual network
> - Android emulator provides mapping `10.0.2.2` -> host machine localhost
> - IOS simulator can directly use `localhost`


## Running application with private network IP
1. Use the private network IP, not localhost
	1. replace `localhost` or `127.0.0.1` with your backend private network `192.168.x.x` or `10.x.x.x`

2. Device/Emulator must be on same network
	1. physical device -> Connected to the same wifi as your backend machine.
	2. Android emulator -> Configured to bridge to your host network (or use `10.0.2.2`) as host gateway.
	3. IOS simulator -> Can typically access host machines' private IPs directly via `localhost` or by using your machine private IP.

> [!NOTE]
> - Backend binding -> backend must listen on `0.0.0.0` (all interface), not just `127.0.0.1`