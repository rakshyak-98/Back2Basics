- is a JavaScript library designed for creating and manipulating HTML templates.
- it simplifies the process of converting structured data into HTML markup or other text format using an intuitive syntax.
#### Features
- Lightweight: minified and gzipped size of only 1.9kb
- no dependencies
- Template system: It provides a single function, `Makr.up(template, context)`, that allows developers to inject data from a context object into a string template.

```html
<--! include the script -->
<script src="markup.min.js"></script>
```

#### Example of Template Rendering
```javascript
var context = {name: {first: "john", last: "doe"}};
var template = "Hi, {{name.first}}!";
var result = Mark.up(template, context);
```

#### Advance Features
- Array handling: `Markup.js` can iterate over arrays within the context, allowing for dynamic list generation.
```javascript
var context = { brothers: ["Jack", "Joe", "Jim"] };
var template = "<ul>{{brothers}}<li>{{.}}</li>{{/brothers}}</ul>";
var result = Mark.up(template, context); // "<ul><li>Jack</li><li>Joe</li><li>Jim</li></ul>"
```

#### Function call
- the library supports calling function on objects within the template.
```javascript
var context = { num: 1.23 };
var template = "{{num|call>toPrecision>5}}";
var result = Mark.up(template, context); // "1.2300"
```
- `num` is being accessed from the context.
- The `call` filter is used to invoke the `toPrecision` method on the number, formatting it to five significant digits.
