> [!NOTE] System call are the primary means by which user applications interact with the kernel.
- these functions allow user programs to request services from the kernel, such as file operations, process control, and communication between processes.
- low level functions
- primary way for a program to interact with the operating system.
- __System call Table__ the Linux kernel uses a system call table where each entry is a pointer to a system call handler.
	- when a _system call_ is made, the kernel uses the system call number to look up the corresponding function pointer and execute the appropriate handler.

> [!INFO] When a program needs to request a service from the operating system's kernel, such as reading from a file, writing to a file, creating a new process,or communicating with hardware devices, it makes a system call.

> [!INFO] User programs operate in user mode.

### Computed calls
- process where the address of the function to be called is determined at runtime rather than at compile time.
#### how computed calls work
- __Function Pointer__ holds the address of a function.
	- the function to be called can be changed at runtime by assigning a different function's address to the pointer.
	- the function pointer is then used to call the function. Since the actual function being called can change, this provides flexibility and dynamism in program behavior.
- computed calls are crucial for implementing _polymorphism_ is __C language__.
	- _Structures_ can contain function pointers, allowing different structures to have different implementations of the same operations.

## `fsync`
- system call in operating systems that ensures data integrity by forcing data in memory buffers to be written to disk.
- commonly used in prevent data loss during power failures or crashes by synchronizing file content with the storage device.
### What happens middle of the `fsync` power failure?
If a power failure occurs during an `fsync` operation, **the data can become partially written**, leading to two potential outcomes:
1. **Data Corruption**: Part of the file may get corrupted. This is particularly common in file systems that do not handle atomic writes well, as only some of the file’s data blocks are written, leaving it in an inconsistent state.
2. **Metadata Inconsistency**: In addition to file data, file metadata (like size, timestamps) might be only partially updated. This mismatch can cause further corruption or prevent the file from being read properly.
### How File Systems Handle This Situation
To mitigate these issues, modern file systems employ strategies like:
- **Journaling** (e.g., Ext4, NTFS): Keeps a log (journal) of pending changes to ensure that incomplete operations do not corrupt the file. After a crash, the system can roll back to a safe state by referencing this journal.
- **Copy-on-Write (COW)** (e.g., ZFS, Btrfs): Instead of overwriting data, it writes to a new location and only updates metadata after the write completes. This approach ensures that either the old or the new data is intact after a crash.