#!/usr/bin/env python3
"""Restore Standard config, Triage, Gotchas for notes stripped to boilerplate only."""

from __future__ import annotations

from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent

SECTIONS = """

## Standard config / commands

{std}

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
{triage}

---

## Gotchas

> [!WARNING]
> {gotcha}

---

## When NOT to use

- {when_not}

"""

NOTES: dict[str, dict[str, str]] = {
    "GIT/git commit.md": {
        "std": """```bash
git add file.txt
git commit -m "describe the change"
git commit --amend --no-edit          # add to last commit, keep message
git commit --amend -m "new message"
git status
git diff --cached                   # what will be committed
```""",
        "triage": """| Nothing to commit | `git status`; unstaged changes | `git add` first |
| Commit rejected (hook) | `.git/hooks/pre-commit` output | Fix hook failure or `--no-verify` only if policy allows |
| Wrong files committed | `git show --stat HEAD` | `git reset --soft HEAD~1` then re-stage |
| Author/email wrong | `git config user.name`; `git config user.email` | Set locally or globally before commit |""",
        "gotcha": "**Commit only stages what you added** — `git commit` does not pick up unstaged edits.",
        "when_not": "Do not commit secrets, build artifacts, or `.env` files — use `.gitignore`.",
    },
    "GIT/git diff.md": {
        "std": """```bash
git diff                            # unstaged changes
git diff --cached                   # staged changes
git diff HEAD                       # staged + unstaged
git diff main..feature              # commits on feature not on main
git diff branch1 branch2 -- path/   # one file between branches
git diff --stat
```""",
        "triage": """| Empty diff but file changed | Line endings / assume-unchanged | `git diff --ignore-cr-at-eol`; `git update-index` |
| Diff shows whole file | File mode or encoding flip | Check `core.filemode`; normalize encoding |
| Cannot diff binary | Expected for images/binaries | `git diff --numstat`; use external diff tool |
| Wrong comparison range | `..` versus `...` syntax | `A..B` = reachable from B not A; `A...B` = symmetric difference since merge base |""",
        "gotcha": "`git diff` without flags shows **working tree versus index** — not last commit.",
        "when_not": "Do not rely on diff alone for merge conflict resolution — open conflicted files and read conflict markers.",
    },
    "GIT/git error.md": {
        "std": """```bash
git status
git remote -v
GIT_TRACE=1 git fetch
git config --list --show-origin
```""",
        "triage": """| Permission denied (publickey) | SSH key loaded; remote URL | `ssh -T git@github.com`; fix `~/.ssh/config` |
| Repository not found | Remote URL; access token scope | Verify org/repo name and credentials |
| Failed to push (non-fast-forward) | Remote has new commits | `git pull --rebase` then push |
| Unable to index file | File permissions; line endings | `chmod`; check `core.autocrlf` |""",
        "gotcha": "Read the **first error line** in the message — later lines are often cascading noise.",
        "when_not": "Do not force-push to shared branches to silence errors — coordinate with the team.",
    },
    "GIT/git credential.md": {
        "std": """```bash
git config --global credential.helper cache
git config --global --unset credential.helper
git credential reject   # paste host=... protocol=https
```""",
        "triage": """| Repeated password prompts | Helper not configured | Set `credential.helper` or use SSH remote |
| Stored wrong password | Cached credentials | `git credential reject`; clear OS keychain entry |
| Token works in browser not git | Using account password not PAT | Create personal access token; use as password |
| HTTPS 401 after password change | Stale cache | Unset helper cache; re-authenticate |""",
        "gotcha": "Git credential helpers store secrets on disk or in the OS keychain — lock your workstation.",
        "when_not": "Do not embed tokens in remote URLs committed to the repository.",
    },
    "GIT/git commit template.md": {
        "std": """```bash
git config --global commit.template ~/.config/git/commit-template
cat ~/.config/git/commit-template
```""",
        "triage": """| Template not applied | Wrong path; not global | `git config --get commit.template`; use absolute path |
| Editor opens empty | Template path typo | Verify file exists and is readable |
| Template shows in log | Committed template file by mistake | Keep template outside repository or in dotfiles only |""",
        "gotcha": "The template pre-fills the editor — it does not enforce format unless hooks do.",
        "when_not": "Skip a template when a project mandates commitizen or another enforced format.",
    },
    "GIT/git guidlines.md": {
        "std": """Use conventional prefixes in subject line:
- `feat:` new behavior
- `fix:` bug repair
- `docs:` documentation only
- `chore:` tooling or maintenance""",
        "triage": """| History hard to read | Mixed message styles | Agree on prefix convention in team doc |
| Revert hard to find | No scope in subject | Add scope: `fix(auth): ...` |
| Broken bisect | WIP commits on main | Squash or rebase before merge to main |""",
        "gotcha": "One commit should be **one logical change** — easier to revert and bisect.",
        "when_not": "Do not rewrite published history on shared branches to fix message typos.",
    },
    "GIT/git repo config.md": {
        "std": """```bash
git config --local user.email "you@company.com"
git config --local core.hooksPath .githooks
git config --list --local
```""",
        "triage": """| Wrong identity on commits | Local versus global config | `git config --show-origin user.email` |
| Hooks not running | `core.hooksPath` unset | Set path; ensure scripts are executable |
| Line ending chaos on Windows | `core.autocrlf` mismatch | Align team policy; add `.gitattributes` |""",
        "gotcha": "Repository config in `.git/config` overrides global `~/.gitconfig` for the same keys.",
        "when_not": "Do not store secrets in repository config — use environment variables or a secret manager.",
    },
    "GIT/git ssh config.md": {
        "std": """```bash
# ~/.ssh/config
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_github
  IdentitiesOnly yes
chmod 600 ~/.ssh/config
```""",
        "triage": """| Bad owner or permissions on ~/.ssh/config | File mode or ownership | `chmod 600 ~/.ssh/config`; owned by your user |
| Wrong key offered | Multiple keys; no IdentitiesOnly | Set `IdentityFile` per Host block |
| Host key verification failed | DNS or MITM; rotated host key | Verify fingerprint; update `known_hosts` |
| Connection timed out | Firewall; wrong HostName | `ssh -vT git@github.com` |""",
        "gotcha": "SSH config `Host` is a **label** — it does not have to match the real DNS name.",
        "when_not": "Do not disable `StrictHostKeyChecking` in production automation.",
    },
    "ssh/ssh agent.md": {
        "std": """```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh-add -l
ssh-add -d ~/.ssh/id_ed25519    # remove one key
kill $SSH_AGENT_PID             # stop agent
```""",
        "triage": """| Could not open a connection to your authentication agent | Agent not running | Start `ssh-agent`; `eval` in shell |
| Permission denied still | Wrong key not loaded | `ssh-add -l`; add correct `IdentityFile` |
| Passphrase asked every time | Agent not started in login shell | Add agent start to shell profile or desktop keyring |
| Agent forwards in untrusted host | `ForwardAgent yes` | Disable agent forwarding except jump hosts you trust |""",
        "gotcha": "Keys in the agent are **decrypted in memory** — lock screen when away from the machine.",
        "when_not": "Do not run ssh-agent forwarding into untrusted servers.",
    },
    "ssh/ssh login.md": {
        "std": """```bash
ssh user@host
ssh -i ~/.ssh/id_ed25519 user@host
ssh -p 2222 user@host
ssh -J jump@bastion user@internal
```""",
        "triage": """| Connection refused | sshd down; wrong port | `ss -tlnp | grep 22`; check firewall |
| Permission denied (publickey) | Key not on server | Install public key in `~/.ssh/authorized_keys` |
| Too many authentication failures | Client offers too many keys | `IdentitiesOnly yes` in `~/.ssh/config` |
| Hangs after password | DNS reverse lookup delay | Server `UseDNS no` (administrator setting) |""",
        "gotcha": "SSH authenticates **the client key to the server** — username must exist on the server OS.",
        "when_not": "Do not enable password authentication on internet-facing servers if key-based login is available.",
    },
    "ssh/SSH authentication.md": {
        "std": """```bash
ssh -v user@host                 # verbose auth debug
ssh-keygen -lf ~/.ssh/id_ed25519.pub
cat ~/.ssh/authorized_keys
```""",
        "triage": """| Publickey denied | Key not in authorized_keys | Match `.pub` fingerprint on server |
| Wrong signature algorithm | Old server; new key type | Use ed25519 or rsa-sha2; check server `PubkeyAcceptedAlgorithms` |
| Keyboard-interactive loop | PAM or 2FA module | Complete second factor; check server logs |
| Certificate expired | SSH certificate auth | Re-sign host/user cert with CA |""",
        "gotcha": "Server chooses allowed methods — client cannot force publickey if the server disables it.",
        "when_not": "Do not share private keys between users or machines.",
    },
    "ssh/ssh private network.md": {
        "std": """```bash
ip route
ssh -J bastion.internal user@10.0.5.20
# ~/.ssh/config ProxyJump bastion.internal
```""",
        "triage": """| Timeout to private IP | No route; VPN down | Connect VPN; verify route to RFC1918 range |
| Bastion works; inner host fails | Security group; inner sshd | Open port 22 on inner SG; check inner sshd |
| Wrong source IP seen on inner host | Jump not used | Use `ProxyJump` or `-J` |
| MTU black hole | VPN plus small MTU | Lower interface MTU on client |""",
        "gotcha": "Private IPs are **not routable on the public internet** — you need VPN or a jump host.",
        "when_not": "Do not expose private RFC1918 addresses directly to the internet with port forwarding.",
    },
    "Nginx/directives.md": {
        "std": """See [[Configuration]] for full examples. Minimal server block:
```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
}
```""",
        "triage": """| Wrong server block chosen | `server_name` mismatch; default_server | Check `nginx -T`; SNI and listen order |
| 404 on existing file | `root`/`alias` path wrong | `namei -l /path`; permissions for `www-data` |
| Proxy returns 502 | upstream down; bad `proxy_pass` URL | `curl` backend; trailing slash rules |
| Config test fails | typo in directive name | `nginx -t` shows file:line |""",
        "gotcha": "`alias` replaces the matched location path — `root` appends the full URI.",
        "when_not": "Do not put TLS certificates only in the default_server block if you serve many names.",
    },
    "Nginx/nginx URL rewrite.md": {
        "std": """```nginx
rewrite ^/old/(.*)$ /new/$1 permanent;
location /api/ {
    rewrite ^/api/(.*)$ /$1 break;
    proxy_pass http://backend;
}
```""",
        "triage": """| Redirect loop | `rewrite` plus `try_files` interaction | Test with `curl -I`; simplify rules |
| Query string dropped | rewrite without `$args` | Append `$is_args$args` when needed |
| 301 when expecting internal | `permanent` flag | Use `last` or `break` for internal rewrite |
| Wrong backend path | `proxy_pass` URI part | With URI in proxy_pass, location prefix is replaced |""",
        "gotcha": "`rewrite ... permanent` sends **301** to the client — browser will cache it.",
        "when_not": "Prefer `return 301` for simple host or scheme redirects — clearer than rewrite.",
    },
    "Nginx/URL Rewriting.md": {
        "std": """```nginx
location /legacy/ {
    return 301 /new$request_uri;
}
```""",
        "triage": """| Old URLs still hit application | rewrite order; location precedence | More specific `location` wins; check `^~` prefix |
| Case-sensitive mismatch | `rewrite` is case-sensitive | Normalize with `lower` map or explicit rules |""",
        "gotcha": "Long rewrite chains are hard to debug — document each rule and test with `curl -I`.",
        "when_not": "Do not chain more than a few rewrites — use application routing for complex rules.",
    },
    "Nginx/multi-domain.md": {
        "std": """```nginx
server {
    listen 443 ssl;
    server_name a.example.com b.example.com;
    ssl_certificate     /etc/letsencrypt/live/a.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/a.example.com/privkey.pem;
}
```""",
        "triage": """| Certificate name mismatch | SNI; wrong cert on default | Separate `server` per cert or SAN cert |
| Wrong site content | `default_server` catches unknown Host | Set explicit `server_name` on each vhost |
| ACME challenge fails | `.well-known` not reachable | Dedicated location for `/.well-known/acme-challenge/` |""",
        "gotcha": "Each `server_name` needs a matching certificate unless you use a SAN or wildcard cert.",
        "when_not": "Do not serve many unrelated tenants from one `server` block without strict `server_name` lists.",
    },
    "Nginx/Nginx ingress.md": {
        "std": """```bash
kubectl get ingress -A
kubectl describe ingress my-app -n prod
helm upgrade ingress-nginx ingress-nginx/ingress-nginx -n ingress-nginx
```""",
        "triage": """| 404 from ingress | path rule; backend Service | `kubectl describe ingress`; check `pathType` |
| 502/503 | Endpoints empty; pod not ready | `kubectl get endpoints`; readiness probe |
| Certificate not issued | cert-manager issuer; challenge | `kubectl describe certificate` |
| Wrong host routed | Ingress class; duplicate ingress | Check `ingressClassName` and annotation precedence |""",
        "gotcha": "Ingress only routes HTTP — you still need a **Service** with healthy Endpoints behind it.",
        "when_not": "Use Gateway API instead of Ingress when you need advanced traffic splitting at scale.",
    },
    "Nginx/nginx core functionality.md": {
        "std": """Roles: reverse proxy, static file server, TLS termination, load balancer (`upstream`).""",
        "triage": """| High worker CPU | SSL renegotiation; gzip on huge files | Tune `worker_connections`; offload TLS |
| Slow static files | disk IO; sendfile off | Enable `sendfile`; check filesystem |
| Upstream flapping | health checks missing | `max_fails` and `fail_timeout` in upstream |""",
        "gotcha": "Nginx handles many connections with **few worker processes** — mis-tuned `worker_connections` causes 502 storms.",
        "when_not": "Do not use Nginx alone for WebSocket-heavy apps without proper `proxy_read_timeout` tuning.",
    },
    "Nginx/nginx fastcgi.md": {
        "std": """```nginx
location ~ \\.php$ {
    include fastcgi_params;
    fastcgi_pass unix:/run/php/php8.2-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
}
```""",
        "triage": """| 502 Bad Gateway | php-fpm socket down | `systemctl status php8.2-fpm`; socket path |
| File download instead of execute | missing `fastcgi_pass` | PHP must pass to FPM not `root` |
| PATH_INFO broken | split path info rules | Use documented `try_files` + fastcgi pattern |""",
        "gotcha": "`SCRIPT_FILENAME` must be the **real filesystem path** PHP can open.",
        "when_not": "Prefer php-fpm over legacy `mod_php` in Apache for isolation.",
    },
    "Nginx/static file.md": {
        "std": """```nginx
location /assets/ {
    alias /var/www/static/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```""",
        "triage": """| 403 Forbidden | directory listing off; perms | `chmod` for nginx user; `index` directive |
| Stale asset after deploy | browser cache | Cache-bust filenames; shorten `expires` on HTML |
| Wrong MIME type | missing types block | `include mime.types;` |""",
        "gotcha": "Use `alias` for prefix locations — trailing slash on both `location` and `alias` matters.",
        "when_not": "Do not serve user-uploaded files from the same path as executable scripts.",
    },
    "helm/helm.md": {
        "std": """```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-release bitnami/nginx
helm upgrade my-release bitnami/nginx -f values.yaml
helm rollback my-release 1
```""",
        "triage": """| Pending install forever | CRD missing; webhook timeout | `kubectl get events`; install CRDs first |
| Wrong chart version | repo not updated | `helm repo update`; pin version in install |
| Values ignored | wrong file; subchart key | `helm get values`; nest under chart name for subcharts |
| Release exists cannot install | name collision | `helm uninstall` or choose new release name |""",
        "gotcha": "Helm stores release state in cluster **Secrets** — protect etcd backups.",
        "when_not": "Do not hand-edit rendered manifests in the cluster — change values and upgrade.",
    },
    "helm/cli.md": {
        "std": """```bash
helm list -A
helm status my-release -n prod
helm get manifest my-release
helm template my-release ./chart --debug
```""",
        "triage": """| cannot re-use a name that is still in use | failed release not purged | `helm uninstall`; or `helm history` + rollback |
| connection refused to Kubernetes | kubeconfig context | `kubectl cluster-info`; fix `KUBECONFIG` |
| chart not found | repo not added | `helm search repo` after `helm repo add` |""",
        "gotcha": "`helm template` renders locally — it does not prove the cluster will accept resources.",
        "when_not": "Do not use `helm install` in production without version-pinned charts in CI.",
    },
    "Kubernates/Pods.md": {
        "std": """```bash
kubectl get pods -A -o wide
kubectl describe pod my-pod -n default
kubectl logs my-pod -c app
kubectl delete pod my-pod --grace-period=0 --force   # last resort
```""",
        "triage": """| CrashLoopBackOff | `kubectl logs --previous`; probe failures | Fix exit code; adjust command or probes |
| ImagePullBackOff | image name; pull secret | `kubectl describe pod`; fix registry auth |
| Pending | CPU/memory; PVC bind | `kubectl describe node`; check requests and storage class |
| Running but not Ready | readiness probe failing | Hit probe path from inside cluster |""",
        "gotcha": "Restarting a Pod **creates a new identity** — IP and in-memory state are lost unless volumes back them.",
        "when_not": "Do not run more than one main process per container — use sidecars for helpers.",
    },
    "Kubernates/Kubernetes services.md": {
        "std": """```bash
kubectl get svc -A
kubectl describe svc my-service
kubectl get endpoints my-service
```""",
        "triage": """| Service has no endpoints | selector mismatch; pods not ready | Labels on Pod template must match Service selector |
| ClusterIP works; NodePort does not | firewall; wrong nodePort | Open node port; curl node IP:port |
| DNS name does not resolve | CoreDNS down; wrong namespace | `kubectl -n kube-system get pods -l k8s-app=kube-dns` |
| External traffic not reaching pods | `externalTrafficPolicy: Local` | Check endpoints on node receiving traffic |""",
        "gotcha": "A Service is a **stable virtual IP** — kube-proxy or dataplane programs rules to Pod IPs behind it.",
        "when_not": "Do not use NodePort for production internet exposure — use LoadBalancer or Ingress.",
    },
    "Kubernates/Kubernetes config.md": {
        "std": """```bash
kubectl config view
kubectl config use-context prod
kubectl config set-context --current --namespace=team-a
```""",
        "triage": """| wrong cluster targeted | current context | `kubectl config current-context`; switch context |
| certificate expired | client cert on kubeconfig | Refresh credentials; `kubeadm` or cloud IAM |
| namespace not found | typo; context default namespace | `kubectl get ns`; set `-n` explicitly |""",
        "gotcha": "`~/.kube/config` merges multiple clusters — **context** picks cluster + user + default namespace.",
        "when_not": "Do not commit kubeconfig with embedded credentials to git.",
    },
    "Database/migration.md": {
        "std": """Use versioned migration files; apply in order; never edit applied migrations in production.""",
        "triage": """| Migration fails mid-way | transaction support per DDL | Fix forward-only migration; restore from backup if needed |
| Schema drift between environments | manual hotfix on prod | Reconcile via new migration; avoid hand-editing prod |
| Lock timeout during migration | long table rewrite | Run during maintenance window; use online DDL tools |""",
        "gotcha": "Destructive migrations need **backfill and verify** steps before dropping columns.",
        "when_not": "Do not run ad-hoc ALTER on production without a reviewed migration script.",
    },
    "Database/mysql/partitioning.md": {
        "std": """```sql
ALTER TABLE orders PARTITION BY RANGE (YEAR(created_at)) (
  PARTITION p2024 VALUES LESS THAN (2025),
  PARTITION p2025 VALUES LESS THAN (2026)
);
```""",
        "triage": """| Partition pruning not used | query misses partition key | Filter on partitioned column in WHERE |
| All rows in one partition | boundary values wrong | Redefine LESS THAN boundaries |
| Slow ALTER | copy entire table | Use online schema change tool for large tables |""",
        "gotcha": "Partitions help **prune scans** — they do not remove the need for indexes on query columns.",
        "when_not": "Do not partition tiny tables — overhead exceeds benefit.",
    },
    "Database/mysql partitioning.md": {
        "std": "See [[mysql/partitioning]] for commands and examples.",
        "triage": """| Duplicate note content | two partitioning notes | Prefer [[mysql/partitioning]] as canonical |""",
        "gotcha": "Keep one canonical partitioning note to avoid conflicting advice.",
        "when_not": "Remove duplicate stub if [[mysql/partitioning]] covers the topic.",
    },
    "Database/write-ahead logging.md": {
        "std": "WAL (Write-Ahead Log): commit records to log **before** applying pages to data files.",
        "triage": """| Data loss after crash | fsync disabled; wrong durability setting | Enable synchronous_commit / full WAL sync per engine docs |
| WAL disk full | long transactions; replication slot | Drop idle replication slots; increase disk; archive segments |
| Recovery slow | huge WAL backlog | Tune checkpoint; ensure archive command keeps up |""",
        "gotcha": "Without WAL fsync policy matching your durability goal, **committed transactions can vanish** after power loss.",
        "when_not": "Do not disable WAL on production databases to gain speed.",
    },
}


def fix_ssh_agent_header(text: str) -> str:
    text = text.replace(
        '# and define "github-personal" in ~/.ssh/config with the right IdentityFile',
        "# ssh agent",
    )
    text = text.replace("~/.ssh/configuration", "~/.ssh/config")
    text = text.replace(
        '> and define "github-personal" in ~/.ssh/config with the right IdentityFile',
        "> ssh agent — holds decrypted private keys in memory so you type the passphrase once per login session",
    )
    return text


def main() -> None:
    for rel, parts in NOTES.items():
        path = VAULT / rel
        if not path.exists():
            print("missing", rel)
            continue
        text = path.read_text(encoding="utf-8")
        if "## Standard config / commands" in text:
            print("skip (already has sections)", rel)
            continue
        block = SECTIONS.format(**parts)
        if "## Related" in text:
            text = text.replace("\n---\n\n## Related", block + "\n---\n\n## Related")
        else:
            text = text.rstrip() + block
        if rel == "ssh/ssh agent.md":
            text = fix_ssh_agent_header(text)
        if rel == "Kubernates/Pods.md":
            text = text.replace(
                "[[kubectl]]] [[[kubectl pod creation]]] [[[Kubernetes services]]] [[[ingress]]",
                "[[kubectl]] · [[kubectl pod creation]] · [[Kubernetes services]] · [[ingress]]",
            )
        path.write_text(text, encoding="utf-8")
        print("restored", rel)


if __name__ == "__main__":
    main()
