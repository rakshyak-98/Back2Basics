## Destructuring assignment

- Copies values from arrays or objects into variables.
- Skip items with an extra comma: `[a, , c] = arr`
- Works with any iterable on the right side.
- Left side can be any valid assignment target: `[user.name, user.surname] = "john smith".split(" ")`
- Missing values become `undefined`: `let [firstName, lastName] = [];`
- Default values with `=`: `let {width = 100, height = 100, title = "Menu"} = options`
- Swap without temp: `({title, width, height} = {title: "Menu", width: 100, height: 100})`

> [!NOTE] Bare `{...}` looks like a code block. Wrap in `(...)` when assigning: `({a} = obj)`.
