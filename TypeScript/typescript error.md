## Augmentations for the global scope can only be directly nested in external modules or ambient module declarations.

The error can be fixed by adding the `export {}` statement at the end of the file. This turns the file into a module, which is required for global augmentations in TypeScript.

> [!NOTE] TypeScript allows global augmentations in modules. The empty export doesn't affect runtime behavior

> [!INFO] **"no overlap"** message in the error means that TypeScript is telling you these two types **do not share any common values** and thus, the comparison is likely incorrect.

### All declaration must have identical modifiers Error
- might have missed the `typeof` keyword and directly used the property when creating a generic type.