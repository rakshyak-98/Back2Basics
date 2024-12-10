The Prisma client is generated as a set of TypeScript or JavaScript files and is located in the `node_modules` directory.
- Default location `./node_modules/@prisma/client` this folder contains the generated code that Prisma uses to interact with the database.
- You do not directly edit this files; they are managed by Prisma

```shell
npx prisma generate; # generat the prisma client
```
- Read the `schema.prisma` file.
- Regenerate the Prisma Client files.

> [!INFO] Prisma uses generated internal files to map your high-level API calls into SQL queries.

## Customizing the Output Directory
- You can specify a custom directory for the generated Prisma Client in the `schema.prisma` file:
```js

```