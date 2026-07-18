```shell
supervisorctl reread
supervisorctl update
supervisorctl start <program name>

```

```toml
# basic configuration
[program:celery_worker]
command=/path/to/your/virtualenv/bin/celery -A your_project_name worker -l info
directory=/path/to/your/project
user=your_unix_user
autostart=true
autorestart=true
stopasgroup=true
stdout_logfile=/var/log/celery/worker.log
stderr_logfile=/var/log/celery/worker.err

```