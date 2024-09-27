- temporary storage location in memory used to hold data while it's being transferred between two location or processes that operate at different speeds or different data transfer rates.
- used in input/output operations, networking, and inter-process communication to manage data flow efficiently.

### User space buffer and Kernel space buffers
- when an application performs I/O. it interacts with the kernel's [[Buffer cache]]
	- User space buffer: the application maintains a buffer in its own address space
	- System call: the application invokes a system call like `write()` passing the user buffer
	- Kernel copies data: the kernel copies the data from the user buffer to a kernel buffer using `copy_from_user()`
		- this indirection is necessary because user and kernel have different address spaces.
	- Kernel buffer cache: the kernel buffer is then added to the buffer cache to be written to disk

also view
[[buffer lifecycle]]