```javscript
app.set()
```
- may store any value that you want, but certain names can be used to configure the behavior of the server.
- [app settings table](https://expressjs.com/en/4x/api.html#app.settings.table)

>[!NOTE ] calling `app.set('foo', true)` for a boolean property is same as calling `app.engable('foo')`. Similarly `app.set('foo', false)` is `app.disable('foo')`

> [!INFO] empty object (`{}`) if there was no body to parse, the `Content-Type` was not matched, or an error occurred.

>[!INFO] `reviver` parameter in `JSON.parse` is a function that allows you to transform the values during the parsing process

```javascript
const jsonString = '{"name": "John", "age": 25, "birthdate": "1990-01-15T00:00:00Z"}';

// Reviver function to convert birthdate string into a Date object
const reviver = (key, value) => {
  if (key === 'birthdate') {
    return new Date(value);
  }
  return value;
};

const parsedObject = JSON.parse(jsonString, reviver);

console.log(parsedObject);
// Output: { name: 'John', age: 25, birthdate: 1990-01-15T00:00:00.000Z }

console.log(parsedObject.birthdate instanceof Date);  // true
```

### Inspecting
```js
console.log(app._router.stack);
```
- property holds middleware and route definitions.