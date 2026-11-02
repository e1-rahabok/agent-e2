---
id: vsphere/cpu/architecture/host-power-management
type: concept
scope: vsphere
resources: [cpu]
objects: [esxi]
related:
  - vsphere/cpu/architecture/hyper-threading
  - vsphere/cpu/architecture/numa
  - vsphere/cpu/architecture/bios-settings
  - vsphere/cpu/resource-management/dpm
source:
  document: Performance Best Practices for VMware vSphere 9.0 (revision 20250731)
  path: ESX CPU Considerations > Host Power Management in ESX (pp. 29-30); Hardware BIOS Settings > Power Management BIOS Settings (pp. 21-22)
corrections: []
review_notes:
  - "Superseded: vSphere 9.1 (revision 20260624) exists. This file was written from the 9.0 document (revision 20250731). Re-check against 9.1 before review."
  - "Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-90-performance-best-practices"
  - "Not read: Host Power Management Policies in the vSphere Resource Management guide (referenced for Custom policy details). Running Network Latency Sensitive Workloads (p. 49) is network, not CPU."
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

## BIOS power management settings (pp. 21-22)
- Set power management in the BIOS to "OS Controlled Mode" or an equivalent setting.
- Effect: ESX controls the CPU power-saving features. This applies even when those features are not used.
- C1E:
  - a hardware-managed state. ESX puts the CPU into C1. The CPU hardware can deepen the state to C1E on its own criteria.
  - Typically reduces power consumption with little or no performance impact.
  - Exception: a few multithreaded workloads highly sensitive to I/O latency (the source names financial platforms, and media and entertainment). C-states including C1E can reduce their performance. Deactivating them in the BIOS can improve performance.
- Deeper C-states (typically C3 and/or C6):
  - managed by software. They give further power savings.
  - For the best performance per watt, activate all C-states in the BIOS.
  - This leaves the choice of use to ESX host power management.
- Turbo Boost or Turbo Core activated: C1E and deep halt states (C3, C6) can sometimes increase performance of lightly threaded workloads, which leave hardware threads idle.
- Results vary between processor vendors and generations.

## Traps
- "Deactivate C-states for better performance everywhere" → the source names only a few latency-sensitive multithreaded workloads that gain from it. Activating all C-states gives the best performance per watt.
- "Balanced always lowers performance" → typically it has little or no effect. On systems with idle CPUs it can raise performance through Turbo Boost.
- "Low Power is a safe default" → Low Power reduces power aggressively, at the risk of reduced performance.
