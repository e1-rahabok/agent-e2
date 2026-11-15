# Export templates: headers, units, formats

Work in progress (2026-11-15). Collected so far: Windows (typeperf, systeminfo, Win32_PageFileUsage), vCenter real-time, last-day and last-week exports for host and VM (see vcenter-chart-export/README.md), and VCF Operations metric keys (see the section below). Not yet collected: VCF Operations labels and List export, esxtop, Linux, and the remaining vCenter objects.

## Windows typeperf

- File: [windows-typeperf/typeperf-10x1s.csv](windows-typeperf/typeperf-10x1s.csv), made as in [windows-typeperf/README.md](windows-typeperf/README.md).
- First line: `(PDH-CSV 4.0) (<time zone>)(<offset>)`, then the header, then one line per sample.
- Delimiter `,`; every field is in double quotes.
- Time stamp: `MM/DD/YYYY HH:MM:SS.fff`, in local time, with the zone in the first header field.
- Names: each counter is `\\HOST\<object>(<instance>)\<counter>`, with the machine name replaced by `HOST` in the saved copy. Processor instances are numbered `(0)` to `(11)` on this laptop, plus `(_Total)`.
- Values are quoted strings with full precision (for example `14.092408881254403497`), not rounded.
- Units: follow each counter's own name (`% ...` is percent; `Pages/sec`, `Disk Transfers/sec`, `Context Switches/sec` are per second). The memory units (MB or bytes) and the screen equivalence are not yet checked against a screen.

## Windows systeminfo and Win32_PageFileUsage (text)

- `systeminfo` lines: `Virtual Memory: Max Size:`, `Virtual Memory: Available:`, `Virtual Memory: In Use:` with values in MB and a thousands separator, `Page File Location(s):`.
- `Get-CimInstance Win32_PageFileUsage` fields: `Name`, `AllocatedBaseSize` (MB), `CurrentUsage` (MB), `PeakUsage` (MB).

## vCenter chart export (CSV)

- Folder: [vcenter-chart-export/](vcenter-chart-export/), with the exports and the README (menu path and versions).
- Header: `"Time"` followed by one column per object, named `<Measurement> for <object>`. Examples: `Usage for sun05-webmin01`, `Readiness for 1`, `Usage in MHz for 0`, `Granted for sun05-webmin01`, `Read latency for scsi0:0`, `Data receive rate for vmnic3`, `Read latency for <datastore>`. The disk labels are raw keys: `counter.disk.read.label for ...`.
- Object names: VMs in the host CPU export appear as numeric object IDs, not names. Other objects (the host, the VM itself) appear by name.
- Time stamp: `"2026-11-15T09:05:40.000Z"`, ISO 8601 in UTC with milliseconds. The screen shows local time (UTC+8 on this client).
- Interval: 20 seconds in real-time (about 180 rows per hour); last day is a 5-minute rollup (288 rows), last week a 30-minute rollup (336 rows). Only the VM CPU % view has both.
- Delimiter `,`; header and time stamp quoted; values not quoted; UTF-8 with a byte-order mark.
- Units: not in the file. The legend shows them: % for Usage and Readiness, MHz for Usage in MHz, KB for memory counters (Active, Ballooned memory, Consumed, Granted).
- Screen versus export: the legend's Rollup and Units columns are not in the file. The unit must come from the chart legend or from the view name.

## Not collected yet (and why)

- vCenter: the remaining objects (other datastores, host network and storage adapters, the other VMs), and the Past day and Past week views of the other charts. Each needs its own chart and export in the browser.
- VCF Operations metric names and List export: needs the metric picker in the logged-in browser.
- sun05-webmin01 (Ubuntu): no login was made to it; the Linux outputs below come from the VCF Operations appliance instead (Photon OS). The vCenter appliance's root login was refused with the stored vCenter password, so it was not used.
- VCF Operations UI: the metric picker labels and the List export are not captured. A headless login works, and the Inventory tree loads; the VM's metric page is the next step.

## VCF Operations (metric keys)

- Folder: [vcf-operations/](vcf-operations/), with [README.md](vcf-operations/README.md) (what was read, the requested metric mapping, and what is missing).
- Names are the suite API's keys, for example `cpu|readyPct`, `mem|balloonPct`, `guest|cpu_queue`, `virtualDisk:scsi0:0|totalReadLatency_average`. The screen label (metric picker) is not in the API; the labels are in [picker-labels.md](vcf-operations/picker-labels.md), for example `Ready (%)`, `Peak vCPU Ready within collection cycle (%)`, `Balloon (%)`, `Swap In Rate (KBps)`, `Guest Free Memory (KB)`, `Read Latency (ms)`.
- Version: VCF Operations 9.1.1.0 (as the API reports it).
- Not found: VM Decompression Rate (the picker has no entry for it); an exact Network Peak Transmitted Packet Dropped.
- Chart CSV (from the chart's More Actions menu, "Download comma separated data"): title line `<object> - <metric label>`, blank line, header `Date & Time,Value,Low DT,High DT,Smooth,` (trailing comma), then rows `"<Month D, YYYY, H:MM:SS AM/PM GMT+08:00>",<value>,-,-,-,`. Time in the browser's zone; values at full precision, unquoted; 5-minute interval. Sample: [chart-export-sample.csv](vcf-operations/chart-export-sample.csv).
- Not collected yet: the List view export.

## esxtop (batch and panels)

- Folder: [esxtop/](esxtop/), with [README.md](esxtop/README.md): batch header, one data row, six panels, from ESXi 9.0.2 Update 0 (build 25148076).
- Delimiter `,`; every field in double quotes. First field `(PDH-CSV 4.0) (UTC)(0)`.
- Column names: `\<host>\<Group>\<Counter>` (for example `\sun05-esxi47.acepod.com\Memory\Memory Overcommit (1 Minute Avg)`); per-world columns carry the world name in parentheses.
- Time stamp in each data row: `"MM/DD/YYYY HH:MM:SS"` in UTC, quoted. Values quoted, two decimals in the sample.
- Open: the header has 12,608 fields and the data row 12,708; not resolved.

## Linux (Photon OS)

- Folder: [linux-photon/](linux-photon/), with [README.md](linux-photon/README.md): top, sar, iostat, free, ip -s link, swap counters, kernel version. From the VCF Operations appliance, Photon OS 5.0, kernel 6.1.176-4.ph5.
- `/proc/pressure/memory` is not present on this kernel; recorded as missing.
