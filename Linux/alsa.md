[[Linux terminal]] [[commands/fonts commands]]

# alsa

> ALSA (Advanced Linux Sound Architecture) is the kernel sound layer — `aplay`, `amixer`, and `/proc/asound` expose cards and PCM devices to userspace.

Desktop sessions often route through **PipeWire** or **PulseAudio**, which still talk to ALSA devices underneath.

## List devices

```bash
aplay -l
arecord -l
cat /proc/asound/cards
```

## Volume and mute

```bash
amixer scontrols
amixer set Master 80%
amixer set Master mute
alsamixer    # TUI
```

## Test playback

```bash
speaker-test -c 2 -t wav
aplay /usr/share/sounds/alsa/Front_Center.wav
```

## Troubleshooting

| Symptom | Check |
|---------|-------|
| No sound after HDMI connect | `pactl list sinks` or re-plug; set default sink |
| Device busy | `lsof /dev/snd/*` |
| Wrong card default | `/etc/asound.conf` or `~/.asoundrc` |

## Related

[[Linux configuration]] · [[gnome Colorschem]]

## Sources

- [ALSA project documentation](https://www.alsa-project.org/wiki/Documentation)
- `man 1 amixer`, `man 1 aplay`
