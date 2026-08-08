[[Streaming]]

# SDP (Service Discovery Protocol)

> SDP (Service Discovery Protocol) — as SDP Server is a component in a Bluetooth device that advertises available services (like audio sink, file transfer, serial port, etc.) to

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

As SDP Server is a component in a Bluetooth device that advertises available services (like audio sink, file transfer, serial port, etc.) to remote devices.
- Runs on each Bluetooth device.
- Stores a **service record database** (XML-like structure).
- Responds to SDP queries from other devices during connection setup.
Example
- your phone connects to a Bluetooth speaker.
- the phone queries the speaker's **SDP server** to discover `A2DP` (audio profile).
- if supported, phone proceeds to connect using that profile.
| Profile   | Purpose                  |
| --------- | ------------------------ |
| A2DP      | Audio streaming          |
| HFP / HSP | Headset/hands-free       |
| OBEX      | File transfer            |
| HID       | Keyboard/mouse           |
| PAN       | Personal Area Networking |
| SPP       | Serial Port Profile      |
> [!INFO]
> you can see available SDP services via tools like
```bash
sdptool browse <bdaddr>;
```

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
