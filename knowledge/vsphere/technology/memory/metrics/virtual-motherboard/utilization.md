# VM Memory Utilization (VCF Operations)

## Formula
```text
Utilization (KB) = Guest Needed Memory (KB)
                 + Guest Page In Rate per second × Guest Page Size (KB)
                 + Memory Total Capacity (KB) - Guest Physically Usable Memory (KB)
```
- Can exceed 100%.

## Use
- For operations: capacity. It is the VM term of ESXi Memory Utilization, the host memory demand of VCF Operations ([`vsphere/technology/memory/metrics/host/utilization`](../host/utilization.md), section Formula).
- VCF Operations 9.1 collects Mem|Utilization (KB) (`mem|vmMemoryDemand`) by default and describes it as the guest OS memory required, or the VM's consumption (Virtual Machine metrics).
- Not a performance counter: a high value says the VM's memory is spoken for, not that the VM waits.

## High value with a low guest
- Guest metrics from VMware Tools not collected: Utilization (KB) = Consumed (KB) (Broadcom KB 439253, KB 390432). A mixed source makes the value fluctuate.
- Guest Physically Usable Memory below configured memory. Example: 58 GB usable on an 80 GB VM.
- Low utilization: 5% of total memory is added, not 5% of used. A 128 GB VM shows 6.4 GB extra.
- The 5% is a hardcoded buffer inside Guest Needed Memory, the first term of the formula: Needed = physical - max(0, Unneeded - 5% of physical). See [`guest-os/memory/windows-memory`](../../../../../guest-os/memory/windows-memory.md), section Needed Memory.
- Excessive paging is added. Excessive is relative.
- Linux Available and Windows Cache are included, to be conservative.

## Misconceptions
- "Utilization above 100% is an error" → the formula adds paging and unusable memory.

## Metadata
```yaml
id: vsphere/technology/memory/metrics/virtual-motherboard/utilization
retriever_guide: metric-meaning
scope: vsphere
technology:
- memory
pillar:
- capacity
product:
- vcf-operations
- windows
- linux
object:
- VirtualMachine
layer:
- virtual-motherboard
metric_class: consumption
internal_derive:
- vsphere/technology/memory/concepts/guest-os-vs-vm-memory
- guest-os/memory/windows-memory
same_name: []
same_meaning: []
related:
- vsphere/technology/memory/metrics/virtual-motherboard/usage
- vsphere/technology/memory/metrics/host/utilization
- guest-os/memory/windows-memory
- vsphere/technology/memory/concepts/guest-os-vs-vm-memory
source:
  document: Knowledge base; VCF Operations 9.1 documentation (TechDocs, last updated 2026-11-12), Virtual Machine Metrics; Broadcom KB 439253, Understanding Demand vs. Utilization Memory Metrics in VMware Aria Operations (VCF Operations); Broadcom KB 390432, VM Memory Utilization (KB) Discrepancy between Aria Operations (formerly vRealize Operations) and Guest OS
  path: Memory > VM > Consumption Metrics > Utilization
corrections:
- 'Section ''Formula'': Broadcom KB 439253 writes the last term as Total Capacity - Guest Physically Free. The term is Guest Physically Usable Memory: KB 390432 writes Guest|Physically (cut off), and Total Capacity minus free memory would count the used memory a second time on top of Needed Memory.'
review_notes:
- 'Section ''Formula'' and ''Use'': https://knowledge.broadcom.com/external/article/439253, https://knowledge.broadcom.com/external/article/390432 and VCF Operations 9.1 Virtual Machine Metrics, https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-1/infrastructure-operations/metric-property-and-alert-definitions/metrics-definitions-in-vrealize-operations-manager/metrics-for-vcenter-server-components/virtual-machine-metrics.html.'
status: draft
```
