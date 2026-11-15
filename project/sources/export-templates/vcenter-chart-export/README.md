# vCenter chart export template

**Versions:** vCenter 9.1.0.0 (build 25370922, from the appliance version API); ESXi 9.0.2.0 on the host used (sun05-esxi47.acepod.com, Summary page).

**How it was made (read-only, 2026-11-15):**
1. vSphere Client > host `sun05-esxi47.acepod.com` > Monitor > Performance > Advanced.
2. Period: Real-time. View: CPU usage in %. Chart options left as they were.
3. Chart menu (the three-line icon at the top right of the chart) > Export to CSV. The browser saved `exported.csv` to the Downloads folder.

**What the export contains:** one row per 20-second sample over 1 hour (179 rows plus the header), one column per object in the chart legend.

**Sample kept:** [host-cpu-usage-realtime-sample.csv](host-cpu-usage-realtime-sample.csv): the header and the first three data rows, no other edits.

**Format:**
- File starts with a UTF-8 byte-order mark (`EF BB BF`), then the header.
- Delimiter `,`. Header fields are quoted. Time stamp is quoted, in the form `2026-11-15T09:01:20.000Z`: ISO 8601, UTC (`Z`), with milliseconds.
- Values are unquoted decimals with up to two decimals. The export has no unit row or units column.
- Time is UTC. The chart on screen shows local time (UTC+8 on this lab's client), so 09:01:20Z is 17:01:20 on screen.

**Column names:**
- Header: `Time`, then one column per object as `Usage for <object>`.
- The VMs appear as their numeric object IDs (`Usage for 11`, `Usage for 4`, and so on), the same numbers as the Object column in the legend. The host appears by name (`Usage for sun05-esxi47.acepod.com`).
- Screen versus export: the legend heading is "Measurement: Usage", "Rollup: Average", "Units: %". The export carries only the measurement and the object in the name; the rollup and unit are not in the file.

**Not in this folder yet:** VM CPU, VM memory, VM network, VM disk, datastore, and the Past day and Past week exports. See [HEADERS.md](../HEADERS.md).

**Observed on the same host (not a template item):** the Summary and Monitor pages show "ESXi Shell for the host has been enabled" and "SSH for the host has been enabled" (configuration issues, 15/11/2026 12:22). They were not changed here.
