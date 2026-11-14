# SplitRx on VMXNET3 and E1000E

## Prompt
- An ESX 9.1 host receives one multicast stream from a single source through a 25 Gb/s physical NIC. One receive queue of the physical NIC is heavily utilized and gets about 25,000 multicast packets per second. Four VMs on the host subscribe to the stream, and every one of them receives it over that physical NIC.
- Net.NetSplitRxMode is at its default on the host. Nothing else changed on the host.
- The four VMs, as they are now:
  - VM 1: VMXNET3 adapter. No ethernetX.emuRxMode parameter in its .vmx file.
  - VM 2: VMXNET3 adapter. ethernet0.emuRxMode = "0" was added two weeks ago, and the VM was restarted afterwards.
  - VM 3: VMXNET3 adapter. ethernet0.emuRxMode = "0" was added 10 minutes ago in Edit Configuration while the VM kept running. The VM has not been restarted and the adapter has not been disconnected.
  - VM 4: E1000E adapter. No ethernetX.emuRxMode parameter.
- The stream has been constant for the past hour.

Which statements are correct?

- A. SplitRx mode is active now on VM 1's adapter.
- B. SplitRx mode is active now on VM 2's adapter.
- C. SplitRx mode is active now on VM 3's adapter.
- D. SplitRx mode is active now on VM 4's adapter.
- E. Setting Net.NetSplitRxMode to "0" on the host takes effect at once, with no host restart.
- F. Restarting the ESX host is the only way to put VM 3's new parameter into effect.

## Likely wrong answer
C left out, because a per-adapter change is assumed to apply at once. Or D: SplitRx is read as a host-wide feature for every adapter type. Or B: the per-adapter parameter is read as ignored while the host default is on.

## Expected key points
- Answer: A, C, E.
- A is true: with Net.NetSplitRxMode at its default "1", ESX activates SplitRx automatically for a VMXNET3 adapter when a single queue of the physical NIC is both heavily utilized and gets more than 10,000 broadcast or multicast packets per second, and the traffic comes in over a physical NIC.
- B is false: ethernetX.emuRxMode = "0" overrides the host-wide setting for that adapter and deactivates SplitRx. The change is in force because the VM was restarted afterwards.
- C is true: the per-adapter parameter takes effect only after the VM is restarted or the vNIC is disconnected and connected again. Until then the adapter keeps the automatic behavior, so SplitRx stays active.
- D is false: VMXNET3 is the only adapter type on which SplitRx is supported, so the E1000E adapter never gets it.
- E is true: a host-wide change of Net.NetSplitRxMode takes effect immediately and needs no host restart.
- F is false: a VM restart, or a disconnect and reconnect of the vNIC, puts the per-adapter parameter into effect; the host need not restart.

## Notes
- Public source: Performance Best Practices for VMware vSphere 9.1, revision 20260624, "SplitRx Mode" (pages 49-50): automatic activation for VMXNET3 only, the 10,000 packets per second condition, the host-wide variable (immediate effect, no restart), the per-NIC variable ethernetX.emuRxMode that overrides the host-wide setting, and "The change will not take effect until the virtual machine has been restarted or the relevant vNIC is disconnected from the virtual machine and connected again." https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices (read 2026-11-13 from the saved PDF).
- Why this key: each VM maps to one sentence of the document: automatic activation (VM 1), override with restart (VM 2), override not yet in force (VM 3), unsupported adapter type (VM 4).
- Debatable risk: the document does not say outright what a not-yet-effective parameter does to the running state; "the change will not take effect until restart" means the earlier state (automatic) stays. The prompt states that the stream has been constant, so the activation condition holds for an hour.
- Options rewritten 2026-11-14 to the option rules (design.md 3.9; project/question-pairing-2026-11-14.md): one option per VM instead of sets of VMs; the restart rule added to the splitrx-mode knowledge file (it decides C and F); the stem's "so the queue meets the conditions on all four VMs" removed (it interpreted the case); E and F added. Key changed from B to A, C, E.
- Rewritten 2026-11-13 to raise difficulty: four adapters with different histories (override, override not yet in force, unsupported type); the answer needs the per-adapter override rules and the restart condition, not only the supported adapter type.

## Metadata
```yaml
id: "0295"
title: SplitRx on VMXNET3 and E1000E
product: [vsphere]
technology: [network, cpu]
task: explain-mechanism
level: 400
answer_type: deterministic
input: [text]
object: [esxi, vm, network]
tool: [none]
knowledge:
  - vsphere/technology/network/configuration/splitrx-mode
knowledge_main: vsphere/technology/network/configuration/splitrx-mode
attachments: []
origin: synthetic
source_path: "Drafted 2026-11-13 for the coverage gap (project/plan.md)"
answer: [A, C, E]
misconception: [B, D]
misconception_type: []
status: draft
```
