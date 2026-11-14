# vSphere cluster: operations complexity

## Cluster as one computer
- Operationally a cluster is the smallest logical building block: one large, complex machine.
- Its basic CPU, memory, disk and network counters are the sum of its hosts.
- Cluster-level features add complexity beyond the sum of hosts.

## Feature impact
| Feature | Area | Impact |
|---|---|---|
| HA | Capacity | HA options complicate usable capacity. |
| HA | Availability | Two metrics: actual and operational availability. After an HA event, verify VM availability and application dependencies; keep boot order current. Report and investigate with log analysis. |
| HA | Configuration | Hosts should have identical hardware and software. Clusters should be configured consistently. |
| HA | Inventory | Actual must match plan: amount, movement, status. |
| DRS | Performance | Rising vMotion stun time hints at host performance. vMotion can affect latency-sensitive applications; measure the vMotion rate against expectation. |
| DRS | Configuration | Settings such as automation level must match the standard. VM-level exceptions get buried in large environments. |
| Affinity | Configuration | Affinity and anti-affinity rules must match plan; easily overlooked across hundreds of clusters. |
| Resource pool | Capacity, performance, configuration | Shares, limits and reservations at pool level must be compatible with the child VMs. VMs must not be siblings of resource pools. Cascading pools complicate. |
| DPM | Capacity | Changes total capacity. |
| DPM | Performance | Considers ESXi utilization only, not VM contention. |
| Stretched cluster | Configuration | VMs should access local-site storage. |
| Stretched cluster | Capacity | Sites may be intentionally unbalanced (primary and DR). |
| Stretched cluster | Performance | Horseshoe traffic between VMs on the same site; ping-pong traffic between VMs on different sites. |
| Stretched cluster | Availability | Test site failover at least once a year. |
| vSAN | All | Affects Day 0, 1 and 2. Network and storage counters become mandatory. |

## Base metrics in vSphere Client
- 4 groups. Cluster Services has 3 metrics.

## Imbalance
- Imbalance explains contention while total utilization is below 100%.

| Type | Facts |
|---|---|
| Utilization, inter-host | See [`vsphere/technology/cpu/metrics/cluster/inter-host-imbalance`](../../../technology/cpu/metrics/cluster/inter-host-imbalance.md). |
| Utilization, intra-host | Report at cluster level as the highest among hosts. |
| Overcommit | Running VM vCPU : ESXi usable threads differs between hosts. High overcommit is fine at low utilization. CPU is riskier than memory: more volatile. |
| Monster VM | Concentration of monster VMs on one host raises contention risk. A monster VM has more than 50% of the host's physical cores (not threads), or more than 40% of its DRAM or 256 GB, whichever is smaller. Two such VMs rarely get runtime at once, since vSAN, NSX and VMkernel also demand CPU time. Definition: [`vsphere/object-types/cluster/models/cluster-risk`](../models/cluster-risk.md), section Monster VM. |

## Misconceptions
- "Cluster utilization = average of hosts tells the story" → imbalance hides behind the average.

## Metadata
```yaml
id: vsphere/object-types/cluster/concepts/cluster-operations
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
- memory
- storage
- network
- system
pillar:
- availability
- performance
- capacity
product:
- vsphere
- vsan
object:
- ClusterComputeResource
internal_derive: []
related:
- vsphere/technology/cpu/metrics/cluster/inter-host-imbalance
- vsphere/object-types/cluster/metrics/vm-operations
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: Provider Objects > Overview > vSphere Cluster; Imbalance
corrections:
- 'Monster VM row: the source document said above 45% of the host''s threads. Superseded by the adapter definition.'
review_notes: []
status: draft
```
