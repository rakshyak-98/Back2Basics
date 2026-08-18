[[kotlin]]

# kotlin data flow

> kotlin data flow — by lets one object handle that logic of property on behalf of another object.

## Mental model

**Say it in one breath:** kotlin data flow — by lets one object handle that logic of property on behalf of another object.

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

## Related

[[kotlin]]
