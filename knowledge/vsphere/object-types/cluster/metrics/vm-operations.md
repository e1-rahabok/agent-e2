# Cluster VM operations event counts

## Meaning
- Counts of VM operations in the cluster, one counter per operation type (stat type absolute in the vSphere API 9.1). Cumulative since the object was created; a vCenter restart does not reset them.
- VCF Operations converts them to rates and rolls them up to Datacenter, vCenter and vSphere World.
- Relevance for operations: configuration and change management (power, reconfigure, delete and move operations against the change requests) and inventory dynamics; not a performance or capacity counter.

## Counters
| Category | Metric | vCenter counter | Notes |
|---|---|---|---|
| Change of state | VM guest reboot count | `vmop.numRebootGuest` | Restart Guest OS through VMware Tools; the VM is not powered off. |
| Change of state | VM guest shutdown count | `vmop.numShutdownGuest` | Shut Down Guest OS through VMware Tools; the VM powers off when the Guest OS halts. |
| Change of state | VM standby guest count | `vmop.numStandbyGuest` | Standby of the Guest OS through VMware Tools. |
| Change of state | VM power off count | `vmop.numPoweroff` | Power off of the VM, without the Guest OS shutting down first. |
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

- vCenter stores all 20 counters on the cluster and on the datacenter (rollup latest, stat type absolute). The vCenter 9.1 API offered them at level 1 in one inventory export; the vSphere 9.1 documentation lists only numChangeDS, numChangeHost and numChangeHostDS at level 1 and all VM operations counters at level 2 (Statistics Levels, p. 2031).

## Use
- Compare dynamics with expectations. In production these numbers should be low.
- Shutdowns should match change requests and happen in the maintenance window. Exceptions: for example, scheduled VDI reboots.

## Misconceptions
- "Counts are per interval" → the vCenter counters are cumulative totals; subtract two samples for the operations in between. VCF Operations shows them as rates.

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
  document: Knowledge base; VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number)
  path: Provider Objects > Overview > vSphere Cluster > VM Operations; vSphere 9.1 Statistics Levels (p. 2031)
corrections: []
review_notes:
- 'To check: Section ''Counters'': whether a guest shutdown through VMware Tools also counts in `vmop.numPoweroff`, and whether a Guest OS restart started inside the guest counts in `vmop.numRebootGuest`; compare the counts with the VM events on a vCenter 9.1.'
- 'To check: Section ''Meaning'': that the vmop counters are cumulative since the object was created and survive a vCenter restart, and that VCF Operations shows them as rates; a vCenter 9.1 chart and the VCF Operations 9.1 metric.'
status: draft
```
