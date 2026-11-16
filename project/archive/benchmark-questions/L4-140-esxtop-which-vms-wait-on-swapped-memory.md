# esxtop: which VMs wait on swapped memory now

## Prompt
See [the esxtop memory panel](0389/esxtop-memory-panel-swap-compression.png).

- The ESXi host has been short of memory for half an hour, and users of several applications complain.
- The on-call engineer plans to tell the owner of the VM with the most memory in its swap file that their VM is the slow one, and to migrate that VM first.

Which statements are correct?

- A. SWCUR is memory held in the swap file now, not a swap rate.
- B. Compression is running on at least one VM at the moment of the screen.
- C. A VM with only SWW/s above 0 is not waiting: pages written out cost it nothing until touched.
- D. At least one VM on the screen is reading pages back from its swap file now.
- E. The header shows the host in the high memory state.
- F. The VM holding the most memory in its swap file is the VM slowed most by memory right now.
- G. While ESXi compresses a page, the vCPU of that VM stops until the compression is done.
- H. Memory that sits in a swap file is harmless to its VM from now on.
- I. Moving the VM with the largest SWCUR to another host first gives its users relief soonest.

## Input to supply
- Product: ESXi 9.1, esxtop over SSH. One host under memory pressure (state soft or hard in the header), with no host cache configured.
- Screen: esxtop, memory panel (`m`), fields added with `f`: MCTLSZ, SWCUR, SWR/s, SWW/s, ZIP/s, UNZIP/s, CACHEUSD (keep NAME and MEMSZ). Show the header lines and at least 3 VM rows, sorted by SWCUR. Save as `benchmark/questions/0389/esxtop-memory-panel-swap-compression.png`.
- Condition the key depends on, all on the one screen:
  - header `state` soft or hard;
  - VM X: the largest SWCUR on the screen (1 GB or more), with SWR/s and UNZIP/s at 0.00;
  - VM Y (not X): SWR/s at 1 MB/s or more;
  - VM Z (not X, not Y): ZIP/s above 0, with SWR/s and UNZIP/s at 0.00;
  - no host cache configured on the host (swap to host cache plays no part).
- How to produce it in a lab: overcommit a small host with VMs that touch their memory. Let VM X touch all its memory and then go idle (its pages are swapped and stay cold); let VM Y loop over all its memory (it reads swapped pages back); start VM Z's load last (its pages are being compressed).
- Masking: mask every VM, host, datastore and cluster name (the NAME column and the host name).

## Likely wrong answer
F: "The VM with the most memory in swap is the slowest one."

## Expected key points
- Answer: A, B, C, D.
- A true: SWCUR is the amount in the swap file now; SWR/s and SWW/s are the rates.
- B true: one VM shows ZIP/s above 0.
- C true: SWW/s and ZIP/s move pages out, a capacity problem of the host. A page that is not touched again costs the VM no wait.
- D true: one VM shows SWR/s above 0: a vCPU that touched a swapped page waits for it. That is memory contention.
- E false: the header shows the soft or hard state, where ESXi reclaims memory.
- F false: the largest amount in swap is not the largest wait. That VM's SWR/s and UNZIP/s are 0.00: it reads nothing back now.
- G false: compression moves a page out. The VM waits only when it touches a compressed page and ESXi decompresses it (UNZIP/s).
- H false: over-correction. A swapped page costs no wait until the VM touches it; then the vCPU waits for the swap-in. The more is swapped, the higher the chance.
- I false: the wrong action from F. That VM does not wait now; the VMs reading back from swap or the compression cache do.

## Notes
- Retired 2026-11-15 (question bank audit): its partner 0068 already gives the esxtop memory panel as text, so an export adds no new fact (exports review 2026-11-15, section 4).
- Paired with 0068 (theory and practical; benchmark/design.md, section 3.9). Pairing plan 2026-11-14, item C15.
- The options name VMs by their values, not by name, because the names are masked.
- Review fixes 2026-11-15: options reworded away from 0068; the reading of the largest-SWCUR VM moved into the key, since it negated F (T2); screen readings added (B, D true; E false); host cache excluded. Key A, B, C, H → A, B, C, D.
- The key holds whenever the condition of `## Input to supply` holds.
- Written 2026-11-14 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after approval (design.md, section 6.2).

## Metadata
```yaml
id: "0389"
title: "esxtop: which VMs wait on swapped memory now"
product: [vsphere]
technology: [memory]
task: troubleshoot
level: 400
answer_type: deterministic
input: [screenshot]
object: [vm, esxi]
tool: [esxtop]
knowledge:
  - vsphere/tools/esxtop/memory
  - vsphere/technology/memory/concepts/swap-and-compression
  - vsphere/technology/memory/concepts/host-memory-states
  - vsphere/technology/memory/metrics/virtual-motherboard/latency
knowledge_main: vsphere/tools/esxtop/memory
attachments:
  - 0389/esxtop-memory-panel-swap-compression.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C15"
answer: [A, B, C, D]
misconception: [F]
misconception_type: [reclamation-as-contention, cumulative-vs-current]
status: retired
```
