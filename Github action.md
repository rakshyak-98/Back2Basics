## Actions
### Use secret in workflow
```yaml
steps:
  - name: Hello world action
    with: # Set the secret as an input
      super_secret: ${{ secrets.SuperSecret }}
    env: # Or as an environment variable
      super_secret: ${{ secrets.SuperSecret }}
```
### Pre-installed Run-times
- GitHub Action, executes in a virtual environment (like Ubuntu, Windows, or macOS) that GitHub provides.
- in workflow YAML file, you specify the environment in which your action runs.
- if your workflow is set to run on `ubuntu-latest`. It will use a virtual machine that already has Node.js installed.

## Workflow

workflows in git repository are defined in the `.github/workflow`

workflow triggers are events that cause a workflow to run:
- Events that occur in workflow's repository
- Event that occur outside of Github and trigger a **repository_dispatch** event on GitHub.

### Workflow components
#### actions
- reusable tasks the perform specific jobs withing a workflow
#### workflows
- automated processes defined in git repository that coordinate one or more jobs, triggered by events or on a schedule.
#### jobs
- groups of steps that executes on the same runner, typically running in parallel unless configured otherwise.
#### steps
- individual tasks within a job that run commands or actions sequentially.
#### runs
- instances of workflows execution triggered by events, representing the complete run-through of a workflow.
#### runners
- servers that host the environment where the jobs are executed, available as GitHub-hosted or self-hosted options.
#### marketplace
- a platform to find and share reusable actions, enhancing workflow capabilities with community-developed tools.

## Triggering schedule event
- schedule can use a `cron` expression to trigger a workflow at a specific time or day.
```yml
on:
	schedule:
		- cron: '30 5 * * 1,3'
		- cron: '30 5 * * 2,4'
jobs:
	test_schedule:
		runs-on: ubuntu-latest
		steps:
			- name: Not on Monday or Wednesday
			if: github.event.schedule !== '30 5 * * 1,3'
			run: echo "Skip this step on Monday and Wednesday"
			- name: Event time
			run: echo "This step will alsays run"
```

## Triggering Single or Multiple events
```yaml
name: CI on PUSH

on:
	push:
		branch:
			- main
jobs:
	build:
		- uses: actions/checkout@v2
		- name: Run a one-line script
		- run: echo "Hello, World!"
```

### How to disable CodeQL
1. go to repository settings
2. scroll to Security Left hand side
3. click on Code security.
4. scroll to Code Scanning section.
5. find tools section.
6. you can select and disable.