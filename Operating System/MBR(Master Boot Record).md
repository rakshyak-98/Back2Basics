[[Operating System]] [[MBR]] [[UEFI]] [[Persistent Block Storage]]

# MBR(Master Boot Record)

> MBR is the first 512-byte sector of a disk — boot stub plus up to four primary partition entries (alias of [[MBR]]).

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** BIOS loads LBA0 to `0x7C00`; code chainloads a bootloader; the embedded table points at partitions (2 TiB / 4-slot limits).

```txt
LBA0 (512 B):  [ boot code ~446 | 4×16 B parts | 55 AA ]
```

Canonical deep note: [[MBR]].

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **MBR** | Master Boot Record | “First sector: code + partition table.” |
| **Primary** | One of four slots | “Need extended for more partitions.” |
| **0x55AA** | Signature | “BIOS checks the trailing magic.” |
| **2 TiB limit** | 32-bit LBA×512 | “Bigger disks need GPT.” |
| **Protective MBR** | GPT’s fake MBR | “Warns old tools the disk isn’t MBR.” |
| **GRUB i386-pc** | BIOS GRUB | “Embeds in post-MBR gap / BIOS boot.” |

### How the story goes

1. **BIOS POST** — select boot disk.
2. **Read MBR** — validate signature.
3. **Run boot code** — find active partition / load stage2.
4. **Hand off** — kernel path (legacy).

---

## Standard config / commands

```bash
sudo fdisk -l /dev/sda
sudo parted /dev/sda print
sudo dd if=/dev/sda bs=512 count=1 | hexdump -C | tail
sudo sfdisk -d /dev/sda > layout.txt
# Full playbook: [[MBR]]
```

| Knob | Why it matters |
|------|----------------|
| Active/boot flag | Which primary boots |
| Extended + logical | >4 partitions workaround |
| GRUB target `i386-pc` | BIOS vs UEFI install |
| Backup of sector 0 | Disaster recovery |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `no bootable device` | Signature / boot flag | Restore MBR; set bootable |
| Missing partitions | Overwritten table | `sfdisk` restore from backup |
| Disk >2 TiB unused | MBR addressing | Convert to GPT + UEFI |
| Dual-boot wiped | Last `grub-install` | Repair both boot paths |
| GPT disk “broken” | Someone wrote classic MBR | Stop; recover GPT backups |
| VM won’t boot | Firmware mode mismatch | Match BIOS↔MBR or UEFI↔GPT |

---

## Gotchas

> [!WARNING]
> **Alias file** — keep wording aligned with [[MBR]]; don’t fork facts.

> [!WARNING]
> **`dd` of sector 0** — easy to destroy; backup first.

> [!WARNING]
> **Extended partitions** — logical drives confuse some imaging tools.

> [!WARNING]
> **Cloud** — new images prefer GPT/UEFI; MBR is legacy path.

---

## When NOT to use

- **New UEFI deployments** — GPT + ESP ([[UEFI]], [[UEFI (2)]]).
- **Disks >2 TiB** — GPT only.
- **Explaining LPAR “logical partitions”** — different meaning ([[logical partitions]]).

---

## Related

[[MBR]] [[UEFI]] [[UEFI (2)]] [[Extensible Firmware interface (efi)]] [[Persistent Block Storage]] [[logical partitions]]
