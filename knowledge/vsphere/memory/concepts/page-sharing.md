# Page sharing

## Definition
- ESX transparently shares memory pages that are identical between VMs.
- Result: redundant copies of memory pages are eliminated.

## Scope since vSphere 6.0
- Sharing within a VM (intra-VM sharing): active by default.
- Sharing between VMs (inter-VM sharing): active only when the VMs have the same salt value.
- Reason for the change: security.
- Earlier releases (and some patched releases) shared pages between VMs by default.

## Salt
- Default salt: the VM's `vc.uuid`. It is unique for each VM on a host, which prevents inter-VM sharing.
- Two ways to allow inter-VM sharing:
  - host option `Mem.ShareForceSalting` set to 0. This applies to all VMs on the ESX host and restores the pre-6.0 default. See KB 2097593.
  - VMX option `sched.mem.pshare.salt`, set to the same value in each VM that should share pages with another. VMs with the same salt form a sharing pool.
- Setting the same salt for every VM in an environment creates a single page-sharing pool.

## Effect by environment
- Most environments: little effect, because of the prevalence of 2 MB large pages.
- Environments with extensive small memory pages, such as many VDI deployments: sharing can reduce memory usage considerably.

## Interaction with large pages
- ESX does not share 2 MB large pages. See `vsphere/memory/concepts/large-memory-pages`.
- Page sharing can start only when overcommitment is high enough to break large pages into small pages.

## Traps
- "Page sharing shares pages between all VMs by default" → since vSphere 6.0, the default is sharing within a VM only.
- "Page sharing saves significant memory in most deployments" → the source says the effect is little in most deployments. Benefit is large in small-page environments such as VDI.
- "Setting one salt for all VMs is harmless" → the source describes it as a single pool, which recreates the pre-6.0 default. Review the security implications (KB 2080735, 2097593).

## Metadata
```yaml
id: vsphere/memory/concepts/page-sharing
retriever_guide: how-it-works
scope: vsphere
technology:
- memory
pillar:
- capacity
- security
product:
- vsphere
object:
- HostSystem
- VirtualMachine
internal_derive: []
related:
- vsphere/memory/concepts/host-memory-states
- vsphere/memory/concepts/large-memory-pages
source:
  document: Performance Best Practices for VMware vSphere 9.1 (revision 20260624)
  path: ESX Memory Considerations > Memory Overcommit Techniques > Page Sharing (p. 33); Memory Page Sharing (pp. 34-35)
corrections: []
review_notes:
- Checked against 9.1 (revision 20260624). Pages 33-35 unchanged.
- 'Source URL: https://www.vmware.com/docs/vsphere-esxi-vcenter-server-9-1-performance-best-practices'
- 'Source KB articles for security issues: 2080735 and 2097593. Not read.'
status: draft
```
