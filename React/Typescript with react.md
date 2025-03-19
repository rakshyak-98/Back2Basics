```shell
grep -r "defaultExportName" src/

```

> [!INFO] `useRef` has a type overload for the specific case in which the type argument doesn't include `null` but the initializer is `null`

React has a built-in interface, `Reducer` that takes two type arguments: the state and the action interface, both of which are readily available.

> [!WARNING] when we apply `forwardRef` to the component, the type argument is somehow forgotten and replace by `unknown`
- the problem is the `forwardRef` does not return a component with the same type that you pass into it.
```typescript
import React from 'react'
declare module "react" {
	function forwardRef<T, P = {}> (
		render: (props: P, ref: ForwardRef<T>) => ReactElement | null
	): (props: P & RefAttributes<T>) => ReactElement | null;
}
```
- Typescript definition file `*.d.ts` in source tree `<root>/react-augmented.d.ts`