- Universal Module Definition
- it aims to make module compatible with different module systems, including AMD, CommonJS, and global variables.
- pattern that allows JavaScript modules to be used in different environment, including the browser as a global variable.
- in context of UMD global it refer to a module that's made available as a global variable when the script is loaded in a browser environment that doesn't support module systems.
```javascript
window.MyLibrary
```

> [!NOTE] UMD is more about creating a wrapper that makes modules work across different environments, which may or may not have a `require` function depending on the specific environment.