---
id: vsphere/cpu/configuration/host-power-management
retriever_guide: what-to-set
scope: vsphere
technology:
- cpu
pillar:
- performance
- value
product:
- vsphere
object:
- HostSystem
internal_derive: []
related:
- vsphere/cpu/concepts/hyper-threading
- vsphere/cpu/concepts/numa
- vsphere/system/configuration/bios-settings
- vsphere/cluster-resource-management/concepts/dpm
- vsphere/cpu/concepts/power-states
- vsphere/cpu/concepts/cpu-frequency
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: ESX CPU Considerations > Host Power Management in ESX (pp. 31-32); Power Management BIOS Settings (pp. 22-23); Intel Hardware P-States (p. 12)
corrections: []
review_notes:
- Checked against 9.1 (revision 20260624). Pages 31-32 read. Verification path changed to Overview tab. ACPI CPPC and Intel HWP added (pp. 12, 32).
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- 'Not read: Host Power Management Policies in the vSphere Resource Management guide (referenced for Custom policy details). Running Network Latency Sensitive Workloads (p. 49) is network, not CPU.'
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

## Verify technology availability (9.1 p. 32)
1. In the vSphere Client, select the host.
2. Select the Configure tab.
3. Under Hardware, select Overview. Scroll to the bottom.
4. Look for Power Management. The Technology field lists the available technologies.
- ACPI C-states: ESX manages deeper C-states (C2 or below). If not listed, ESX does not use deeper C-states.
- ACPI P-states: ESX uses software-based P-state management to control active frequencies.
- ACPI CPPC: ESX uses Intel hardware-based P-state management (HWP), configured per the power policy.
- Neither ACPI P-states nor ACPI CPPC listed: the firmware has not given P-state control to ESX. The BIOS then controls P-states.
- For the best power savings: one P-state technology (ACPI P-states or ACPI CPPC) plus ACPI C-states.
- Missing technologies do not cause problems. The system can use more power than necessary.

## Intel Hardware P-States (HWP) (9.1 p. 12)
- ESX 9.0 and later support HWP on fourth-generation and later Intel Xeon Scalable processors, starting with Sapphire Rapids. This is also called ACPI CPPC.
- Before ESX 9.0, ESX managed P-states directly. ESX 9.0 and later still manage P-states directly on Intel Xeon processors before fourth generation, and on AMD processors.
- ESX attempts to enable HWP at boot. ESX gives hints to the processor based on the power policy. The CPU microcode tracks load and sets frequencies at core and package level.
- Conditions: HWP must not be disabled in the BIOS, and the BIOS must allow frequency control by the OS. When these are met, ESX 9.0 and later enable HWP by default.

## BIOS power management settings (pp. 21-22)
- Set power management in the BIOS to "OS Controlled Mode", "OS Controlled EPB", or an equivalent setting (9.1 p. 22).
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

- Intel Granite Rapids C-state recommendations by workload: see `vsphere/system/configuration/bios-settings`.

## Traps
- "Deactivate C-states for better performance everywhere" → the source names only a few latency-sensitive multithreaded workloads that gain from it. Activating all C-states gives the best performance per watt.
- "Balanced always lowers performance" → typically it has little or no effect. On systems with idle CPUs it can raise performance through Turbo Boost.
- "Low Power is a safe default" → Low Power reduces power aggressively, at the risk of reduced performance.
