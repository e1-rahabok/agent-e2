# VM configuration review

## VMware Tools
- Essential for workloads on VCF: drivers and observability. Benefits list: Broadcom KB 315382.
- **Installed?** The usual reason it is missing: the ISV of an appliance refuses software it has not certified.
- **Running?** Application teams sometimes stop it. Document why it must run at all times and tell them.
- **Current?** Up to date and compatible with the VM hardware version.
  - Older Tools versions do not report some Guest OS counters: CPU run queue, context switches, disk queue length, memory used.
  - Too many Tools versions; newer ones give better observability.

## VM hardware and settings
- Outdated VM hardware versions, and too many of them.
- Advanced settings: as few as possible, each per the standard.
- Multiple networks: a VM that is not a network appliance should not span more than one network. Several vNICs can bridge networks: a security and network risk. One vNIC can also reach several networks with several interfaces, each with its own IP: check the configuration, not only the vNIC count.
- Drivers: correct and current.

## Compute
- **Relative size**: the VM must not exceed its ESXi host. With Hyper-Threading, count physical cores, not logical processors.
- **NUMA**:
  - more vCPUs than cores per socket → the VM spans NUMA nodes; on a multi-socket host remote memory access lowers performance. Keep it within a socket;
  - chiplet CPUs (AMD EPYC): a 64-core CPU of 8 chiplets of 8 cores, each with its own L3 cache. A VM above 8 vCPUs spans chiplets;
  - vSocket and vCore configured per vNUMA practice: `vsphere/technology/cpu/concepts/virtual-numa`.
- **Large VMs**:
  - vMotion, Storage vMotion and backup take longer;
  - a monster VM running hot hurts other VMs: default shares scale with size, so it gets more under contention. Others get CPU only when it is under-utilized.
- **Hot add**: CPU and memory hot add only on the VMs that use it. CPU hot add deactivates vNUMA, so memory is interleaved across nodes. Use it only when the benefit outweighs that cost.

## Storage
- **Virtual disk**:
  - thin and under-used: other VMs can share the datastore, but track snapshots closely; a large thin disk raises the risk of a full datastore;
  - unmap reclamation: how much space can be returned;
  - monitor each virtual disk (IOPS, throughput, latency), not only the VM. More disks, more to monitor and troubleshoot;
  - several disks for performance: name the counter that proves one disk is not enough. One may be.
- **Snapshot**: removed within one day of the change request. A forgotten snapshot grows and slows the VM: `vsphere/technology/storage/concepts/snapshot-impact`.
- **Disaster recovery**: vSphere Replication settings drift when owners do not report changes. Check that every VM protected by Site Recovery is still meant to be protected; review the recovery plan: how often it runs, when it last ran.
- **Fault Tolerance**: only on the VMs meant to have it; it brings its own complexity.
- **vVols**: per design practice. vVols are deprecated in VCF 9.
- **Shared disks**: VMs sharing a VMDK or RDM.
- **Guest partition to virtual disk**: 1:1 is simplest. Logical volumes across disks in Windows or Linux add complexity.
- **VM to datastore**: avoid VMs spanning datastores. M:N mapping complicates troubleshooting and capacity planning.
- **RDM**: keep few. RDMs cause LUN sprawl and leave unused RDM objects on the array. Look for RDMs used where a VMDK would do, unused or hardly used, and oversized.

## Traps
- "The VM has 48 vCPUs and the host has 48 logical processors, so it fits" → count physical cores. 48 vCPUs on 24 cores with Hyper-Threading competes for cores.
- "16 vCPUs on a 32-core AMD EPYC socket stay in one NUMA node" → the socket has several L3 cache domains; 16 vCPUs span two 8-core chiplets.
- "Enable CPU hot add on every VM for flexibility" → it deactivates vNUMA; large VMs lose memory locality.
- "Guest OS run queue is missing, so the Guest OS is fine" → an old VMware Tools version does not report it. Check the Tools version.
- "One vNIC, so the VM is on one network" → one vNIC can carry several interfaces on several networks.
- "Several virtual disks always perform better" → prove it with the per-disk counter; one disk may meet the demand.
- "Keep the snapshot until the change is fully accepted" → remove it within a day; it grows and slows the VM.

## Metadata
```yaml
id: vsphere/object-types/vm/configuration/vm-configuration-review
retriever_guide: what-to-set
scope: vsphere
technology:
- cpu
- memory
- storage
- network
- system
pillar:
- performance
- availability
- compliance
- capacity
product:
- vsphere
object:
- VirtualMachine
internal_derive:
- sp5-framework/concepts/configuration-management
related:
- guest-os/system/concepts/guest-os-configuration-review
- vsphere/object-types/vm/configuration/resource-settings-guidance
- vsphere/technology/cpu/concepts/virtual-numa
- vsphere/technology/cpu/concepts/idle-and-unused-vcpus
- vsphere/technology/storage/concepts/snapshot-impact
- vsphere/technology/storage/configuration/storage-configuration-review
source:
  document: PART 1 - Concepts of Operations Management.docx
  path: 'Configuration Management > Review List > Consumer Objects > Tools; VM; Compute-related; Storage-related Configuration (pp. 135-138)'
corrections: []
review_notes:
- 'Q112 answered by the author (2026-11-08): DRS runs every minute; vVol checks kept for existing estates with the deprecation stated; snapshots removed within one day; VMware Tools KB 315382.'
- 'Section ''VMware Tools'': Broadcom KB 315382 (author, Q112, 2026-11-08); the book cited KB 340.'
- 'Section ''Compute'', relative size: physical cores here; sp5-framework/performance/noisy-neighbour sizes by logical CPUs. Q111 (with Q100).'
- 'Section ''Storage'', vVols deprecated: Broadcom KB 401070 (https://knowledge.broadcom.com/external/article/401070), VCF 9.0 vSphere product support notes; Protection and Recovery 9.1 release notes call 9.1 its last release supporting vVols. Q112.'
- 'Snapshot removed within one day: author, Q112 (2026-11-08).'
- 'Section ''Compute'', chiplets: 8-core blocks hold for AMD EPYC, not Intel Xeon (Q125).'
- 'Traps 1 and 2: examples by Claude from the book''s rules.'
status: draft
```
