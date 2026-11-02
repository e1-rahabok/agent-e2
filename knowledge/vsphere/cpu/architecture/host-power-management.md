---
id: vsphere/cpu/architecture/host-power-management
type: concept
scope: vsphere
resources: [cpu]
objects: [esxi]
related:
  - vsphere/cpu/architecture/hyper-threading
  - vsphere/cpu/architecture/numa
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: ESX CPU Considerations > Host Power Management in ESX (pp. 29-30)
corrections: []
review_notes:
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
  - "Not read: Hardware BIOS Settings (p. 21), Distributed Power Management (p. 82), Host Power Management Policies in the vSphere Resource Management guide, Running Network Latency Sensitive Workloads (p. 49)."
status: draft
---

# Host power management (ESX)

## Purpose
- Reduces the power consumption of powered-on ESX hosts.
- Different from Distributed Power Management (DPM). DPM powers off hosts that are not in use. See the source, p. 82.
- Host power management and DPM can be used together for best power saving.

## Policies
| Policy | Behaviour | Performance effect |
|---|---|---|
| High Performance | No power saving features | Maximum performance when all or most cores are fully loaded. Less optimal when many cores are unused or lightly used. The effect is more pronounced on recent CPUs. |
| Balanced (default) | Reduces power and keeps usage flexibility | Typically little or no performance reduction. When some CPUs are idle part of the time, active CPUs can enter faster Turbo Boost states than High Performance allows, which can increase performance. |
| Low Power | Reduces power aggressively | Risk of reduced performance |
| Custom | Starts as Balanced. Individual parameters can be changed. | Depends on the parameters chosen. |

- Custom parameters: see "Configure Custom Policy Parameters for the ESX Host Power Management" in the vSphere Resource Management guide.

## Latency-sensitive workloads
- The Balanced policy can slightly reduce performance of latency-sensitive workloads.
- In those cases, High Performance gives the full hardware performance.

## Verify technology availability
1. In the vSphere Client, select the host.
2. Select the Configure tab.
3. Under Hardware, select Power Management.
4. The Technology field lists the available technologies: ACPI P-states, ACPI C-states, or both.
- Both technologies available: best power savings.
- Missing technologies do not cause problems. The system can use more power than necessary.

## Traps
- "Balanced always lowers performance" → typically it has little or no effect. On systems with idle CPUs it can raise performance through Turbo Boost.
- "Low Power is a safe default" → Low Power reduces power aggressively, at the risk of reduced performance.
