# ESXi host specification from class of service

## Why Day 2 sets the hardware
- The host specification cannot be chosen without two Day 2 inputs: the average VM profile (RAM per vCPU) and the overcommit ratio planned for each class of service.
- RAM is sold together with vCPU. RAM beyond what the sellable vCPUs bring stays unsold: there is no vCPU left to sell with it.
- Day 2 → Day 0 → Day 1: `operations-management/performance/purpose-driven-architecture`.

## Method
```text
Sellable vCPU  = (host cores - cores kept for infrastructure) × CPU overcommit per core
VM memory (GB) = Sellable vCPU × GB per vCPU / memory overcommit
Host RAM (GB)  = VM memory + RAM kept for infrastructure
```
- RAM per vCPU (4 GB in the examples) is a planning guideline. Customers may buy more or less memory per vCPU.
- Infrastructure share: non-business work on every host, such as vSAN with deduplication, NSX, vSphere Replication, and kernel processing for IO-heavy VMs. Book example: 8 cores and 64 GB per host.
- The basis of the CPU overcommit ratio changes the answer by 2x with Hyper-Threading: 4:1 per core is 2:1 per physical thread. The knowledge base states overcommit per physical thread (`vsphere/foundations/noisy-neighbour`); the book's examples here state it per core.

## Silver: cost optimized (book example)
- Host: 64 cores. Kept for infrastructure: 8 cores, 64 GB. Left: 56 cores.
- CPU overcommit 4:1 per core (2:1 per physical thread): 56 × 4 = 224 vCPU.
- 224 vCPU × 4 GB = 896 GB. Memory overcommit 2:1: 448 GB for VMs.
- Host RAM: 448 + 64 = 512 GB.
- Specification: 64 cores, 512 GB.

## Gold: performance optimized (book example)
- No CPU or memory overcommit: 1 vCPU per core.
- 64 cores → 64 vCPU × 4 GB = 256 GB.
- A host with 1 TB would leave 768 GB unsold.
- The book's Gold example keeps no cores or RAM for infrastructure. With the Silver share (8 cores, 64 GB) it becomes 56 vCPU, 224 + 64 = 288 GB.

## Silver at 3:1 CPU, no memory overcommit
- Average VM: 1 vCPU, 4 GB. CPU overcommit 3:1 per core, memory 1:1.
- Each core sells 3 vCPU × 4 GB = 12 GB of RAM.
- 64 cores: 64 × 12 = 768 GB.
- The book picks 64 cores to make full use of the vSphere license. That held under per-CPU licensing (up to 32 cores per CPU license, so 2 × 32). VCF 9 is licensed per core, with a minimum of 16 cores per CPU: core count no longer has a license sweet spot above 16 per CPU.
- No infrastructure share in this example. vSAN and NSX overhead is added on top.
- Price at 67% of Gold: `operations-management/performance/class-of-service`.

## Reading the examples
- On the same 64-core host, Gold takes less RAM than Silver (256 GB vs 512 GB): Gold sells fewer vCPUs per host, and RAM follows the vCPUs sold.
- Each class gets its own host specification, or its own cluster with a matching specification. Mixing classes on one host specification leaves RAM unsold in one of them.
- Silver ratios differ between the book's examples: CPU 4:1 with memory 2:1 here; CPU 3:1 with memory 1:1 in the planning example; memory 1.5:1 in the class of service table of `vsphere/foundations/noisy-neighbour`. Each is a business choice per provider.

## Traps
- "Buy as much RAM as the host takes; memory is cheap" → RAM is sold with vCPU. Beyond (sellable vCPU × GB per vCPU / memory overcommit) + infrastructure share, it cannot be sold.
- "Gold hosts take the most RAM" → at 1 vCPU per core Gold sells fewer vCPUs, so it takes less RAM per host than an overcommitted class.
- "4:1 overcommit means the same capacity on every host" → say whether it is per core or per physical thread; with Hyper-Threading the two differ by 2x.
- "All cores of the host can be sold" → vSAN, NSX, replication and kernel IO work take a share of every host; subtract it first.

## Metadata
```yaml
id: operations-management/capacity/host-spec-from-class-of-service
retriever_guide: how-it-works
scope: operations-management
technology:
- cpu
- memory
pillar:
- capacity
product:
- vsphere
- vsan
- nsx
object:
- HostSystem
internal_derive:
- operations-management/performance/purpose-driven-architecture
- vsphere/foundations/noisy-neighbour
related:
- operations-management/performance/class-of-service
- operations-management/capacity/capacity-model
- operations-management/performance/iaas-business
- vsphere/foundations/overhead
source:
  document: PART 1 - Concepts of Operations Management.docx
  path: 'Your Private Cloud > Purpose-Driven Architecture > Begin with The End in Mind > Day 0 | Day 1 | Day 2 (pp. 14-15); Service Level Agreement > Price & SLA (p. 37)'
corrections: []
review_notes:
- 'Section ''Method'': formula written by Claude from the book''s Silver example.'
- 'Section ''Method'', last bullet: overcommit per physical thread is the author''s rule (Q079, 2026-11-06). The book''s Silver example is per core (Q087 a).'
- 'Section ''Gold'', last bullet: Gold with the Silver infrastructure share computed by Claude; the book keeps none for Gold (Q087 b).'
- 'Section ''Reading the examples'': first two bullets are Claude''s reading of the book''s numbers. Silver memory 2:1 here vs 1.5:1 in Noisy Neighbour (Q087 c).'
- 'Section ''Silver at 3:1 CPU'': the book''s planning table gives Silver CPU 1:2 and RAM 1:1.5; its text gives 3:1 and no RAM overcommit (Q099). Licensing bullet: per-core licensing with a 16-core minimum per CPU from Broadcom KB 313548 (https://knowledge.broadcom.com/external/article/313548) and the VCF 9.0 Licensing Model page (https://techdocs.broadcom.com/us/en/vmware-cis/vcf/vcf-9-0-and-later/9-0/licensing/licensing-overview/licensing-model.html); the 32-core per-CPU licence is Claude''s knowledge. Book correction: Q107.'
status: draft
```
