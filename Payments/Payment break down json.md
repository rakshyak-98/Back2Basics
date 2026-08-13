[[Payments]]

# Payment break down json

> Payment break down json — "lengthOfStay": "At check in, the front desk will verify your check-out date. Rates quoted are based on check-in date and length…

---

## How it works

```json
{
  "data": {
    "createReservation": {
      "data": {
        "digitalPayment": null,
        "enroll": {
          "hhonorsNumber": null,
          "resourceAlreadyExists": true
        },
        "mfa": null,
        "sca": null,
        "reservation": {
          "addOnsResModifyEligible": false,
          "confNumber": "54129806",
          "arrivalDate": "2025-04-27",
          "departureDate": "2025-04-30",
          "cancelEligible": true,
          "modifyEligible": true,
          "cxlNumber": null,
          "restricted": false,
          "adjoiningRoomStay": false,
          "adjoiningRoomsFailure": null,
          "scaRequired": false,
          "autoUpgradedStay": false,
          "showAutoUpgradeIndicator": false,
          "specialRateOptions": {
            "corporateId": null,
            "groupCode": null,
            "hhonors": false,
            "pnd": null,
            "promoCode": null,


---

## Standard config / commands

```bash
# version + config path
# dry-run when available
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Retry storm | backoff / jitter | Cap retries; circuit break |
| Config drift | plan/apply or lockfile | Single source of truth |
| Poison message | DLQ | Quarantine and alert |

---

## Gotchas

> [!WARNING]
> Make retries safe or you will duplicate side effects.

---

## When NOT to use

- Avoid the tool if a simpler built-in covers the job.

---

## Related

[[Payments]]

## Sources

- [Wikipedia — Payment break down json](https://en.wikipedia.org/wiki/Payment_break_down_json)
