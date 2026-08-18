[[Linux]] [[nvidia-smi]]

# alsa

> ALSA (Advanced Linux Sound Architecture) is the kernel sound stack — desktops usually mix through PipeWire/Pulse on top.

## Mental model

**Say it in one breath:** ALSA owns the card; PipeWire/Pulse mix apps; `aplay`/`alsamixer` prove the hardware path.

```txt
app ──► PipeWire/Pulse ──► ALSA PCM ──► sound card
                 ↑
           alsamixer / amixer
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |

| **ALSA** | Kernel drivers + libs | “Hardware path is ALSA; desktop audio is usually PipeWire.” |
| --- | --- | --- |
| **PCM device** | `hw:X,Y` / `plughw` | “Wrong card index = silent speakers.” |
| **mixer** | Volume/mute controls | “Muted Master looks like ‘no sound’.” |
| **PipeWire/Pulse** | Session mixing | “Many apps share one card through the daemon.” |
| **asoundrc** | ALSA defaults | “A bad `~/.asoundrc` forces the wrong device.” |

## Standard config / commands

```bash
aplay -l
arecord -l
cat /proc/asound/cards
alsamixer          # F6 = card; unmute MM→00
amixer -c 0 sget Master
speaker-test -c 2 -t wav
lsmod | grep snd
```

| Knob | Why it matters |

| Default sink/PCM | Must match the real output device |
| --- | --- |
| `audio` group | Needed for raw device access |

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| No sound | `aplay -l`; alsamixer mute | Unmute; select card; restart PipeWire |
| Only HDMI works | Default device | Set sink in `pactl` / WirePlumber |
| Crackling | USB power / latency | Different port; raise PipeWire latency |
| Permission denied | Groups | `usermod -aG audio $USER` + re-login |
| Mic silent | Capture mute | Unmute Capture; check browser permission |

## Gotchas

> [!WARNING]
> **Chrome/Electron ≠ raw ALSA** — they use Pulse/PipeWire; fixing only `~/.asoundrc` often does nothing.

> [!WARNING]
> **Card index changes** after dock/HDMI — don’t hardcode `hw:0` in scripts.

## When NOT to use

- **Headless servers** — disable unused audio stacks; don’t chase ALSA.
- **Containers** — bind the host PipeWire socket; don’t expect cards inside.

## Related

[[Linux]] [[nvidia-smi]] [[terminal emulator]]
