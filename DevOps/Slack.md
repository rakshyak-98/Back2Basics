[[webhook]] [[Messaging/Web hooks]] [[DevOps]] [[Jenkins]]

# Slack (ops & alerting)

> **Team notification bus for on-call** — Incoming Webhooks, Bot tokens, Workflow Builder, and Slack CLI for deploy/CI signals. Not a product pitch; wiring alerts that don't spam or leak secrets.

## Mental model

Slack receives **HTTP POST** (webhook URL or Web API with bot token) → message in channel/DM. Ops stack: **Alertmanager/PagerDuty/CI → Slack** for human triage. Webhook URL **is a secret** (anyone with URL can post).

```
Prometheus/CI ──► webhook POST JSON ──► #alerts channel
                         │
                         └── optional: threads, @channel, Block Kit for context
```

Separate **noisy dev channel** from **prod paging channel**; use **severity routing** (warning → Slack, critical → PagerDuty + Slack).

## Standard config / commands

### Incoming Webhook (fastest path)

1. Slack app → Incoming Webhooks → Add to workspace → pick channel.
2. Store URL in secret manager (not git).

```bash
curl -X POST "$SLACK_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d '{"text":"deploy prod api v1.2.3 — success","username":"deploy-bot"}'
```

### Block Kit (structured alert)

```json
{
  "blocks": [
    { "type": "header", "text": { "type": "plain_text", "text": "🔥 HighErrorRate prod-api" } },
    { "type": "section", "fields": [
      { "type": "mrkdwn", "text": "*Service:*\napi" },
      { "type": "mrkdwn", "text": "*Runbook:*\n<https://wiki/runbooks/api|open>" }
    ]},
    { "type": "actions", "elements": [
      { "type": "button", "text": { "type": "plain_text", "text": "Dashboard" },
        "url": "https://grafana/d/abc" }
    ]}
  ]
}
```

### Alertmanager → Slack

```yaml
receivers:
  - name: slack-prod
    slack_configs:
      - api_url: '<webhook>'
        channel: '#alerts-prod'
        send_resolved: true
        title: '{{ .Status | toUpper }} {{ .CommonLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
```

### GitHub Actions / CI

```yaml
- name: Notify Slack
  if: failure()
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
  run: |
    curl -X POST "$SLACK_WEBHOOK_URL" -H 'Content-Type: application/json' \
      -d "{\"text\":\"❌ ${GITHUB_REPOSITORY} ${GITHUB_REF_NAME} — ${GITHUB_RUN_ID}\"}"
```

### Bot token (interactive / threads)

- `chat.postMessage` with `xoxb-` token — needed for threads, reactions, updating messages.
- OAuth scopes: `chat:write`, `channels:read` minimum for posting.

```bash
curl https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"channel":"C123","text":"rollback started","thread_ts":"1234567890.123456"}'
```

### Slack CLI (app lifecycle)

```bash
# Install/manage Slack apps locally — see official docs
slack login
slack run   # dev mode for workflow apps
# Uninstall: slack cli guides/uninstalling-the-slack-cli
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `404 invalid_payload` | Malformed JSON; missing `text` or `blocks` | Validate JSON; min required fields |
| `403 / channel_not_found` | Webhook tied to channel; app not invited | Re-add app to private channel |
| Alerts stopped entirely | Rotated webhook; secret expired | Regenerate webhook; update vault/CI secret |
| Spam flood | Alert threshold too low; no grouping | Alertmanager `group_wait`/`group_interval`; inhibit rules |
| Secrets in channel | CI pasted env dump | Redact in template; use links to logs |
| Rate limited (`429`) | Burst during incident | Batch messages; thread updates vs new posts |
| Button links don't work | URL not https; Block Kit malformed | Fix block JSON |

## Gotchas

> [!WARNING]
> **Webhook URL in repo = full channel write access** — rotate immediately if leaked.

> [!WARNING]
> **`@channel` in every deploy** — alert fatigue; reserve for human-action-required prod incidents.

> [!WARNING]
> **Same webhook prod + staging** — staging load tests page on-call; separate apps/channels.

> [!WARNING]
> **Slack message ≠ audit log** — retain Prometheus/CloudTrail; Slack history retention limits.

## When NOT to use

- **Primary incident record** — use ticket + status page; Slack is coordination.
- **High-cardinality metrics dump** — link to dashboard, don't paste 200 lines.
- **Sole paging for life-critical** — add PagerDuty/SMS for SEV1.

## Related

[[webhook]] · [[Messaging/Web hooks]] · [[Jenkins]] · [[Airflow]] · [[DevOps]]
