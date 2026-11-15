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

- **Metric picker labels: collected**, see [picker-labels.md](picker-labels.md) and the grid [picker-search-grid.png](picker-search-grid.png). Read from the Metrics tab of a VM in the inventory, by typing each name into the picker's search box. Only the labels were read; no values.
- **List view export** (VMs, a few metrics, Max/Min/First/Last over 7 days): not done. It is a UI export, and the headless session can reach the Metrics page to do it.
- **CSV export format of a chart: collected**, see [chart-export-sample.csv](chart-export-sample.csv) (header, first three rows, last two of 7,741). The export is the chart widget's "More Actions" > "Download comma separated data". Format: line 1 is `<object> - <metric label>`; line 2 is blank; line 3 is the header `Date & Time,Value,Low DT,High DT,Smooth,` (the trailing comma is in the file). Each row: time stamp in double quotes, for example `"November 15, 2026, 8:28:38 PM GMT+08:00"` (the browser's zone, not UTC), then the value at full precision, unquoted, then four fields that are `-` when empty. Interval 5 minutes. The chart range was about four weeks, not the "Last 7 days" label on the page. A List view export is still not collected.
- **Decompression Rate** (no picker entry, "No metrics to select.") and the exact "Peak Transmitted Packet Dropped" key: not found under those names. Recorded above as missing or unclear, not guessed.
