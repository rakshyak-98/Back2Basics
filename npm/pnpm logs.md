[[npm]]

# pnpm logs

> pnpm logs — pNPM, like npm, stores logs when commands fail or require debug information.

## Mental model

**Say it in one breath:** pnpm logs — pNPM, like npm, stores logs when commands fail or require debug information.

### **Location of PNPM Logs**
PNPM, like npm, stores logs when commands fail or require debug information.
### 1. **Default PNPM Log Location**
PNPM logs are stored under the cache directory:
[]()- **Path**:
    ```
    ~/.local/share/pnpm/store/v3/tmp
    ```
    - **For Linux/Mac**: `/home/username/.local/share/pnpm/store/v3/tmp/`
    - **For Windows**: `C:\Users\username\AppData\Local\pnpm\store\v3\tmp\`
### 2. **Generate Logs in Verbose Mode**
PNPM does not always generate detailed logs unless requested. Use `--reporter ndjson` or `--loglevel` options for debug logs.
- **Run a PNPM Command with Debug Logs**:
    ```bash
    pnpm install --loglevel debug
    ```
    - It outputs detailed logs directly in the terminal.
### 3. **Redirect PNPM Logs to a File**
Manually redirect PNPM output to a file for storage:
- **Example**:
    ```bash
    pnpm install > pnpm-debug.log 2>&1
    ```
- **View the Logs**:
    ```bash

## Related

[[npm]]
