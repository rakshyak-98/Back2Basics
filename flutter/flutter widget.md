If `MaterialPageRoute` took a direct widget instance instead of a builder, you would have to create that screen's widget in memory before you even navigated to it.
By using `builder`, you are essentially giving Flutter a "recipe" rather than the "backed cake". Flutter will hold onto that recipe and only execute it (build the widget) at the exact moment the user navigates to that route.

The `builder` function provides a `BuildContext`

```dart
builder: (BuildContext context) => MyNewScreen(),
```
- every widget in Flutter need a `BuildContext` to know where it lives in the overall Widget tree. The context provide by the `builder` is the context of the new route, not the screen you are leaving.
- Because the `builder` is a function executed at runtime, it allows you to pass dynamic arguments to your new screen exactly when it is being created.