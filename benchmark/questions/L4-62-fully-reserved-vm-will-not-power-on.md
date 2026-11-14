# A fully reserved VM will not power on

## Prompt
- A standalone ESXi 9.1 host (no cluster) with 512 GB of memory.
- The host summary shows memory reservation available (unreserved): 481 GB. Host Consumed is about 30%.
- A new database test VM: 64 vCPUs, 480 GB of memory, with "Reserve all guest memory" set (480 GB reserved).
- Power-on fails with "Insufficient memory resources".
- The administrator says: "481 GB is unreserved and the VM needs 480 GB, and the host is only 30% used. Why does it fail, and what do I change?"

Answer the administrator.

## Likely wrong answer
"It should fit: 481 GB is free for 480 GB. The host is only 30% used, so it is a bug; retry or reboot the host."

## Expected key points
- Admission control checks reservations, not usage: Consumed at 30% plays no part.
- The VM needs its memory reservation plus its overhead reservation. The memory for the VMM and the virtual devices is reserved at power-on, on top of the 480 GB (VMX swap keeps most of the VMX process memory out of the reservation).
- Overhead grows with the vCPU count and the configured memory. For 64 vCPUs and 480 GB it is well above the 1 GB that is left.
- The exact overhead of the VM is written to its vmware.log at power-on.
- Change: reserve less than all guest memory, or make the VM smaller, by more than the overhead; or free reservations held by other VMs; or use a host with more memory.

## Notes
- Sources: the knowledge base, Memory overhead (per-VM overhead reserved at power-on, in addition to configured memory; the largest fully reserved VM that powers on is smaller than free host memory; vmware.log, VMMEM) and Cluster admission control (reservations, not usage; overhead always checked); vSphere 9.1 documentation, vSphere Resource Management, Overhead Memory on Virtual Machines and VMX Swap Files (p. 1839), Admission Control; Troubleshooting > The Reservable Memory is Lower than Expected (p. 1958: a 256 GB VM has an overhead of about 4.5% of its size; the overhead must be considered for the largest VM that powers on with full reservation).

## Metadata
```yaml
id: "0152"
title: "A fully reserved VM will not power on"
product: [vsphere]
technology: [memory, system]
task: troubleshoot
level: 400
answer_type: judged
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
