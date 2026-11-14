# A powered-on VM with a crashed Windows

## Prompt
- The service desk opens a P1 ticket: "Server down." The availability report counts outages per VM.
- You open [the VM's Summary page](0435/vcenter-vm-summary-tools-not-running.png) and [its web console](0435/vcenter-vm-console-stop-screen.png).

Which statements are correct?

- A. The VM is down: the console shows that Windows has crashed.
- B. A VM stays available while its virtual hardware runs, whatever happens in its Guest OS.
- C. Windows is the layer that is unavailable.
- D. VMware Tools shows as not running because the Guest OS it runs in has stopped.
- E. Record this incident as VM downtime in the availability report.
- F. The applications on this VM are available, because the VM is powered on.
- G. The VM's power state tells whether its Guest OS is available.
- H. vCenter stops collecting the VM's CPU and memory counters while Windows is down.

## Input to supply
- Product and version: vSphere 9.1 (vSphere Client); a test Windows Server VM with VMware Tools installed.
- How to produce it: in Windows, turn off automatic restart after a system failure (System Properties > Advanced > Startup and Recovery > clear "Automatically restart"), then crash the guest, for example with Sysinternals NotMyFault (`notmyfault64.exe /crash`). If vSphere HA VM Monitoring is on for the cluster, exclude the VM so it is not reset while you capture.
- Screen 1: the VM > Summary, with the power state (Powered On) and the VMware Tools status (Not running) visible, a few minutes after the crash. Save as `0435/vcenter-vm-summary-tools-not-running.png`.
- Screen 2: the VM's web console showing the Windows stop screen. Save as `0435/vcenter-vm-console-stop-screen.png`.
- Condition the key depends on: power state Powered On; VMware Tools Not running; the console shows the Windows stop screen.
- Masking: mask every VM, host, datastore and cluster name, the guest host name and any IP address.

## Likely wrong answer
A: the Guest OS crash read as a VM outage, and E, the action that follows from it. Or F, the over-correction.

## Expected key points
- Answer: B, C, D.
- A false: the misconception. It mixes two layers: the Guest OS is down; the VM, the virtual hardware, is powered on.
- B true: a VM is unavailable only when powered off or frozen with its clock paused; if its BIOS runs, it is available, even with no OS running.
- C true: Windows is the layer that failed.
- D true: VMware Tools runs inside the Guest OS; when Windows stops, Tools stops reporting.
- E false: the wrong action. The outage belongs to the Guest OS and the applications, not to the VM.
- F false: the over-correction. The applications run on the Guest OS, which is down.
- G false: Guest OS availability needs checks from inside the OS (the RPC service on Windows); the power state reads the VM only.
- H false: CPU and memory counters of the VM are measured by the VMkernel outside the guest; they keep their data while the guest is down.

## Notes
- Practical half of 0015 (pair: design.md, section 3.9).
- Drafted 2026-11-14 for the question pairing plan (project/question-pairing-2026-11-14.md, item C32). The options hold for any capture that meets the condition above. Counts only after author approval.

## Metadata
```yaml
id: "0435"
title: "A powered-on VM with a crashed Windows"
product: [vsphere, windows]
technology: [system]
task: troubleshoot
level: 300
answer_type: deterministic
input: [screenshot]
object: [vm, guest-os]
tool: [vcenter]
knowledge:
  - vsphere/architecture/vm-vs-guest-os
knowledge_main: vsphere/architecture/vm-vs-guest-os
attachments:
  - 0435/vcenter-vm-summary-tools-not-running.png
  - 0435/vcenter-vm-console-stop-screen.png
origin: synthetic
source_path: "Pairing plan 2026-11-14, item C32"
answer: [B, C, D]
misconception: [A, E]
misconception_type: [layer-confusion]
pair: "0015"
status: awaiting-input
```
