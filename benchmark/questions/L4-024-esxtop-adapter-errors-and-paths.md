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
- D. The failed commands on vmhba3 (FCMDS/s 3.40) need investigation even though latency is normal.
- E. ABRTS/s of 0.20 is less than one abort per second, so it is background noise that needs no follow-up.
- F. The vSphere Client charts show failed commands and aborts per adapter, so their normal values clear vmhba3.
- G. The missing paths most likely belong to LUNs that the array no longer presents to this host.
- H. Check which paths each LUN still has: a LUN whose paths all run through one HBA stops if that HBA fails.
- I. vmhba3 carries about half the commands of vmhba2, which shows that its LUNs carry a lighter load.
- J. Next: path state per LUN on vmhba3, its driver and firmware, the cable, the SFP, the switch port and the zoning.
- K. The paths of vmhba3 can be listed in a separate esxtop panel for paths, one row per path.

## Likely wrong answer
- B: "Latency is normal, so the storage is healthy: nothing to do."

## Expected key points
- Answer: A, C, D, H, J.
- A is correct: 10 LUNs x 2 paths per HBA = 20 paths per HBA by design; vmhba3 has 10.
- B is wrong: normal latency now does not mean safe: redundancy is reduced and vmhba3 shows failed commands and aborts.
- C is correct: I/O still flows on the remaining paths.
- D is correct: for failed commands (FCMDS/s) any value above 0 is a reason to investigate; latency does not clear them.
- E is wrong: aborts and resets are expected to be 0 all the time.
- F is wrong: failed commands are esxtop-only, and the vSphere Client has Commands aborted per device only, with no per-adapter counter; normal latency charts do not rule out a fault.
- G is wrong: vmhba2 still sees 20 paths, 2 for each of the 10 LUNs, so every LUN is still presented; the paths are missing on vmhba3 only.
- H is correct: a LUN with all its paths on one HBA has a single point of failure.
- I is wrong: every LUN has paths on both HBAs and Round Robin spreads I/O over the paths that remain; 20 paths against 10 gives the 2:1 command ratio (4,150 against 2,072): fewer paths, not a lighter load.
- J is correct: the errors and the lost paths are on vmhba3 only: its HBA, its link and its fabric.
- K is wrong: esxtop has no path panel (its storage panels are Disk VM, Disk Adapter and Disk Device); the paths of a LUN show when its device is expanded in the Disk Device panel, where NPH gives the path count per device.

## Notes
- Synthetic, 2026-11-05, from the knowledge files listed in `knowledge`. Revised 2026-11-12 for question set 1.0: the screenshot replaced by an esxtop excerpt in text. Counts only after author approval.
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Review 2026-11-14: options F and I turned into near-miss false options that test the same facts (no per-adapter error counters in the vSphere Client; the command ratio follows the path count), so fewer options are true.
- Changed in the 2026-11-15 audit: K added (lost paths read as standby paths); misconception_type average-hides-worst replaced by tool-confusion (F reads the vSphere Client as if it showed per-adapter errors).
- Changed 2026-11-16: D narrowed to failed commands, so D (FCMDS/s) and E (ABRTS/s) no longer negate each other. K replaced: the old K (lost paths read as standby paths) negated A; the new K tests the esxtop panels (no path panel), false as before.

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
source_path: "Synthetic, 2026-11-05"
misconception_type: [tool-confusion]
status: draft
```
