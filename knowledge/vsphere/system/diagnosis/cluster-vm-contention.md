# VMs in a cluster face contention

## Checks, in order
1. Worst VM CPU Ready and worst VM memory contention: depth.
2. % of VMs with CPU Ready and with memory contention: breadth.
3. Breadth high: the cause is likely host or cluster level, not a VM setting.
4. Check imbalance among hosts. Cluster utilization is rarely high (HA and buffer), so look for hot hosts.
5. Check vSAN CPU Ready and ESXi error packets.

## How to read the result
| Finding | Possible cause | Action |
|---|---|---|
| Many VMs affected | VMs that are siblings of a resource pool make pool VMs suffer | Fix the resource pool hierarchy. |
| Many VMs affected | Unbalanced shares: some VMs with large shares | Review shares. |
| Many VMs affected | High ESXi utilization on some hosts | Check imbalance causes: DRS settings, VM-host or VM-VM affinity, resource pools, inconsistent configuration (storage or network not on all hosts). |
| vSAN CPU Ready | Kernel scheduling | Only changeable through ESXi advanced settings. |
| ESXi error packets | NIC | Check vmnic driver and firmware. |

## Traps
- "Few VMs affected means the cluster is fine" → depth matters: one VM can be badly hit.

## Metadata
```yaml
id: vsphere/system/diagnosis/cluster-vm-contention
retriever_guide: what-to-check
scope: vsphere
technology:
- cpu
- memory
- storage
- network
- system
pillar:
- performance
product:
- vsphere
- vcf-operations
object:
- ClusterComputeResource
internal_derive:
- vsphere/system/concepts/cluster-utilization-vs-contention
related:
- vsphere/system/metrics/cluster/cluster-performance
- vsphere/cpu/metrics/cluster/inter-host-imbalance
source:
  document: PART 3 - Counters.docx
  path: Provider Objects > Performance > Cluster Performance (%) > Troubleshooting
corrections: []
review_notes: []
status: draft
```
