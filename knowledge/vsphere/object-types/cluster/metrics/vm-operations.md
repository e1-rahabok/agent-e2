# Cluster VM operations event counts

## Meaning
- Counts of VM events in the cluster. Cumulative since the cluster was created.
- VCF Operations converts them to rates and rolls them up to Datacenter, vCenter and vSphere World.

## Counters
| Category | Metric | Notes (book) |
|---|---|---|
| Change of state | VM guest reboot count | Reboot only; the VM is not powered off. |
| Change of state | VM guest shutdown count | Believed to also trigger VM power off. |
| Change of state | VM standby guest count | Guessed to also power off the VM. |
| Change of state | VM power off count | Believed to be a direct, abrupt power off, not a guest shutdown. |
| Change of state | VM power on count | - |
| Change of state | VM reset count | Power cycle: the VM is briefly powered off. |
| Change of state | VM suspend count | Deeper than guest standby. |
| Change of inventory | VM create count | All creations: template, direct, clone. |
| Change of inventory | VM clone count | Clones only. |
| Change of inventory | VM template deploy count | Template deployments only. |
| Change of inventory | VM reconfigure count | Log analysis shows the actual changes. |
| Change of inventory | VM register count, VM unregister count | Unregistered VM files can remain on the datastore. |
| Change of inventory | VM delete count | All deletions, API or UI. |
| Change of location | vMotion count | Host change only. |
| Change of location | Storage vMotion count | Datastore change only. |
| Change of location | VM host and datastore change count | Both in one event. |
| Change of location | VM datastore change count, VM host change count | Powered-off VMs. |

## Use
- Compare dynamics with expectations. In production these numbers should be low.
- Shutdowns should match change requests and happen in the maintenance window. Exceptions: for example, scheduled VDI reboots.

## Traps
- "Counts are per interval" → raw counters are cumulative.

## Metadata
```yaml
id: vsphere/object-types/cluster/metrics/vm-operations
retriever_guide: metric-meaning
scope: vsphere
technology:
- system
pillar:
- availability
- value
product:
- vsphere
- vcf-operations
object:
- ClusterComputeResource
metric_class: context
internal_derive: []
same_name: []
same_meaning: []
related:
- vsphere/object-types/cluster/concepts/cluster-operations
source:
  document: PART 3 - Counters.docx
  path: Provider Objects > Overview > vSphere Cluster > VM Operations
corrections: []
review_notes:
- 'Section ''Counters'': the book lists ''VM host and datastore change count'' twice (powered-on and powered-off). Written once for both; the powered-off variant is grouped with the other powered-off counters.'
status: draft
```
