# Errors and paths in the esxtop disk adapter panel

## Prompt
- Host esx-22 reaches 10 FC LUNs. By design, each LUN has 4 paths: 2 through each of its 2 HBAs. The path selection policy is Round Robin on every LUN.
- Latency on this host is normal in the vSphere Client charts.
- The esxtop disk adapter panel (d), with the error and path fields added, shows:

```text
ADAPTR  NPTH   CMDS/s  DAVG/cmd  KAVG/cmd  FCMDS/s  ABRTS/s  RESETS/s
vmhba2    20  4150.3      0.82      0.01     0.00     0.00      0.00
vmhba3    10  2071.8      0.85      0.01     3.40     0.20      0.00
```

What do you conclude from the panel, and what do you check next?

## Likely wrong answer
"Latency is normal, so the storage is healthy: nothing to do."

## Expected key points
- vmhba3 has 10 paths where the design gives 20: half its paths to the LUNs are gone. The host has lost redundancy, while IO still flows on the remaining paths.
- vmhba3 carries about half the commands of vmhba2: with Round Robin over the remaining paths, consistent with fewer paths, not with a lighter load.
- Failed commands (FCMDS/s 3.40) and aborts (ABRTS/s 0.20) on vmhba3 need investigation: they should be 0. Failed commands are esxtop-only, and the vSphere Client has no per-adapter abort counter (only Commands aborted per device), so normal latency charts do not rule out a fault.
- Normal latency now does not mean safe: redundancy is reduced. Check per LUN which paths remain: a LUN left with paths on one HBA only stops if that HBA or its fabric fails.
- Next: path state per LUN on vmhba3, the HBA driver and firmware, the cable, the SFP and the fabric switch port of that adapter, and the zoning.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: the screenshot replaced by an esxtop excerpt in text. Counts only after author approval.

## Metadata
```yaml
id: "0070"
title: "Errors and paths in the esxtop disk adapter panel"
product: [vsphere]
technology: [storage]
task: troubleshoot
level: 400
answer_type: judged
input: [text]
object: [esxi]
tool: [esxtop]
knowledge:
  - vsphere/tools/esxtop/storage
  - vsphere/technology/storage/metrics/host/adapter-and-path
  - vsphere/technology/storage/concepts/storage-layers
knowledge_main: vsphere/tools/esxtop/storage
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
misconception_type: [average-hides-worst]
status: draft
```
