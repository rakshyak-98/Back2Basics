### Types
- You can define global level types, to use types without importing them and still use them in your code.
#### Global types
```typescript
declare type MyType = {
	name: string;
	age: number
}
```
```typescript
const person: MyType = {
	name: "john",
	age: 32
}
```

#### Ambient Modules
- 

## Namespaces
- used to organize and share code across multiple files.
- allow you to group related functionality into a single unit and prevent naming conflicts.

## Compilation
- TypeScript can perform incremental compilation, which means it only re-compiles files that have change since the last compilation.

the `node_modules/.tmp` directory is used to store temporary files generated during the build process.

### How does typescript identifies types declarations
```shell
tsc --traceResolution; # see how TypeScript resolves types.
tsc --explainFiles; # see which files TypeScript includes in the compilation.
tsc --showConfig; # to check type roots.
```

```json
{
	"compilerOptions": {
		"traceResolution": true
	}
}
```
- Enable verbose logging in `tsconfig.json`.

### Reference directives
[triple-slash directives](https://www.typescriptlang.org/docs/handbook/triple-slash-directives.html)
```ts
/// <reference types="..." />
```
- used to include type definitions from external declaration files.
- they ensure that TypeScript correctly resolves types from the specified pacakges.
