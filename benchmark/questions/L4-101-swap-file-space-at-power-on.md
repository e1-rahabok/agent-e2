# Swap file space at power-on

## Prompt
- A new VMFS datastore, DS-A, holds the files of the VMs below. For these VMs the swap file location is Default and the cluster setting is Virtual machine directory.
- The ESX hosts do not overcommit memory, and no host-level swapping is expected. Ignore the VMX swap file and the VM overhead.
- Before the planned weekend maintenance every VM is shut down, and on Monday all VMs are powered on again. Memory settings are as they are today.

| Group | VMs | Configured memory per VM | Notes |
|---|---|---|---|
| G1 | 12 | 128 GB | Reservation 0. |
| G2 | 10 | 256 GB | Reservation 256 GB. |
| G3 | 16 | 64 GB | The reservation was raised from 32 GB to 48 GB yesterday, while the VMs ran. |
| G4 | 6 | 192 GB | Reservation 0 until last week, when an administrator added an NVIDIA vGPU device to each VM and changed nothing else. |
| G5 | 8 | 96 GB | Reservation 24 GB. The per-VM option Swap file location points to another datastore, DS-B. |
| G6 | 20 | 128 GB | Reservation 0. The VM directories are on a vSAN datastore, not on DS-A. |
| G7 | 6 | 32 GB | Reservation 0. These VMs stay powered off. |

How much space on DS-A do the regular swap (.vswp) files need after all the VMs that run are powered on again?

- A. 1,792 GB
- B. 2,048 GB
- C. 2,944 GB
- D. 2,368 GB
- E. 4,352 GB

## Likely wrong answer
B (the old reservation of G3), C (G4 counted at its configured memory), D (G5 counted although its swap is on DS-B) or E (G6 counted although it is on vSAN).

## Expected key points
- Answer: A (1,792 GB).
- ESX creates the swap file at power-on with the size of the configured memory minus the memory reservation. A reservation equal to the configured memory gives a zero-byte file. The size follows the reservation at the time of the power-on, so after a full power cycle G3 uses 64 - 48 = 16 GB per VM.
- G1: 12 x 128 GB = 1,536 GB. G2: 10 x (256 - 256) = 0 GB. G3: 16 x 16 GB = 256 GB. G4: the vGPU device forces a full memory reservation (the vSphere documentation says it is applied automatically), so 0 GB. G5: the swap files are on DS-B. G6: on a vSAN datastore (and on vVols) the swap file is a separate object on that datastore, so it does not use DS-A. G7: powered off, no swap file. Total on DS-A: 1,536 + 256 = 1,792 GB.
- B (2,048 GB) uses the old reservation of 32 GB for G3 (16 x 32 = 512 GB). C (2,944 GB) adds G4 at 6 x 192 = 1,152 GB. D (2,368 GB) adds G5 at 8 x (96 - 24) = 576 GB. E (4,352 GB) adds G6 at 20 x 128 = 2,560 GB.

## Notes
- Public source: Performance Best Practices for VMware vSphere 9.1, revision 20260624, "Memory Swapping Optimizations" (p. 35): swap file "equal in size to the difference between the virtual machine's configured memory size and its memory reservation", created when the VM is first powered on. VMware vSphere 9.1 PDF (build of 2026-11-02), Resource Management, "Swap File Location" (created at power-on; on vSAN and vVols "the swap file is created as a separate vSAN or vVols object"; per-VM override of the location); "Using Swap Files": do not store swap files on thin-provisioned LUNs; the vGPU configuration topic of the vSphere documentation: "Full memory reservation will be applied automatically, it's required for PCI device". Broadcom KB 342554, "All guest OS memory reserved when disabling VM swap file" (swap size formula; 16 GB VM: 0% reservation gives 16 GB, 50% gives 8 GB, 100% gives 0 bytes; the VM must be powered off for the swap file size to change with the reservation; Updated On field empty).
- Why one answer: the size is a stated formula, the prompt gives all values and says which VMs are on DS-A, and each wrong option corresponds to one specific reading error.
- Debatable risk: whether the swap file of a running VM is resized when the reservation changes is not needed, because the prompt asks for the state after a full power cycle. The vGPU rule is one line in the vSphere 9.1 documentation (vGPU passthrough); the prompt says the administrator changed nothing else. The vSAN swap object placement is stated for the default location only; the prompt says the VM directories are on vSAN.
- Rewritten 2026-11-13 to raise difficulty: from one multiplication to a seven-group table with a reservation changed on running VMs, a device that forces a full reservation, a per-VM swap location, a vSAN datastore and powered-off VMs; each wrong option is one of those traps.

## Metadata
```yaml
id: "0296"
title: Swap file space at power-on
product: [vsphere, vsan]
technology: [memory, storage]
task: decide-capacity
level: 400
answer_type: deterministic
input: [text]
object: [datastore, vm]
tool: [none]
knowledge:
  - vsphere/technology/memory/configuration/host-level-swapping
  - vsphere/technology/memory/concepts/memory-overhead
knowledge_main: vsphere/technology/memory/configuration/host-level-swapping
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [A]
misconception: [B, E]
misconception_type: []
status: draft
```
