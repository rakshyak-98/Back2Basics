### Peer address port and Local Address Port
These terms describe the two endpoints of a network connection:

Local Address Port -> This is the port on your machine (the one running your application). It's assigned when you create a socket connection and is typically a randomly chosen port from the ephemeral range (usually 49152-65545 on most systems), unless you explicitly bind to a specific port.

Peer Address Port -> This is the port on the remote machine you're connecting to. It identifies which service or application on the remote host you want to communicate with.
Example -> You're connecting to a web server at `example.com:443` (HTTPS)