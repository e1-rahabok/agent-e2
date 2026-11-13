# CPU topology: CPU vs vCPU

## Hyper-Threading inside a VM
![Physical CPU with threads vs vCPU with virtual sockets and cores](../images/physical-cpu-threads-vs-vcpu-virtual-sockets-and-cores.png)
- vSphere exposes only virtual sockets and virtual cores to a VM.
- A virtual core has no hyper-threads.
- So Hyper-Threading exists at the physical CPU level only, not at the vCPU level.

## System on a Chip
- A CPU socket is not a simple, linear collection of cores. CPU design moves toward System on a Chip.
- Example: 64-core AMD EPYC 7003 (Zen 3).
  - 8 Core Complex Dies (CCD).
  - Each CCD has its own L3 cache.
  - Each CCD has 8 Zen 3 cores.
  - Each core has its own L2 cache.
- Consequence: locality exists inside one socket. A thread is closer to another thread on the same CCD than to one on another CCD.
- Every core reaches every memory DIMM of its socket through the die fabric, but the paths are not equal. Memory behind a distant controller costs:
  - hop latency: the signal crosses die boundaries;
  - fabric congestion: threads that keep fetching across the central crossbar share its finite bandwidth, which saturates under high utilization.
- So NUMA matters inside one socket too: ESX aligns a VM's threads with the nearest memory controllers through the physical NUMA nodes and the VM's vNUMA layout.
- Placement inside a socket affects application performance.

## NUMA
- NUMA node = package, not always socket. One socket can hold more than one package, for example with Intel Xeon Cluster-on-Die enabled.
- AMD EPYC 9005: AMD states the socket is best divided into 4 NUMA domains. The setting is called NPS4.
- In NPS4, each domain has 6 memory DIMMs and 3 memory controllers.
- Intel: SAP recommends enabling Sub-NUMA Clustering (SNC). The workload situation is similar to AMD NPS4.
- Where the domains come from, by processor (the BIOS setting that matches the silicon):

| Processor | Silicon | Memory | Matching setting | NUMA node |
|---|---|---|---|---|
| AMD EPYC 9005 (Zen 5, Turin) | up to 16 CCDs around one central IOD | 12 DDR5 channels | NPS4 | 4 per socket, 3 channels each |
| Intel Xeon 6 6900P (Granite Rapids AP) | up to 3 compute tiles and 2 I/O tiles; the memory controllers sit in the compute tiles | 12 DDR5 channels | SNC3 | 3 per socket, one per compute tile, 4 channels each |
| AMD EPYC 9006 (Zen 6, Venice), e.g. EPYC 9996 | 8 CCDs of 32 cores (256 cores); two IODs per socket | 16 DDR5 channels | NPS2 | 2 per socket, one per IOD: 128 cores and 8 channels each |

- The setting follows the silicon: a node boundary at a real die boundary (an IOD, a compute tile with its own controllers) keeps a thread's memory behind its own controllers.
- The vSphere default for AMD is NPS-1 ([`vsphere/technology/cpu/configuration/numa-settings`](../configuration/numa-settings.md)); the table gives the setting that matches the silicon. Author question Q198.
- Broadcom KB 314059 shows a NUMA effect: NUMA nodes heavily load-imbalanced.

## Cache latency
- Intel Xeon 6 test: local L3 cache latency 33 ns.
- Remote L3 cache (further away on the die): 80 ns.

## Misconceptions
- "A vCPU can use Hyper-Threading" → a virtual core has no hyper-threads. Hyper-Threading is a property of the physical core.
- "All cores in a socket are equal distance from each other" → CCD and L3 boundaries create locality inside a socket.
- "NUMA node = socket" → NUMA node = package or a sub-socket domain (Cluster-on-Die, NPS4, SNC).

## Metadata
```yaml
id: vsphere/technology/cpu/concepts/cpu-topology
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
- memory
pillar:
- performance
product:
- vsphere
object:
- HostSystem
- VirtualMachine
internal_derive: []
related:
- vsphere/technology/cpu/concepts/numa
- vsphere/technology/cpu/concepts/virtual-numa
- vsphere/technology/cpu/concepts/hyper-threading
- vsphere/technology/cpu/configuration/numa-settings
- vsphere/technology/cpu/concepts/vcpu-states
images:
  - path: ../images/physical-cpu-threads-vs-vcpu-virtual-sockets-and-cores.png
    product: [vsphere]
    object: [HostSystem, VirtualMachine]
    topic: 'CPU topology'
    image_type: diagram
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: 'CPU > Architecture > CPU vs vCPU > System on a Chip; NUMA. Also the knowledge base, vSphere NUMA Architecture and Sizing Guide (vSphere 9.1), sections 1 and 2'
corrections: []
review_notes:
- "Section 'System on a Chip': AMD source from the book: https://www.amd.com/system/files/documents/overview-amd-epyc7003-series-processors-microarchitecture.pdf (p. 5)."
- "Section 'System on a Chip': performance example from the book: https://blogs.vmware.com/performance/2020/04/amd-epyc-rome-application-performance-on-vsphere-series-part-1-sql-server-2019.html"
- "Section 'NUMA': AMD EPYC 9005 white paper from the book: https://www.amd.com/content/dam/amd/en/documents/epyc-business-docs/white-papers/5th-gen-amd-epyc-processor-architecture-white-paper.pdf"
- 'To check: Section ''NUMA'': Broadcom KB cited by the book, not read (https://knowledge.broadcom.com/external/article/314059/numa-nodes-are-heavily-load-imbalanced-c.html).'
- 'To check: Section ''NUMA'': SAP source cited by the book, not read (https://help.sap.com/docs/SUPPORT_CONTENT/virtualization/4181102237.html).'
- "Section 'Cache latency': test source from the book: https://chipsandcheese.com/p/a-look-into-intel-xeon-6s-memory"
status: draft
```
