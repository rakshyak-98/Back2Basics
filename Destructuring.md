## Destructing assignment
- it _destructrizes_ by copying items into variables.
- ignore elements using comma
- work with any iterable on the right-side
- we can use any _assignables_ on the left side `[user.name, user.surname] = "john smith"`
- absent values are considered undefined. `let [firstName, lastName] = [];`
- for potentially missing properties we can set default values using `=` `let {widht = 100, height = 100, title = {title: "Menue"};`
- `({title, widht, height} = {title: "Menu", width: 100, height: 100})`

> [!NOTE] JavaScript assumes that we have a code block `{key: value, ...}`, that's why there's an error. To show JavaScript that it's not a code block, we can wrap the expression in parentheses `(...)`;
