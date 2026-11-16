# NFS datastore latency in esxtop

## Prompt
- Host esx-31 mounts NFS 4.1 datastore nas-ds01 over a VMkernel port on a 25 GbE network. VMs on it report slow disk IO since this morning.
- In esxtop, the disk device panel (u) shows this row for the NFS datastore:

```text
DQLEN  ACTV  QUED  %USD  LOAD   CMDS/s  DAVG/cmd  KAVG/cmd  GAVG/cmd  QAVG/cmd
    -     -     -     -     -  2210.40     18.42      0.03     18.45         -
```

- The NAS administrator reports an average latency of 1.5 ms for the volume behind nas-ds01 over the same minutes.

Which statements are correct?

- A. For an NFS datastore, DAVG is the time beyond the host's NFS client: the network and the NFS server.
- B. High DAVG points to the HBA: raise the device queue depth of the host for this datastore.
- C. The queue columns and QAVG show no value because NFS has no SCSI device queue in the host.
- D. Check the storage network (drops, retransmits, MTU end to end on the VMkernel path) and the NAS itself.
- E. KAVG near 0 shows the IO does not wait in the host's storage stack: the 18 ms is network path plus NAS.
- F. The vSphere Client Disk (device) charts of esx-31 would show the same 18 ms for this datastore.
- G. With the NAS at 1.5 ms, most of the 18 ms is spent between the host's NFS client and the NAS.
- H. With the NAS at 1.5 ms and KAVG at 0.03 ms, esxtop misreports the latency of this datastore.

## Answers
A, C, D, E, G

## Explanation
- A is correct: an NFS datastore has its own row in the disk device panel; its DAVG = network latency + NAS processing time.
- B is wrong: there is no HBA and no device queue for NFS.
- C is correct: NFS bypasses the block storage stack (PSA), so there is no device queue depth, no kernel device queue and no QAVG.
- D is correct: with DAVG high, look at what DAVG covers: the storage network and the NAS. Engage the NAS owner with the time window.
- E is correct: GAVG ≈ DAVG + KAVG = 18.42 + 0.03. The IO does not queue in the host's storage stack; for NFS, DAVG covers the host's network stack, the network and the NAS.
- F is wrong: the vSphere Client lists only block devices as Disk objects; NFS latency is read on the datastore counters.
- G is correct: DAVG for NFS is network latency plus NAS processing time; with the NAS at 1.5 ms, about 17 of the 18.4 ms lie on the path between the NFS client and the NAS: check the storage network (drops, MTU) first.
- H is wrong: the two readings agree. The NAS reports only its own processing time; DAVG adds the network path, and KAVG near 0 only shows that the IO does not wait in the host's storage stack.
- Misconception: B: tuning a block-storage queue that NFS does not have. Or F: expecting an NFS datastore in the vSphere Client Disk charts.

## Notes
- Synthetic, 2026-11-12. Paired with 0050, which tests the same panel on a screenshot. Counts only after author approval.
- Audit 2026-11-15: the NAS's own latency added to the stem, with G (true: most of the time is on the network path) and H (false: esxtop misreports), so the operator must split network from NAS. Key changed from A, C, D, E to A, C, D, E, G.
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
source_path: "Synthetic, 2026-11-12"
misconception: [B, F]
misconception_type: [tool-confusion]
pair: "0050"
status: draft
```
