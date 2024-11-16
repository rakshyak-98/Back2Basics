## Augmentations for the global scope can only be directly nested in external modules or ambient module declarations.

The error can be fixed by adding the `export {}` statement at the end of the file. This turns the file into a module, which is required for global augmentations in TypeScript.

> [!NOTE] TypeScript allows global augmentations in modules. The empty export doesn't affect runtime behavior