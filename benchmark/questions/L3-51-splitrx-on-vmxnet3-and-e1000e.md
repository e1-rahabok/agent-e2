# SplitRx on VMXNET3 and E1000E

## Prompt
- An ESX 9.1 host receives one multicast stream from a single source through a physical NIC. Two VMs on the host subscribe to the stream.
- VM 1 has a VMXNET3 adapter. VM 2 has an E1000E adapter.
- One receive queue of the physical NIC is heavily utilized and gets more than 10,000 multicast packets per second.
- The host option Net.NetSplitRxMode is at its default. No ethernetX.emuRxMode parameter is set on either VM.

On which virtual NICs does ESX activate SplitRx mode?

- A. Both, because SplitRx mode is a host-wide feature that applies to every adapter type while Net.NetSplitRxMode is at its default.
- B. Only the VMXNET3 adapter of VM 1, because VMXNET3 is the only adapter type that supports SplitRx mode.
- C. Neither, because SplitRx mode starts only after ethernetX.emuRxMode is set to 1 on the adapter.
- D. Neither, because SplitRx mode applies only to traffic that stays inside the ESX host.
- E. Only the VMXNET3 adapter of VM 1, and only after the host is restarted with Net.NetSplitRxMode set to 1.

## Likely wrong answer
A or C: SplitRx mode is read as a host-wide switch for all adapters, or as a feature that always needs a manual setting.

## Expected key points
- Answer: B.
- ESX activates SplitRx mode automatically for a VMXNET3 adapter, the only adapter type that supports it, when a single queue of the physical NIC is both heavily utilized and gets more than 10,000 broadcast or multicast packets per second. All of this holds for VM 1.
- The default Net.NetSplitRxMode = "1" allows the automatic activation. No per-adapter parameter is needed (C is wrong), and no restart is needed: a change of the host option takes effect immediately (E is wrong).
- The E1000E adapter of VM 2 is not supported (A is wrong).
- Automatic activation covers traffic that comes in over a physical NIC. Traffic that stays inside the host needs manual activation with ethernetX.emuRxMode (D is wrong).

## Notes
- Public source: Performance Best Practices for VMware vSphere 9.1, revision 20260624, "SplitRx Mode" (pages 49-50). https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices (fetched 2026-11-13).
- Why one answer: the document names VMXNET3 as the only supported adapter type and gives the automatic activation condition, the 10,000 packets per second value, the default, and the manual path for internal traffic.
- Debatable risk: none found. The prompt states that the traffic arrives over a physical NIC and that the queue meets both conditions, so "when would it activate" is not in question.

## Metadata
```yaml
id: "0295"
title: SplitRx on VMXNET3 and E1000E
product: [vsphere]
technology: [network, cpu]
task: explain-mechanism
level: 300
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
