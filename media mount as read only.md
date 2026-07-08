A USB drive mounting as **read-only** usually indicates that the operating system has restricted write access to protect the data from potential corruption or physical failure.

### Common Causes

- **Filesystem Corruption:** The most frequent cause. If the drive was unplugged without being safely unmounted (or if a power loss occurred), the kernel detects an "unclean" state and locks it to prevent further damage.
    
- **Physical Write-Protection:** Some drives have a physical hardware switch (on the side or bottom) that enables read-only mode.
    
- **Hardware Failure:** Flash storage has a finite number of write cycles. When the drive controller detects that the NAND memory is dying, it may force itself into read-only mode to allow you to rescue your data before the drive fails completely.
    
- **Permissions/Mount Options:** Sometimes the drive is mounted with incorrect user permissions or the `ro` (read-only) flag in `/etc/fstab` or mount defaults.
    

### Troubleshooting Steps

#### 1. Check for Hardware Switches

Inspect the casing of the USB drive for a small sliding switch. If it is set to "Lock" or a red indicator is visible, toggle it back to the "Unlock" position.

#### 2. Check System Messages

Run this command immediately after plugging in the drive to see if the kernel logs explain why it was mounted as read-only:

Bash

```
dmesg | tail -n 50
```

Look for lines containing `EXT4-fs error`, `FAT-fs error`, or `Remounting filesystem read-only`. These messages confirm filesystem corruption.

#### 3. Attempt a Filesystem Repair

If the issue is corruption, you can try to repair it. Replace `/dev/sdX1` with your actual device identifier (verify using `lsblk`):

Bash

```
# Unmount the drive first
sudo umount /dev/sdX1

# Run the appropriate check for your filesystem (e.g., vfat, ntfs, ext4)
# For FAT32/exFAT:
sudo fsck.vfat -a /dev/sdX1
# For ext4:
sudo fsck -y /dev/sdX1
```

#### 4. Remount as Read-Write

If the filesystem is clean but the mount option is stuck, attempt to force a remount:

Bash

```
sudo mount -o remount,rw /dev/sdX1 /your/mount/point
```

#### 5. Check for Wear (The "Failing Drive" Sign)

If you can fix the errors but they return immediately or the drive persists in read-only mode, the internal controller has likely marked the NAND as "End of Life."

- **Recommendation:** Copy your data off immediately and replace the drive. Do not trust it for critical storage if the controller is initiating self-preservation mode.
    

**Do you have the specific error output from `dmesg` or `mount` that you'd like me to analyze?**