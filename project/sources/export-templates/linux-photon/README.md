# Linux (Photon OS): performance command outputs

Collected 2026-11-15 from the VCF Operations appliance `vcf-m02-ops01.acepod.com`, which runs VMware Photon OS 5.0 (kernel `6.1.176-4.ph5`, build `b9d98344d`, 8 vCPU). The command outputs were read over SSH, one command per file. Nothing was changed on the appliance.

## Files and commands

| File | Command | Notes |
|---|---|---|
| `top-b-n1.txt` | `top -b -n 1 \| head -n 40` | Batch mode, one iteration, first 40 lines. |
| `sar-u-1-5.txt` | `sar -u 1 5` | CPU, five 1-second samples and an average. |
| `iostat-xd-1-3.txt` | `iostat -xd 1 3` | Extended disk statistics, three samples. |
| `free-m.txt` | `free -m` | Memory in MB. |
| `ip-s-link.txt` | `ip -s link` | Interface counters. MAC addresses replaced with `xx:xx:...`. |
| `vmstat-swap.txt` | `grep -E '^(pswpin\|pswpout) ' /proc/vmstat` | Swap in and out, pages since boot. |
| `pressure-memory.txt` | `cat /proc/pressure/memory` | **Not available**: the file is missing on this kernel (no pressure stall information). The file holds the error, not data. |
| `uname.txt` | `uname -a` and `/etc/photon-release` | Kernel and OS version. |

## Format notes

- `sar -u` prints a date in `MM/DD/YYYY` form on the banner line and 12-hour times (`11:29:45 AM`) on each row; columns `%user %nice %system %iowait %steal %idle`.
- `iostat -xd` and `free -m` use the sysstat and procps headings as shipped on Photon 5.0.
- `ip -s link` gives two counter lines per interface (RX and TX), each with bytes, packets, errors, dropped, overrun.
- The `top -b` output starts with the summary block (uptime, tasks, CPU, memory) and then the process table.

## Not collected

- `/proc/pressure/memory`: not present on this kernel.
- Anything that needs a stored login beyond the one used here.
