# Side-channel vulnerabilities and the ESX scheduler

## Vulnerability classes
- Side-channel vulnerabilities include Spectre, Meltdown, Foreshadow, L1TF, and others.
- Some mitigations have a significant performance impact.
- Performance Best Practices for vSphere 9.1 and the vSphere 9.1 documentation have no side-channel section; Performance Best Practices for vSphere 9.0 had one. The current guidance for the ESX scheduler is Broadcom KB 317621 (legacy 55806), which covers ESXi 5.5 to 9.x.
- vSphere 9.1 cluster configuration has an ESX advanced setting to allow warnings about unmitigated hyperthreading vulnerabilities (vSphere 9.1 documentation, p. 856).

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
  - addressed by updates that apply automatically (Broadcom KB 317621, legacy 55806),
  - no significant performance impact.
- Concurrent-context attack vector:
  - the updates can address it, but they do not do so by default,
  - addressing it requires activating the ESX Side-Channel-Aware Scheduler, which is not enabled by default in any release the KB covers, 9.x included,
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

## Configuration
- `VMkernel.Boot.hyperthreadingMitigation`: default FALSE. TRUE enables the Side-Channel-Aware Scheduler after a reboot (Broadcom KB 317621).
- `VMkernel.Boot.hyperthreadingMitigationIntraVM`: default TRUE, which gives SCAv1 when the scheduler is enabled. FALSE gives SCAv2, from ESXi 6.7 Update 2.

## Guest OS mitigations
- Some side-channel mitigations take place inside the guest OS.
- These mitigations address serious security vulnerabilities, but can affect performance.
- Lower the performance impact by choosing recent CPUs that mitigate some vulnerabilities in hardware (Performance Best Practices for vSphere 9.0, p. 55).

## Tool
- HTAware Mitigation Tool (KB 56931):
  - estimates the performance impact of activating SCAv1,
  - reports potential issues before activation,
  - activates and deactivates SCAv1, SCAv2 and related settings.

## Misconceptions
- "Side-channel mitigation has no performance cost" → some mitigations have significant impact. Hardware mitigations on newer CPUs usually have little or none.
- "Hyper-Threading is safe by default" → with L1TF, the concurrent-context vector is not addressed by default: the Side-Channel-Aware Scheduler is off until `VMkernel.Boot.hyperthreadingMitigation` is set to TRUE (Broadcom KB 317621).

## Metadata
```yaml
id: vsphere/technology/cpu/configuration/side-channel-scheduling
retriever_guide: what-to-set
scope: vsphere
technology:
- cpu
pillar:
- security
- performance
product:
- vsphere
object:
- HostSystem
- VirtualMachine
internal_derive: []
related:
- vsphere/technology/cpu/concepts/hyper-threading
- vsphere/technology/cpu/concepts/hardware-assisted-virtualization
source:
  document: Broadcom KB 317621 (legacy 55806); Performance Best Practices for VMware vSphere 9.0 (revision 20250731); VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number)
  path: 'KB 317621 (VMware response to L1 Terminal Fault - VMM, CVE-2018-3646), Environment and Resolution. Performance Best Practices 9.0 (no such section in 9.1, revision 20260624): CPU Hardware Considerations > Side-Channel Vulnerabilities (pp. 11-12); ESX CPU Considerations > Side-Channel Vulnerability Mitigation in ESX (pp. 25-26); Guest OS CPU Considerations (p. 55). vSphere 9.1, cluster quickstart, ESX Advanced Settings (p. 856)'
corrections: []
review_notes:
- 'To check: Sections ''Mitigation layers'', ''Guest OS mitigations'' and ''Tool'': from Performance Best Practices for vSphere 9.0 (pp. 11-12, 25-26, 55), with no 9.1 counterpart; check the HTAware Mitigation Tool for 9.x (Broadcom KB 56931, legacy id) and KB 52245, 54951, 55636 (knowledge.broadcom.com).'
status: draft
```
