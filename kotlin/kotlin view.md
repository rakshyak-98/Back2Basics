`binding` is a ViewBinding object that provides type-safe access to UI element from your layout XML file.

> [!INFO]
> Instead of using `findViewById()`, you use `binding.viewName` to access views

```kotlin
val progressBar = findViewById<ProgressBar>(R.id.progressBar);
progressBar.visibility = View.GONE


binding.progressBar.visibility = View.GONE; // Direct access
```

### Recycler View

A Recycler View is a container that displays a list of items on the screen efficiently. It `recycles` views as you scroll.