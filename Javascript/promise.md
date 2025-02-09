Why to switch to the promise-based API
- `async` `await` it's harder to create the kind of [[race condition]].
- with callback-based code, it's not only harder to figure out the order of code execution, it's also harder to control the order. Callback are harder to read and more error-prone to write.
- [[backpressure]] is naturally present when using the promise-based style.

## Promise All
```js
let names = ['iliakan', 'remy', 'jeresig'];

let requests = names.map(name => fetch(`https://api.github.com/users/${name}`));

Promise.all(requests)
  .then(responses => {
    for(let response of responses) {
      alert(`${response.url}: ${response.status}`); 
    }

    return responses;
  })
  .then(responses => Promise.all(responses.map(r => r.json())))
  .then(users => users.forEach(user => alert(user.name)));
	
```