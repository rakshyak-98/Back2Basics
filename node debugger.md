
## Text only REPL-style debugger.

``` bash
node inspect <script>; # start debugger.
```
- Add one or more `debugger;` statements where you want execution to pause


`pwd-node` -> refers to a Node.js debugger provided by the JavaScript Debugger extension in VS Code, which is built into the IDE by default.

> [!INFO]
> `pwd-node` debugger is designed to handle Node.js applications and leverages the Chrome DeveTools Protocol (also know as the Inspector Protocol) to provide a robust debugging experience.
> - it supports advanced features like conditional breakpoints, watch expression, call stack inspection, and better integration with tools like Chrome DevTools.

```json
// launch.json

{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "pwa-node",
      "request": "launch",
      "name": "Launch Program",
      "program": "${workspaceFolder}/index.js",
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
```
- "type": "pwa-node": Specifies the debugger type as the modern Node.js debugger.
- "request": "launch": Indicates that the debugger will launch the Node.js application. Alternatively, "attach" can be used to connect to an already running Node.js process.
- "name": A user-friendly name for the configuration, shown in the debug dropdown.
- "program": The entry point of your Node.js application (e.g., index.js).
- "skipFiles": Excludes internal Node.js modules from debugging to focus on your code.

## How it works when running the debugger

- **Launch Mode**:
	- If request is set to "launch", VS Code starts a new Node.js process with debugging enabled (equivalent to running node --inspect or node --inspect-brk).
	- The debugger automatically attaches to this process, allowing you to set breakpoints, step through code, and inspect variables.
- **Attach Mode**:
	- If request is set to "attach", the debugger connects to an existing Node.js process that was started with the --inspect or --inspect-brk flag (e.g., node --inspect index.js).
	- You need to specify the port (default is 9229) and other settings like address or remoteRoot if debugging remotely or in a container.
- **Debugging Features**:
	- You can set breakpoints by clicking to the left of line numbers in your code.
	- The debugger pauses execution at breakpoints, allowing you to inspect variables, view the call stack, and step through code using controls like "Step Over," "Step Into," or "Continue."
	- Source maps are supported, enabling debugging of transpiled code (e.g., TypeScript or minified JavaScript).

### Troubleshooting Common Issues

1. **Debugger Not Attaching**:
	- Ensure the Node.js process is running with --inspect or --inspect-brk (e.g., node --inspect index.js).
	- Check that the port specified in launch.json (default 9229) matches the port used by the Node.js process.
	- Verify that skipFiles is set to ["<node_internals>/**"] to avoid stepping into Node.js core modules.
2. **Breakpoints Not Hitting**:
	- Ensure source maps are enabled if debugging transpiled code (e.g., TypeScript). Add "sourceMaps": true to your launch.json.
	- Check that the localRoot and remoteRoot paths are correctly configured for remote or containerized debugging.
3. **pwa-node Not Recognized**:
	- Confirm that the JavaScript Debugger extension is enabled in VS Code. It’s built-in by default, but older versions may require manual installation.
	- If using an older VS Code version, you might need to update or fall back to type: "node".

### Additional Tips
- **Nodemon Integration**: For auto-restarting apps during development, use pwa-node with nodemon by setting "runtimeExecutable": "nodemon" and "restart": true in launch.json.