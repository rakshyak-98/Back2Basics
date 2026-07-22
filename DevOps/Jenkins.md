[[GIT/git command]] [[Docker compose]] [[terraform]]

# Jenkins

> One-line: CI orchestrator — pipelines as code, agents execute steps; most outages are credentials, disk, or plugin drift — **operational field notes**.

## Mental model

Controller holds job config, queue, and UI. **Agents** (static VMs, Docker, K8s pods) run build steps. **Pipeline** = Groovy DSL (`Jenkinsfile`) or declarative stages calling shell, git, docker, etc.

```
Developer push → webhook/poll SCM → Jenkins queue
       → agent allocated → checkout → build → test → deploy
       → artifacts archived / notifications
```

| Concept | Role |
|---------|------|
| Controller | Schedules, stores config, serves UI |
| Agent / node | Executes steps (`agent { label 'docker' }`) |
| Executor | Slot on agent (one job step at a time per executor) |
| Workspace | Per-job checkout dir on agent — can fill disk |
| Credential | Username/password, SSH key, secret text — bound by ID |
| Shared library | Reusable Groovy `@Library` |

## Standard config / commands

```groovy
// Jenkinsfile (declarative baseline)
pipeline {
  agent { label 'linux && docker' }
  options {
    timeout(time: 45, unit: 'MINUTES')
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }
  environment {
    DOCKER_BUILDKIT = '1'
  }
  stages {
    stage('Checkout') { steps { checkout scm } }
    stage('Test') {
      steps { sh 'make test' }
      post { always { junit 'reports/**/*.xml' } }
    }
    stage('Build') {
      steps {
        withCredentials([string(credentialsId: 'npm-token', variable: 'NPM_TOKEN')]) {
          sh 'make build'
        }
      }
    }
  }
  post {
    failure { slackSend channel: '#ci', message: "Failed ${env.BUILD_URL}" }
  }
}
```

```shell
# Controller CLI (jenkins.war / container)
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth user:token help

# Agent connectivity from agent host
curl -I http://jenkins-controller:8080

# Clear stuck workspace (agent)
du -sh /var/lib/jenkins/workspace/* | sort -h
# Safe: delete workspace via UI "Wipe Out Workspace" or job config

# Thread dump (controller hung)
kill -3 $(pgrep -f jenkins.war)   # or Groovy script console: Thread.currentThread().getAllStackTraces()
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Jobs stuck in queue | `# executors` vs queue; agent offline | Bring agents online; add executors; label mismatch |
| `offline` agent | Agent log; JNLP/WebSocket port | Fix firewall 50000/JNLP; rotate agent secret; reconnect |
| `Insufficient permission` | Matrix auth / folder ACL | Job folder credentials scope; service account role |
| `Credentials not found` | Credential ID typo; folder vs global | Match `credentialsId` exactly; migrate to folder store |
| Random `No such DSL method` | Shared library version pin | Pin `@Library('lib@main')` → `@v1.2.3` |
| Builds pass, deploy wrong artifact | `latest` tag; no immutable tag | Tag with `BUILD_NUMBER` / git SHA; promote artifacts |
| Disk full on controller | `/var/lib/jenkins` workspace + logs | `buildDiscarder`; clean workspaces; move artifacts to S3 |
| Plugin upgrade broke pipeline | Manage Jenkins → plugin changelog | Pin plugin versions; test in staging controller |
| Git clone fails intermittently | SSH key agent vs HTTPS cred | Use credential binding; `GIT_SSH_COMMAND` with key |
| Docker pipeline fails | Agent has no docker.sock / DinD | Mount socket (security tradeoff) or Kaniko/buildkit |
| Slow every build | Checkout every time; no cache | shallow clone; cache deps; separate lightweight agents |

## Gotchas

> [!WARNING]
> **Controller disk exhaustion** takes down the entire CI platform. Monitor workspace + `$JENKINS_HOME` — not optional.

> [!WARNING]
> **Unpinned `@Library('foo@main')`** — one Groovy change breaks all pipelines. Version libraries like prod code.

- **Controller running builds** (`executor on master`) — disable for prod; agent-only execution.
- **Credential masking** isn't perfect — avoid `echo $SECRET` in shells; use `withCredentials` wrapping only needed steps.
- **Replay** mutates debugging — never replay-to-prod without merging fix to SCM Jenkinsfile.
- **Reverse proxy** (`X-Forwarded-For`, `JenkinsUrl`) misconfig → broken webhooks and agent URLs.
- **Orphaned agents** after K8s pod recycle — use ephemeral agents + pod template, not static pod names.

## When NOT to use

- Greenfield CI with container-native GitOps → GitHub Actions / GitLab CI may be simpler ops.
- Complex DAG data pipelines → [[Airflow]] or dedicated orchestrator, not Jenkins Groovy hacks.

## Related

[[GIT/git command]] · [[Docker compose]] · [[terraform]] · [[Airflow]]
