# Setting a vNIC speed

## Prompt
- An application owner asks for their VM to be limited to 500 Mbps of network bandwidth.
- The VM has one VMXNET3 adapter. Windows shows its link speed as 10 Gbps, although the host uplinks are 25 GbE.

Can you set the VM's vNIC speed to 500 Mbps to do this? If not, what controls exist, and what does each one limit?

## Likely wrong answer
"Yes: set the adapter speed to 500 Mbps in Windows or in the VM settings, and the VM can send no more than that."

## Expected key points
- No. The link speed a VMXNET3 adapter reports to the guest is a label, not a limit: 10 Gbps by default, whatever the physical uplink. Changing it inside the guest does not cap throughput.
- The adapter moves data as fast as the host CPU, the virtual switch policies and the uplinks allow. VM-to-VM traffic on one host can exceed the reported speed.
- A VMX setting can change the reported speed, but only upward from 10 Gbps, and it limits nothing either.
- Real controls: traffic shaping on the port group (average and peak bandwidth; on a distributed switch for each direction), or a Network I/O Control limit on the VM's network adapter.
- A Network I/O Control limit acts on transmit traffic only, and it applies even when the uplink is idle.

## Notes
- Drafted by Claude 2026-11-05 from the knowledge files listed in `knowledge` (origin: synthetic). Counts only after author approval.
- Revised 2026-11-12. The VMX setting is `ethernetX.linkspeed`, from vSphere 8.0 Update 2, 10,000 to 65,000 Mbps; values outside the range fall back to 10 Gbps. Vendor sources for the reported link speed: Broadcom KB 368812, How to change the vmxnet3 link speed of a VM, https://knowledge.broadcom.com/external/article/368812/how-to-change-the-vmxnet3-link-speed-of.html; Broadcom KB 444078, VMXNET3 guest OS link speed does not enforce bandwidth limits, https://knowledge.broadcom.com/external/article/444078/vmxnet3-guest-os-link-speed-resets-and-d.html.
- The knowledge base says the vNIC takes the speed of the vmnic behind its port group (network-characteristics, Coarse allocation). The KB articles above say VMXNET3 reports 10 Gbps by default. The key follows the vendor articles; reported for a knowledge base fix.

## Metadata
```yaml
id: "0041"
title: "Setting a vNIC speed"
product: [vsphere, windows]
technology: [network]
object: [vm, network]
tool: [vcenter, guest-os-tools]
task: judge-setting
level: 200
answer_type: judged
input: [text]
knowledge:
  - vsphere/technology/network/concepts/network-characteristics
  - vsphere/technology/network/concepts/netioc
  - vsphere/architecture/resource-controls
knowledge_main: vsphere/technology/network/concepts/network-characteristics
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-05"
misconception_type: []
status: draft
```
