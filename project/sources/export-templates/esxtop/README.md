# esxtop: batch export and panels

Collected 2026-11-15 from `sun05-esxi47.acepod.com` (VMware ESXi 9.0.2 Update 0, build 25148076, as the host reports it over SSH). The batch header and one data row come from `esxtop -b`; the panels come from the interactive esxtop, one screen each. Nothing was written to the host: the batch output was piped to the terminal, and the panels were read over an SSH pty.

## Files

- `batch-header.txt`: the first line of `esxtop -b -n 1`. It has 12,608 fields by the CSV parser. IP-like text in RPC world names was replaced with `x.x.x.x`.
- `batch-data-row-1.txt`: the last line of `esxtop -b -n 2`, one data row. It has 12,708 fields by the CSV parser. This does not match the header's 12,608, and the cause is not yet known. Open item.
- `panel-c.txt`, `panel-m.txt`, `panel-n.txt`, `panel-d.txt`, `panel-u.txt`, `panel-v.txt`: the CPU, memory, network, disk adapter, disk device and virtual machine disk panels, as plain text (escape codes removed).

## Format (from the header and the data row)

- Delimiter `,`. Every field is in double quotes, including the time stamp. No spaces around the delimiter.
- First header field: `(PDH-CSV 4.0) (UTC)(0)`. The zone is UTC; the offset is 0.
- Column names: `\\<host>\<Group>\<Counter>`, for example `\\sun05-esxi47.acepod.com\Memory\Memory Overcommit (1 Minute Avg)`. The group is the first segment after the host (`Memory`, `Physical Cpu Load`, and so on). Per-world and per-VM columns carry the world or VM name in parentheses.
- Time stamp in the data row: `"MM/DD/YYYY HH:MM:SS"` (for example `"11/15/2026 11:30:17"`), in UTC. The header has no time column of its own; the first field of each data row is the time.
- Values: quoted, two decimal places in the sample (for example `"0.00"`, `"2.21"`), not the full precision that typeperf gives.
- Sample interval: `-d` defaults to 5 seconds; the sample above is one 5-second sample.

## Panels

The panel files are esxtop's own screens, with cursor and escape codes removed. Column headers (for example `%USED`, `%RDY`, `%CSTP` in the CPU panel) are the names an administrator sees on the screen, and they are shorter than the batch names. The batch name is the one the export file uses.

## Open items

- The 100-field difference between the header and the data row (above).
- The `-d` and `-n` values used for a multi-sample batch file in the field, and the row count of a real export.
- Units of each column are the esxtop counter's own: `%` for percentages, MB or KB for memory, as the column name says. No column in the sample was checked against a screen value.
