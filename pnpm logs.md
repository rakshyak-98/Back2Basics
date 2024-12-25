### **Location of PNPM Logs**

PNPM, like npm, stores logs when commands fail or require debug information.

---

### 1. **Default PNPM Log Location**

PNPM logs are stored under the cache directory:

[]()- **Path**:
   
    ```
    ~/.local/share/pnpm/store/v3/tmp
    ```
    
    - **For Linux/Mac**: `/home/username/.local/share/pnpm/store/v3/tmp/`
    - **For Windows**: `C:\Users\username\AppData\Local\pnpm\store\v3\tmp\`

---

### 2. **Generate Logs in Verbose Mode**

PNPM does not always generate detailed logs unless requested. Use `--reporter ndjson` or `--loglevel` options for debug logs.

- **Run a PNPM Command with Debug Logs**:
    
    ```bash
    pnpm install --loglevel debug
    ```
    
    - It outputs detailed logs directly in the terminal.

---

### 3. **Redirect PNPM Logs to a File**

Manually redirect PNPM output to a file for storage:

- **Example**:
    
    ```bash
    pnpm install > pnpm-debug.log 2>&1
    ```
    
- **View the Logs**:
    
    ```bash
    cat pnpm-debug.log
    ```
    

---

### 4. **Real-Time JSON Logs**

To see structured logs, use the `--reporter` option with `ndjson` format:

- **Example**:
    
    ```bash
    pnpm install --reporter ndjson
    ```
    
    - The logs will output as JSON, making them easier to parse.

---

### 5. **Set PNPM Log Level**

Adjust log levels to get the necessary details:

- **Supported Levels**: `info`, `warn`, `error`, `debug`
    
- **Example**:
    
    ```bash
    pnpm config set loglevel debug
    ```
    
- **Reset to Default (info)**:
    
    ```bash
    pnpm config set loglevel info
    ```
    

---

### Summary of PNPM Logs:

| **Purpose**           | **Command or Path**                  |
| --------------------- | ------------------------------------ |
| Default logs location | `~/.local/share/pnpm/store/v3/tmp`   |
| Run with debug logs   | `pnpm install --loglevel debug`      |
| Structured JSON logs  | `pnpm install --reporter ndjson`     |
| Redirect logs to file | `pnpm install > pnpm-debug.log 2>&1` |
| Change log level      | `pnpm config set loglevel debug`     |

---