[[Operating System]] [[MBR(Master Boot Record)]] [[Boot/UEFI]] [[logical partitions]] [[Persistent Block Storage]]

# MBR

> The Master Boot Record is the first 512-byte sector of a legacy BIOS-boot disk — partition table plus a tiny boot code stub that chain-loads the real bootloader.

**MBR** layout (classic):

```txt
Byte 0–445:   boot code (446 bytes max)
Byte 446–510: 4 × 16-byte partition entries
Byte 510–511: 0xAA55 signature
```

One partition may be marked **active** for BIOS handoff. Extended partitions enable [[logical partitions]] beyond four slots.

## Modern status

[[Boot/UEFI]] + GPT replaced MBR for new systems (>2 TiB disks, Secure Boot). MBR remains in CSM legacy mode and old images.

Boot repair on MBR disks: reinstall stage1/stage2 to the boot sector or embed GRUB in the gap after MBR.

## Sources

- Wikipedia: [Master boot record](https://en.wikipedia.org/wiki/Master_boot_record)
- GRUB documentation — BIOS boot installation
