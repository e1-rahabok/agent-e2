---
id: vsphere/cpu/architecture/virtualization-overhead
type: concept
scope: vsphere
resources: [cpu]
objects: [vcpu, vm, esxi, cluster]
related:
  - vsphere/cpu/architecture/idle-and-unused-vcpus
  - vsphere/cpu/architecture/numa
  - vsphere/foundations/overhead
  - vsphere/foundations/visibility-layers
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: ESX CPU Considerations (pp. 24-25)
corrections: []
review_notes:
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
  - "Old file vsphere/cpu/counters/esxi/cpu.usage.average.md states 'sustained values above ~80-85%' with no source. This source gives 80% (PCPU ceiling) and 90% (warning) for esxtop. Author to decide whether to replace the old threshold."
status: draft
---

# CPU virtualization overhead

## Definition
- CPU virtualization overhead depends on two things:
  - the share of the VM workload that runs directly on the physical processor,
  - the cost of virtualizing the rest of the workload.

## Workload classes
| Class | Effect of overhead | Result |
|---|---|---|
| Most workloads | Very small | Performance essentially comparable to native |
| Workloads that spend most time waiting for external events (user interaction, device input, data retrieval) | Absorbed by otherwise unused CPU cycles | Throughput similar to native; possible slight latency increase |
| CPU-bound workloads where virtualization adds overhead | Not absorbed | Possible noticeable degradation in throughput and latency |

## Commitment and overcommit
- Full commitment: total vCPUs on the host equal total physical cores on the host.
- Full commitment is allowed in most environments.
- Overcommit: total vCPUs on the host exceed total physical cores on the host.
- Significant overcommit is allowed in most environments without impacting VM performance.
- Saturation: if the VMs on a host consume all their allocated CPU, the host becomes CPU saturated.
- A saturated host reduces the performance of some or all VMs on it.
- Latency-sensitive workloads are hit hardest by saturation.
- Leave some CPU resources for ESX.
- Commit physical cores fully only where VMs rarely, if ever, use all their allocated CPU at the same time.
- Remedies named by the source:
  - power off some VMs,
  - migrate VMs to another host. DRS can do this automatically.

## Host CPU monitoring
- Tools: vSphere Client, esxtop, resxtop.
- esxtop CPU panel, first line (load average): a value equal to or greater than 1 means the system is overloaded.
- esxtop PCPU line (usage of physical CPUs): 80% is a reasonable ceiling.
- esxtop PCPU line: 90% should be a warning.
- The source notes that organizations set their own standards for the target load percentage.

## Traps
- "Overcommit is never safe" → overcommit is allowed in most environments. The risk is saturation, which happens when VMs use their full allocations at the same time.
- "Host average CPU looks fine, so there is no saturation risk" → saturation risk depends on how many VMs can use their full allocation at once, not only on the average.
