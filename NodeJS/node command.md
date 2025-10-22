#### run if Node.js environment is not accessible
```bash
set -gx NVM_DIR $HOME/.nvm;
nvm install lts;
set --universal nvm_default_version lts;
```

```bash
node -e "import 'dotenv/config'; console.log(process.env)"
```