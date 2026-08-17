[[Linux system management]] [[inittramfs]] [[Linux configuration]]

# GRUB

> Bootloader that loads the kernel and initramfs — edit `/etc/default/grub`, then regenerate; never hand-edit `grub.cfg`.

```txt
        GRUB ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Boot recovery literacy: UEFI vs BIOS, `GRUB_CMDLINE_LINUX`, `update-grub`, an…

## Sources
- [GNU GRUB manual](https://www.gnu.org/software/grub/manual/grub/) — deep-dive
- [Wikipedia — GNU GRUB](https://en.wikipedia.org/wiki/GNU_GRUB) — overview

## Key Concepts
- **Generated config:** package updates overwrite `grub.cfg`.
- **Kernel cmdline:** live in `GRUB_CMDLINE_LINUX*` until regenerated.
- **Rescue / `e`:** one-boot edits for recovery.
- **UEFI vs BIOS:** different install paths and menu key habits.


- **Core:** Firmware (BIOS or UEFI) loads GRUB from the ESP or MBR

## Technical Details
```
UEFI/BIOS ──► GRUB ──► vmlinuz + initrd ──► systemd (PID 1)
              │
              └── grub.cfg from update-grub/grub2-mkconfig
```

| Path | Role |
|------|------|
| `/etc/default/grub` | Timeout, default, cmdline knobs |
| `/etc/grub.d/` | Script fragments for menu entries |
| `/boot/grub/grub.cfg` | Generated output |
| `/boot/efi/EFI/*/grubx64.efi` | UEFI binary on ESP |

```bash
grub-install --version
[ -d /sys/firmware/efi ] && echo UEFI || echo BIOS
sudo update-grub
sudo grub2-mkconfig -o /boot/grub/grub.cfg
sudo grub-install /dev/sda
```

- Kernel cmdline examples: `systemd.unit=rescue.target`, `nomodeset`, `intel_io…

- Interactive: Shift (BIOS) or Esc (UEFI) for menu; `e` edits once.

| Symptom | Check | Fix |
|---------|-------|-----|
| `grub rescue>` | Missing `/boot`, wrong UUID | Live USB repair; reinstall |
| Panic after upgrade | Bad initramfs / kernel | Previous entry; `update-initramfs -u` |
| Defaults edit ignored | Forgot regenerate | `update-grub` |
| Windows missing | os-prober off | `GRUB_DISABLE_OS_PROBER=false` |
| Secure Boot blocks | Unsigned module | Signed shim or disable SB |

## Mistakes to Avoid
- **Mistake:** Editing `/boot/grub/grub.cfg` directly
- **Mistake:** `grub-install` to the wrong disk without checking `lsblk` and fi…
- **Mistake:** Forgetting serial console args on cloud VMs

## Pros/Cons or Trade-offs
- **Pro:** Flexible multi-OS menus and persistent cmdline policy.
- **Con:** Easy to brick with wrong `grub-install` disk or hand-edited cfg.

## Comparison
- vs systemd-boot: simpler UEFI-only path on some distros.
- vs hypervisor cmdline: containers/VMs often get cmdline from the platform, not GRUB.


### Use cases
- Add `console=ttyS0` for cloud serial consoles, or boot `rescue.target` once v…
