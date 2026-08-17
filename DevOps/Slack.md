[[webhook]] [[Messaging/webhook]] [[Jenkins]] [[Airflow]] [[orchestration]]

# Slack (ops & alerting)

> Team chat that receives HTTP posts from Alertmanager, PagerDuty, or CI so humans can triage — the webhook URL is a secret with channel write access.

```txt
        Slack (ops & alert ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about Slack in ops contexts to see if you separate noisy cha…

## Sources
- [Slack API — Incoming webhooks](https://api.slack.com/messaging/webhooks) — overview
- [Slack API — chat.postMessage](https://api.slack.com/methods/chat.postMessage) — deep-dive
- [Prometheus Alertmanager — Slack](https://prometheus.io/docs/alerting/latest/configuration/#slack_config) — overview

## Key Concepts
- **Incoming webhook:** simplest POST-to-channel path — URL is a secret.
- **Bot token / Web API:** needed for threads, reactions, message updates (`chat.postMessage`).
- **Severity routing:** warning → Slack; critical → PagerDuty plus Slack.
- **Channel hygiene:** separate development noise from production paging.
- **Not an audit log:** retention limits; keep Prometheus/CloudTrail as source of truth.


- **Core:** For operations, Slack is a notification and coordination surface: monitoring …

## Technical Details
```
Prometheus/CI ──► webhook POST JSON ──► #alerts channel
                         │
                         └── optional: threads, @channel, Block Kit for context
```

- Incoming webhook:

```bash
curl -X POST "$SLACK_WEBHOOK_URL" \
  -H 'Content-Type: application/json' \
  -d '{"text":"deploy production api v1.2.3 — success","username":"deploy-bot"}'
```

- Block Kit sketch:

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

- Alertmanager receiver:

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

- Bot API (threads):

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

## Mistakes to Avoid
- **Mistake:** Committing the webhook URL to git — rotate immediately if leaked
- **Mistake:** Using `@channel` on every deploy
- **Mistake:** Pasting high-cardinality metric dumps — link dashboards instead
- **Mistake:** Treating Slack as the sole SEV1 page path without SMS/phone esca…
- **Mistake:** Dumping environment variables or secrets into channel templates

## Pros/Cons or Trade-offs
- **Pro:** Fast human triage with context links and threaded incident chat.
- **Con:** Alert fatigue if every deploy `@channel`s.
- **Con:** Message history is not a durable audit or paging system for SEV1.

## Comparison
- vs PagerDuty/SMS: Slack coordinates; paging wakes humans for life-critical SEV1.
- vs ticket/status page: those remain the incident record; Slack is the hallway.
- vs raw email alerts: Slack is faster for teams already living in chat — still needs grouping.


### Use cases
- CI failure notifies `#ci`

- **Example:** Staging load tests page on-call because staging and production s…
