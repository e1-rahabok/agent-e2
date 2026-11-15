# VCF Operations: metric picker labels

Read 2026-11-15 from VCF Operations 9.1.1.0 (`vcf-m02-ops01.acepod.com`). The labels are what the metric picker shows on the Metrics tab of the VM `vcf-m02-services01-4cb8t`. Each query was typed into the picker's search box, and the matching entries were read from the screen. The picker path (group > subgroup) is written after the label.

Search grid: [picker-search-grid.png](picker-search-grid.png). One panel per query, in alphabetical order of the query.

## Requested metrics

| Requested | Picker label (unit) | Picker path | Key (from the API, see [README](README.md)) |
|---|---|---|---|
| CPU Ready | Ready (%) | Metrics > CPU | `cpu\|readyPct` |
| CPU Ready (peak) | Peak vCPU Ready within collection cycle (%) | Metrics > CPU | `cpu\|peak_vcpu_ready` |
| CPU Ready (highest) | Highest vCPU Ready of all instances (%) | Metrics > CPU | not checked against a key |
| CPU Co-stop | Co-stop (%) | Metrics > CPU | `cpu\|costopPct` |
| CPU Co-stop (peak) | Peak vCPU Co-Stop within collection cycle (%) | Metrics > CPU | not checked |
| CPU Contention | CPU\|Contention (%) | Contention (favorites) | `cpu\|capacity_contentionPct` |
| CPU Ready (contention view) | CPU\|Ready (%) | Contention (favorites) | `cpu\|readyPct` |
| Memory Contention | Memory\|Contention (%) | Contention (favorites) | `mem\|host_contentionPct` |
| Balloon | Balloon (%) | Metrics > Memory | `mem\|balloonPct` |
| Compressed | Compressed (KB) | Metrics > Memory | `mem\|compressed_average` |
| Swap In Rate | Swap In Rate (KBps) | Metrics > Memory | `mem\|swapinRate_average` |
| Swap Out Rate | Swap Out Rate (KBps) | Metrics > Memory | `mem\|swapoutRate_average` |
| Swapped | Swapped (KB) | Metrics > Memory | `mem\|swapped_average` |
| Swap wait | Swap wait (%) | Metrics > CPU | `cpu\|swapwaitPct` |
| Guest Remaining Swap Space | Remaining Swap Space (KB) | Metrics > Guest | `guest\|swap.spaceRemaining_latest` |
| Guest Free Memory | Guest Free Memory (KB) | Utilization (partly visible) | `guest\|mem.free_latest` |
| Guest Needed Memory | Guest Needed Memory (KB) | Utilization (partly visible) | `guest\|mem.needed_latest` |
| Page Out Rate | Page Out Rate per second | Metrics > Guest | `guest\|page.outRate_latest` |
| Guest CPU Queue | Guest CPU Queue (the label was cut off in the grid) | Metrics > Guest | `guest\|cpu_queue` |
| Network dropped transmitted | (DEP) Transmitted Packets Dropped | Metrics > Network | `net\|droppedTx_summation` (the closest key) |
| Virtual disk latency | Read Latency (ms), Total Latency (ms), Write Latency (ms) | Metrics > Datastore > Aggregate of all instances | per-disk key: `virtualDisk:scsi0:0\|totalReadLatency_average` |
| IOPS | Total IOPS, Read IOPS, Write IOPS | Metrics > Datastore > Aggregate of all instances | per-datastore: `datastore:<id>\|numberReadAveraged_average` |

## Not found

- **Decompression Rate**: the picker returns "No metrics to select." No label for it exists in this version.
- **Peak Transmitted Packet Dropped**: the picker shows "(DEP) Transmitted Packets Dropped" and "Total Received Packets Dropped". The label used for an exact match on "Peak" is absent. Recorded as unclear.

## Notes

- The picker shows several labels for one key: `Ready (%)` under Metrics > CPU, and `CPU|Ready (%)` under the Contention favorite. Both appear; the export column name follows the label the author chooses, so both must be checked in an export before a template is fixed.
- Page Out has a Datastore entry, "Outstanding IO requests (OIOs)", that is not the guest page-out rate.
- The grid shows labels as the picker truncates them; the full label was read where it fits.
- The List export (VMs, several metrics, Max/Min/First/Last over 7 days) is not captured here.
