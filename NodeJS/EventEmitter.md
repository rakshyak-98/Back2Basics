```js
const EventEmitter = require('events');

class MyEmitter extends EventEmitter {}
const myEmitter = new MyEmitter();

// 1. Listen for an event
myEmitter.on('coffeeReady', (size, type) => {
  console.log(`☕ Your ${size} ${type} is ready! Enjoy!`);
});

// Optional: listen only once
myEmitter.once('coffeeReady', () => {
  console.log('(First time only) Sending notification to phone...');
});

// 2. Later... something happens → emit the event
setTimeout(() => {
  myEmitter.emit('coffeeReady', 'large', 'cappuccino');
}, 2000);

// Output after 2 seconds:
// ☕ Your large cappuccino is ready! Enjoy!
// (First time only) Sending notification to phone...
```

## File read

```js
const fs = require('fs');

const reader = fs.createReadStream('large-video.mp4');

reader.on('data', (chunk) => {
  console.log(`Received ${chunk.length} bytes`);
});

reader.on('end', () => {
  console.log('File completely read ✅');
});

reader.on('error', (err) => {
  console.error('Oh no!', err);
});
```