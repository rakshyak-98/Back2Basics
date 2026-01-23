```js
const EventEmitter = require('events');  // or: import { EventEmitter } from 'events';

// Most built-in modules already use it internally (http, fs, stream, process, etc.)
```

> [!INFO]
> You can create your own event emitters too.

|Method|What it does|Example|
|---|---|---|
|`.on(eventName, listener)`|Register a function to call when event happens|`ee.on('userLogin', callback)`|
|`.emit(eventName, ...args)`|Trigger/fire the event (call all listeners)|`ee.emit('userLogin', user)`|
|`.once(eventName, listener)`|Like `.on`, but listener runs **only once**|Useful for "first connection" events|