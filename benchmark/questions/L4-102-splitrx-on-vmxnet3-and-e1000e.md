# SplitRx on VMXNET3 and E1000E

## Prompt
- An ESX 9.1 host receives one multicast stream from a single source through a 25 Gb/s physical NIC. One receive queue of the physical NIC is heavily utilized and gets about 25,000 multicast packets per second. Four VMs on the host subscribe to the stream, and every one of them receives it over that physical NIC.
- Net.NetSplitRxMode is at its default on the host. Nothing else changed on the host.
- The four VMs, as they are now:
  - VM 1: VMXNET3 adapter. No ethernetX.emuRxMode parameter in its .vmx file.
  - VM 2: VMXNET3 adapter. ethernet0.emuRxMode = "0" was added two weeks ago, and the VM was restarted afterwards.
  - VM 3: VMXNET3 adapter. ethernet0.emuRxMode = "0" was added 10 minutes ago in Edit Configuration while the VM kept running. The VM has not been restarted and the adapter has not been disconnected.
  - VM 4: E1000E adapter. No ethernetX.emuRxMode parameter.
- The stream has been constant for an hour, so the queue meets the packet rate and utilization conditions on all four VMs.

On which virtual NICs is SplitRx mode active now?

- A. VM 1 only.
- B. VM 1 and VM 3.
- C. VM 1, VM 3 and VM 4.
- D. All four VMs.
- E. VM 1, VM 2 and VM 3.

## Likely wrong answer
A, because a per-adapter change is assumed to apply at once. Or C and D: SplitRx is read as a host-wide feature for every adapter type. Or E: the per-adapter parameter is read as ignored while the host default is on.

## Expected key points
- Answer: B.
- With Net.NetSplitRxMode at its default "1", ESX activates SplitRx automatically for a VMXNET3 adapter when a single queue of the physical NIC is both heavily utilized and gets more than 10,000 broadcast or multicast packets per second, and the traffic comes in over a physical NIC. This holds for VM 1, VM 2 and VM 3.
- VM 2: ethernetX.emuRxMode = "0" overrides the host-wide setting for that adapter and deactivates SplitRx. The change is in force because the VM was restarted afterwards. E is wrong.
- VM 3: the per-adapter parameter takes effect only after the VM is restarted or the vNIC is disconnected and connected again. Until then the adapter still follows the automatic behavior, so SplitRx stays active. A is wrong.
- VM 4: VMXNET3 is the only adapter type on which SplitRx is supported, so the E1000E adapter never gets it. C and D are wrong.
- Contrast: a host-wide change of Net.NetSplitRxMode takes effect at once and needs no host restart, but a per-adapter change does not.

## Notes
- Public source: Performance Best Practices for VMware vSphere 9.1, revision 20260624, "SplitRx Mode" (pages 49-50): automatic activation for VMXNET3 only, the 10,000 packets per second condition, the host-wide variable (immediate effect, no restart), the per-NIC variable ethernetX.emuRxMode that overrides the host-wide setting, and "The change will not take effect until the virtual machine has been restarted or the relevant vNIC is disconnected from the virtual machine and connected again." https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices (read 2026-11-13 from the saved PDF).
- Why one answer: each VM maps to one sentence of the document: automatic activation (VM 1), override with restart (VM 2), override not yet in force (VM 3), unsupported adapter type (VM 4).
- Debatable risk: the document does not say outright what a not-yet-effective parameter does to the running state; "the change will not take effect until restart" means the earlier state (automatic) stays. The prompt states that the stream has been constant, so the activation condition holds for an hour.
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
answer: [B]
misconception: [A, C]
misconception_type: []
status: draft
```
