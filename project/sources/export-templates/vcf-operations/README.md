# VCF Operations: metric keys and export names

Collected 2026-11-15 from the lab's VCF Operations 9.1.1.0 (release name as the API reports it). The key lists are the names the suite API returns for each object; they are the exact strings a metric export or a list export uses.

## What was read, and how

- VM `sun05-webmin01`: full key list, `vm-statkeys.txt` (266 keys). Read with `GET /suite-api/api/resources/{id}/statkeys` (`stat-key` array, one `key` per item).
- Host `sun05-esxi47.acepod.com`: 794 keys in total; `host-statkeys-filtered.txt` keeps the cpu, mem, disk, datastore and net keys (201), without the per-datastore instance IDs.
- Cluster `vcf-m02-cl01`: the cpu keys were read (for example `cpu|demandmhz`, `cpu|capacity_contentionPct`, `cpu|usagemhz_average`).
- Datastore instances appear with numeric IDs in the key (for example `datastore:232|...`). The name comes from the UI, not from the key.

## Key names for the requested VM metrics

Key on the left, the API name. The screen label is not in the API: it comes from the metric picker, which is not yet captured (see below).

| Requested metric | Key | Exists |
|---|---|---|
| CPU Ready | `cpu|readyPct` | yes |
| CPU Co-stop | `cpu|costopPct` | yes |
| CPU Net Run | `cpu|net_run` | yes |
| CPU Contention | `cpu|capacity_contentionPct` | yes (host-side: `mem|host_contentionPct` for memory) |
| CPU Usage | `cpu|usage_average`, MHz: `cpu|usagemhz_average` | yes |
| CPU Demand | `cpu|demandPct`, MHz: `cpu|demandmhz` | yes |
| Peak vCPU Ready | `cpu|peak_vcpu_ready` | yes |
| Memory Contention | `mem|host_contentionPct` | yes |
| Memory Usage | `mem|usage_average` | yes |
| Memory Balloon | `mem|balloonPct` | yes |
| Swap In Rate | `mem|swapinRate_average` | yes |
| Compressed | `mem|compressed_average` | yes |
| Decompression Rate | none found in the VM key list | **no** |
| Guest Free Memory | `guest|mem.free_latest` | yes |
| Guest Needed Memory | `guest|mem.needed_latest` | yes |
| Page Out Rate | `guest|page.outRate_latest` | yes |
| Guest CPU Queue | `guest|cpu_queue` | yes |
| Network Peak Transmitted Packet Dropped | none exact; `net|droppedTxPct_max` and `net|droppedTx_summation` are the closest | **unclear** |
| Virtual disk read latency | `virtualDisk:scsi0:0|totalReadLatency_average` | yes (per disk) |
| Virtual disk IOPS per `scsiX:Y` | `virtualDisk:scsi0:0|numberReadAveraged_average`, `numberWriteAveraged_average` | yes (per disk) |
| Virtual disk peak latency | `virtualDisk|peak_vDisk_readLatency`, `peak_vDisk_writeLatency` | yes |

Host and cluster CPU (Usage, Demand, Contention) are `cpu|usage_average`, `cpu|demandPct`, `cpu|capacity_contentionPct` on the host, and `cpu|usagemhz_average`, `cpu|demandmhz`, `cpu|capacity_contentionPct` on the cluster.

Datastore IOPS per host: `datastore:<id>|numberReadAveraged_average` and `numberWriteAveraged_average` for each datastore instance; the aggregate is `datastore:Aggregate of all instances|...`, which has latency and usage but no IOPS keys.

## Not collected yet

- **Metric picker labels.** The screen names (and their order in the picker) are not in the API. They need the logged-in browser session on the VCF Operations UI. The author has to sign in again in the browser; no credentials are entered by Claude.
- **List view export** (VMs, a few metrics, Max/Min/First/Last over 7 days). This is a UI export and is not done.
- **Decompression Rate** and the exact "Peak Transmitted Packet Dropped" key: not found under those names. Recorded above as missing or unclear, not guessed.
