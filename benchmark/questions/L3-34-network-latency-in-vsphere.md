# Where is the network latency counter?

## Prompt
- An application owner reports that calls from web-03 to db-05 took twice as long between 14:00 and 14:30 yesterday.
- Both VMs are on the same cluster, different hosts, same distributed port group. Neither VM shows dropped packets in vCenter for that window.
- The owner asks you to open the VM network latency chart in vCenter for both VMs and the hosts in between.

Which statements are correct?

- A. vCenter keeps a network latency counter for each VM's virtual NIC.
- B. Hand the case to the network team, since vSphere holds no evidence that bears on this delay.
- C. For a VM, dropped packets are the only network contention counter that vSphere keeps.
- D. With no dropped packets on either VM in that window, the network and the hosts added no delay to these calls.
- E. CPU contention (Ready, Co-stop) on either VM adds delay without a drop: a packet waits until the vCPU runs.
- F. Virtual interrupt coalescing on the adapter batches packets and can add a few hundred microseconds to a few milliseconds.
- G. A VM in the path, such as an NSX Edge or a security agent VM, can slow every flow through it with no drop on the two VMs.
- H. Latency is measured where traffic ends: in the application, in the guest, or with the network team's flow and packet tools.
- I. The distributed port group has its own performance chart in vCenter, with latency for each port.
- J. Both VMs sit on one distributed port group, so their traffic never leaves the hosts and the physical network is ruled out.
- K. Next, compare Ready and Co-stop of web-03, db-05 and any VM in the path for 14:00-14:30.

## Likely wrong answer
- A: "Open the VM's network latency counter in the vSphere Client."
- D: "No dropped packets, so the network added no delay."

## Expected key points
- Answer: C, E, F, G, H, K.
- A is false: vSphere has no network latency metric for a VM.
- B is false: vSphere has no latency counter, but CPU contention on the VMs and on any VM in the path is vSphere evidence for the same window.
- C is true: for a VM, dropped packets are the only sign of network contention.
- D is false: no drops does not mean no delay; several vSphere conditions add delay without dropping a packet.
- E is true: CPU contention on the VM can add network latency; the packet is processed only when the vCPU runs.
- F is true: coalescing is on by default for all virtual NICs and can add from a few hundred microseconds to a few milliseconds.
- G is true: a VM in the data path with its own CPU or memory contention looks like a network problem to the business VMs (NSX Edge, security agent VM).
- H is true: latency is read in the application, in the guest (round-trip times, TCP statistics), or with flow records and packet capture.
- I is false: the distributed port group has no vCenter performance counters, and the vSphere Client shows no performance charts for switches or port groups.
- J is false: only VM-to-VM traffic on the same host stays inside the host; these VMs are on different hosts, so their traffic crosses the uplinks and the physical network.
- K is true: CPU contention of the two VMs and of any VM in the path is the vSphere evidence to check for that window.

## Notes
- Drafted by Claude 2026-11-12 (origin: synthetic). Counts only after author approval.
- TCP retransmits seen inside the guest belong to a Guest OS question of the set; this one tests what vSphere measures and what it can add.
- Converted from judged to multiple choice (Q199 F, 2026-11-14).
- Options rewritten 2026-11-14 to the theory option rules (design.md 3.9; project/question-pairing-2026-11-14.md): the negation pair A/B resolved (old B, "no latency, jitter or retransmit counter", dropped; the retransmit fact stays in 0268 only); B is now the over-correction and wrong action. Key changed from B, C, E, F, G, H, K to C, E, F, G, H, K.

## Metadata
```yaml
id: "0214"
title: "Where is the network latency counter?"
product: [vsphere]
technology: [network, cpu]
object: [vm, network]
tool: [vcenter]
task: explain-mechanism
level: 300
answer_type: deterministic
answer: [C, E, F, G, H, K]
misconception: [A, D]
input: [text]
knowledge:
  - vsphere/technology/network/concepts/network-characteristics
  - vsphere/technology/network/metrics/vm-network-metrics
  - vsphere/technology/network/configuration/rss-and-interrupt-coalescing
  - vsphere/technology/network/concepts/network-observability
knowledge_main: vsphere/technology/network/metrics/vm-network-metrics
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12"
misconception_type: [tool-confusion]
status: draft
```
