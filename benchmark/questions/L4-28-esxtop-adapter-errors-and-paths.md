# Errors and paths in the esxtop disk adapter panel

## Prompt
The attached screenshot is the esxtop disk adapter panel (d) of one ESXi host, with the error and path columns shown.

- By design, each host has 4 paths to every LUN through 2 HBAs.
- Latency on this host is normal in the vSphere Client charts.

What do you conclude from the panel, and what do you check next?

## Input to supply
- Tool: esxtop on one ESXi 9.1 host with Fibre Channel or iSCSI storage, disk adapter panel (press d), error and path fields added (press f).
- Must show the columns ADAPTR, NPTH, CMDS/s, DAVG/cmd, KAVG/cmd, FCMDS/s, ABRTS/s, RESETS/s for every vmhba.
- Condition for the key: one vmhba shows NPTH below the design (for example 2 instead of 4 per LUN, or half of the other HBA), and FCMDS/s or ABRTS/s above 0 on that adapter. Latency columns are normal.
- Mask WWNs and IQNs.
- Save as `benchmark/questions/70/esxtop-disk-adapter-errors.png`.

## Likely wrong answer
"Latency is normal, so the storage is healthy: nothing to do."

## Expected key points
- Failed commands (FCMDS/s) above 0 need investigation; ABRTS/s and RESETS/s should be 0. These counters are not in the vSphere Client, so normal latency charts do not rule out a fault.
- NPTH below the design means paths are missing on that adapter: the host has lost redundancy, even while IO still flows on the other paths.
- Next: check the path state per LUN, the HBA driver and firmware, the cable and the fabric switch port or the iSCSI network of that adapter.
- Normal latency now does not mean normal under failure: with half the paths, one more failure stops IO.

## Notes
- Previous id: question-0070 (renamed 2026-11-05).
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
## Metadata
```yaml
id: "0070"
title: "Errors and paths in the esxtop disk adapter panel"
product: [vsphere]
technology: [storage]
task: troubleshoot
level: 400
answer_type: judged
input: [screenshot]
knowledge:
  - vsphere/tools/esxtop/storage
  - vsphere/technology/storage/metrics/host/adapter-and-path
attachments:
  - 0070/esxtop-disk-adapter-errors.png
origin: synthetic
source_path: "Drafted by Claude 2026-11-05 for the Level 400 allocation (benchmark/design.md, section 3.6)"
status: awaiting-input
```
