```json
{
  "scripts": {
    "dev": "bash -c 'nodemon \"$0\"' --"
  }
}

```

```bash
npm run dev -- myfile.js;
```

`--` -> send every thing after as directly to the command. 


## Generate custom flag and read input

- Use a CLI parser

``` bash
npm install minimist yargs commander;
```