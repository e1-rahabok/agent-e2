# Architectural Architectural Trade-Offs and Guest-Blind Decoupling in Hypervisor-Level Memory Tiering


Modern hypervisor memory tiering over NVMe/CXL expands addressable host capacity by dynamically partitioning virtual machine memory into Tier 0 (DRAM) and Tier 1 (NVMe). However, by operating purely at the hardware MMU layer via Extended/Nested Page Table (EPT/NPT) Access and Dirty (A/D) bit tracking, the hypervisor remains entirely decoupled from Guest OS internal memory state. 

This paper examines the structural limitations of this "guest-blind" approach—including the suppression of paravirtualized ballooning (`vmmemctl`), unallocated non-zeroed memory inflation, asymmetric hysteresis during capacity drops, and unnecessary NVMe write endurance degradation. We contrast this model with paravirtualized free-page reporting architectures and define mitigation strategies for enterprise workloads.

---

## 1.0 Evolution of Memory Reclamation

Hypervisor memory management has evolved from reactive, emergency reclamation techniques to proactive, hierarchical tiering. Historically, ESXi relied on a strict reclamation pipeline when physical DRAM approached exhaustion (~99.1% DRAM consumed / `minFree` soft thresholds): Transparent Page Sharing (TPS) for deduplication, guest-cooperative memory ballooning (`vmmemctl`), memory compression, and hypervisor swapping.

With the introduction of Memory Tiering over NVMe in ESXi 9.x, the hypervisor shifts from emergency page eviction to continuous capacity expansion. By treating local fast NVMe devices or CXL-attached memory as a secondary page store, ESXi expands total addressable host memory to a ratio up to 1:1 against physical DRAM. However, this shift alters the fundamental relationship between hypervisor page scheduling and guest OS kernel memory semantics.

---

## 2.0 Architecture of ESXi Memory Tiering

ESXi memory tiering operates transparently below the Guest OS abstraction layer. The architecture relies on three primary kernel mechanisms:

* **Activation & Demotion Thresholds:** The page-heat scanner initiates background demotion from Tier 0 (DRAM) to Tier 1 (NVMe) once host physical DRAM consumption reaches approximately **80%**. This 20% DRAM headroom buffer is deliberately maintained to ensure immediate, zero-latency allocation for incoming VM working sets and hardware DMA structures.
* **Page-Heat Tracking via Hardware MMU:** Page classification is performed at $4\text{ KB}$ granularity using physical CPU EPT/NPT Access and Dirty (A/D) hardware bits. Pages are categorized along a temporal frequency/recency decay curve into hot, warm, cold, and very cold states.
* **Asynchronous Demotion vs. Fault-Driven Promotion:** Cold pages are demoted to Tier 1 asynchronously in the background. When a guest vCPU attempts to read or write a demoted page, an EPT page fault triggers a synchronous microsecond-scale read from Tier 1, promoting the page back to Tier 0 DRAM.

---

## 3.0 Limitations of Guest-Blind Tiering

While hardware transparency guarantees universal compatibility across any guest operating system without requiring guest agents or drivers, it introduces severe micro-architectural blind spots.

### 3.1 Unallocated Non-Zeroed Memory Inflation
Modern guest OS kernels (such as Linux and Windows Server) allocate memory dynamically to user-space processes. When a process terminates or frees a memory block, the guest kernel returns those physical frames to its internal buddy allocator or free-list. However, unless the guest kernel explicitly zeroes those freed pages or issues hypervisor trim hints, the underlying physical host frames remain marked as allocated in the hypervisor's EPT structures.

Because these freed pages are no longer touched by guest application threads, their hardware A/D bits decay to zero. The ESXi page-heat scanner classifies them as "verified cold memory" and demotes them to Tier 1 NVMe. This results in **garbage page tiering**: PCIe bus bandwidth and NVMe NAND write cycles are wasted to store data that the Guest OS already considers unallocated.

### 3.2 Asymmetric Hysteresis and Reverse-Migration Inertia
ESXi memory tiering exhibits extreme asymmetric hysteresis:
* **Demotion Trigger:** Proactive and aggressive at ~80% DRAM consumption.
* **Promotion Trigger:** Strictly demand-driven (EPT page fault upon vCPU access) or activity-rebalanced.

If host DRAM consumption drops from 90% down to 70% (due to VM shutdowns or vMotion migrations), cold pages belonging to remaining VMs stay pinned on Tier 1 NVMe. The VMkernel will not proactively drain cold pages back into free DRAM simply because DRAM capacity became available. From an infrastructure optimization perspective, the host maintains idle DRAM while active VMs retain pages on slower storage—a paradox created because moving unaccessed bytes yields zero immediate application latency benefit.

### 3.3 The Suppression of Guest-Cooperative Ballooning
Because memory tiering activates at ~80% DRAM consumption and expands the effective addressable pool to Tier 0 + Tier 1 capacity, physical DRAM rarely reaches the 99.1% `minFree` threshold required to trigger the `vmmemctl` balloon driver.

This effectively neutralizes guest-cooperative reclamation. Ballooning allows the guest OS kernel to apply semantic intelligence—discarding clean file system page caches and shrinking internal kernel structures—before physical memory is reclaimed. Memory tiering bypasses this semantic layer entirely, offloading raw $4\text{ KB}$ anonymous and file pages indiscriminately to NVMe based solely on hardware access timers.

---

## 4.0 Comparative Analysis

| Architectural Dimension | ESXi Memory Tiering (NVMe/CXL) | Legacy Guest Ballooning (`vmmemctl`) | Paravirtual Free-Page Reporting |
| :--- | :--- | :--- | :--- |
| **Operating Layer** | Hypervisor MMU (EPT/NPT A/D Bits) | Guest Kernel Module (OS Driver) | Guest Allocator + Paravirtual Bus |
| **Activation Point** | ~80% Host DRAM Consumed | ~99.1% Host DRAM Consumed (Emergency) | Continuous / On Allocation Release |
| **Guest OS Awareness** | **Transparent (Guest-Blind)** | Cooperative (Guest Kernel Aware) | Cooperative (Free-List Hinting) |
| **Page Selection Logic** | Hardware access recency/frequency decay | Guest OS page-cache eviction / OS swap | Unallocated kernel buddy-list frames |
| **Retrieval Latency Penalty** | Microsecond-scale (PCIe NVMe read fault) | Millisecond-scale (Guest disk vswp I/O) | Zero (Page returned instantly to host) |
| **Storage / Bus Overhead** | High NVMe NAND wear & PCIe DMA traffic | High Guest Virtual Storage I/O | Zero Storage I/O (Hypervisor drop) |

---

## 5.0 Engineering Rationale & Ecosystem Trade-Offs

Why did hypervisor architects choose a guest-blind hardware MMU model over enhancing `vmmemctl` with paravirtualized free-page reporting (such as Linux `virtio-balloon` with `VIRTIO_BALLOON_F_FREE_PAGE_HINT`)?

1. **Application-Level Heap Pre-Allocation:** Enterprise applications (e.g., Oracle DB, SAP HANA, Microsoft SQL Server, and Java Virtual Machines) pre-allocate up to 90% of guest vRAM at process startup and manage internal user-space free lists. To the Guest OS kernel, these memory pages appear permanently allocated and anonymous. A guest kernel free-page hint API would report 0 GB free, rendering paravirtualized reporting useless for major database workloads. Hardware EPT A/D tracking is the only mechanism capable of peering inside application-level heaps to identify cold blocks.
2. **Kernel Stability & Ecosystem Maintenance:** Hooking directly into the internal buddy-allocator paths of dozens of supported Windows Server builds and Linux kernel distributions without causing kernel panics or race conditions presents an immense software maintenance burden compared to robust hardware MMU traps.
3. **Zero-Page Deduplication Efficiency:** ESXi mitigates unallocated page tiering via Transparent Page Sharing (TPS). When guest kernels zero freed pages, TPS collapses those identical `0x00` frames in DRAM into a single shared physical reference, preventing them from consuming Tier 1 NVMe capacity.

---

## 6.0 Recommendations & Operational Guidelines

To prevent capacity skew and performance degradation in memory-tiered environments, enterprise infrastructure architects should implement the following engineering policies:

* **Workload Partitioning:** Strictly disable memory tiering on latency-critical database instances or real-time streaming engines by setting the VM advanced parameter `sched.mem.enableTiering = FALSE`.
* **Active Working Set Sizing:** Ensure the total active working set of all aggregated VMs on a host does not exceed 50% of the combined physical memory capacity (Tier 0 DRAM + Tier 1 NVMe).
* **Tier-Disabled Ratio Accounting:** When mixing tier-enabled and tier-disabled VMs on the same host, account for the fact that tier-disabled VMs lock Tier 0 DRAM exclusively, artificially accelerating the ~80% demotion threshold for remaining tier-enabled workloads.

---

## 7.0 References & Data Sources

1. Broadcom TechDocs (2026). *vSphere 9.1 Resource Management Guide: Administering Memory Resources and Memory Tiering over NVMe*. Broadcom Inc.
2. VMware Cloud Foundation Engineering Team (2026). *Why VMware Memory Tiering is Not Just Swapping to NVMe*. VMware Cloud Foundation Technical Blog.
3. Broadcom Knowledge Base (2026). *Understanding NVMe Memory Tiering Activation Thresholds and Monitoring in vSphere 9.x (KB 449016)*. Broadcom Support Portal.
4. VMware Cloud Foundation Engineering Team (2026). *NVMe Memory Tiering Design and Sizing on VMware Cloud Foundation 9 Part 7: Advanced Configuration*. VMware Cloud Foundation Technical Blog.
