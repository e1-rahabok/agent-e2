# NIC teaming

## Purpose
- A NIC team connects one virtual switch to two or more physical NICs (uplinks): more bandwidth for the switch as a whole, and failover.
- Set per standard switch or standard port group, and per distributed port group or distributed port. A port group setting overrides the switch; a distributed port overrides its port group.
- All uplinks of a team sit in one Layer 2 broadcast domain on the physical side.

## Transmit only, one uplink per port
- The virtual switch balances transmit traffic only. Receive traffic arrives on the port the physical switch picks: the physical switch's own policy decides it.
- Every algorithm except IP hash maps a whole vNIC (or VMkernel port) to one uplink. One vNIC never gets more than one uplink's speed. A VM gets more than one uplink only through more vNICs, or through IP hash with many destinations.
- A team of four 10 GbE uplinks is not one 40 Gb/s pipe. It is four 10 Gb/s pipes, each serving the ports mapped to it.

## Load balancing algorithms
| Algorithm | Unit mapped to an uplink | Aware of uplink load | Physical switch change | Notes |
|---|---|---|---|---|
| Route based on originating virtual port (default, standard and distributed switch) | Virtual port ID | No | None | Computed once per port: when the VM powers on or arrives by vMotion, or when uplinks are added or removed. A port that moves to another host can land on another uplink. |
| Route based on source MAC hash | Source MAC address | No | None | The MAC is static, so power cycles keep the uplink. More CPU than the virtual port method. |
| Route based on IP hash | Source and destination IP of each packet (last octets, XOR, modulo the uplink count) | No | Static EtherChannel (802.3ad static) on one switch or a stack | The only standard switch method that spreads one vNIC across uplinks, and only across different IP pairs. Highest CPU cost. |
| Route based on physical NIC load (Load Based Teaming, distributed switch only) | Virtual port ID, moved when an uplink is busy | Yes | None | Checks every 30 seconds; an uplink above 75% usage has its busiest port moved to another uplink. Failback is not supported with it. |
| Use explicit failover order | First healthy uplink in the Active list | No | None | No balancing: the first active uplink carries everything; Standby takes over only on failure. |
| LACP link aggregation group (distributed switch) | LACP hash of the LAG | No | Dynamic LACP port channel | Teams the LAG ports; one LAG per port group handles its traffic. |

## IP hash in detail
- One source-destination pair always hashes to the same uplink. One application server talking to one database server uses one uplink, whatever the team size.
- Requirements: a static EtherChannel with as many ports as uplinks; every uplink Active (Standby and Unused empty); failure detection Link status only. Mixing IP hash with no EtherChannel, or the reverse, disrupts the network: the physical switch sees one MAC on several ports and keeps rewriting its address table.
- Standard switches support only static EtherChannel; dynamic LACP needs a distributed switch LAG.

## Load Based Teaming in detail
- It moves ports, not packets: the moved port then sends on its new uplink until the next move. A single vNIC still cannot exceed one uplink.
- It reacts to sustained load (30-second checks against 75%), not to a burst within those 30 seconds.
- It moves the port with the highest IO, VMkernel ports included.
- With NetIOC, shares and reservations are applied per physical NIC: a move changes which traffic competes on each uplink ([`vsphere/technology/network/concepts/netioc`](netioc.md)).

## Failure detection, failback, notify switches
- Link status only: sees a dead cable, a dead port, a powered-off switch. It does not see a port blocked by spanning tree, a wrong VLAN, or a broken link further upstream.
- Beacon probing: each uplink sends a broadcast beacon every second and listens for the others. It finds failures that keep the link up. With two uplinks it cannot tell which one failed and sends on both; three or more are needed (n-2 failures before the result is ambiguous). Not with IP hash.
- Failback (on by default): a returning uplink takes its Active slot back. A flapping first uplink makes traffic move back and forth; the physical port may drop traffic for about 30 seconds while spanning tree converges, unless PortFast (or the vendor's equivalent) is set.
- Notify switches: on a failover or a vMotion, the virtual switch sends frames so the physical switches update their address tables at once.

## LACP limits (distributed switch)
- Not with software iSCSI port binding (iSCSI multipathing over a LAG without port binding is supported).
- The teaming and failover health check does not run on LAG ports: LACP checks them.
- Not in host profiles; not with the ESXi dump collector; LACP PDUs are not mirrored by port mirroring.
- Up to 64 LAGs per distributed switch and 32 per host; the usable number of ports per LAG is set by the physical switch.

## Reading the team
- esxtop network panel: TEAM-PNIC on a VM or VMkernel row is the uplink that port uses now ([`vsphere/tools/esxtop/network`](../../../tools/esxtop/network.md)). Sum MbTX/s of the ports on each vmnic to see which ports load it.
- One uplink near line rate while the others idle, with one large flow on it: the mapping, not the team size, caps the flow. The fix is more vNICs, more flows, LBT (it moves the other ports away, not the big flow), or a faster uplink.
- The team average hides a saturated uplink: four uplinks at 95%, 4%, 4% and 3% average 26%. Read each vmnic.
- Receive drops on a vNIC are not a teaming problem: the vSwitch does not balance receive ([`vsphere/technology/network/vnic-rx-drops`](../vnic-rx-drops.md)).

## Misconceptions
- "Four 10 GbE uplinks in a team give a VM 40 Gb/s" → each vNIC maps to one uplink; only IP hash spreads one vNIC, and only across different IP pairs.
- "Load Based Teaming splits one large flow over the uplinks" → it moves whole ports every 30 seconds; a flow stays on one uplink.
- "The team balances incoming traffic too" → the virtual switch balances transmit only; the physical switch decides receive.
- "IP hash spreads a backup to one target over all uplinks" → one source-destination pair always hashes to one uplink.
- "Beacon probing works with two uplinks" → with two it cannot tell which one failed; use three or more.
- "The team averages 26%, so the network has room" → one uplink can be saturated while the average is low.

## Metadata
```yaml
id: vsphere/technology/network/concepts/nic-teaming
retriever_guide: how-it-works
scope: vsphere
technology:
- network
pillar:
- performance
- availability
product:
- vsphere
object:
- HostSystem
- VirtualMachine
internal_derive: []
related:
- vsphere/technology/network/concepts/netioc
- vsphere/tools/esxtop/network
- vsphere/technology/network/configuration/network-configuration-review
- vsphere/technology/network/vnic-rx-drops
- vsphere/technology/network/concepts/network-characteristics
source:
  document: VMware vSphere 9.1 documentation (PDF, project/sources/vmware-vsphere-9-1.pdf)
  path: vSphere Networking > What is Teaming and Failover Policy; Load Balancing Algorithms Available for Virtual Switches; LACP Support on a vSphere Distributed Switch; Limitations of the LACP Support (pp. 1142-1162)
corrections: []
review_notes:
- "To check: Section 'Load balancing algorithms', source MAC hash: the 9.1 documentation says the switch calculates an uplink for every packet, yet the uplink is fixed by the static MAC; read as one uplink per vNIC MAC."
- "To check: Section 'Load balancing algorithms', LACP: the LAG hash options (source and destination IP, TCP/UDP port, VLAN, MAC) and the LACP timeout values are not written; vSphere 9.1 documentation, Change the load balancing mode of the LAG."
status: draft
```
