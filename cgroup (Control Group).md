Control Group (cgroup) in  system services (especially in Linux) is a kernel feature to:
- Group processes
- Limit / track / control resources (CPU, memory, IO, etc.)

User is system services
- every service gets its own cgroup
- `systemd` uses cgroups to mange services
- tracks all processes (event forks) under a service
- ensures resource usage can be attributed and managed per service.

#### Benefits
- precise resource isolation
- auto cleanup of forked processes

