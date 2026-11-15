# Windows typeperf export template

**Made:** 2026-11-15, on a Windows 11 Home laptop (build 10.0.26300), with no lab access.

**Command:** run in PowerShell 7 with the counters listed below, 10 samples at 1 second, written as PDH CSV:

```
typeperf <counters> -sc 10 -si 1 -o <file.csv> -y
```

**Counters** (as collected): `\Processor(*)\% Processor Time`, `% Privileged Time`, `% DPC Time`, `\Processor Information(_Total)\% Processor Utility`, `\System\Processor Queue Length`, `Context Switches/sec`, `Threads`, `\Memory\Available MBytes`, `Committed Bytes`, `Commit Limit`, `% Committed Bytes In Use`, `Cache Bytes`, `Pool Paged Bytes`, `Pages/sec`, `\PhysicalDisk(*)\% Disk Time`, `Avg. Disk Queue Length`, `Current Disk Queue Length`, `Disk Transfers/sec`, `Avg. Disk sec/Transfer`, `% Idle Time`.

**Sanitizing:** the machine name in each header was replaced with `HOST`, and the time zone name and offset were replaced with placeholders. Only the header and the first three lines are kept.

**Files:** `typeperf-10x1s.csv`.

**systeminfo** (`systeminfo`, filtered to the Virtual Memory and Page File lines, values not kept): the fields are `Virtual Memory: Max Size:`, `Virtual Memory: Available:`, `Virtual Memory: In Use:` (each value in MB with a thousands separator), and `Page File Location(s):`.

**Get-CimInstance Win32_PageFileUsage** fields: `Name`, `AllocatedBaseSize` (MB), `CurrentUsage` (MB), `PeakUsage` (MB).
