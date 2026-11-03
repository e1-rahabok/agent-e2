# Hypervisor overhead (CPU and memory)

## Why "hypervisor"
- More than the kernel: user-level processes run on top of it.
- VMkernel traditionally excludes vSAN and NSX (vSAN processes sit under /opt).
- Treated as capacity, not performance: the hypervisor has the highest priority. Per-process ready time is in esxtop.

## Which metric to use for usable capacity
| Metric | Problem |
|---|---|
| Utilization | Changes every second. Usable capacity cannot be volatile. |
| Limit | Does not make sense: hypervisor features affect all VMs and must have priority. |
| Reservation | Too low with vSAN and NSX, too high with ESXi only. Fluctuates. |
- Practice: enter a static value manually.

## Metric types
| Type | Facts |
|---|---|
| Utilization | Actual consumption. Can be below reservation, not above allocation. ESXi utilization covers hypervisor and VMs; separate them only when migrating to another architecture. VM contention serves as the contention proxy (the hypervisor has priority), assuming no manual VM limits. |
| Reservation | Minimum guaranteed so the hypervisor runs when VMs demand 100%. Memory is granted on demand, not up front; CPU is used only when running. Utilization can be below reservation. |
| Allocation | Maximum (limit). Useful for VMs (overcommit). Not for non-VM worlds; some show blank or 0 limits. |

## Why the size is unpredictable
- Some services have static values.
- Some scale with host memory.
- Some scale with the number of active VMs.
- Some grow with work done (storage and network stacks).
- Some depend on configuration (vSAN deduplication and compression).

## Resource groups
| Group | Content |
|---|---|
| host/system | Low-level services and drivers: minfree, kernel, helper, FT, vMotion, Storage vMotion, vmk API modules, idle, drivers. vSAN data plane (no separate counter). Concurrent vMotions raise vmotion use. |
| host/vim | Host management: HA (aam), vpxa, hostd, VIM user (DCUI, shell, SSH, Tools), authd, tmp, envoy, GPU manager, tokend, healthd. vmvisor includes NSX and vSAN management plane. |
| host/user | All running VMs, including VM overhead. Only one metric; no breakdown. |
| host/opt | Mostly vSAN (opt/vsan, for example vsanperfsvc). Since vSphere 8.0.1. |
| host/iofilter | IO filter framework for third-party IO interception. |
- vSphere Client shows no CPU or memory reservation metrics for user and iofilter groups.

| Group | CPU | Memory |
|---|---|---|
| System | Low, can be well below 1 GHz | High, about 20-30 GB |
| VIM | High, about 4-12 GHz | Low, can be 0 GB; no memory reservation |

## CPU metrics
- Kernel CPU: plot host/iofilters, host/system and host/vim, stacked. Sub-pools are part of them and small (well below 0.5 GHz).
- Example: top 7 of about 400 hosts by system group: system up to 3.66 GHz, vim up to 0.48 GHz, iofilters near 0; user dominates Usage.
![ESXi CPU usage by resource group (system, vim, iofilters, user) with Usage and Demand, top 7 of about 400 hosts](../images/esxi-cpu-usage-by-resource-group-system-vim-iofilters-user.png)
- Counters: Usage, Running, Active. Use Usage: it covers all groups. Running and Active lack host/user and host/opt; Active rolls up as Latest.
- Latest roll-ups tend to read higher than averages.
- Host CPU | Usage (MHz) equals System | Resource CPU Usage (Average) (MHz) at host level: it includes VMs.
- 364 hosts, each above 100 GHz with vSAN and NSX: kernel mostly below 10% of total; absolute values vary widely.
- 557 hosts above 100 GHz: most kernel values below 25 GHz; 2 outliers above 40 GHz. No correlation between total and hypervisor CPU use.
- Network: above 40 Gbps and 3 million packets: kernel below 8 GHz.
- Storage: above 200K IOPS: kernel above 10 GHz.
- Reservation is stable; usage fluctuates every 20 s and exceeds reservation at high load. Maximum limited stays flat: kernel processes have no limit.
- host/system CPU reservation is low; host/vim about 6.6 GHz. Across about 400 hosts: mostly 6-10 GHz, usually stable.
![ESXi hypervisor CPU overhead distribution across about 400 hosts: mostly 6-10 GHz](../images/esxi-hypervisor-cpu-overhead-distribution-across-hosts.png)
![No predictable relation between hypervisor reservation, hypervisor use and total use](../images/esxi-hypervisor-cpu-reservation-vs-use-no-correlation.png)

## Memory metrics
- Roll-ups are Latest and stat type Absolute: memory is space.
- Allocation maximum = limit. Allocation minimum = reservation. Shares: internal; do not change.
- Consumed: actual use; can be below reservation. Mapped: meaning unclear, no operational use. Also Overhead, Share Saved, Shared, Swapped, Touched, Zero.
- 607 hosts with vSAN and NSX, 650-1,450 GB consumed: kernel overhead falls below 10% once consumed exceeds 800 GB; absolute values plateau in about 5 levels (likely vSAN configuration).
![ESXi hypervisor memory overhead (GB) vs ESXi Consumed (GB): values cluster in 5 levels](../images/esxi-hypervisor-memory-overhead-vs-consumed-scatter-levels.png)
- Kernel reservation: Memory | ESX System Usage (KB), a legacy name. Across 500+ hosts: 6-88 GB; a 12 TB host with vSAN and NSX: 300 GB.
- Reservation stays steady even when kernel use drops 90% (40 GB to single digits), and when all VMs are gone.
- Actual use: stack Resource Memory Consumed per group; system dwarfs the others.
- Memory | VMkernel consumed covers host/system only, not vSAN.
![Kernel memory overhead relative to consumed, 607 hosts](../images/esxi-hypervisor-memory-overhead-relative-to-consumed-across-hosts.png)

## Recommended static values (book)
| Stack | CPU (at 2.5 GHz) | Memory |
|---|---|---|
| ESXi + vSAN + NSX | 12 threads | 64 GB |
| ESXi only | 4 threads | about 20 GB (not backed by field data) |
- NSX Enhanced Data Path adds 2-4 cores: it polls the NIC.
- Size vSphere Replication and HCX separately.
- vSAN File Services is a VM: 2 vCPU, set a reservation.
- In monitoring, watch contention: the estimate may be too aggressive or conservative.

## Traps
- "Use kernel reservation as overhead" → unstable, and too low or too high depending on the stack.
- "Memory | VMkernel consumed = all hypervisor memory" → system group only.

## Metadata
```yaml
id: vsphere/system/concepts/hypervisor-overhead
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
- memory
- system
pillar:
- capacity
product:
- vsphere
- vsan
- nsx
object:
- HostSystem
internal_derive:
- vsphere/foundations/kernel-worlds
related:
- vsphere/system/concepts/capacity-model
- vsphere/memory/metrics/host/utilization
- vsphere/memory/metrics/host/consumed
images:
  - path: ../images/esxi-cpu-usage-by-resource-group-system-vim-iofilters-user.png
    product: [vsphere]
    object: [HostSystem]
    metric: ['ESXi CPU Usage', 'ESXi CPU Demand', 'ESXi Resource Group CPU Usage']
    image_type: table
    sample: 'top 7 of about 400 hosts'
  - path: ../images/esxi-hypervisor-cpu-overhead-distribution-across-hosts.png
    product: [vsphere]
    object: [HostSystem]
    metric: ['ESXi Resource Group CPU Reservation']
    topic: 'Hypervisor overhead'
    image_type: distribution
    sample: 'about 400 hosts'
  - path: ../images/esxi-hypervisor-cpu-reservation-vs-use-no-correlation.png
    product: [vsphere]
    object: [HostSystem]
    metric: ['ESXi Resource Group CPU Reservation', 'ESXi Resource Group CPU Usage']
    topic: 'Hypervisor overhead'
    image_type: scatter
  - path: ../images/esxi-hypervisor-memory-overhead-vs-consumed-scatter-levels.png
    product: [vsphere]
    object: [HostSystem]
    metric: ['ESXi Memory Consumed', 'ESXi Resource Group Memory Consumed']
    topic: 'Hypervisor overhead'
    image_type: scatter
    sample: '607 hosts'
  - path: ../images/esxi-hypervisor-memory-overhead-relative-to-consumed-across-hosts.png
    product: [vsphere]
    object: [HostSystem]
    metric: ['ESXi Memory Consumed', 'ESXi Resource Group Memory Consumed']
    topic: 'Hypervisor overhead'
    image_type: scatter
    sample: '607 hosts'
source:
  document: PART 3 - Counters.docx
  path: Provider Objects > Capacity > Hypervisor; CPU > Hypervisor; Memory > Hypervisor Metrics
corrections: []
review_notes:
- 'Section ''Resource groups'': the book lists 5 groups but says to plot only iofilters, system and vim for kernel consumption; host/opt (vSAN) is not in that list. Kept as written.'
- 'Section ''Why the size is unpredictable'': based on Host Resources Deep Dive (Denneman, Hagoort), p. 258, cited by the book.'
- 'Section ''Memory metrics'': ESX System Usage = kernel reservation. This is relevant to Q021.'
status: draft
```
