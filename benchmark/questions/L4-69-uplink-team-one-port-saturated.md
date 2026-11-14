# One uplink saturated, three idle

## Prompt
- ESXi 9.1 host esx-14 has four 10 GbE uplinks, vmnic0 to vmnic3, in one team on a distributed switch.
- Port group pg-backup uses load balancing "Route based on originating virtual port". All four uplinks are active.
- A backup proxy VM, bkp-01, has one VMXNET3 adapter. Every night it streams to a single backup target at one IP address.
- The backup now runs over its window. Its throughput never goes above about 9.4 Gb/s.
- esxtop network panel during the backup, columns selected:

```text
   PORT-ID USED-BY              TEAM-PNIC  MbTX/s   MbRX/s
  67108866 vmnic0               -         9512.40   210.33
  67108868 vmnic1               -          402.17   388.90
  67108870 vmnic2               -          366.02   351.48
  67108872 vmnic3               -          298.55   305.12
  67108890 2471102:bkp-01.eth0  vmnic0    9398.71   140.62
```

- The team's capacity report says the uplink team averages 26% transmit utilization, so the network has room.

Which statements are correct?

- A. With this policy a virtual port uses one uplink, so bkp-01 cannot exceed one 10 GbE link.
- B. Adding two more 10 GbE uplinks to this team raises the throughput bkp-01 can reach.
- C. Physical NIC load teaming can move the busy port, but the port still uses one uplink.
- D. IP hash with a static EtherChannel spreads this backup stream over all four uplinks.
- E. A second adapter on bkp-01, with streams over both, can put traffic on a second uplink.
- F. The other three uplinks carry little traffic because their links are down at the switch.

## Likely wrong answer
B: "more uplinks, more bandwidth for the VM". Or the capacity report's view: 26% average utilization means the network has room.

## Expected key points
- Answer: A, C, E.
- A: route based on originating virtual port maps each virtual port to one uplink. One virtual NIC is pinned to one vmnic (here vmnic0), so its ceiling is one 10 GbE link, about 9.4 Gb/s of payload.
- B is wrong: new uplinks add capacity for other ports, not for a port already pinned to one uplink.
- C: physical NIC load (load-based teaming) checks the uplinks every 30 seconds and moves a port when an uplink stays above 75%. It balances ports between uplinks; it does not split one port's traffic.
- D is wrong: IP hash chooses the uplink from the source and destination IP. One VM talking to one target IP hashes to one uplink, so this backup would still use one link. IP hash also needs a static EtherChannel on the physical switch.
- E: each adapter has its own virtual port, which can map to a different uplink, so two streams over two adapters can use two links.
- F is wrong: the uplinks carry about 300-400 Mb/s each; they are up and lightly used.
- The 26% team average hides one saturated uplink: read each uplink, not the team average.

## Notes
- Outside the knowledge base: the knowledge base has no file on NIC teaming policies (only a line on load-based teaming in noisy-neighbour). Keyed from the vendor documents below.
- vSphere Networking, Route Based on Originating Virtual Port and Route Based on IP Hash: https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/vsphere-networking/networking-policies/teaming-and-failover-policy/load-balancing-algorithms-for-virtual-switches/route-based-on-ip-hash.html
- Route Based on Physical NIC Load (30 seconds, 75%): https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/7-0/vsphere-networking/networking-policies/teaming-and-failover-policy/load-balancing-algorithms-for-virtual-switches/route-based-on-physical-nic-load.html
- Broadcom KB 321396, Understanding IP Hash load balancing (a VM talking to several IP addresses can use several uplinks): https://knowledge.broadcom.com/external/article/321396/understanding-ip-hash-load-balancing.html
- Broadcom KB 452506, Expected behavior for Load-Based Teaming port reassignment: https://knowledge.broadcom.com/external/article/452506/expected-behavior-for-loadbased-teaming.html
- vSphere 9.0 networking, Load Balancing Algorithms Available for Virtual Switches (same behaviour as the 8.0 pages: the default policy maps a port to one uplink; one VM is capped at one uplink unless it has several adapters): https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0/vsphere-networking/networking-policies/teaming-and-failover-policy/load-balancing-algorithms-for-virtual-switches.html. No separate 9.1 page was found; the 8.0 and 9.0 pages describe unchanged behaviour.
- Drafted by Claude 2026-11-12 (origin: synthetic). Counts only after author approval.

## Metadata
```yaml
id: "0210"
title: "One uplink saturated, three idle"
product: [vsphere]
technology: [network]
object: [vm, esxi, network]
tool: [esxtop]
task: troubleshoot
level: 400
answer_type: deterministic
input: [text]
knowledge:
  - vsphere/tools/esxtop/network
  - sp5-framework/performance/noisy-neighbour
knowledge_main: vsphere/tools/esxtop/network
attachments: []
origin: synthetic
source_path: "Drafted by Claude 2026-11-12, outside the knowledge base"
answer: [A, C, E]
misconception: [B, D]
misconception_type: [average-hides-worst]
status: draft
```
