```sh
pm2 start npm --name <app name> -- start
pm2 save; # synchronized with saved list.
```

```sh
pm2 delete <app name | id | all>;
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