[[Github action]] [[Airflow]] [[Docker compose]] [[terraform]] [[GIT/git command]] [[Slack]]

# Jenkins

> Continuous integration controller — pipelines as code, agents run the steps; outages usually come from credentials, disk, or plugin drift.





## Interview Relevance
Interviewers use Jenkins to check whether you separate controller from agents, treat `Jenkinsfile` as versioned code, and can debug queue/agent/credential failures without blaming “CI is flaky.”

## Sources
- [Jenkins User Handbook](https://www.jenkins.io/doc/book/) — deep-dive
- [Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/) — deep-dive
- [Wikipedia — Jenkins (software)](https://en.wikipedia.org/wiki/Jenkins_(software)) — overview

## Core Definition
Jenkins is an automation server: a controller schedules jobs and stores configuration, while agents execute build/test/deploy steps defined in Pipeline DSL (often a `Jenkinsfile` in source control).

## Key Concepts
- **Controller:** schedules, stores job configuration, serves UI — should not run heavy builds in production.
- **Agent / node:** executes steps (`agent { label 'docker' }`) — static VMs, Docker, or Kubernetes pods.
- **Executor:** one concurrent step slot on an agent.
- **Workspace:** per-job checkout directory on the agent — common disk-fill culprit.
- **Credentials:** username/password, SSH key, secret text bound by ID — scope global vs folder carefully.
- **Shared library:** reusable Groovy via `@Library` — pin versions like production code.

## Technical Details
```
Developer push → webhook/poll SCM → Jenkins queue
       → agent allocated → checkout → build → test → deploy
       → artifacts archived / notifications
```

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
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth user:token help
curl -I http://jenkins-controller:8080
du -sh /var/lib/jenkins/workspace/* | sort -h
kill -3 $(pgrep -f jenkins.war)   # thread dump if controller hung
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Jobs stuck in queue | Executor count; agent offline | Bring agents online; fix label mismatch |
| `offline` agent | Agent log; JNLP/WebSocket port | Firewall; rotate agent secret; reconnect |
| Credentials not found | ID typo; folder vs global | Match `credentialsId`; migrate to folder store |
| `No such DSL method` | Shared library drift | Pin `@Library('lib@v1.2.3')` |
| Disk full on controller | `$JENKINS_HOME` + workspaces | `buildDiscarder`; wipe workspaces; ship artifacts to object storage |
| Plugin upgrade broke pipeline | Plugin changelog | Pin versions; test on staging controller |

## Real-World Applications
Teams keep a declarative `Jenkinsfile` per service: checkout, test, build with credential binding, archive JUnit, notify [[Slack]] on failure.

**Example:** Builds hang in the queue because Docker-labeled agents are offline — restore agents and stop running executors on the controller.

## Pros/Cons or Trade-offs
- **Pro:** Extremely flexible Pipeline DSL and plugin ecosystem; fits legacy and on-prem.
- **Con:** Controller disk, plugin drift, and Groovy shared libraries become operational debt.
- **Con:** Greenfield GitHub/GitLab-native CI is often simpler to operate than a self-hosted Jenkins fleet.

## Comparison
- vs [[Github action]]: Actions are repository-native and hosted; Jenkins owns more of the platform ops surface.
- vs [[Airflow]]: Airflow orchestrates data/batch DAGs; Jenkins is CI/CD, not a substitute for ETL scheduling.

## Mistakes to Avoid
- Running production builds on the controller — agent-only execution.
- Unpinned `@Library('foo@main')` — one Groovy change breaks every pipeline.
- Echoing secrets in shells — wrap only needed steps in `withCredentials`.
- Replaying a fix straight to production without merging the `Jenkinsfile`.
- Ignoring reverse-proxy `JenkinsUrl` / `X-Forwarded-*` — broken webhooks and agent URLs.
- Tagging deploy artifacts as `latest` instead of build number or git SHA.
