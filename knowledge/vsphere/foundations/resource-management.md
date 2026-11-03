# Resource management

## Controls
| Control | Nature |
|---|---|
| Reservation | Absolute. A guarantee (minimum). |
| Limit | Absolute. A cap. |
| Shares | Relative. Applied at two scheduler levels: cluster and host. |
| Entitlement | Dynamic. Determined by the hypervisor. See below. |

- Reservation, limit and shares are configured on the VM, outside the Guest OS (VM Edit Settings → CPU / Memory). CPU values are in MHz.
- Windows or Linux does not know these settings exist.
- Minimise use of limit and reservation. They make operations more complex.

## Two scheduler levels
| Level | Shares are relative to |
|---|---|
| Cluster | Siblings under the same parent in the cluster resource pool hierarchy (VMs and resource pools). |
| Host | Other VMs running on the same ESXi host. Used for Entitlement. |

## Which metric types apply per resource
| Resource | Utilization | Reservation | Allocation |
|---|---|---|---|
| CPU | Yes (unit: thread and Hertz) | Yes (unit: Hertz) | Yes (unit: vCPU) |
| Memory | Yes | Yes | Yes |
| Disk | Yes | Not applicable | Yes |
| Network | Yes | Yes | Yes |

- ESXi CPU therefore uses 3 different units: thread, Hertz, vCPU.

## Reservation: CPU vs memory
- Reservation is a guarantee. It takes effect at the provider (ESXi), where the reservation is held.
- It behaves differently for CPU and memory.

| Aspect | CPU reservation | Memory reservation |
|---|---|---|
| When it applies | On demand. If the VM does not use CPU, the reservation does not come into play. | Permanent once memory has been used. |
| Effect on utilization metrics | None. Run, Used, Demand, Usage do not include it. They are 0 or near 0 if the Guest OS is not running. | Included. Memory Consumed counts reserved memory even if the pages are not actually consumed yet. |
| Example: 16 GB VM, powered on, sitting at BIOS | CPU metrics ≈ 0. | 10 GB reservation → VM Memory Consumed jumps to 10 GB. The reserved space is not available to other VMs. |
| After use | — | Once the VM asks for memory and is served, the physical RAM stays reserved, even if the VM is idle for days. The page is effectively locked. |

- Before the VM asks for memory, ESXi does not back the reservation with physical RAM.

## Limit
- Not visible to the Guest OS.
- Result is unpredictable. Can cause a worse performance problem than reducing the VM configuration.
- CPU limit: impacts the CPU Ready counter.
- Memory limit: set in the VMX file as `sched.mem.max`.

## Entitlement
- What the VM is entitled to. A dynamic value determined by the hypervisor.
- Changes every second.
- Determined by the VM's own limit, shares and reservation, and by the shares and allocations of other VMs on the same host.
- A VM cannot use more than ESXi entitles it.
```text
Usage <= Entitlement   (at any point in time)
```
- Healthy host (enough resources for all VMs, with headroom) and a highly utilized VM → Entitlement ≈ Usage.
- Low-utilized VM → Entitlement much higher than Usage.

### How memory entitlement is set under overcommit
- Without overcommit, a VM gets all the memory it touches, up to its configured size. The configured size is an implicit limit: a 1 GB VM with a 2 GB limit never gets more than 1 GB.
- Under overcommit, each VM gets an amount between its reservation and its limit, set from two inputs:
  - its shares (a modified proportional-share policy);
  - its estimated working set (Active), sampled every 60 seconds by default (Mem.SamplePeriod).
- The working-set estimate rises fast and falls slowly, so a VM whose idle memory was reclaimed can ramp back up quickly.
- Idle memory tax: idle pages are charged more than active ones, progressively as the idle-to-active ratio rises. A VM with many shares but little activity loses idle memory first. Changing Mem.IdleTax is rarely appropriate.

### Default CPU shares
- Default CPU shares are per vCPU: Low, Normal and High are in the ratio 1:2:4 per vCPU.
- With default settings, a 1-vCPU VM gets half the CPU share of a 2-vCPU VM under contention.

### Why Usage can appear slightly above Entitlement
- Reporting technique, not a real violation.
- vCenter reports Usage in % as the average over the sample period.
- vCenter reports Entitlement in MHz as the latest value in the sample period.
- For a highly utilized vCPU, the average can be slightly above the latest value.

## Traps
- "CPU reservation shows up in CPU usage" → wrong. CPU reservation is on demand and not in utilization metrics.
- "High Memory Consumed means the VM is actively using that memory" → not necessarily. Reservation is counted in Consumed.
- Using a limit instead of right-sizing → unpredictable; the guest cannot see the limit.

## Metadata
```yaml
id: vsphere/foundations/resource-management
retriever_guide: how-it-works
scope: vsphere
technology:
- cpu
- memory
- storage
- network
pillar:
- performance
- capacity
product:
- vsphere
object:
- VirtualMachine
- HostSystem
internal_derive: []
related:
- foundations/terminology
- vsphere/cpu/metrics/comparisons/consumption-metrics
- vsphere/memory/metrics/virtual-motherboard/usage
source:
  document: PART 3 - Counters.docx
  path: The World of Metrics > Metrics Nuances > Virtualization Impact > Resource Management
corrections:
- '2026-11-02: Shares apply at two scheduler levels: cluster and host.'
- '2026-11-02: Memory reservation: Consumed counts the reservation; physical RAM is backed on first use, then stays locked. Confirmed by author.'
- '2026-11-02: Metric-type table, CPU row: Utilization in thread and Hertz, Reservation in Hertz, Allocation in vCPU. Uploaded document leaves CPU Reservation and Allocation cells unlabelled.'
review_notes:
- 'Sections ''How memory entitlement is set under overcommit'', ''Default CPU shares'': from the vSphere 9.1 documentation, vSphere Resource Management > CPU Virtualization, How ESX Hosts Allocate Memory, Memory Tax for Idle Virtual Machines, Edit Settings (pp. 1825-1827, 1838-1839). Shares per vCPU (Normal = 1,000 per vCPU) is Claude''s own knowledge; the documentation states equal share per vCPU and the 1:2:4 ratio.'
- 'Section ''Reservation: CPU vs memory'': the vSphere 9.1 documentation (Virtual Machine Memory, pp. 1833-1834) says that until the VM touches all memory within its reservation, the VMkernel can give the untouched part to other VMs. The table says the reserved space is not available to other VMs. Open question Q047.'
- Cluster-level shares scope (siblings under the same parent resource pool) is from Claude's own knowledge (section: Two scheduler levels, Cluster row). Confirm.
status: draft
```
