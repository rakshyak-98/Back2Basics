D-Bus (Desktop Bus)
- an Inter-process communication (IPC) system primarily used in Linux and Unix-like operating systems. 
- communication between applications and system processes, allowing them to exchange messages and respond to events efficiently.

> [!INFO]
> it is a standard way for an application to discover what services exist and what methods they offer.

> [!INFO]
> switchboard where applications, system services, and background daemons can easily talk to each other without needing to know low-level details like sockets, port or PIDs.

## Message Bus Architecture

- D-Bus operates on a message bus model
- applications communicate by sending messages to a central daemon know as the **D-Bus-daemon**
- this design eliminates the need for each application to establish direct connections with every other application, simplifying the communication process

> [!INFO] support two types of Bus **System Bus** and **Session Bus**

|Bus type|Address|Purpose|Who can connect?|Typical users|
|---|---|---|---|---|
|**System bus**|`unix:path=/run/dbus/system_bus_socket`|System-wide services (privileged)|Mostly root + some trusted users|systemd, NetworkManager, logind, bluetoothd, udisks, polkit, ModemManager…|
|**Session bus**|usually `unix:abstract=/tmp/dbus-XXXXX` or similar|Per-user desktop session|Only your user|GNOME, KDE, Firefox, LibreOffice, file managers, notifications, media players…|

### System bus

- a shared bus for all users
- dedicated to system services and events, such as hardware connections (e.g., USB devices) and system notification

### Session Bus

- is specific to individual user sessions and is used for desktop applications to communicate with one another within that session

> [!INFO] Applications can register as services on the D-Bus, exposing various methods and properties that other applications can invoke.
- each service is identified by a unique name, allowing for organized communication.

|Concept|What it is|Example path / name|
|---|---|---|
|**Bus name**|Unique or well-known name of a service|`org.freedesktop.NetworkManager`, `org.gnome.Shell`|
|**Object path**|Like a URL path inside the service|`/org/freedesktop/NetworkManager/Settings/4`|
|**Interface**|Group of related methods/properties/signals (like a class/interface)|`org.freedesktop.NetworkManager.Connection.Active`|
|**Method**|Function you can call|`ActivateConnection()`, `Reboot()`|
|**Property**|Readable/writable value|`Hostname`, `OnlineStatus`|
|**Signal**|Event broadcast that anyone can subscribe to|`PropertiesChanged`, `DeviceAdded`|

### Object-Oriented Messaging

D-Bus messages are structured as objects containing method names, object paths, are arguments. This design allows developers to use object-oriented programming techniques when building applications that communicate via a D-Bus

### Security features

D-Bus includes mechanisms for authentication and authorization, ensuring that only authorized applications can access certain services. This enhances the security of Inter-process communications.

### Signal Mechanism

Applications can send signals to notify others about events without requiring a direct response. This allows for asynchronous communication and reduces the need for constant polling.

## Use cases

**Desktop integration** enables different desktop applications to work together seamlessly, such as notifying media players when a new track is available or managing system resources like printers and network connections.
**Event Handling** when hardware changes occur (e.g., a USB drive being connected), D-Bus informs all interested applications about the event, allowing them to react appropriately without individual checks.
**Service Management** Applications can manage their lifecycle through D-Bus by launching or terminating services as needed based on user interactions or system events. 

## How to view the methods a service offers

- Pick an interesting service and see its object tree (this is usually the best starting point)

```bash
busctl tree <bus name>; # show the hierarchy of object paths.
```

- Introspect a specific path to see methods, properties, signals

```bash
busctl introspect 
```

|Column|What it means|Common examples|Notes / what to look for|
|---|---|---|---|
|**NAME**|The name of the thing (method, property, signal, or interface)|`.PowerOff` `.StaticHostname` `.NameOwnerChanged`|Dot (`.`) means it belongs to the interface above it|
|**TYPE**|What kind of member it is|`method` `property` `signal` `interface`|Tells you if you can call it, read it, or listen to it|
|**SIGNATURE**|The **type signature** of arguments (input → output)|`b` (boolean in, nothing out) `sb` (string + boolean in) `sss` (3 strings in)|Very important: shows what arguments you must pass and in what order|
|**RESULT/VALUE**|Current value (for properties only) or `-` otherwise|`"myhost"` `100` (numeric state) `-`|Only filled for readable properties|
|**FLAGS**|Extra info about the member|`emits-change` `writable` `-`|`writable` = you may be able to change it `emits-change` = property changes are signaled|

|Code|Meaning|Example usage|
|---|---|---|
|`b`|boolean|`true` / `false`|
|`i`|32-bit signed int|`0`, `42`, `-5`|
|`u`|32-bit unsigned int|`100` (e.g. NetworkManager state)|
|`s`|string|`"hello"`|
|`o`|object path|`/org/freedesktop/NetworkManager/42`|
|`a`|array|`as` = array of strings `ao` = array of object paths|
|`{}`|dictionary (map)|`a{sv}` = array of string→variant|
|`v`|variant|any type (very flexible)|

### How to read busctl introspect quickly

1. Find the **interface** you care about (lines without dot)
2. Look below it for methods/properties/signals starting with .
3. Read the **SIGNATURE** column to know what arguments to pass
4. If it's a property and has a value → you can read it immediately
5. If it says writable → you might be able to change it

### Practical reading tips

1. Look for lines starting with org. or net. or com. → those are **interfaces**.
2. Everything indented under an interface with a . belongs to that interface.
3. If you want to **call** a method → look at the SIGNATURE column:
    - Left of space = input arguments
    - Right of space = output (often - = nothing returned)
4. If you see property and a value → you can read it with

```bash
busctl get-property <service> <path> <interface> <PropertyName>;
```

5. If you see `writable` -> you can try to set it (if policy allows).

```text
.PowerOff                           method    b         -             -
```

```bash
busctl call org.freedesktop.systemd1 /org/freedesktop/systemd1 org.freedesktop.systemd1.Manager PowerOff b true
```