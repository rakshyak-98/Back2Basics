- Universal Module Definition

> [!NOTE]
> - wrapper pattern that make a JS module run in any environment

**Why UMD exists?**
- Before ESM existed, browsers didn't support imports.
- libraries needed one build that 'universally' works.

- it aims to make module compatible with different module systems, including AMD, CommonJS, and global variables.
- pattern that allows JavaScript modules to be used in different environment, including the browser as a global variable.
- in context of UMD global it refer to a module that's made available as a global variable when the script is loaded in a browser environment that doesn't support module systems.

```javascript
window.MyLibrary
```

> [!NOTE] UMD is more about creating a wrapper that makes modules work across different environments, which may or may not have a `require` function depending on the specific environment.
 
 > [!INFO]
 > - `require("lib")` → Node reads file from disk instantly (fast, local).
 > - Browser `require("lib")` → would need to fetch over network (slow, unpredictable).
 > - If browser blocked JS execution until the file finished downloading → **UI freeze**, no rendering, no input, “browser hung”. Because of this, browsers **refused** to implement CJS semantics.

### Therefore

- Node → can use sync loader (filesystem).
- Browser → must use async loader (network).
- CJS → incompatible with async.
- Browser → needed a _new_ module system → ECMAScript Modules (ESM). 

### ESM is async for this reason
- `import` triggers async loading of modules.
- Dependency graph is resolved before execution.
- Browser never blocks the UI thread waiting for network.

**Statically analysed** -> A parser can determine (just by reading the code, not executing it)
- what modules you import
- what exports you provide
- the full dependency graph
- which function/variables are used/unused.