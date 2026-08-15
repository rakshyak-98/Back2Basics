[[dart]] [[flutter widget]] [[Functional Programing]]

# Dart functions

> First-class functions — assign to variables, pass as arguments, return from functions; tear-offs and closures power Flutter callbacks.

## Interview Relevance

Interviewers want first-class functions, optional/named params, tear-offs vs lambdas, and lexical closures capturing state.

## Sources

- [Dart — Functions](https://dart.dev/language/functions) — deep-dive

## Key Concepts

- **Functions are objects:** can be stored and passed.
- **Named / optional positional params:** clear call sites.
- **Tear-off:** `onPressed: controller.save` vs wrapper lambda.
- **Closures:** capture variables from enclosing scope.

## Technical Details

```dart
int add(int a, int b) => a + b;
final op = add;
final sum = op(2, 3);

void paint({required Canvas canvas, double scale = 1.0}) {}

// Tear-off
FloatingActionButton(onPressed: viewModel.increment);
```

| Form | Use |
|------|-----|
| `=>` expression | Short pure functions |
| Block body | Multiple statements |
| Named params | Readable Flutter widget APIs |

## Real-World Applications

Widget callbacks, `list.map((x) => …)`, and dependency injection of strategy functions.

**Example:** Prefer tear-offs when signatures match to avoid allocating a new lambda each rebuild.

## Pros/Cons or Trade-offs

- **Pro:** Expressive APIs; great for UI callbacks.
- **Con:** Accidental closure captures can retain objects longer than expected.

## Comparison

- vs Java lambdas: similar idea; Dart had first-class functions from early on.
- vs [[dart]]: language overview vs function-specific idioms.

## Mistakes to Avoid

- Creating new lambdas in `build` that break equality optimizations unnecessarily.
- Capturing huge objects in long-lived closures.
- Overusing optional positional params when named params are clearer.
