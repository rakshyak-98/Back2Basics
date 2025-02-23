[graphql-yoga](https://github.com/dotansimha/graphql-yoga/tree/HEAD/packages/graphql-yoga)
[graphql-tag](https://www.npmjs.com/package/graphql-tag)
```shell
npm install graphql-yoga graphql
```

### Create graphql server
```js
const express = require("express");
const { createYoga } = require("graphql-yoga");
const { createSchema } = require("graphql-yoga");
const cors = require("cors");

const app = express();
app.use(cors()); // Enable CORS

// 1️⃣ Define the GraphQL schema
const typeDefs = `
  type Query {
    hello: String
  }
`;

// 2️⃣ Define the resolver functions
const resolvers = {
  Query: {
    hello: () => "Hello, GraphQL with Yoga!",
  },
};

// 3️⃣ Create the GraphQL Yoga instance
const yoga = createYoga({
  schema: createSchema({ typeDefs, resolvers }),
});

// 4️⃣ Use Yoga as middleware in Express
app.use("/graphql", yoga);

const PORT = 4000;
app.listen(PORT, () => {
  console.log(`🚀 Server running at http://localhost:${PORT}/graphql`);
});

```