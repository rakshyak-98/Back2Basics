> [!INFO] in most libraries, *multi statements are disallowed by default* to prevent SQL injection
```mysql
SELECT * FROM user WHERE id = 3; DROP DATABASE test; 
```
- this is valid SQL syntax if urn directly in the MySQL cli or with `multiStatements: true`


- Enable `multipleStatement`
```js
const conn = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'test',
  multipleStatements: true // <== Add this
});

```
- use parameterized queries or [[ORM]] (e.g., [[Prisma]], [[Sequelize]]) to avoid injections.
