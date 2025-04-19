## Script tag in html `async` and `defer`
render blocking -> when a script is discovered by the HTML parser, it stops the parsing, fetches the script from wherever you're loading it. Once it's downloaded, it executes the scripts, also still on the the main thread. And then it continue parsing the HTML.

`defer` -> only executed once the HTML parser has completed parsing.