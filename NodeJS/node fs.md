
Check if file exists

```js
import { access, constants } from "fs"
const fileExists = path => access(path, constants.F_OK).then(() => true).catch(() => false);

```

```js
import { existsSync } from "fs";

if(existsSync('./config.yaml')){
	console.log("Config found!");
}

```