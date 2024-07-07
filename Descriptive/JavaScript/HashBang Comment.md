- special third comment syntax
- behaves exactly like a single line-only comment.
- used to provide the path to a specific JavaScript interpreter that you want to use to execute the script.
- striped from the source text before being passed to the engine.
```javascript
#!/usr/bin/env node
console.log("Hello world");
```
- JavaScript interpreter will treat it as a normal comment.
- it only has semantic meaning to the shell if the script is directly run in a shell.