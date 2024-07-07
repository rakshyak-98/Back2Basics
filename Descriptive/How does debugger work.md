1. Debugger initialization
2. Operating system interaction
3. Process Break
4. Context switching
5. Debugging Events
6. Exception Handling
7. User and kernel Modes
8. Symbolic Information
9. User interface
10. Control Transfer

## Debugger Initialization

debugger is launched and attaches to the target process.

- done by user or by an IDE

## Operating System interaction

- gain control over the target process.
- involves, system calls or special debug registers.

## Process break

- debugger pauses the execution of the target process.
- inserting breakpoints into the process’s code.
- break point specific instruction triggers an interrupt, causing the debugger to regain control.

## Context Switching

- operating system kernel performs a context switch to transfer control to the debugger.
- debugger then can inspect and modify the state of the target process (registers, memory, stack)

## Debugging Events

- break-points exception, signals, occur during the execution of the target process.

## Exception handling

- when event occurs, operating system kernel intervenes and transfers control to the debugger.
- debugger examines the event and decides hot to proceed.
- stepping through code, examining memory, or modifying registers.

## User and kernel modes

- debugger operates in both user and kernel modes.
- in user mode, they interact with the target process’s user-level code,
- in kernel mode they interact with the operating system kernel.

### Symbolic information

- debugger use symbolic information (debug symbols) to map machine code addresses to source code lines, function names, and variable names, This allows developers to debug at a higher level of abstraction.

## Control transfer

- debugger can resume of modify the execution of the target process based on user input. This involves relinquishing control back to the operating system kernel.

# How debugger really work

[article link](https://opensource.com/article/18/1/how-debuggers-work) by Levente Kurusa

### ptrace

- ptrace has quite a bit to do with signals.
- system call `ptrace` is a system call which manipulate almost all aspect of a process.

before the debugger can attach to the process, the _tracee_ has to call `ptrace` with the request `PTRACE_TRACEME`. This tells Linux that it is legitimate for the parent to attach via `ptrace` to this process.

_fork and execve_ provides an easy way of calling `ptrace` after fork but before the _tracee_ really starts using _execve_.

- fork will also return the pid of the tracee, which is required for using ptrace later.

important changes take place :

- Every time a signal is delivered to the tracee, it stops and a wait-event is delivered to the tracer that can be captured by the _wait_ family of system calls.
- each _execve_ system call will cause SIGTRAP **to be delivered to the tracee.
- The state of a process is captured by its registers

ptrace has a request to get the registers :

1. PTRACE_GETREGS
2. PTRACE_SETREGS
3. PTRACE_PEEKUSER and PTRACE_POKEUSER

- A debugger will sometimes need to read some parts of the memory or even modify it.
- the GNU Project Debugger (GDB) can use _print_ to get the value of a memory location or a variable.