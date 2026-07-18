Protocol designed to standardise the way development tools (like VS Code, IntelliJ, or Vim) talk to debugger (like [[gdb]], [[LLDB]], or NodeJS runtime debuggers).

## DAP Architecture

DAP acts as a universal "Translator" or intermediate layer between the Development Tool (client) and Debugger (Server/Adapter).
By using DAP, the ecosystem collapses from an M x N problem to an M + N problem. Any editor that implements the DAP client can debug any language that provides a DAP-compliant adapter.

## How DAP communication flow

DAP operates as a request-response protocol, typically running over JSON-RPC.

1. Client (IDE/Editor) -> Sends JSON requests to the debug adapter (e.g., `setBreakpoints`, `next`)
2. Debug Adapter -> Receives these generic requests and translates them into language specific commands that the actual runtime/debugger understands (e.g., GDB commands or V8 inspector protocols).
3. Debugger (Runtime) -> Executes the low-level instructions and returns the state (call stack, variable values) back through the adapter.


> Decoupling -> IDE Developers don't need to know the internals of how a specific language runtime handles memory or stack frames.
> Consistency -> Features like breakpoints, variable inspection, and watch windows look and behave identically, regardless of whether you are debugging C++, Python or Rust.
> Portability -> You can write a single Debug Adapter once, and it will immediately work in any IDE that support DAP.

| **Protocol** | **Purpose**           | **Key Functionalities**                                                   |
| ------------ | --------------------- | ------------------------------------------------------------------------- |
| **LSP**      | **Code Intelligence** | Autocomplete, "Go to Definition," linting, refactoring.                   |
| **DAP**      | **Runtime Execution** | Breakpoints, stepping through code, variable inspection, memory analysis. |
