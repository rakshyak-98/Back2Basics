### Types

- You can define global types once and use them anywhere without importing.

#### Global types

> [!NOTE] `declare` is TypeScript-only — it does not emit JavaScript.

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

- See [[ambient modules]] for typing third-party JS libraries.

## Namespaces

- Group related code across files.
- Avoid name clashes between modules.

## Compilation

- TypeScript can **incrementally compile** — only recompile files that changed since the last run.

The `node_modules/.tmp` folder holds temporary build files.

### How TypeScript finds type declarations

```shell
tsc --traceResolution; # show how types are resolved
tsc --explainFiles;    # list every file in the compile
tsc --showConfig;      # print effective tsconfig
```

```json
{
	"compilerOptions": {
		"traceResolution": true
	}
}
```

- Turn on verbose resolution logs in `tsconfig.json`.

### Reference directives

[triple-slash directives](https://www.typescriptlang.org/docs/handbook/triple-slash-directives.html)

```ts
/// <reference types="..." />
```

- Pull in types from another declaration file.
- Helps TypeScript find types from external packages.

> [!INFO] `dom.iterables`
> - Some DOM lists (e.g. `NodeList`) need `dom.iterable` in `lib` before you can use `forEach`, spread, etc.

```ts
// tsconfig.json
{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"]
  }
}

const elements = document.querySelectorAll("div");
elements.forEach(el => console.log(el)); // ✅ Works fine

```

```ts
const elements: NodeList = document.querySelectorAll("div");
elements.forEach(el => console.log(el)); // ❌ TypeScript error!

```
