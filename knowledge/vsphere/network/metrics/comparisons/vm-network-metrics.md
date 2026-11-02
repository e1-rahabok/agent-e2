# VM network metrics compared

## Set
- A VM is not an OS: far fewer network metrics than Windows or Linux.
- Contention: dropped packets only.
- Traffic type: broadcast and multicast packets. Most traffic should be unicast. Broadcast and multicast can explain drops.
- Utilization: 6 throughput metrics (the book considers them triplicates) and packet counts.
- Each group exists for Transmit (outgoing) and Receive (incoming).

## Instances
- Per vNIC and per VM. Most VMs have 1 vNIC: VM and vNIC values are then identical.
- vNIC instances are named 4000, 4001, ... (first vNIC 4000).
- Example: a vCenter VM receives some broadcast packets, sends none, and has no multicast. Expected.

## Metric details
| Metric | Facts |
|---|---|
| Broadcast packets, Multicast packets | Count in the sampling window, not a rate. Should be low for most VMs. |
| Packets dropped | See `vsphere/network/metrics/virtual-machine/packets-dropped`. |
| Total packets | Includes broadcast and multicast. Excludes dropped. |
| Throughput | KB per second. esxtop uses megabits. Assumed to include broadcast and multicast, exclude dropped. |

## Missing metrics
| Missing | Workaround or note |
|---|---|
| Retransmits | Useful for TCP; does not apply to UDP. |
| Latency | Would help, split internal vs external. CPU contention on the VM can add network latency. Too many hops or firewalls: optimize the path with network insight tools. |
| Packets per second | Packet count / sampling window. 200 packets in 20 s = 10 packets/s. |
| Packet size | Throughput / packet count. Expect about 1,500 bytes. |

## Avoid the non-Total variant
- Where two metrics share a name and one has the prefix Total, use the Total one. The other is averaged over 15 data points and reads 15x lower.

## Traps
- "VM network latency is in vSphere" → no such metric.

## Metadata
```yaml
id: vsphere/network/metrics/comparisons/vm-network-metrics
retriever_guide: metric-meaning
scope: vsphere
technology:
- network
pillar:
- performance
product:
- vsphere
- vcf-operations
object:
- VirtualMachine
metric_class: consumption
internal_derive:
- vsphere/network/concepts/network-observability
same_name: []
same_meaning: []
related:
- vsphere/network/metrics/virtual-machine/packets-dropped
- vsphere/network/metrics/virtual-machine/packets
- vsphere/network/metrics/virtual-machine/throughput
source:
  document: PART 3 - Counters.docx
  path: Network > VM > Overview
corrections: []
review_notes: []
status: draft
```
