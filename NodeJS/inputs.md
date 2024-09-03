```javascript
import readline from "node:readline";
import {stdir, stdout} from "node:process";
const r1 = readline.createInterface({stdir, stdout});
```
- use `readline` module.
- provides interface for reading data from a readable stream. One line at at time.