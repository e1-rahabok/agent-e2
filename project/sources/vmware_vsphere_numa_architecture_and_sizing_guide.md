# VMware vSphere NUMA Architecture and Sizing Guide
**Applies to:** VMware vSphere / ESXi 9.1 (Hardware Version 20+)

## 1. Introduction: The Necessity of NUMA in Modern SoCs

In modern System on a Chip (SoC) and multi-chiplet processor designs, the concept of Non-Uniform Memory Access (NUMA) is more critical than ever. While all CPU cores on a single physical package share physical pathways to all memory DIMMs via internal die fabrics, these paths are not equal. 

Traversing a silicon interposer to access a distant memory controller introduces two major performance penalties:
1.  **Hop Latency:** Electrical signals take longer to cross physical die boundaries compared to local pathways.
2.  **Fabric Congestion:** If execution threads consistently fetch memory across the central crossbar, the finite bandwidth of the internal switch bottlenecks under high utilization.

To mitigate this, ESXi relies on physical and virtual NUMA boundaries to align a virtual machine's CPU execution threads with the closest physical memory controllers.

---

## 2. Physical Architecture & Optimal Hypervisor Baselines

Host-level BIOS configuration is the foundation of vNUMA performance. Processors must be partitioned logically to restrict cross-die memory access.

### AMD EPYC 9005 Series (Zen 5 / Turin)
*   **Architecture:** Up to 16 Core Complex Dies (CCDs) connected to a single, centralized I/O Die (IOD). 12 DDR5 memory channels.
*   **Optimal Setting:** **NPS4** (Nodes Per Socket 4). This divides the socket into 4 logical NUMA domains, each owning 3 memory channels.

### Intel Xeon 6 (Granite Rapids AP / 6900P)
*   **Architecture:** Up to 3 Compute Tiles connected to 2 I/O Tiles. Memory controllers are integrated directly into the Compute Tiles. 12 DDR5 memory channels.
*   **Optimal Setting:** **SNC3** (Sub-NUMA Clustering 3). This divides the socket into 3 logical NUMA domains, each owning 4 memory channels.

### AMD EPYC 9006 Series (Zen 6 / Venice) - e.g., EPYC 9996
*   **Architecture:** 8 CCDs featuring 32 cores per CCD (256 cores total). Zen 6 introduces a split-IOD design, utilizing 2 IODs per socket. 16 DDR5 memory channels.
*   **Optimal Setting:** **NPS2**. The hypervisor maps the two logical NUMA nodes directly to the two physical IOD boundaries. Each node controls 128 cores and 8 memory channels.

---

## 3. Large VM Sizing and Placement Rules

When sizing large ("monster") VMs, the hypervisor's ability to schedule memory efficiently dictates performance. 

### Rule 1: Memory Divisibility
To ensure symmetrical vNUMA nodes, a VM's configured memory must be evenly divisible by the physical NUMA topology of the host. Asymmetrical vNUMA topologies cause unpredictable latency.
*   **For AMD NPS4 Hosts:** VM memory must be divisible by **4**.
*   **For Intel SNC3 Hosts:** VM memory must be divisible by **3**.
*   **For AMD NPS2 Hosts:** VM memory must be divisible by **2**.

### Rule 2: Containment (Example: AMD EPYC 9996)
Whenever possible, size a VM so it fits within a single physical NUMA boundary. 

**Scenario A: 32 vCPU VM on EPYC 9996**
*   **Placement:** The VM fits entirely inside a single 32-core Zen 6 CCD.
*   **Memory Access:** It can safely be allocated up to **50% of the total physical socket memory** (the maximum memory controlled by the local IOD in an NPS2 configuration).
*   **Advantage:** Zero cross-CCD L3 cache latency; zero remote-IOD memory fetches.

**Scenario B: 64 vCPU VM on EPYC 9996**
*   **Placement:** The VM requires two 32-core CCDs. ESXi will place both CCDs behind the *same* physical IOD to keep them within a single NUMA node (which holds up to 128 cores). 
*   **Topology Presentation:** Because it does not cross an IOD boundary, the VM should be presented to the Guest OS as a **UMA (Uniform Memory Access)** machine (a single vNUMA node).
*   **Memory Limits:** The memory allocation must remain under the 50% total socket threshold. If sized larger, the hypervisor will fetch remote memory from the neighboring IOD, inducing cross-fabric latency.

---

## 4. ESXi 9.1 Configuration and Administration

Starting with Virtual Hardware Version 20 (introduced in vSphere 8 and continuing through vSphere 9.1), VMware overhauled how vNUMA topology is managed, moving away from legacy static assignments.

### The `numa.autosize.once` Parameter
*   **Legacy Behavior:** Historically, ESXi calculated the vNUMA topology on the first power-on and locked it (`TRUE`). This prevented unexpected OS topology changes but caused severe performance degradation if the VM was later migrated to a host with a different physical architecture.
*   **Current ESXi 9.1 Behavior:** The default value is now **`FALSE`**. The ESXi CPU scheduler dynamically re-evaluates and rebuilds the optimal vNUMA topology on *every* power cycle to ensure alignment with the current physical host.

### Cluster-Wide vNUMA Persistence (IaaS Environments)
For Cloud Providers or administrators who require the legacy behavior (locking the topology to prevent guest OS disruptions upon reboot), do not use individual VMX parameters. 
*   Navigate to **vCenter -> Cluster -> Configure -> Advanced Settings**.
*   Add or set the advanced parameter `VPXD_PersistVnuma` to `True`.

### UI Changes in vSphere 9.1
Administrators will no longer find `numa.autosize.once` or similar legacy attributes readily available or supported in the Advanced Parameters VMX configuration screen. 
*   Do not inject manual `numa.*` attributes via the Advanced Settings tab.
*   Instead, utilize the natively integrated **vNUMA Topology** menu located within the primary **Edit Settings -> Virtual Hardware -> CPU** dropdown for any required manual topology overrides.