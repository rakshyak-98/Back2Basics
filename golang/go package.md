- each file start with a `package` declaration.
- `go.mod` it is used as the base path for imports within the module.
- A package is a collection of Go course files in the same directory that are compiled together.
- the import path is the unique identifier for a package. It is typically the directory path relative to the `GOPATH` or module root.

> [!NOTE] Each directory of your project determines the package structure. Each directory corresponds to a package.

> [!INFO] the visibility of (variables, functions, types, etc.) is determined by their capitalization.
- Identifiers that start with an uppercase letter are exported (public), while those that start with a lowercase letter are unexported (private)
- Go modules are a way to manage dependencies. A module is a collection of related Go package that are versioned together.
the `go.mod` file at the root of the module defines the module path and its dependencies.
