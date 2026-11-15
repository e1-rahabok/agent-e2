# vCenter chart export templates

**Versions:** vCenter 9.1.0.0 (build 25370922, from the appliance version API). ESXi 9.0.2.0 on the host used (sun05-esxi47.acepod.com, Summary page). VM guest Ubuntu Linux (64-bit), VMware Tools 12389 (Guest Managed), from the VM Summary page.

**How they were made (read-only, 2026-11-15, logged-in browser):**
1. vSphere Client > object > Monitor > Performance > Advanced.
2. Period and View set as in the table. Chart options left as they were.
3. Chart menu (three lines, top right of the chart) > Export to CSV. The browser saved the file to the Downloads folder.

| File | Object | Period | View | Columns in the file |
|---|---|---|---|---|
| [host-cpu-usage-realtime-sample.csv](host-cpu-usage-realtime-sample.csv) | host sun05-esxi47 | Real-time | CPU usage in % | `Usage for <VM object ID>`, `Usage for sun05-esxi47.acepod.com` |
| [host-memory-realtime-sample.csv](host-memory-realtime-sample.csv) | host sun05-esxi47 | Real-time | Memory | `Active`, `Ballooned memory`, `Consumed`, `Granted`, `Shared common`, `Swap consumed` (each for the host) |
| [host-disk-realtime-sample.csv](host-disk-realtime-sample.csv) | host sun05-esxi47 | Real-time | Disk | `counter.disk.read.label` and `counter.disk.write.label` for each NVMe device and the host, `counter.disk.usage.label` for the host |
| [host-datastore-latency-realtime-sample.csv](host-datastore-latency-realtime-sample.csv) | host sun05-esxi47 | Real-time | Datastore | `Read latency` and `Write latency` for each datastore |
| [vm-cpu-usage-readiness-realtime-sample.csv](vm-cpu-usage-readiness-realtime-sample.csv) | VM sun05-webmin01 | Real-time | CPU usage in % | `Usage for sun05-webmin01`, `Readiness for sun05-webmin01`, `Readiness for 1`, `Readiness for 0` |
| [vm-cpu-usage-mhz-realtime-sample.csv](vm-cpu-usage-mhz-realtime-sample.csv) | VM sun05-webmin01 | Real-time | CPU usage in MHz | `Usage in MHz for sun05-webmin01`, `Usage in MHz for 1`, `Usage in MHz for 0` |
| [vm-cpu-usage-last-day-sample.csv](vm-cpu-usage-last-day-sample.csv) | VM sun05-webmin01 | Last day | CPU usage in % | `Usage for sun05-webmin01` only (the Readiness rows are not in this view) |
| [vm-cpu-usage-last-week-sample.csv](vm-cpu-usage-last-week-sample.csv) | VM sun05-webmin01 | Last week | CPU usage in % | `Usage for sun05-webmin01` only |
| [vm-memory-realtime-sample.csv](vm-memory-realtime-sample.csv) | VM sun05-webmin01 | Real-time | Memory | `Active`, `Ballooned memory`, `Consumed`, `Granted` (each for the VM) |
| [vm-network-realtime-sample.csv](vm-network-realtime-sample.csv) | VM sun05-webmin01 | Real-time | Network | `Data receive rate` and `Data transmit rate` for the VM, for each vmnic and for port 4000; `Usage` for the same |
| [vm-virtual-disk-realtime-sample.csv](vm-virtual-disk-realtime-sample.csv) | VM sun05-webmin01 | Real-time | Virtual disk | `Read latency for scsi0:0`, `Write latency for scsi0:0` |

Each file is the header and the first three data rows, with no other edits. Real-time files have 179 data rows for the hour (one row per 20 seconds). The last-day file is 288 rows (5-minute rollup); the last-week file is 336 rows (30-minute rollup).

**Format (the same in all files):**
- UTF-8 with a byte-order mark (`EF BB BF`) at the start of the first line.
- Delimiter `,`. Header fields and the time stamp are quoted; values are not.
- Time stamp: `"2026-11-15T09:05:40.000Z"`, ISO 8601, UTC, with milliseconds. The chart on screen shows the client's local time (UTC+8 on this client), so 09:05:40Z is 17:05:40 on screen.
- Values: plain numbers. The export has no units row or units column.
- Device identifiers in the host disk sample are replaced by placeholders (`<device-A: ...>`, `<device-B: ...>`). The model name is kept, the serial number is removed.

**Column names (exact, and where they differ from the screen):**
- Each column is `<Measurement> for <object>`. VMs in the host CPU export appear by their numeric object ID (`Usage for 11`), not by name.
- Host disk: the export says `counter.disk.read.label for ...` and `counter.disk.write.label for ...`, and the on-screen legend shows the same raw keys (`counter.disk.read.label`, `counter.disk.read.summary`). The UI and the export both show the key, not "Read"/"Write". This is a product labelling defect, not a missing measurement.
- Memory units: the legend says KB, and the values are KB (for example `Granted` 4178384 KB, about 4 GB).
- Network: the screen says KBps; the file gives plain numbers in the same unit.
- The legend's Rollup (Average), Units and Measurement columns are not in the file. The unit comes from the chart legend or the view name.
- The Readiness rows appear only in the real-time CPU % view, not in the last-day or last-week views.

**Not in this folder yet:** the host network and host storage adapter views, the VM disk for other VMs, and the datastore for the VM. See [HEADERS.md](../HEADERS.md).

**Observed on the host sun05-esxi47 (not a template item):** the Summary and Monitor pages show "ESXi Shell for the host has been enabled" and "SSH for the host has been enabled" (configuration issues, 15/11/2026 12:22). Nothing was changed here.
