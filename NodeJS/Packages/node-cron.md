## `node-cron`
- if you didn't save the reference, there is no way to stop or access it after it starts. it becomes garbage-managed, and you lose all control over it. It runs in the background as long as the Node process is alive.

> [!INFO] use a function wrapper to track auto-registers every task

```ts
const taskRegistry: cron.ScheduledTask[] = [];

function registerCron(...args: Parameters<typeof cron.schedule>) {
  const task = cron.schedule(...args);
  taskRegistry.push(task);
  return task;
}

// usage
registerCron('* * * * *', () => console.log('Running...'));

// later stop all
taskRegistry.forEach(t => t.stop());

```

> [!NOTE] always store a reference to your cron job if you may need to stop or inspect it.