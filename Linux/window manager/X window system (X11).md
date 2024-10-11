- also known as X or X11
- graphical windowing system for bitmap displays, commonly used on Unix-like operating system such as Linux and BSD.
- it provide fundamental framework for building **graphical user Interface**, managing graphical display, and handling input devices like keyboards and mice.

## Client Server Architecture
- X use a client-server model
- X server control the display, which the X clients are applications that request the server to display their windows.
- the server manages input / output devices (monitors, mice, keyboards), while clients send requests (e.g, drawing windows, receiving user input) to the server.
- X11 is hardware-independent it can run on any hardware with the correct drivers, making it adaptable to various devices and display types.

> [!INFO] you can run an application on a remote server and have the interface display on your local machine.

> [!NOTE] X itself does not manage windows or how they are drawn (e.g borders, titles). This task is handled by a window manager (e.g. GNOME, KDE, Openbox, i3wm) which provides window decorations, resizing, and other graphical management features.

### Component of X window
1. X server is the core of the X window System, responsible for handling all graphical display and input device management. It runs on the machine where the display hardware is located.
2. X client communicate with X server to display windows and handle input
3. X Display refer to the screen or screens being controlled by the X server Each display consist of a screen (actual monitor) and an associated keyboard and mouse.
4. Window manager controls the appearance and functionality of the windows in the system, such as window border, closing/maximizing buttons, and how windows are arranged on the screen.
