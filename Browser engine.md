also known as **Layout engine** or **rendering engine**

- primary job of a browser engine is to transform HTML documents and other resources of a web page into an interactive visual representation on a User's device.
- browser engine is not a stand-alone computer program.
- a browser engine enforces the [[content security policy]] between documents, handle navigation through hyperlinks and data submitted through forms, and implements the Document Object Model, exposed to scripts associated with the document.

### References

[Browser engine](https://en.wikipedia.org/wiki/Browser_engine)

> [!NOTE]
> CJS -> sync + dynamic -> incompatible with browser runtime.
> ESM -> async + static -> designed for browser runtime.

Browser support ESM (asynchronous + static)
- path is known at parse time.
- browser can build dependency graph before running code.
- pre-fetch modules is parallel.
- execute in order.
- no UI blocking.