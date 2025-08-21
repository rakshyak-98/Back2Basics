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