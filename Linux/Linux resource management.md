### Managed Out-of-Memory
The path `/run/systemd/io.system.ManagedOOM` Memory management feature provided by `systemd`
- Purpose is a control interface used by `systemd-oomd`, a system service responsible for monitoring and managing system memory pressure.
- it is part of the linux `cgroups` (control groups) infrastructure that allows tracking and limiting resources usage.
- helps avoid system instability during out-of-memory conditions by identifying and killing processes consuming excessive memory. It operates based on policies and resource pressure thresholds.
```shell
systemctl status systemd-oomd;
journalctl -u systemd-oomd;
```
- config: `/etc/systemd/oomd.conf`

```bash
pmap -x $(pidof <process name>)
```
Here is a list of essential command-line interface (CLI) commands for monitoring performance on Linux operating systems:

### 1. **top**
Displays real-time information about running processes, including CPU and memory usage. It updates continuously, allowing administrators to monitor system performance dynamically.

### 2. **htop**
An enhanced version of `top`, providing a more user-friendly interface with color-coded output. It allows for easier sorting and filtering of processes.

### 3. **vmstat**
Reports on system memory, processes, and CPU activity. It provides snapshots of various statistics, helping to identify resource constraints over time.

### 4. **free**
Displays memory usage, showing total, used, and available memory, including swap space. Useful for quickly assessing memory status.

### 5. **iostat**
Monitors disk input/output statistics and CPU utilization. It helps identify disk performance issues and throughput.

### 6. **netstat**
Shows network connections, routing tables, and interface statistics. It is useful for diagnosing network-related issues.

### 7. **iftop**
Monitors network traffic in real-time, displaying bandwidth usage per connection. It helps identify bandwidth-hungry applications.

### 8. **sar**
Collects and reports system activity information over time, covering CPU, memory, and I/O statistics. It is useful for historical performance analysis.

### 9. **dstat**
Combines the functionality of various monitoring tools, providing real-time performance monitoring of CPU, disk, network, and other resources.

### 10. **mpstat**
Displays CPU usage statistics, allowing for monitoring of individual CPU cores.

### 11. **atop**
Shows resource utilization by process, user, and CPU usage history, providing a comprehensive view of system performance.

### 12. **pidstat**
Reports statistics for individual processes, including CPU, memory, and I/O usage.

### 13. **lsof**
Lists open files and the processes that opened them, which is useful for diagnosing file system issues.

### 14. **tcpdump**
Captures and analyzes network packets, useful for network troubleshooting and analysis.

### 15. **strace**
Traces system calls and signals for a running process, helpful for debugging and performance tuning.

Citations:
[1] https://www.tecmint.com/command-line-tools-to-monitor-linux-performance/
[2] https://www.geeksforgeeks.org/linux-system-monitoring-commands-and-tools/
[3] https://www.linuxteck.com/linux-system-monitoring-command-cheat-sheet/
[4] https://www.linkedin.com/advice/0/what-best-linux-system-performance-commands
[5] https://www.fosslinux.com/112297/linux-performance-commands-for-system-administrators.htm
[6] https://gcore.com/learning/linux-system-monitoring-command-line/
[7] https://www.site24x7.com/learn/linux/monitor-linux-server-performance.htmel