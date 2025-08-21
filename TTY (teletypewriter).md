## PTS
A pseudo-TTY is a software-based implementation of a TTY that enables terminal emulators, such as GNOME terminal, Console, and xterm etc. to function. When you launch a terminal emulator, it requests a PTS from the operating system, which is then used for input/output operations.

## TTY Device files
- in Linux  each TTY (virtual or pseudo) is represented by a device file located in the `/dev` directory.  For example `/dev/tty1` represents the first virtual TTY, while `/dev/pts/0` represents the first pseudo-TTY.

## Virtual TTY
- text-based interface that allows users to interact with the operating system using a keyboard and display.
- the virtual TTY are used for login, system maintenance, and troubleshooting when the graphical desktop environment is not functioning properly.

### How to use TTY in Linux
- Access Virtual  TTY : Press `Ctrl + Alt + F1` to `Ctrl + Alt + F6` to switch between virtual TTYs. `Ctrl + Alt + F7`. Typically returns you to the graphical desktop environment.
- Check the Current TTY : Use the `tty` command in a terminal to display the name of the current TTY device file.
- Enable TTY Mode on Mobile Phones: Some mobile phones have a TTY mode that allows users with hearing or speech impairments to communicate using text-to-voice or voice-to-text technology.