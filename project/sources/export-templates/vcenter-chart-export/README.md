# vCenter chart export templates

**Versions:** vCenter 9.1.0.0 (build 25370922, from the appliance version API); ESXi 9.0.2.0 on the host used (sun05-esxi47.acepod.com, Summary page); VM guest Ubuntu Linux (64-bit), VMware Tools 12389 (Guest Managed), as shown on the VM Summary page.

**How they were made (read-only, 2026-11-15, logged-in browser):**
1. vSphere Client > object > Monitor > Performance > Advanced.
2. Period: Real-time. View: the group named below. Chart options left as they were, except where noted.
3. Chart menu (three lines, top right of the chart) > Export to CSV. The browser saved the file to the Downloads folder.

| File | Object | View | Counters in the file |
|---|---|---|---|
| [host-cpu-usage-realtime-sample.csv](host-cpu-usage-realtime-sample.csv) | host sun05-esxi47 | CPU usage in % | `Usage` for each VM object ID and for the host |
| [vm-cpu-usage-readiness-realtime-sample.csv](vm-cpu-usage-readiness-realtime-sample.csv) | VM sun05-webmin01 | CPU usage in % | `Usage` for the VM, `Readiness` for the VM and for instances `0` and `1` |
| [vm-cpu-usage-mhz-realtime-sample.csv](vm-cpu-usage-mhz-realtime-sample.csv) | VM sun05-webmin01 | CPU usage in MHz | `Usage in MHz` for the VM and for instances `0` and `1` |
| [vm-memory-realtime-sample.csv](vm-memory-realtime-sample.csv) | VM sun05-webmin01 | Memory | `Active`, `Ballooned memory`, `Consumed`, `Granted` for the VM |

Each file is the header and the first three data rows, with no other edits. Every file has about 179 data rows for the hour shown (one row per 20 seconds in real-time).

**Format (the same in all four files):**
- UTF-8 with a byte-order mark (`EF BB BF`) at the start of the first line.
- Delimiter `,`. Header fields and the time stamp are quoted; values are not.
- Time stamp: `"2026-11-15T09:05:40.000Z"`, ISO 8601, UTC, with milliseconds. The chart on screen shows the client's local time (UTC+8 on this client), so 09:05:40Z is 17:05:40 on screen.
- Values: plain numbers. The export has no units row or units column.

**Column names (exact):**
- Host CPU: `Usage for 11`, `Usage for 4`, ... (one per VM, named by its numeric object ID), and `Usage for sun05-esxi47.acepod.com`.
- VM CPU in %: `Usage for sun05-webmin01`, `Readiness for sun05-webmin01`, `Readiness for 1`, `Readiness for 0`.
- VM CPU in MHz: `Usage in MHz for 1`, `Usage in MHz for sun05-webmin01`, `Usage in MHz for 0`. The MHz view names the instances `Usage in MHz for <n>`; the % view names them `Readiness for <n>`.
- VM memory: `Active for sun05-webmin01`, `Ballooned memory for sun05-webmin01`, `Consumed for sun05-webmin01`, `Granted for sun05-webmin01`.

**Screen versus export (checked on these files):**
- Memory units: the chart legend says KB. The values are KB (for example `Granted` is 4178384 KB, which is 4 GB). Memory `Consumed` on screen is labelled "Consumed" with the same name in the file.
- The legend's Rollup (Average), Units (%, MHz, KB) and Measurement columns are not in the file. The measurement name is in the column header; the unit is in the view name.
- The `Readiness` rows appear in the CPU % view even though the chart's legend calls the measurement "Readiness" and its unit "%". The file uses the same name.

**Not in this folder yet:** host memory, host and VM disk, VM network, datastore, the Past day and Past week exports, and the chart options with more counters (Co-stop, Demand, Entitlement and others are listed in the Chart Options dialog of the VM CPU group). See [HEADERS.md](../HEADERS.md).

**Observed on the host sun05-esxi47 (not a template item):** the Summary and Monitor pages show "ESXi Shell for the host has been enabled" and "SSH for the host has been enabled" (configuration issues, 15/11/2026 12:22). Nothing was changed here.
