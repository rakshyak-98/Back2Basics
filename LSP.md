[Language Server Protocol](https://en.wikipedia.org/wiki/Language_Server_Protocol), is an open source JSON-RPC-based protocol for use between source code editors or IDE and servers that provide "language intelligence tools"
- features like *code completion*, *syntax highlighting* and marking of warnings and errors as well as refactoring routines.
- goal of the protocol is to allow programming language support independently. 
- native search-and-replace could introduce errors. Can replace the partial matches. It can rename identically-named variables in other scopes.
compiler or interpreters for a specific programming language are typically unable to provide these language services.
- compiler goal either transforming the source code into object code or immediately executing the code.
- in order to provide instant feedback to the user, the editing tool must be able to very quickly evaluate the syntactical and semantical consequences of a specific modification.
The LSP allow for decoupling language services from the editor so that the services may be contained within a general-purpose *language servers*.

### Technical overview
When a user edits one or more source code files using a language server protocol enabled tool
- tool acts as a client that consumes the *language services* provided by a *language server*.
- the tool may be text editor or IDE and the language service could be refactoring, code completion etc.
1. client informs the server about what the user is doing, opening a file or inserting a character at a specific text position.
2. the client can also request the server to perform a language service, to format a specified range in the text document.
3. the server answer's client's request with an appropriate response. The formatting request is answered either by a response that transfers the formatted text to the client or by an error response containing details about the error.
### Reference
- [Language server protocol explained](https://www.youtube.com/watch?v=2GqpdfIAhz8)

## Difference between Go to Reference, Definition, Implementation

| Feature              | Description                                                                    | Use case                                                                                      |
| -------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| Go to reference      | Find all occurrences of a symbol in the code.                                  | Locate all usages of a variable of function across the project.                               |
| Go to Definition     | Navigates to where the symbol is defined                                       | Jump to the exact line where a function, class or variable is defined.                        |
| Go to Implementation | Navigates tot he concrete implementation(s) of a method, function or interface | For an interface, jump to the class that implements it. For a virtual function, find override |