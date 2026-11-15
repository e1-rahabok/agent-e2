# Export templates: headers, units, formats

Work in progress (2026-11-15). Collected so far: Windows (typeperf, systeminfo, Win32_PageFileUsage). Not yet collected: vCenter chart exports, VCF Operations, esxtop, Linux. The gaps are listed at the end.

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

## Not collected yet (and why)

- vCenter chart exports (VM CPU, VM memory, VM network, VM disk, host, datastore): needs the chart export UI on each object in the logged-in Chrome window. Not done yet.
- VCF Operations metric names and List export: needs the metric picker in the logged-in Chrome window. Not done yet.
- esxtop batch CSV and the panel screens: the esxtop session is in the Terminal panel tab `c1`. The tool used here can open new tabs, but it cannot type into an existing tab, so the keys must be pressed by the user, or a new SSH tab must be opened and the password typed by the user.
- Linux: no Linux VM has been identified as reachable with the login.
