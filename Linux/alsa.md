[[Linux terminal]] [[Linux configuration]] [[gnome Colorschem]] [[commands/fonts commands]]

# alsa

> ALSA (Advanced Linux Sound Architecture) is the kernel sound layer — cards and PCM devices show up as `/dev/snd` and tools like `aplay` / `amixer`.





## Interview Relevance
Interviewers use sound-stack questions to see if you separate kernel drivers (ALSA) from userspace mixers (PipeWire / PulseAudio) when debugging “no audio” on Linux desktops and servers with HDMI audio.

## Sources
- [ALSA project documentation](https://www.alsa-project.org/wiki/Documentation) — overview
- `man 1 amixer`, `man 1 aplay` — deep-dive

## Core Definition
ALSA provides drivers, the mixer API, and PCM I/O. Desktop sessions usually talk to PipeWire or PulseAudio, which still open ALSA devices underneath.

## Key Concepts
- **Card / device / subdevice:** Hardware shows as card N, device M — `aplay -l` lists what the kernel sees.
- **PCM vs control:** Playback/capture streams vs mixer controls (`Master`, `PCM`, mute).
- **Default route:** `/etc/asound.conf` or `~/.asoundrc` picks the default card when multiple outputs exist (HDMI vs analog).
- **Userspace stack:** PipeWire/PulseAudio sit above ALSA; fixing sinks often means both layers.

## Technical Details
```bash
aplay -l
arecord -l
cat /proc/asound/cards

amixer scontrols
amixer set Master 80%
amixer set Master mute
alsamixer    # TUI

speaker-test -c 2 -t wav
aplay /usr/share/sounds/alsa/Front_Center.wav
```

| Symptom | Check |
|---------|-------|
| No sound after HDMI connect | `pactl list sinks` or re-plug; set default sink |
| Device busy | `lsof /dev/snd/*` |
| Wrong card default | `/etc/asound.conf` or `~/.asoundrc` |

## Real-World Applications
After docking a laptop to an HDMI monitor, playback stays on the laptop speakers until the default ALSA/PipeWire sink is switched to the HDMI card.

## Pros/Cons or Trade-offs
- **Pro:** Direct kernel control — works without a desktop sound server (servers, embedded).
- **Con:** Multi-app mixing and Bluetooth are painful without PulseAudio/PipeWire on top.

## Comparison
vs PipeWire/PulseAudio: ALSA is the device driver layer; those are session mixers and policy. vs OSS (legacy): ALSA replaced the older Open Sound System model on modern Linux.

## Mistakes to Avoid
- Editing only `alsamixer` while PipeWire still routes to a muted or disconnected sink.
- Assuming one “sound card” — HDMI often appears as a second ALSA card.
- Leaving a process holding `/dev/snd/*` and blaming the driver for “device busy.”
