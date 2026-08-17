[[kotlin syntax]] [[android]] [[flutter widget]]

# Kotlin View Binding

> Generated binding class for an XML layout — type-safe getters for views so you avoid `findViewById` casts and null mistakes.

```txt
        Kotlin View Bindin ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Android interviews contrast `findViewById`, ButterKnife-era binders, View Bin…

## Sources
- [Android — View binding](https://developer.android.com/topic/libraries/view-binding) — deep-dive

## Key Concepts
- **Generated class:** `ActivityMainBinding` (from `activity_main.xml`).
- **Type-safe access:** `binding.titleText.text = …`
- **Lifecycle:** inflate in `onCreate` / `onCreateView`
- **Null safety:** binding replaces nullable `findViewById` results for required ids.

## Technical Details
- Enable in module `build.gradle`; inflate:

```kotlin
private lateinit var binding: ActivityMainBinding

override fun onCreate(savedInstanceState: Bundle?) {
  super.onCreate(savedInstanceState)
  binding = ActivityMainBinding.inflate(layoutInflater)
  setContentView(binding.root)
  binding.submitButton.setOnClickListener { /* … */ }
}
```

| Approach | Risk |
|----------|------|
| `findViewById` | Wrong id/type; boilerplate |
| View Binding | Compile-time views for that layout |
| Compose | Declarative UI; no XML binding |

## Mistakes to Avoid
- **Mistake:** Holding fragment binding after view destruction
- **Mistake:** Mixing outdated kotlin-synthetic plugins with View Binding
- **Mistake:** Assuming Compose and View Binding are interchangeable in one fil…

## Pros/Cons or Trade-offs
- **Pro:** Safer and faster than `findViewById`.
- **Con:** Still XML-based; Compose is the long-term direction for many teams.

## Comparison
- vs Data Binding: View Binding is lighter (no expression language).
- vs Flutter widgets: Flutter rebuilds widget trees; Android XML binding points at mutable views.


### Use cases
- Activities/Fragments still on XML migrate to View Binding quickly

- **Example:** Fragment leaks — null out `_binding` in `onDestroyView`.
