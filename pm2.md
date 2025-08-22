```sh
pm2 start npm --name <app name> -- start
pm2 save; # synchronized with saved list.
pm2 show <process id>; # view the details of the process.
pm2 env <process id>; # show all environment variabel of process id.
```

```sh
pm2 delete <app name | id | all>;
```

```bash
pm2 start app.js --watch --ignore-watch="node_modules logs .git"
```

`fastchi_pass` -> 

```txt
[PM2][WARN] Current process list is not synchronized with saved list. App booking-engine-app differs. Type 'pm2 save' to synchronize.
```
- this warning means `pm2` processes are not synced with saved list. If you reboot or use `pm2 resurrect` only the saved list is restored.
- `pm2` keeps 2 versions of your process list
	- current running process
	- saved process list `~/.pm2/dump.pm2`
	
> [!WARNING] your current process `<app name> ` will not auto restart unless saved.

## Config file
```js
module.exports = {
  apps: [
    {
      name: 'app',
      script: 'app.js',
      watch: true,
      ignore_watch: ['node_modules', 'logs', '.git'],
      watch_options: {
        followSymlinks: false
      }
    }
  ]
}
```

### pm2 modes
### Fork mode (default)
Runs a single instance of your app, like `node app.js`.
```bash
pm2 start app.js --name myapp -x; # x means fork mode;
```

### Cluster mode
Uses node.js cluster module to spawn multiple processes (one per CPU core, or a number you specify)
- Enable load balancing across cores.
```bash
pm2 start app.js -i max; # one process per CPU core.
```

#### Migrate an app from fork_mode to cluster mode
```bash
pm2 reload <app name> -i max;
```

```bash
pm2 describe <app name>;
```

## pm2 deployment system
```bash
pm2 forward <app name>;
```
- is used when you configure an app with pm2 deploy.

```bash
pm2 forward <app name> ;
[PM2] Updating to next commit repository for process name backend
[PM2] No versioning system found for process backend

```
- means that pm2 tried to fetch the next commit from Git for the process, but your app was not started using `pm2 deploy` with Git integration.

```bash
pm2 deploy ecosystem.config.js production setup;
pm2 deploy ecosystem.comfig.js production;
```

```bash
pm2 list --namespace <app name>;
```