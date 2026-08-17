[[Github action]] [[Airflow]] [[Docker compose]] [[terraform]] [[GIT/git command]] [[Slack]]

# Jenkins

> Continuous integration controller — pipelines as code, agents run the steps; outages usually come from credentials, disk, or plugin drift.

```txt
        Jenkins ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers use Jenkins to check whether you separate controller from agents…

## Sources
- [Jenkins User Handbook](https://www.jenkins.io/doc/book/) — deep-dive
- [Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/) — deep-dive
- [Wikipedia — Jenkins (software)](https://en.wikipedia.org/wiki/Jenkins_(software)) — overview

## Key Concepts
- **Controller:** schedules, stores job configuration, serves UI
- **Agent / node:** executes steps (`agent { label 'docker' }`)
- **Executor:** one concurrent step slot on an agent.
- **Workspace:** per-job checkout directory on the agent — common disk-fill culprit.
- **Credentials:** username/password, SSH key, secret text bound by ID
- **Shared library:** reusable Groovy via `@Library` — pin versions like production code.


- **Core:** Jenkins is an automation server: a controller schedules jobs and stores confi…

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

## Mistakes to Avoid
- **Mistake:** Running production builds on the controller
- **Mistake:** Unpinned `@Library('foo@main')`
- **Mistake:** Echoing secrets in shells
- **Mistake:** Replaying a fix straight to production without merging the `Jenk…
- **Mistake:** Ignoring reverse-proxy `JenkinsUrl` / `X-Forwarded-*`
- **Mistake:** Tagging deploy artifacts as `latest` instead of build number or …

## Pros/Cons or Trade-offs
- **Pro:** Extremely flexible Pipeline DSL and plugin ecosystem; fits legacy and on-prem.
- **Con:** Controller disk, plugin drift, and Groovy shared libraries become operational debt.
- **Con:** Greenfield GitHub/GitLab-native CI is often simpler to operate than a self-hosted Jenkins fleet.

## Comparison
- vs [[Github action]]: Actions are repository-native and hosted
- vs [[Airflow]]: Airflow orchestrates data/batch DAGs


### Use cases
- Teams keep a declarative `Jenkinsfile` per service: checkout, test, build wit…

- **Example:** Builds hang in the queue because Docker-labeled agents are offli…
