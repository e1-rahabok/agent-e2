---
id: vsphere/cpu/architecture/side-channel-scheduling
type: concept
scope: vsphere
resources: [cpu]
objects: [esxi, vm, guest-os]
related:
  - vsphere/cpu/architecture/hyper-threading
  - vsphere/cpu/architecture/hardware-assisted-virtualization
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: "Not in the 9.1 document. Previously in 9.0: CPU Hardware Considerations > Side-Channel Vulnerabilities (pp. 11-12); ESX CPU Considerations > Side-Channel Vulnerability Mitigation in ESX (pp. 25-26); Guest OS CPU Considerations (p. 55)"
corrections: []
review_notes:
  - "Not in the 9.1 document. Its table of contents has no side-channel section. Checked CPU hardware pp. 11-13, ESX pp. 25-32, guest OS pp. 55-57. Content is from the 9.0 document. Verify against KB 55806 and current VMware security documentation before use."
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
  - "Only the 9.0 source was read. The default scheduler behaviour in vSphere 9.x is not checked against KB 55806."
  - "Not read: KB 52245, 54951, 55636, 56931. Source names these for details."
status: draft
---

# Side-channel vulnerabilities and the ESX scheduler

> Not in the 9.1 document. Content below is from the 9.0 document. Verify before use.

## Vulnerability classes
- Side-channel vulnerabilities include Spectre, Meltdown, Foreshadow, L1TF, and others.
- Some mitigations have a significant performance impact.
- The source does not cover the topic in full. Use the VMware KB articles it names.

## Mitigation layers
| Layer | Performance effect | Notes |
|---|---|---|
| Hardware (newer CPUs) | Little or no impact | Newer CPUs can give a performance gain over older CPUs that require microcode or software mitigations. |
| Microcode | Mitigates some vulnerabilities | Microcode ships with the CPU. It can be updated through BIOS or OS updates. Some ESX versions can update microcode. |
| Software, hypervisor level | Possible impact | Mitigations in ESX. |
| Software, guest OS level | Possible impact | Mitigations inside the guest OS. |

## L1TF (CVE-2018-3646) and the ESX scheduler
- L1TF can leak information between VMs, or between a VM and ESX, when Hyper-Threading is active.
- Sequential-context attack vector:
  - addressed by updates that apply automatically (KB 55806),
  - no significant performance impact.
- Concurrent-context attack vector:
  - the updates can address it, but they do not do so by default,
  - addressing it requires activating the ESX Side-Channel-Aware Scheduler,
  - possible significant performance impact,
  - possible limitations on running certain VMs.

## Side-Channel-Aware Scheduler versions
- SCAv1:
  - first version, released in updates for earlier ESX versions,
  - limits the scheduler to one thread per core.
- SCAv2:
  - released with ESXi 6.7 Update 2,
  - activates multithreading,
  - never schedules threads from different VMs on the same core at the same time,
  - lower performance penalty than SCAv1 in nearly all cases.

## Guest OS mitigations (p. 55)
- Some side-channel mitigations take place inside the guest OS.
- These mitigations address serious security vulnerabilities, but can affect performance.
- Lower the performance impact by choosing recent CPUs that mitigate some vulnerabilities in hardware.

## Tool
- HTAware Mitigation Tool (KB 56931):
  - estimates the performance impact of activating SCAv1,
  - reports potential issues before activation,
  - activates and deactivates SCAv1, SCAv2 and related settings.

## Traps
- "Side-channel mitigation has no performance cost" → some mitigations have significant impact. Hardware mitigations on newer CPUs usually have little or none.
- "Hyper-Threading is safe by default" → with L1TF, the concurrent-context vector is not addressed by default. Hyper-Threading is in use when the risk applies.
