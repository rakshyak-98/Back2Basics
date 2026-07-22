[[Linux system management]] [[inittramfs]] [[Linux configuration]]

# GRUB

> One-line: **GRand Unified Bootloader** — first stage that loads the kernel + initramfs; edit here for dual-boot, recovery entries, kernel cmdline (nomodeset, iommu). **GRUB 2 on virtually all modern distros.**

## Mental model

Firmware (BIOS or UEFI) loads GRUB from the ESP (EFI System Partition) or MBR. GRUB reads `/boot/grub/grub.cfg` (generated — **do not hand-edit**) from templates in `/etc/default/grub` and `/etc/grub.d/*`. Kernel parameters on the linux line affect every boot until regenerated.

```
UEFI/BIOS ──► GRUB ──► vmlinuz + initrd ──► systemd (PID 1)
              │
              └── grub.cfg from update-grub/grub2-mkconfig
```

| Path | Role |
|------|------|
| `/etc/default/grub` | User knobs: timeout, default entry, `GRUB_CMDLINE_LINUX` |
| `/etc/grub.d/` | Script fragments that build menu entries |
| `/boot/grub/grub.cfg` | Generated output |
| `/boot/efi/EFI/*/grubx64.efi` | UEFI binary on ESP |

## Standard config / commands

```bash
# Confirm GRUB2
grub-install --version
# grub-install (GRUB) 2.06

# UEFI vs BIOS
[ -d /sys/firmware/efi ] && echo UEFI || echo BIOS
ls -l /sys/firmware/efi                    # typo fix: firmware not fireware

# Regenerate config after editing /etc/default/grub
sudo update-grub                           # Debian/Ubuntu
sudo grub2-mkconfig -o /boot/grub/grub.cfg # RHEL/Fedora

# Common /etc/default/grub tweaks
# GRUB_TIMEOUT=5
# GRUB_DEFAULT=0
# GRUB_CMDLINE_LINUX="console=tty0 crashkernel=auto"
# GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
```

**Kernel cmdline examples (append via `GRUB_CMDLINE_LINUX`):**

```bash
# Recovery / debug
systemd.unit=rescue.target
single
init=/bin/bash

# GPU / passthrough
nomodeset
intel_iommu=on iommu=pt

# After edit — always regenerate
sudo update-grub
```

**Reinstall GRUB to disk/ESP (broken boot):**

```bash
# UEFI (adjust disk/partition)
sudo grub-install /dev/sda
sudo update-grub

# Mount root + ESP from live USB first if system won't boot
```

**Interactive at boot:** hold **Shift** (BIOS) or **Esc** (UEFI) for menu; `e` to edit entry temporarily (not persistent).

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Drops to `grub rescue>` | Missing `/boot`, wrong UUID | Live USB → `ls` → `set root` → `linux`/`initrd` → `boot`; reinstall |
| Kernel panic after upgrade | Bad initramfs / wrong kernel | Previous menu entry; `update-initramfs -u`; reinstall kernel package |
| Edit `/etc/default/grub` no effect | Forgot regenerate | `update-grub` / `grub2-mkconfig` |
| Windows gone after Linux install | os-prober off | `GRUB_DISABLE_OS_PROBER=false`; `update-grub` |
| NVMe vs SATA root wrong | `GRUB_DISABLE_LINUX_UUID=false` | Regenerate; check `/etc/fstab` UUIDs match |
| Secure Boot blocks custom kernel | Unsigned module | Use signed shim or disable SB in firmware |

## Gotchas

> [!WARNING]
> **Never edit `/boot/grub/grub.cfg` directly** — package updates overwrite it. Only `/etc/default/grub` and `/etc/grub.d/`.

> [!WARNING]
> **`grub-install` to wrong disk** — can erase another OS boot chain. Triple-check `lsblk` and firmware boot order.

> [!WARNING]
> **Btrfs/ZFS layouts** — GRUB module support and `/boot` on separate ext4 partition is common pattern; snapshot distros differ.

> [!WARNING]
> **Cloud VMs** — serial console kernel args (`console=ttyS0`) often required to see boot logs in provider console.

## When NOT to use

- **systemd-boot on Arch/minimal UEFI** — no GRUB; different path.
- **Container/VM image** — provider/kernel cmdline set in hypervisor.
- **Runtime kernel tuning** → `sysctl`, not GRUB (except params that must be boot-time).

## Related

[[inittramfs]] [[Linux system management]] [[Linux configuration]] [[MBR]] [[Operating System]]
