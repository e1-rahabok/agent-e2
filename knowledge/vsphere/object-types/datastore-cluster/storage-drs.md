# Storage DRS space balancing

## Definition
- Storage DRS places and moves VM disks between the datastores of a datastore cluster, for space. I/O load balancing is gone: Storage I/O Control components are deprecated from VCF 9.0 (vSphere 9.1 documentation, Storage I/O Control; Activate Storage DRS lists only space balancing).
- It gives initial placement (create, clone, add a disk, move a disk into the cluster) and ongoing balancing recommendations. Fully Automated applies them; Manual lists them on the Storage DRS Recommendations page.

## Invocation
- Storage DRS runs at the configured frequency, every eight hours by default, and also when a datastore crosses the space utilization threshold.
- Each run checks the space utilization of each member datastore, not of the datastore cluster as a whole.

## Space thresholds
- The space utilization threshold (default 80%) is set on the datastore cluster but applies to each member datastore. A datastore over it is a source, whatever the cluster average is, because an average hides a full member.
- The minimum space utilization difference (default 5 points) is checked for each source and destination pair: a datastore is a destination only when its utilization is more than that difference below the source. Example: a source at 90% does not move disks to a datastore at 87%, while a datastore at 60% in the same cluster still qualifies.
- A destination must also stay under the space utilization threshold after the move. A datastore just under the threshold cannot take a disk that would push it over, even when it passes the difference check.
- The space utilization threshold is a soft constraint: Storage DRS crosses it on a destination only when no member datastore in the cluster is below it.
- Storage DRS moves enough disks to bring each source back under the threshold. It does not level all members to the cluster average: datastores already under the threshold are left alone.
- Thin and thick disks use the same space calculation. For thin disks Storage DRS also weighs the growth rate of each VMDK.
- Storage DRS prefers destinations connected to all hosts of the compute cluster.

## Recommendations
- Mandatory recommendations: a datastore out of space, an affinity or anti-affinity rule violated, or a datastore entering maintenance mode.
- Optional recommendations: a datastore close to running out of space, or a space adjustment.
- Storage DRS moves powered-on and powered-off VMs for space balancing, including powered-off VMs with snapshots.

## Misconceptions
- "The datastore cluster is at 70%, below the 80% threshold, so Storage DRS does nothing" → the threshold applies to each member datastore; one member over it is enough.
- "Storage DRS balances all datastores to the cluster average" → it moves enough to bring each source under the threshold, no more.
- "Any datastore under the threshold is a valid destination" → the destination must be more than the minimum space utilization difference below the source and must stay under the threshold after the move.
- "A source is skipped when the nearest datastore is within the minimum difference" → the difference is checked per source and destination pair; a farther, emptier datastore still qualifies.

## Metadata
```yaml
id: vsphere/object-types/datastore-cluster/storage-drs
retriever_guide: how-it-works
scope: vsphere
technology:
- storage
pillar:
- capacity
- performance
product:
- vsphere
object:
- StoragePod
- Datastore
- VirtualMachine
internal_derive: []
related:
- vsphere/object-types/datastore-cluster/datastore-cluster-alerts
- vsphere/object-types/datastore/datastore-alerts
- vsphere/technology/storage/datastore-space-headroom
source:
  document: VMware vSphere 9.1 product documentation (PDF built 2026-11-02; the copyright page carries no revision number); Storage DRS FAQ (Broadcom KB 2149938)
  path: vSphere Resource Management > Creating a Datastore Cluster > Initial Placement and Ongoing Balancing, Storage Migration Recommendations, Activate Storage DRS, Setting the Aggressiveness Level for Storage DRS, Set Storage DRS Runtime Rules (pp. 1927-1929); KB 2149938 for the defaults (80%, 5 points), the threshold per datastore, the soft constraint, thin and thick disks and host connectivity
corrections: []
review_notes:
- 'To check: Section ''Space thresholds'': that a destination must stay under the space utilization threshold after the move, and that moves stop once each source is under the threshold; the vSphere 9.1 documentation (pp. 1927-1929) says only that Storage DRS balances space use across the datastore cluster when a datastore exceeds the threshold (Storage DRS FAQ, KB 2149938).'
status: draft
```
