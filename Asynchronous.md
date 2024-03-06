- things can happen independently of the main program flow.
in the current consumer computers, every program runs for a specific time slot and then it stops its execution to let another program continue their execution.
- this thing runs in a cycle so fast that it's impossible to notice.
- programs internally use interrupts, a signal that's emitted to the processor to gain the attention of the system.
- when a program is waiting for a response from the network, it cannot halt the processor until the request finishes.
- async operations handled by using threads, spawning a new process.