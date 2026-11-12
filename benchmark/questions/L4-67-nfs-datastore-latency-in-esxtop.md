# NFS datastore latency in esxtop

## Prompt
- Host esx-31 mounts NFS 4.1 datastore nas-ds01 over a VMkernel port on a 25 GbE network. VMs on it report slow disk IO since this morning.
- In esxtop, the disk device panel (u) shows this row for the NFS datastore:

```text
DQLEN  ACTV  QUED  %USD  LOAD   CMDS/s  DAVG/cmd  KAVG/cmd  GAVG/cmd  QAVG/cmd
    -     -     -     -     -  2210.40     18.42      0.03     18.45         -
```

Which statements are correct?

- A. For an NFS datastore, DAVG is the time beyond the host's NFS client: the network and the NFS server.
- B. High DAVG points to the HBA: raise the device queue depth of the host for this datastore.
- C. The queue columns and QAVG show no value because NFS has no SCSI device queue in the host.
- D. Check the storage network (drops, retransmits, MTU end to end on the VMkernel path) and the NAS itself.
- E. KAVG near 0 shows the IO does not wait in the host's storage stack: the 18 ms is network path plus NAS.
- F. The vSphere Client Disk (device) charts of esx-31 would show the same 18 ms for this datastore.

## Likely wrong answer
B: tuning a block-storage queue that NFS does not have. Or F: expecting an NFS datastore in the vSphere Client Disk charts.

## Expected key points
- Answer: A, C, D, E.
- A: an NFS datastore has its own row in the disk device panel; its DAVG = network latency + NAS processing time.
- C: NFS bypasses the block storage stack (PSA), so there is no device queue depth, no kernel device queue and no QAVG.
- D: with DAVG high, look at what DAVG covers: the storage network and the NAS. Engage the NAS owner with the time window.
- E: GAVG ≈ DAVG + KAVG = 18.42 + 0.03. The IO does not queue in the host's storage stack; for NFS, DAVG covers the host's network stack, the network and the NAS.
- B is wrong: there is no HBA and no device queue for NFS.
- F is wrong: the vSphere Client lists only block devices as Disk objects; NFS latency is read on the datastore counters.

## Notes
- Drafted by Claude 2026-11-12 for question set 1.0, Storage slot "NFS in esxtop" (project/plan.md, M2). The deferred screenshot question 0050 tests the same panel on a picture after 1.0. Counts only after author approval.
- Vendor document: Broadcom KB 427727, "VMs on NFS datastore observe latency" (https://knowledge.broadcom.com/external/article/427727): NFS datastore latency is read as DAVG and KAVG in esxtop; the resolution is on the NFS server side.

## Metadata
```yaml
id: "0186"
title: "NFS datastore latency in esxtop"
product: [vsphere]
technology: [storage, network]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
object: [esxi, datastore]
tool: [esxtop, vcenter]
knowledge:
  - vsphere/tools/esxtop/storage
  - vsphere/technology/storage/concepts/esxi-storage-latency-stack
knowledge_main: vsphere/technology/storage/concepts/esxi-storage-latency-stack
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12 for the Storage slots (benchmark/design.md, section 3)"
answer: [A, C, D, E]
misconception: [B, F]
misconception_type: [tool-confusion]
status: draft
```
