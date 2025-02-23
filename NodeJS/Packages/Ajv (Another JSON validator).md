is a fast and flexible JavaScript library for JSON Schema validation.
- used for validate JSON data against JSON schema standards.

#### Installation
```shell
npm install ajv;
```

```js
const Ajv = require("ajv");
const ajv = new Ajv();

// Define JSON Schema
const schema = {
  type: "object",
  properties: {
    name: { type: "string" },
    age: { type: "integer", minimum: 18 },
    email: { type: "string", format: "email" }
  },
  required: ["name", "email"]
};

// JSON Data to Validate
const data = {
  name: "John Doe",
  age: 25,
  email: "john.doe@example.com"
};

// Compile Schema
const validate = ajv.compile(schema);

// Validate Data
const valid = validate(data);

if (valid) {
  console.log("✅ Data is valid!");
} else {
  console.log("❌ Validation errors:", validate.errors);
}

```

#### Handle errors
```js
const invalidData = {
  name: "Alice",
  age: 16,
  email: "not-an-email"
};

const isValid = validate(invalidData);
console.log("Valid?", isValid);
console.log("Errors:", validate.errors);

```

