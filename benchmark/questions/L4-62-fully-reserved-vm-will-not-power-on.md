# A fully reserved VM will not power on

## Prompt
- A standalone ESXi 9.1 host (no cluster) with 512 GB of memory.
- The host summary shows memory reservation available (unreserved): 481 GB. Host Consumed is about 30%.
- A new database test VM: 64 vCPUs, 480 GB of memory, with "Reserve all guest memory" set (480 GB reserved). It has no CPU reservation.
- Power-on fails with "Insufficient memory resources".
- The administrator says: "481 GB is unreserved and the VM needs 480 GB, and the host is only 30% used. Why does it fail, and what do I change?"

Which statements are correct?

- A. It should fit, since 481 GB is unreserved for 480 GB and the host is only 30% used: the failure is a fault, and a retry or a host reboot clears it.
- B. The power-on also needs the VM's overhead memory reserved on top of the 480 GB, and for 64 vCPUs and 480 GB that overhead is far more than the 1 GB left.
- C. The per-VM overhead is part of the 480 GB of configured memory, so it needs no reservation of its own.
- D. The VMX swap file takes all of the VM's overhead out of the reservation, so overhead cannot be what blocks the power-on.
- E. The per-VM overhead is about 100 MB whatever the size of the VM, so it cannot explain the failure.
- F. The 64 vCPUs need CPU that the host cannot reserve, and that is what blocks the power-on.
- G. Lowering the memory reservation by 1 GB, to 479 GB, is enough to let the VM power on on this host.

## Likely wrong answer
- A: "It should fit: 481 GB is free for 480 GB. The host is only 30% used, so it is a bug; retry or reboot the host."
- C: "The overhead is inside the VM's configured memory."

## Expected key points
- Answer: B.
- A false: admission control compares reservations with the unreserved memory, so the 30% Consumed plays no part; the VM asks for 480 GB plus its overhead, more than 481 GB, and the result does not change on a retry.
- B true: the memory of the VMM and the virtual devices is fully reserved at power-on, in addition to the configured memory; overhead grows with the vCPU count and the configured memory (about 4.5% of a 256 GB VM in the documentation). The largest VM that powers on with a full reservation is smaller than the unreserved memory.
- C false: the per-VM overhead is reserved in addition to the configured memory.
- D false: VMX swap reduces the VMX part of the reservation; the VMM and virtual device memory stay fully reserved at power-on.
- E false: the overhead depends on the vCPU count and the configured memory; a 480 GB, 64-vCPU VM carries gigabytes of it.
- F false: the VM has no CPU reservation, and a VM with no reservation passes CPU admission control; the error names memory.
- G false: 479 GB plus an overhead of several GB is still above the 481 GB unreserved. The fix is to lower the reservation, or the configured memory, by more than the overhead; or free reservations held by other VMs; or use a host with more memory.

## Notes
- Sources: the knowledge base, Memory overhead (per-VM overhead reserved at power-on, in addition to configured memory; the largest fully reserved VM that powers on is smaller than free host memory; vmware.log, VMMEM) and Cluster admission control (reservations, not usage; overhead always checked); vSphere 9.1 documentation, vSphere Resource Management, Overhead Memory on Virtual Machines and VMX Swap Files (p. 1839), Admission Control; Troubleshooting > The Reservable Memory is Lower than Expected (p. 1958: a 256 GB VM has an overhead of about 4.5% of its size; the overhead must be considered for the largest VM that powers on with full reservation).
- Converted from judged to multiple choice (Q199 F, 2026-11-14). Dropped from the old key: "the exact overhead is written to vmware.log at power-on" (a file name, not a mechanism: design.md, section 11, item 7). Two old key points are tested by false options whose reasons state them, so that this question has one correct option: "admission control checks reservations, not usage" (A) and the fix, lowering the reservation by more than the overhead (G).

## Metadata
```yaml
id: "0152"
title: "A fully reserved VM will not power on"
product: [vsphere]
technology: [memory, system]
task: troubleshoot
level: 400
answer_type: deterministic
answer: [B]
misconception: [A,C]
input: [text]
object: [vm, esxi]
tool: [vcenter]
knowledge:
  - vsphere/technology/memory/concepts/memory-overhead
  - vsphere/object-types/cluster/concepts/admission-control-and-cluster-state
  - vsphere/technology/memory/metrics/host/reservation
knowledge_main: vsphere/technology/memory/concepts/memory-overhead
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [consumption-as-contention, provider-vs-consumer]
status: draft
```
