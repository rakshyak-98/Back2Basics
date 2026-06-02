`by` lets one object handle that logic of property on behalf of another object.

```kotlin
class User {
	val name: String
	get() {
		// custom logic
	}
}
```
- you can move that logic into a separate reusable class and delegate to it.

**Without delegation**

```kotlin
class User {
	private var _config: Config? = null_
	
	val config: Config
		get() {
			if (_config == null){
				_config = loadConfig()
			}
			return _config!!
		}
}
```

**With delegation**

```kotlin
val config by lazy {
	loadConfig();
}
```


Why was it added?
- To avoid repeating common property behavior.
- instead of implementing these in every class, Kotlin lets you resuse them through delegation.


> [!INFO]
> `viewModels<>()` is an Android KTX helper function that returns a property delegate for a ViewModel.

## Data flow

```text
ViewModel: _bookingList.postValue(response)
    ↓
Fragment: bookingList.observe() receives it
    ↓
Data is available in the response object
    ↓
forEach loop just prints it (debugging only)
```


## Adapter

An adapter is a bridge between data and the UI list (RecyclerView/ListView). When you update the adapter, it reference what's displayed on screen.

```text
Data (List of bookings)
    ↓
Adapter (converts data to UI views)
    ↓
RecyclerView (displays the views)
```