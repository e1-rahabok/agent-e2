# Resource controls

## Controls
| Control | Nature |
|---|---|
| Reservation | Absolute. A guarantee (minimum). |
| Limit | Absolute. A cap (maximum). |
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

## Shares
- Shares act only under contention, when demand exceeds supply. Without contention each VM gets its demand.
- Shares divide only what is left after reservations: with 80% of a host reserved, shares divide the other 20%.
- Relative to siblings (VMs or resource pools under the same parent) at the cluster level, and to the other VMs at the host level (section Two scheduler levels).
- Default VM shares are proportional to configured size: per vCPU for CPU, per MB for memory. A VM 10x bigger gets 10x the shares.

| Level | VM CPU (per vCPU) | VM memory | Pool CPU | Pool memory |
|---|---|---|---|---|
| Low | 500 | 5 per MB | 2,000 | 81,920 |
| Normal | 1,000 | 10 per MB (10,240 per GB) | 4,000 | 163,840 |
| High | 2,000 | 20 per MB | 8,000 | 327,680 |

- A Normal resource pool weighs as much as a Normal VM with 4 vCPU and 16 GB: 4,000 = 4 × 1,000; 163,840 = 10 × 16,384 MB. Against a 1-vCPU, 1-GB sibling VM it gets 4x the CPU shares and 16x the memory shares; against one 8-vCPU, 32-GB sibling VM it gets half.
- A VM's shares are shared among its vCPUs: a busy vCPU beside an idle sibling gets the idle sibling's part too ([`sp5-framework/performance/noisy-neighbour`](../../sp5-framework/performance/noisy-neighbour.md), section CPU).
- Resizing a VM in the vSphere Client recalculates default shares; resizing through the API does not. Shares set by hand keep their number after a resize.
- A share number is relative: a VM moved to another cluster keeps its number, but the number means another share there.
- Example: a host of 4 cores × 2.5 GHz = 10 GHz, Hyper-Threading off. VM A has 2 vCPU (2,000 shares), VM B has 4 vCPU (4,000 shares); both demand all their vCPUs, 15 GHz together. Split 1:2: VM A gets 3.33 GHz and VM B 6.67 GHz, 1.67 GHz per vCPU for both. Default shares give every vCPU the same runtime; only custom shares per class change that. If total demand is 10 GHz or less, each VM gets its demand.

## Controls per resource
- CPU and memory: reservation, limit and shares on the VM (Edit Settings → CPU, Memory).
- Disk: an IOPS limit and shares per virtual disk; no reservation for IOPS or throughput.
- Network, two controls:
  - Network I/O Control v3 on a distributed switch: each VM network adapter has shares (1-100), a reservation (Mbps) and a limit, set in the VM's network adapter settings. A VM configuration property.
  - Traffic shaping per port group or port: average, peak and burst. A distributed switch shapes in and out; a standard switch outbound only. A port group policy, not a VM property.
  - The lower of the two wins: a 200 Mbps adapter limit under a 100 Mbps shaping average gives 100 Mbps.
  - Network I/O Control is off when Network Offloads compatibility is on; SR-IOV is not available with Network I/O Control v3.
  - A vNIC reservation is checked by the distributed switch, DRS and HA admission control: HA restarts a VM only on a host that meets its vNIC reservation.

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

### Why Usage can appear slightly above Entitlement
- Reporting technique, not a real violation.
- vCenter reports Usage in % as the average over the sample period.
- vCenter reports Entitlement in MHz as the latest value in the sample period.
- For a highly utilized vCPU, the average can be slightly above the latest value.

## Misconceptions
- "CPU reservation shows up in CPU usage" → wrong. CPU reservation is on demand and not in utilization metrics.
- "High Memory Consumed means the VM is actively using that memory" → not necessarily. Reservation is counted in Consumed.
- Using a limit instead of right-sizing → unpredictable; the guest cannot see the limit.
- "Shares guarantee CPU" → shares act only under contention, and only on what reservations leave. A reservation is the guarantee.
- "2,000 shares means the same priority on every cluster" → shares are relative to siblings; the same number is another share elsewhere.
- "There is no network limit on a VM" → Network I/O Control gives each VM network adapter a limit, a reservation and shares; traffic shaping caps the port group.
- "Default shares give a bigger VM priority" → per vCPU the runtime is equal; a bigger VM gets more in total because it has more vCPUs.

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
- vsphere/object-types/vm/configuration/resource-settings-guidance
- vsphere/object-types/resource-pool/configuration/resource-pool-design
- vsphere/technology/network/concepts/netioc
source:
  document: Private Cloud Management by Iwan Rahabok (https://isvara.io/download)
  path: The World of Metrics > Metrics Nuances > Virtualization Impact > Resource Management
corrections:
- 'Sections Reservation: CPU vs memory: CPU reservation capped at base clock speed × cores, and applies only under contention (quiz CPU Q8 key options A and B).'
- '2026-11-02: Shares apply at two scheduler levels: cluster and host.'
- 'Section ''Reservation: CPU vs memory'': memory reservation is also on demand. Consumed does not jump to the reservation at power-on; until the VM has touched all memory within its reservation, the VMkernel can allocate the untouched part to other VMs; touched reserved memory is kept, even when idle. Verified on a live vCenter; corrects the book and the 2026-11-02 entry.'
- '2026-11-02: Metric-type table, CPU row: Utilization in thread and Hertz, Reservation in Hertz, Allocation in vCPU. Uploaded document leaves CPU Reservation and Allocation cells unlabelled.'
review_notes:
- 'Section ''Shares'': default values from the vSphere Web Services API, SharesInfo.Level, and vSphere 9.1 documentation, Create a Resource Pool; the pool-weight explanation and the example (Q108) are not in the book. Section ''Controls per resource'', network: vSphere 9.1 documentation (What is vSphere Network I/O Control; Defining Bandwidth Requirements for a Virtual Machine; Traffic Shaping Policy; Factors Considered for Virtual Machine Restarts) (Q109).'
- 'Section ''How memory entitlement is set under overcommit'' is from the vSphere 9.1 documentation, vSphere Resource Management > CPU Virtualization, How ESX Hosts Allocate Memory, Memory Tax for Idle Virtual Machines, Edit Settings (pp. 1825-1827, 1838-1839).'
- 'To check: Section ''Two scheduler levels'', Cluster row: cluster-level shares scope (siblings under the same parent resource pool).'
status: draft
```
