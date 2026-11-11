# Resource controls

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

## Allocation vs reservation
- Allocation: what a consumer is given (configured vCPU, memory). Not guaranteed. A maximum: utilization cannot exceed it.
- Reservation: a guarantee. A minimum. Utilization can stay below it.
```text
utilization <= allocation
reservation is guaranteed; utilization may be < reservation
```
- Allocation can be overcommitted, because it is not a guarantee. Reservation cannot, because it is one.
- Mixed names are invalid: "Allocation Reservation" is meaningless; "Maximum Reservation" means allocation; "Minimum Allocation" means reservation.

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
- CPU reservation matters only under contention. When the host has enough CPU for every VM, each VM gets its runtime with or without a reservation. Like a restaurant with free seats: a booking without a named table changes nothing.
- The total CPU reservation on an ESXi host is capped at the host's base (nominal) clock speed × cores. A CPU has 3 frequencies: base, All-Core Turbo, single-core Turbo. ESXi guarantees a reservation only from the base frequency, because Turbo is not guaranteed. A conservative design.
- Reservation is a guarantee. It takes effect at the provider (ESXi), where the reservation is held.
- It behaves differently for CPU and memory.

| Aspect | CPU reservation | Memory reservation |
|---|---|---|
| When it applies | On demand, and only under contention. If the VM does not use CPU, or the host has enough CPU for every VM, the reservation does not come into play. | Also on demand: only memory the VM has touched is held. Once touched, it stays held. |
| Effect on utilization metrics | None. Run, Used, Demand, Usage do not include it. They are 0 or near 0 if the Guest OS is not running. | None at power-on. Consumed grows as the VM touches memory; it does not jump to the reservation. |
| Example: 16 GB VM, powered on, sitting at BIOS | CPU metrics ≈ 0. | 10 GB reservation → VM Memory Consumed stays low. Until the VM has touched all memory within its reservation, the VMkernel can give the untouched part to other VMs. |
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
- The VM's shares are shared among its vCPUs: a busy vCPU beside an idle sibling gets the idle sibling's part too. See [`sp5-framework/performance/noisy-neighbour`](../../sp5-framework/performance/noisy-neighbour.md).

### Why Usage can appear slightly above Entitlement
- Reporting technique, not a real violation.
- vCenter reports Usage in % as the average over the sample period.
- vCenter reports Entitlement in MHz as the latest value in the sample period.
- For a highly utilized vCPU, the average can be slightly above the latest value.

## Misconceptions
- "CPU reservation shows up in CPU usage" → wrong. CPU reservation is on demand and not in utilization metrics.
- "High Memory Consumed means the VM is actively using that memory" → not necessarily. Reservation is counted in Consumed.
- Using a limit instead of right-sizing → unpredictable; the guest cannot see the limit.

## Metadata
```yaml
id: vsphere/architecture/resource-controls
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
- glossary
- vsphere/technology/cpu/metrics/comparisons/consumption-metrics
- vsphere/technology/memory/metrics/virtual-motherboard/usage
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: The World of Metrics > Metrics Nuances > Virtualization Impact > Resource Management
corrections:
- 'Sections Reservation: CPU vs memory: CPU reservation capped at base clock speed × cores, and applies only under contention (quiz CPU Q8 key options A and B).'
- '2026-11-02: Shares apply at two scheduler levels: cluster and host.'
- 'Section ''Reservation: CPU vs memory'': memory reservation is also on demand. Consumed does not jump to the reservation at power-on; until the VM has touched all memory within its reservation, the VMkernel can allocate the untouched part to other VMs; touched reserved memory is kept, even when idle. Verified on a live vCenter; corrects the book and the 2026-11-02 entry.'
- '2026-11-02: Metric-type table, CPU row: Utilization in thread and Hertz, Reservation in Hertz, Allocation in vCPU. Uploaded document leaves CPU Reservation and Allocation cells unlabelled.'
review_notes:
- 'To check: Section ''Default CPU shares'': Normal = 1,000 shares per vCPU; the documentation states equal share per vCPU and the 1:2:4 ratio. Sections ''How memory entitlement is set under overcommit'' and ''Default CPU shares'' are from the vSphere 9.1 documentation, vSphere Resource Management > CPU Virtualization, How ESX Hosts Allocate Memory, Memory Tax for Idle Virtual Machines, Edit Settings (pp. 1825-1827, 1838-1839).'
- 'To check: Section ''Two scheduler levels'', Cluster row: cluster-level shares scope (siblings under the same parent resource pool).'
status: draft
```
