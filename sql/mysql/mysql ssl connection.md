```js
const pool =  mysql.createPool({
	ssl: {
		ca: fs.readFileSync("./ca.pem"),
		rejectUnauthorize: true,
	},
	connectionTimeout: 1500,
	supportBigNumbers: true,
	binNumberStrings: true
})
```

Verify SSL is Actually used

```sql
SHOW STATUS LIKE 'Ssl_cipher';
```