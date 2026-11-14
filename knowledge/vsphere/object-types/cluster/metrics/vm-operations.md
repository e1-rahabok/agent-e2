# Cluster VM operations event counts

## Meaning
- Counts of VM events in the cluster. Cumulative since the object was created; a vCenter restart does not reset them.
- VCF Operations converts them to rates and rolls them up to Datacenter, vCenter and vSphere World.

## Counters
| Category | Metric | vCenter counter | Notes |
|---|---|---|---|
| Change of state | VM guest reboot count | `vmop.numRebootGuest` | Reboot only; the VM is not powered off. |
| Change of state | VM guest shutdown count | `vmop.numShutdownGuest` | Believed to also trigger VM power off. |
| Change of state | VM standby guest count | `vmop.numStandbyGuest` | Guessed to also power off the VM. |
| Change of state | VM power off count | `vmop.numPoweroff` | Believed to be a direct, abrupt power off, not a guest shutdown. |
| Change of state | VM power on count | `vmop.numPoweron` | - |
| Change of state | VM reset count | `vmop.numReset` | Power cycle: the VM is briefly powered off. |
| Change of state | VM suspend count | `vmop.numSuspend` | Deeper than guest standby. |
| Change of inventory | VM create count | `vmop.numCreate` | All creations: template, direct, clone. |
| Change of inventory | VM clone count | `vmop.numClone` | Clones only. |
| Change of inventory | VM template deploy count | `vmop.numDeploy` | Template deployments only. |
| Change of inventory | VM reconfigure count | `vmop.numReconfigure` | Log analysis shows the actual changes. |
| Change of inventory | VM register count, VM unregister count | `vmop.numRegister`, `vmop.numUnregister` | Unregistered VM files can remain on the datastore. |
| Change of inventory | VM delete count | `vmop.numDestroy` | All deletions, API or UI. |
| Change of location | vMotion count | `vmop.numVMotion` | Host change of a powered-on VM. |
| Change of location | Storage vMotion count | `vmop.numSVMotion` | Datastore change of a powered-on VM. |
| Change of location | VM host and datastore change count (powered on) | `vmop.numXVMotion` | Host and datastore change in one event; powered-on and suspended VMs. |
| Change of location | VM host and datastore change count (powered off) | `vmop.numChangeHostDS` | Same, for powered-off and suspended VMs. |
| Change of location | VM host change count, VM datastore change count | `vmop.numChangeHost`, `vmop.numChangeDS` | Powered-off and suspended VMs. |

- vCenter stores all 20 counters on the cluster and on the datacenter, at level 1 (rollup latest, stat type absolute).
- Whether vCenter accumulates them while VCF Operations shows a rate is not settled.

## Use
- Compare dynamics with expectations. In production these numbers should be low.
- Shutdowns should match change requests and happen in the maintenance window. Exceptions: for example, scheduled VDI reboots.

## Misconceptions
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
internal_derive:
- vsphere/object-types/cluster/concepts/cluster-operations
- vsphere/object-types/cluster/concepts/drs-overview
- sp5-framework/observability/input-types
same_name: []
same_meaning: []
related:
- vsphere/object-types/cluster/concepts/cluster-operations
source:
  document: Knowledge base
  path: Provider Objects > Overview > vSphere Cluster > VM Operations
corrections: []
review_notes: []
status: draft
```
