> [!INFO] 
> extraneous -> A package is installed in `node_modules` but not listed in `dependencies` or `devDependencies` in `package.json`.

- [lodash](https://www.npmjs.com/package/lodash) - JavaScript utility library
- [mathjs](https://mathjs.org/)
- [vercel/ms](https://github.com/vercel/ms) use this package to easily convert time formats to milliseconds
- [express-validator]()
- [express-]
- [compression]
- [express-async-erros]
- [express-rate-limit]
- [express-session]
- [express-slow-down]
- [helmet]
- [http-graceful-shutdown]
- [http-status-code]
- [hpp](https://www.npmjs.com/package/hpp/v/0.1.2) -> middleware to **protect against HTTP Parameter Pollution attacks**
- [multer]
- [nocache]
- [swagger-u-express]
- [nodemailer]
- [cors](https://www.npmjs.com/package/cors)
- [file-type](https://www.npmjs.com/package/file-type) -> For detecting binary-based file formats, not text-based formats.
- [got]() - HTTP request library for NodeJS, alternative to axios and Node's built-in `http` module, provider stream support
- [uWebSocket](https://github.com/uNetworking/uWebSockets) -> low-latency [[WebSocket]] and HTTP server library written c++
- [class-transformer](https://www.npmjs.com/package/class-transformer) -> if you're using typeScript, this package is used for serializing and transforming objects.
- [node-cron](https://www.npmjs.com/package/node-cron) -> 
	- `node-cron` schedules tasks in-memory within the NodeJS process - not at the OS level.

## yup
```js
import * as yup from 'yup';

const schema = yup.object({
  guestDetails: yup.array().of(yup.object()).required(),
  personalDetails: yup.object({
    FirstName: yup.string().required(),
    LastName: yup.string().required(),
    Email: yup.string().email().required(),
    Mobile: yup.string().required(),
    Address: yup.string().required(),
    Country: yup.string().required(),
    State: yup.string().required(),
    Zipcode: yup.string().required(),
    Comment: yup.string().nullable(),
  }).required(),
});

```

```json
{
	guestDetails: [],
	personalDetails: {
		FirstName: "",
		LastName: "",
		Email: "",
		Mobile: "",
		Address: "",
		Country: "",
		State: "",
		Zipcode: "",
		Comment: "",
	},
}
```

## CORS
```js
origin: (origin, callback) => {
  const allowed = ["https://mydomain.com"];
  if (allowed.includes(origin)) return callback(null, true);
  return callback(new Error("Not allowed by CORS"));
}

```

## multer

> [!NOTE]
> This must be set by the browser or client when uploading files. If you're using `fetch`, do **not manually** set `Content-Type` when using `FormData` — let the browser do it.
> - The key must match the name you defined in `multer.single()` or `multer.array()`.

| Backend (`multer`)                                        | Frontend Requirement                         |
| --------------------------------------------------------- | -------------------------------------------- |
| `upload.single('file')`                                   | `formData.append('file', file)`              |
| `upload.array('files', 5)`                                | `formData.append('files', file1)` (multiple) |
| `upload.fields([{ name: 'avatar' }, { name: 'resume' }])` | Use matching keys for each                   |