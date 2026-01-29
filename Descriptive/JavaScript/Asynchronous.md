- things can happen independently of the main program flow.
- this thing runs in a cycle so fast that it's impossible to notice.
- programs internally use interrupts, a signal that's emitted to the processor to gain the attention of the system.
- when a program is waiting for a response from the network, it cannot halt the processor until the request finishes.
- async operations handled by using threads, spawning a new process.
in the current consumer computers, every program runs for a specific time slot and then it stops its execution to let another program continue their execution.

### functions

1. initiator style / input
2. middleware
3. terminator

### State management

Functions may or may not be state dependent.
- State dependency arises when the input or other variable of a function relies on an outside function.

#### strategies for state management

1. passing in variables directly to function
2. acquiring a variable value from a cache, session, file, database, network or other outside source.
> [!Warning] Managing state with global variable is ant-pattern that makes impossible to guarantee state.
- Making HTTP request using `fetch()`.
- Accessing a user's camera or microphone using `getUserMedia()`.
- Asking a user to select files using `showOpenFilePicker()`.

### Reference

- [Mixu's Node book](http://book.mixu.net/node/ch7.html)
- [async-flow-control](https://nodejs.org/en/learn/asynchronous-work/asynchronous-flow-control)