[[Linux system management]] [[Linux configuration]] [[date]] [[systemd]]

# NTP sync

> keep host clocks aligned to UTC via NTP so TLS, JWT, Kerberos, DB expiry, and distributed logs stay trustworthy — **Stevens UNP + Kerrisk LPI**.

---

## Mental model

Every Linux host has a **system clock** (wall time, `CLOCK_REALTIME`) and a **monotonic clock** (`CLOCK_MONOTONIC`) used for timeouts. NTP sync only disciplines **wall time**. Clients periodically exchange UDP packets with upstream **stratum** servers; lower stratum = closer to a reference clock (GPS, atomic).

```
Host ──UDP/123──► pool.ntp.org / corporate NTP / hypervisor
         │
         ▼
  chrony / systemd-timesyncd / ntpd
         │
         ▼
  kernel adjtime / step clock ──► timedatectl status
```

| Daemon                  | Typical distro                     | Role                                                |
| ----------------------- | ---------------------------------- | --------------------------------------------------- |
| **chrony**              | RHEL, Fedora, modern Ubuntu server | Full NTP client/server; handles VM clock drift well |
| **systemd-timesyncd**   | Ubuntu desktop, minimal images     | Lightweight SNTP client only                        |
| **ntpd** (NTP ref impl) | Legacy installs                    | Full NTP; avoid mixing with chrony on same host     |

**One sync daemon per host.** `timedatectl` is the control plane; it enables/disables sync but does not replace chrony/timesyncd.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **NTP** | Network Time Protocol | “Skewed clocks break TLS and auth.” |
| **chrony / systemd-timesyncd** | Common clients | “chrony for servers; timesyncd for desktops.” |
| **stratum** | Distance from true time | “Lower stratum = closer to reference.” |
| **step vs slew** | Jump vs gradual adjust | “Large offset may step once at boot.” |
| **RTC** | Hardware clock | “hwclock syncs BIOS time.” |

## Standard config / commands

### Verify sync state (always start here)

```bash
timedatectl status
# Look for: System clock synchronized: yes, NTP service: active

chronyc tracking          # chrony: offset, stratum, leap status
chronyc sources -v        # which upstreams are reachable
timedatectl timesync-status   # systemd-timesyncd detail
```

### chrony (production default on most Linux servers)

```bash
# Install (if missing)
sudo apt install chrony        # Debian/Ubuntu
sudo dnf install chrony        # RHEL/Fedora

# /etc/chrony/chrony.conf (or /etc/chrony.conf on RHEL)
# pool 2.debian.pool.ntp.org iburst
# server ntp.internal.corp iburst
# driftfile /var/lib/chrony/drift
# makestep 1.0 3          # step if offset >1s in first 3 updates (VM boot)
# rtcsync                 # sync RTC from system clock (helps after power loss)

sudo systemctl enable --now chronyd    # RHEL: chronyd; Debian: often 'chrony'
sudo chronyc makestep                  # force immediate step (maintenance window)
```

**Why `iburst`:** sends a burst of requests on startup so the clock converges in seconds instead of minutes — safe on clients, not on overloaded public pools at fleet scale (use internal NTP or `pool` with reasonable `maxsources`).

### systemd-timesyncd (lightweight / cloud-init images)

```bash
# /etc/systemd/timesyncd.conf
# [Time]
# NTP=ntp.internal.corp 0.pool.ntp.org
# FallbackNTP=time.cloudflare.com

sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
timedatectl timesync-status
```

Use when you only need a client and no NTP server role. Disable chrony/ntpd first — they fight over port 123.

### Manual time set (break-glass only)

```bash
# Prefer stepping via chrony; avoid raw date -s in production
sudo timedatectl set-ntp false          # stops auto sync
sudo timedatectl set-time '2026-07-30 12:00:00'   # emergency only
sudo timedatectl set-ntp true           # re-enable; let NTP slew/step back
```

### Firewall / outbound

NTP is **UDP 123 outbound** to upstreams. Inbound 123 is only needed if this host is an NTP server for others.

```bash
# Confirm chrony is listening (only if configured as server)
ss -ulnp | grep :123
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `System clock synchronized: no` | `timedatectl status`; `chronyc tracking` | Enable NTP: `timedatectl set-ntp true`; start `chronyd`/`systemd-timesyncd` |
| Large offset (>1s) after VM migrate/suspend | `chronyc tracking` → `System time` | `chronyc makestep` or `makestep` in chrony.conf; ensure `rtcsync` |
| `Can't synchronise: no reachable sources` | `chronyc sources -v`; `dig pool.ntp.org` | Fix DNS; open UDP/123 egress; point to reachable internal NTP |
| Clock drifts again after `date -s` | `timedatectl`; which daemon runs? | Re-enable NTP; remove cron jobs that set time |
| TLS/cert errors, `certificate not yet valid` | `date -u`; compare to `openssl s_client` peer | Fix NTP first; renew certs after clock is correct |
| JWT `exp`/`nbf` failures, SSO loops | Skew across app servers: `date -u` on each | Sync all nodes; check load balancer sticky sessions aren't masking mixed clocks |
| Postgres `recovery_target_time` / replication lag weirdness | `SELECT now();` on primary vs replica | Sync replicas; check `track_commit_timestamp` workloads |
| Two daemons fighting | `systemctl status chronyd ntpd systemd-timesyncd` | Disable all but one; `timedatectl set-ntp true` for timesyncd **or** chrony, not both |
| Container time wrong but host OK | `date` inside container vs host | Containers inherit host clock; fix the **host** (or VM hypervisor time sync) |
| AWS/hypervisor clock jump | `chronyc tracking`; instance type | Enable chrony `makestep`; on Xen/KVM use `chrony` not bare ntpd |

## Gotchas

> [!WARNING]
> **Never run chrony + ntpd + timesyncd together.** Only one should own clock discipline. Symptom: oscillating offset, `timedatectl` flapping, or silent no-sync.

> [!WARNING]
> **`timedatectl set-ntp false` + manual `date -s` in prod** — breaks Kerberos (5 min skew limit), TLS handshakes, and distributed DB TTL logic. Document break-glass and re-enable NTP immediately after.

> [!WARNING]
> **Leap seconds** — rare but real. chrony handles smearing or stepping per config; apps assuming linear epoch time can glitch at leap boundaries. Prefer UTC everywhere; test billing/TTL logic if sub-second matters.

- **VMs without virtio clock or after long pause** — hardware clock freezes; chrony `makestep` on boot is standard.
- **Docker `--privileged` / `CAP_SYS_TIME`** — container can change **host** clock; almost never grant this.
- **NTP amplification (UDP 123)** — do not expose NTP to the internet unless hardened (`ntpd` `restrict`, chrony `allow`/`deny`). See [[UDP]].
- **Public pool abuse** — thousands of hosts hitting `pool.ntp.org` without `iburst` discipline can get rate-limited; use vendor NTP (AWS `169.254.169.123`, Azure, GCP) or internal stratum-1/2.
- **`hwclock` vs system clock** — BIOS/RTC drifts; `hwclock --systohc` after NTP stable if dual-boot or offline boots matter.

## When NOT to use

- **Sub-millisecond ordering across datacenters** — NTP gives ms–tens-of-ms; use **PTP (IEEE 1588)** or application logical clocks (see [[ACID]], Spanner/HLC patterns).
- **Measuring elapsed time / timeouts** — use monotonic clocks in code, not `date` or wall clock.
- **Timezone display** — NTP syncs **UTC**; timezone is `timedatectl set-timezone` / `/etc/localtime` — orthogonal to sync.
- **Replacing audit trail timestamps** — sync enables trustworthy logs; retention and NTP are not a substitute for centralized log shipping with server-side timestamps.

## Related

[[date]] [[Linux system management]] [[Linux configuration]] [[systemd]] [[journalctl]] [[JWT authentication]] [[TLS (Transport Layer Security)]] [[UDP]] [[ACID]]
