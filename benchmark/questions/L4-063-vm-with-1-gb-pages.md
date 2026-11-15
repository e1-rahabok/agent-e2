# A VM with 1 GB pages

## Prompt
- A SQL Server VM with 256 GB of memory on an ESXi 9.1 host that has memory tiering (DRAM and an NVMe tier).
- The VM was set up for 1 GB pages: `sched.mem.lpage.enable1GPage = TRUE`, with all guest memory reserved.
- VCF Operations, last 30 days: Memory|Consumed flat at 256 GB; Memory|Non Zero Active between 30 and 45 GB.
- The capacity team lists it among "VMs holding idle memory that ESXi can take back when the host needs it".

Which statements are correct?

- A. The 1 GB pages need a full reservation: all its memory is allocated at power-on and is never reclaimed.
- B. About 210 GB of the VM's memory is idle, so ESXi will reclaim it by ballooning or swapping once the host runs short.
- C. The VM is excluded from memory tiering: all its 256 GB stay in DRAM, which leaves less DRAM for the tiered VMs.
- D. After a vMotion, part of its memory may no longer be backed by 1 GB pages, because host memory fragments over time.
- E. Lowering its reservation to 64 GB keeps the 1 GB pages and frees about 192 GB of the host for other VMs.

## Likely wrong answer
B: Consumed above Active read as idle memory that ESXi can take back.

## Expected key points
- Answer: A, C, D.
- A: 1 GB pages are opt-in per VM and need a full reservation. All memory is preallocated at power-on and is never reclaimed: Consumed equals configured for the VM's lifetime, whatever the guest uses.
- B is wrong: the reservation and the 1 GB pages keep all of it; nothing is ballooned or swapped. Whether SQL Server needs it is read in the guest, not from Consumed or Active.
- C: 1 GB page VMs stay in DRAM. A full reservation in DRAM also lowers the DRAM left for tiered VMs.
- D: backing with 1 GB pages is best effort; a freshly booted host has the most contiguous memory. DRS and HA ignore 1 GB page capability in placement.
- E is wrong: a VM with 1 GB pages powers on only with a full reservation. To free memory, resize the VM from what SQL Server needs, or drop the 1 GB pages.

## Notes
- Sources: vSphere 9.1 documentation, Backing Guest vRAM with 1 GB Pages (full reservation, preallocation, best effort, vMotion), and Memory Tiering over NVMe (VMs kept in DRAM); the knowledge base, Large memory pages, section 1 GB pages.

## Metadata
```yaml
id: "0153"
title: "A VM with 1 GB pages"
product: [vsphere, vcf-operations, windows]
technology: [memory]
task: decide-capacity
level: 400
answer_type: deterministic
input: [text]
object: [vm, esxi]
tool: [vcf-operations]
knowledge:
  - vsphere/technology/memory/concepts/large-memory-pages
  - vsphere/technology/memory/concepts/memory-tiering
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/technology/memory/concepts/large-memory-pages
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
answer: [A, C, D]
misconception: [B]
misconception_type: [consumption-as-contention]
status: draft
```
