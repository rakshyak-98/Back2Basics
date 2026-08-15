[[webhook]] [[Messaging/webhook]] [[Jenkins]] [[Airflow]] [[orchestration]]

# Slack (ops & alerting)

> Team chat that receives HTTP posts from Alertmanager, PagerDuty, or CI so humans can triage — the webhook URL is a secret with channel write access.

## Interview Relevance

Interviewers ask about Slack in ops contexts to see if you separate noisy channels from paging channels, treat webhooks as credentials, and know Slack is coordination — not the system of record.

## Sources

- [Slack API — Incoming webhooks](https://api.slack.com/messaging/webhooks) — overview
- [Slack API — chat.postMessage](https://api.slack.com/methods/chat.postMessage) — deep-dive
- [Prometheus Alertmanager — Slack](https://prometheus.io/docs/alerting/latest/configuration/#slack_config) — overview

## Core Definition

For operations, Slack is a notification and coordination surface: monitoring and CI systems POST JSON via an incoming webhook or Bot User OAuth token (`xoxb-`) into a channel or DM, often with Block Kit for structured alerts.

## Key Concepts

- **Incoming webhook:** simplest POST-to-channel path — URL is a secret.
- **Bot token / Web API:** needed for threads, reactions, message updates (`chat.postMessage`).
- **Severity routing:** warning → Slack; critical → PagerDuty plus Slack.
- **Channel hygiene:** separate development noise from production paging.
- **Not an audit log:** retention limits; keep Prometheus/CloudTrail as source of truth.

## Technical Details

```
Prometheus/CI ──► webhook POST JSON ──► #alerts channel
                         │
                         └── optional: threads, @channel, Block Kit for context
```

Incoming webhook:

```bash
curl -X POST "$SLACK_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d '{"text":"deploy production api v1.2.3 — success","username":"deploy-bot"}'
```

Block Kit sketch:

```json
{
  "blocks": [
    { "type": "header", "text": { "type": "plain_text", "text": "HighErrorRate production-api" } },
    { "type": "section", "fields": [
      { "type": "mrkdwn", "text": "*Service:*\napi" },
      { "type": "mrkdwn", "text": "*Runbook:*\n<https://wiki/runbooks/api|open>" }
    ]}
  ]
}
```

Alertmanager receiver:

```yaml
receivers:
  - name: slack-production
    slack_configs:
      - api_url: '<webhook>'
        channel: '#alerts-prod'
        send_resolved: true
        title: '{{ .Status | toUpper }} {{ .CommonLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
```

Bot API (threads):

```bash
curl https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"channel":"C123","text":"rollback started","thread_ts":"1234567890.123456"}'
```

| Symptom | Check | Fix |
|---------|-------|-----|
| `invalid_payload` | Malformed JSON | Validate; require `text` or `blocks` |
| `channel_not_found` | App not in channel | Invite app; recreate webhook |
| Alerts stopped | Rotated webhook | Update vault/CI secret |
| Spam flood | Thresholds / no grouping | `group_wait` / inhibit rules |
| Rate limited (`429`) | Burst during incident | Batch; thread updates |

## Real-World Applications

CI failure notifies `#ci`; Alertmanager posts high-error-rate alerts with dashboard links; on-call threads updates during rollback.

**Example:** Staging load tests page on-call because staging and production share one webhook — use separate apps and channels.

## Pros/Cons or Trade-offs

- **Pro:** Fast human triage with context links and threaded incident chat.
- **Con:** Alert fatigue if every deploy `@channel`s.
- **Con:** Message history is not a durable audit or paging system for SEV1.

## Comparison

- vs PagerDuty/SMS: Slack coordinates; paging wakes humans for life-critical SEV1.
- vs ticket/status page: those remain the incident record; Slack is the hallway.
- vs raw email alerts: Slack is faster for teams already living in chat — still needs grouping.

## Mistakes to Avoid

- Committing the webhook URL to git — rotate immediately if leaked.
- Using `@channel` on every deploy — reserve for human-action-required production incidents.
- Pasting high-cardinality metric dumps — link dashboards instead.
- Treating Slack as the sole SEV1 page path without SMS/phone escalation.
- Dumping environment variables or secrets into channel templates.
