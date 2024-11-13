IPC- Inter-process communication
- mechanisms provided by an operating system 
- for processes to manage share data.
- applications can use IPC, categorized as clients and servers, where client request data and the server responds to client requests.
### Approaches
Different approaches to IPC have been tailored to different software requirements.

### Reference
[Inter-process communication (IPC)](https://en.wikipedia.org/wiki/Inter-process_communication)

## How does process communicat through port with external requests outside of os

Processes communicate with external requests outside of an operating system primarily through **network sockets** and **ports**. 

1. **Network Sockets**: These are endpoints for sending and receiving data across a network, using protocols like TCP or UDP. Each socket is associated with a port number, which identifies the specific process that should handle the incoming data[4][5].

2. **Ports**: A port number allows the operating system to direct incoming traffic to the correct application. For example, HTTP traffic typically uses port 80, while HTTPS uses port 443[4][5]. 

3. **Inter-process Communication (IPC)**: This includes mechanisms like message queues, pipes, and shared memory, allowing processes to exchange data even if they are not on the same machine[6]. 

This architecture enables robust communication between processes and external systems.

Citations:
[1] Communicating between two processes on heroku (what port to ... https://stackoverflow.com/questions/9562170/communicating-between-two-processes-on-heroku-what-port-to-use
[2] Ports used for connections - Configuration Manager https://learn.microsoft.com/en-us/mem/configmgr/core/plan-design/hierarchy/ports
[3] Consume the output of external program at a process' own pace https://elixirforum.com/t/consume-the-output-of-external-program-at-a-process-own-pace/25960
[4] What are port numbers and how do they work? - TechTarget https://www.techtarget.com/searchnetworking/definition/port-number
[5] What Are Ports? | How Do Ports Work? - Akamai https://www.akamai.com/glossary/what-are-ports
[6] Inter-process communication - Wikipedia https://en.wikipedia.org/wiki/Inter-process_communication
[7] Inter-Process Communication, Technique T1559 - MITRE ATT&CK® https://attack.mitre.org/techniques/T1559/
[8] Process Communication - an overview | ScienceDirect Topics https://www.sciencedirect.com/topics/computer-science/process-communication
