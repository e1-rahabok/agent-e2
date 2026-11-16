# A powered-on VM with a crashed Windows

## Prompt
- The service desk opens a P1 ticket: "Server down." The availability report counts outages per VM.
- You open [the VM's Summary page](0435/vcenter-vm-summary-tools-not-running.png) and [its web console](0435/vcenter-vm-console-stop-screen.png).

Which statements are correct?

- A. The P1 ticket is right: the console proves the VM is down.
- B. The Summary page shows the VM powered on.
- C. The Summary page shows VMware Tools running.
- D. VMware Tools shows as not running because the Guest OS it runs in has stopped.
- E. Close the P1 as a VM outage in the availability report.
- F. The users' applications are still reachable, since the VM is on.
- G. The power state tells whether the Guest OS is available.
- H. vCenter stops collecting the VM's CPU and memory counters while Windows is down.
- I. The console shows that the Windows layer has stopped.

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
- Answer: B, D, I.
- A false: the misconception. It mixes two layers: the Guest OS is down; the VM, the virtual hardware, is powered on and so available.
- B true: the Summary page reads Powered On.
- C false: the Summary page reads VMware Tools Not running.
- D true: VMware Tools runs inside the Guest OS; when Windows stops, Tools stops reporting.
- E false: the wrong action. The outage belongs to the Guest OS and the applications, not to the VM.
- F false: the over-correction. The applications run on the Guest OS, which is down.
- G false: Guest OS availability needs checks from inside the OS (the RPC service on Windows); the power state reads the VM only.
- H false: CPU and memory counters of the VM are measured by the VMkernel outside the guest; they keep their data while the guest is down.
- I true: the console shows the Windows stop screen: the Guest OS layer has failed.

## Notes
- Deferred 2026-11-15: availability is not in release 1.0 (author, exports review 2026-11-15, section 9).
- Review 2026-11-15: options reworded away from the theory half 0015; screen readings added (B true, C false, I true). Key changed from B, C, D to B, D, I.
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
answer: [B, D, I]
misconception: [A, E]
misconception_type: [layer-confusion]
pair: "0015"
status: deferred
```
