# A fully reserved VM will not power on

## Prompt
- A standalone ESXi 9.1 host (no cluster) with 512 GB of memory.
- The host summary shows memory reservation available (unreserved): 481 GB. Host Consumed is about 30%.
- A new database test VM: 64 vCPUs, 480 GB of memory, with "Reserve all guest memory" set (480 GB reserved). It has no CPU reservation.
- Power-on fails with "Insufficient memory resources".
- The administrator says: "481 GB is unreserved and the VM needs 480 GB, and the host is only 30% used. Why does it fail, and what do I change?"

Which statements are correct?

- A. It should fit, since 481 GB is unreserved for 480 GB and the host is only 30% used: the failure is a fault, and a retry or a host reboot clears it.
- B. The power-on also needs the VM's overhead reserved on top of the 480 GB; for 64 vCPUs and 480 GB it is far above the 1 GB left.
- C. Creating the 1 GB system swap file with `esxcli` moves per-VM overhead out of host memory and makes room for this VM.
- D. The VMX swap file takes all of the VM's overhead out of the reservation, so overhead cannot be what blocks the power-on.
- E. The per-VM overhead is about 100 MB whatever the size of the VM, so it cannot explain the failure.
- F. The 64 vCPUs need CPU capacity that the host cannot reserve for the VM, and that is what blocks the power-on.
- G. Lowering the memory reservation by 1 GB, to 479 GB, is enough to let the VM power on on this host.
- H. Setting `sched.swap.vmxSwapEnabled = FALSE` on the VM lowers the memory reservation its power-on needs.

## Likely wrong answer
- A: "It should fit: 481 GB is free for 480 GB. The host is only 30% used, so it is a bug; retry or reboot the host."

## Expected key points
- Answer: B.
- A is wrong: admission control compares reservations with the unreserved memory, so the 30% Consumed plays no part; the VM asks for 480 GB plus its overhead, more than 481 GB, and the result does not change on a retry.
- B is correct: the memory of the VMM and the virtual devices is fully reserved at power-on, in addition to the configured memory; overhead grows with the vCPU count and the configured memory: by the documented representative values (4.5% of a 256 GB VM, more for smaller VMs) a 256 GB VM carries about 11.5 GB, and overhead grows with the configured memory and the vCPU count, so a 480 GB, 64-vCPU VM carries more than that (the exact value is in its vmware.log, VMMEM). The largest VM that powers on with a full reservation is smaller than the unreserved memory.
- C is wrong: the system swap file covers the system-wide overhead of the VMkernel and host agents (up to 1 GB, under memory pressure); it is separate from the per-VM swap files and holds no per-VM overhead. Even a full 1 GB gained leaves far less than the VM's overhead.
- D is wrong: VMX swap reduces the VMX part of the reservation; the VMM and virtual device memory stay fully reserved at power-on.
- E is wrong: the overhead depends on the vCPU count and the configured memory; a 480 GB, 64-vCPU VM carries gigabytes of it.
- F is wrong: the VM has no CPU reservation, and a VM with no reservation passes CPU admission control; the error names memory.
- G is wrong: 479 GB plus an overhead of several GB is still above the 481 GB unreserved. The fix is to lower the reservation, or the configured memory, by more than the overhead; or free reservations held by other VMs; or use a host with more memory.
- H is wrong: without a VMX swap file the VMX memory must be reserved too, so the reservation rises significantly; VMX swap is what lowers it.

## Notes
- Sources: the knowledge base, Memory overhead (per-VM overhead reserved at power-on, in addition to configured memory; the largest fully reserved VM that powers on is smaller than free host memory; vmware.log, VMMEM) and Cluster admission control (reservations, not usage; overhead always checked); vSphere 9.1 documentation, vSphere Resource Management, Overhead Memory on Virtual Machines and VMX Swap Files (p. 1839), Admission Control; Troubleshooting > The Reservable Memory is Lower than Expected (p. 1958: a 256 GB VM has an overhead of about 4.5% of its size; the overhead must be considered for the largest VM that powers on with full reservation).
- C replaced in the 2026-11-16 re-review: the old C (overhead inside the configured memory) was the negation of B. The new C tests the system swap file (knowledge base, Memory overhead, System-wide overhead), same truth value.
- H added in the 2026-11-15 audit (mechanism option: VMX swap off raises the reservation; knowledge base, Memory overhead, VMX swap).

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
misconception: [A]
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
source_path: "Synthetic, 2026-11-12"
misconception_type: [consumption-as-contention]
status: draft
```
