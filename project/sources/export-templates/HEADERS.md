# Export templates: headers, units, formats

Work in progress (2026-11-15). Collected so far: Windows (typeperf, systeminfo, Win32_PageFileUsage) and vCenter real-time, last-day and last-week exports for host and VM (see vcenter-chart-export/README.md). Not yet collected: VCF Operations, esxtop, Linux, and the remaining vCenter objects.

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
- esxtop batch CSV and the panel screens: the session is in the Terminal panel tab `c1`; keys cannot be typed into it from here.
- Linux: sun05-webmin01 is Ubuntu Linux (64-bit) and powered on, but no login was made to it, so `top`, `sar`, `iostat` and the other Linux outputs are not collected.
