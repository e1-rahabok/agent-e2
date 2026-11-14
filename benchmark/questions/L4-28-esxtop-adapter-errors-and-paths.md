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

Which statements about the panel and the next checks are correct?

- A. vmhba3 shows 10 paths where the design gives it 20: half of its paths to the LUNs are gone.
- B. Latency on the host is normal in the vSphere Client, so the storage is healthy and there is nothing to do.
- C. The host has less path redundancy than designed, even though I/O still flows.
- D. Failed commands and aborts on vmhba3 should be 0; any value above 0 needs investigation.
- E. ABRTS/s of 0.20 is less than one abort per second, so it is background noise that needs no follow-up.
- F. The vSphere Client charts show failed commands and aborts per adapter, so their normal values clear vmhba3.
- G. The missing paths most likely belong to LUNs that the array no longer presents to this host.
- H. Check which paths each LUN still has: a LUN whose paths all run through one HBA stops if that HBA fails.
- I. vmhba3 carries about half the commands of vmhba2, which shows that its LUNs carry a lighter load.
- J. Next: path state per LUN on vmhba3, its driver and firmware, the cable, the SFP, the switch port and the zoning.

## Likely wrong answer
- B: "Latency is normal, so the storage is healthy: nothing to do."

## Expected key points
- Answer: A, C, D, H, J.
- A true: 10 LUNs x 2 paths per HBA = 20 paths per HBA by design; vmhba3 has 10.
- B false: normal latency now does not mean safe: redundancy is reduced and vmhba3 shows failed commands and aborts.
- C true: I/O still flows on the remaining paths.
- D true: failed commands (FCMDS/s 3.40) and aborts (ABRTS/s 0.20) should be 0; any value above 0 is a reason to investigate.
- E false: aborts and resets are expected to be 0 all the time.
- F false: failed commands are esxtop-only, and the vSphere Client has Commands aborted per device only, with no per-adapter counter; normal latency charts do not rule out a fault.
- G false: vmhba2 still sees 20 paths, 2 for each of the 10 LUNs, so every LUN is still presented; the paths are missing on vmhba3 only.
- H true: a LUN with all its paths on one HBA has a single point of failure.
- I false: every LUN has paths on both HBAs and Round Robin spreads I/O over the paths that remain; 20 paths against 10 gives the 2:1 command ratio (4,150 against 2,072): fewer paths, not a lighter load.
- J true: the errors and the lost paths are on vmhba3 only: its HBA, its link and its fabric.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Revised 2026-11-12 for question set 1.0: the screenshot replaced by an esxtop excerpt in text. Counts only after author approval.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Review 2026-11-14: options F and I turned into near-miss false options that test the same facts (no per-adapter error counters in the vSphere Client; the command ratio follows the path count), so fewer options are true.

## Metadata
```yaml
id: "0070"
title: "Errors and paths in the esxtop disk adapter panel"
product: [vsphere]
technology: [storage]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [A,C,D,H,J]
misconception: [B]
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
