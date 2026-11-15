# VMware ESXi Storage Subsystem Architecture

When a virtualized workload (running inside a Guest OS such as Windows or Linux) issues an unbuffered Direct I/O write to a virtual disk (`.vmdk`) backed by a local VMFS datastore on a physical motherboard-attached SSD, the **payload data block** still moves physically **exactly two times** across hardware boundaries:

1. **Transfer 1 (Host Physical RAM** $\rightarrow$ **Storage Controller Memory):** Initiated via Direct Memory Access (DMA) over the host PCIe bus directly from host RAM into the onboard SRAM/DRAM cache of the physical SSD/NVMe controller.
2. **Transfer 2 (Storage Controller Memory** $\rightarrow$ **Physical Flash Media):** Internal hardware write execution from device controller cache onto physical NAND flash cells.

### Why Virtualization Does Not Add Extra Payload Data Copies
x86 hardware virtualization utilizes **Extended Page Tables (EPT) / Nested Page Tables (NPT)**. Memory allocated by the Guest OS (Guest Physical Address or GPA) maps directly to actual Host Physical Addresses (HPA) in physical DRAM. 

When the Paravirtualized SCSI (`PVSCSI`) device driver inside the Guest OS submits an I/O request, the VMkernel translates the descriptor’s memory addresses from GPA to HPA. The physical storage controller’s DMA engine then reads data **directly** out of host DRAM (which is the exact physical location holding the guest memory page). The hypervisor does **not** copy the payload bytes into a secondary host buffer.

The virtualization layers added by VMware ESXi—including the PVSCSI virtual device emulation, VMM ring buffers, Virtual Machine File System (`VMFS`), Pluggable Storage Architecture (`PSA`), and ESXi native drivers—operate entirely within the **Control Plane**.

---

## 2. Fundamental Distinction: Control Plane vs. Data Plane in ESXi

| Dimension | Control Plane (Virtualization & Metadata) | Data Plane (Physical Data Payload) |
| :--- | :--- | :--- |
| **What moves?** | Command descriptors, SCSI CDBs, PVSCSI Ring Descriptors, File-to-LUN block maps, I/O requests (`scsi_cmnd`). | The raw application data bytes (e.g., $8\text{ KB}$ database page). |
| **Execution Space** | Guest Kernel, VMM (Virtual Machine Monitor), VMkernel address space (`esx-base`). | Host PCIe bus, Host DRAM (HPA), physical SSD controller cache, NAND flash chips. |
| **Physical Hops** | Traverses Guest OS stack $\rightarrow$ PVSCSI device emulation $\rightarrow$ VMkernel Storage Stack $\rightarrow$ Physical HBA driver. | **2 physical hops** (Host RAM $\rightarrow$ Controller SRAM/DRAM $\rightarrow$ Flash Cells). |
| **Payload Copying** | Zero payload data copying. VMkernel rewrites address descriptors from GPA to HPA. | Hardware DMA engine streams payload bytes across the physical PCIe bus without CPU involvement. |

---

## 3. Physical Spaces & Hardware Memory Mapping

Despite passing through a virtualized environment, there are only **three physical hardware locations** where the data payload resides.

```mermaid
flowchart TD
    S1["SPACE 1: Host system RAM (physical DRAM frame)<br/>Guest RAM (GPA) mapped to host RAM (HPA) via CPU EPT or NPT"]
    S2["SPACE 2: Physical storage controller memory<br/>Onboard NVMe controller or HBA DRAM or SRAM cache"]
    S3["SPACE 3: Physical storage media<br/>Non-volatile NAND flash cells on motherboard SSD"]

    S1 -->|"Physical hop 1: PCIe bus DMA read"| S2
    S2 -->|"Physical hop 2: flash controller write"| S3
```

### Memory Address Translation (GPA to HPA)
1. **User Application (Guest OS):** Allocates memory buffer at Virtual Memory Address (GVA).
2. **Guest Kernel:** Maps GVA to Guest Physical Address (GPA) and pins the page frame.
3. **VMkernel / PVSCSI Emulation:** Translates GPA to Host Physical Address (HPA) using hardware-assisted memory virtualization (Intel EPT or AMD NPT).
4. **Physical HBA Driver:** Constructs hardware Scatter-Gather List (SGL) containing the translated HPA pointers.
5. **Physical DMA Engine:** Fetches data directly from the physical DRAM location corresponding to HPA.

---

## 4. End-to-End Control Plane Traversal

This section traces a single SCSI write command from an application inside a VM down to the physical SSD.

```mermaid
flowchart TD
    subgraph GuestUser["Guest OS - user space"]
        N1["1. Application (SQL / Database)<br/>Write API with O_DIRECT or FILE_FLAG_NO_BUFFERING"]
    end
    subgraph GuestKernel["Guest OS - kernel space"]
        N2["2. Guest file system<br/>Offset to guest LBA"]
        N3["3. Guest block layer<br/>Packages request into bio or IRP"]
        N4["4. Guest PVSCSI driver<br/>Writes descriptor to PVSCSI command ring in shared RAM<br/>Rings virtual doorbell via MMIO or hypercall"]
    end
    subgraph Hypervisor["Hypervisor - VMM and VMkernel"]
        N5["5. VMM / virtual device layer<br/>Intercepts doorbell, translates GPA to HPA"]
        N6["6. VMFS file system layer<br/>.vmdk offset to VMFS physical block address"]
        N7["7. VMkernel storage core (FSS)<br/>Schedules scsi_cmnd in VMkernel queue"]
        N8["8. PSA / HPP path management<br/>Routes request"]
        N9["9. Physical native driver<br/>Converts to hardware protocol (nvme-pcie, vmw_ahci)<br/>Writes PCIe submission queue, rings hardware doorbell"]
    end

    N1 --> N2 --> N3 --> N4
    N4 -->|"Virtualization boundary"| N5
    N5 --> N6 --> N7 --> N8 --> N9
```

### Component Breakdown: Program vs. Memory Context

| Step | Component / Layer | Context / Space | Operation Performed on Command Descriptor |
| :--- | :--- | :--- | :--- |
| **1** | User Application | Guest User Space | Prepares data block in memory; calls system write API (`FILE_FLAG_NO_BUFFERING` / `O_DIRECT`). |
| **2** | Guest Filesystem | Guest Kernel Space | Translates file byte offset to Guest Logical Block Address (Guest LBA). |
| **3** | Guest PVSCSI Driver | Guest Kernel Space | Formats request into a SCSI command descriptor; writes to **PVSCSI Request Ring** (shared memory buffer). Writes to PVSCSI MMIO register. |
| **4** | Virtual Machine Monitor (VMM) | Hypervisor / VMM Context | Intercepts MMIO access; pulls descriptor from ring buffer; translates Guest Physical Address (GPA) pointers to Host Physical Address (HPA). |
| **5** | VMFS Filesystem (`vmfs.ko`) | VMkernel Execution Space | Maps `.vmdk` block offset to VMFS Datastore Logical Unit (LUN) block offset. Handles extent locking if allocation is dynamic. |
| **6** | File System Switch (FSS) | VMkernel Execution Space | Coordinates virtual disk file handles and passes command to the VMkernel Storage Core. |
| **7** | PSA / HPP Engine | VMkernel Execution Space | Routes I/O through **Pluggable Storage Architecture (PSA)** or **High Performance Plug-in (HPP)** for path optimization and queue depth checks. |
| **8** | Native Device Driver | VMkernel Driver Space | Translates VMkernel SCSI command into native storage controller format (e.g., `nvme-pcie`). Writes entry to physical controller Submission Queue. |
| **9** | Physical Storage Controller | Physical Hardware | Executes MMIO Doorbell write. Hardware DMA engine pulls payload data directly from physical RAM (HPA). |

---

## 5. ESXi Storage Queue Metrics (`esxtop` Analysis)

In a virtualized ESXi environment, storage queue statistics are monitored using **`esxtop`** (Storage View: `d` for disk adapters, `u` for LUNs, `v` for VMs). 

Unlike bare-metal operating systems which measure queue depth at a single driver boundary, ESXi breaks down latency and queuing across **four distinct layers**:

```mermaid
flowchart TD
    G["Guest OS application<br/>GAVG: total round trip seen by the VM"]
    K["ESXi VMkernel storage stack (PSA / HPP / device driver queues)<br/>QAVG: time waiting in VMkernel queues<br/>KAVG: kernel latency = QAVG + stack overhead"]
    D["Physical storage hardware, controller, disk<br/>DAVG: device latency"]

    G --> K --> D
```

### Key Latency & Queue Formulas in `esxtop`

$$
\text{GAVG} = \text{KAVG} + \text{DAVG}
$$

$$
\text{KAVG} = \text{QAVG} + \text{VMkernel Processing Latency}
$$

| Metric | Full Name | Location Tracked | What It Actually Measures |
| :--- | :--- | :--- | :--- |
| **`DAVG`** | Device Average Latency | Physical Hardware / HBA | Time (ms) elapsed from when ESXi submits a command to the physical controller until the controller returns execution completion. Represents pure hardware response time. |
| **`QAVG`** | Queue Average Latency | VMkernel Scheduler Queue | Time (ms) spent by an I/O request waiting in VMkernel software queues because hardware or device queue depth limits (`LUN Queue Depth`) have been reached. |
| **`KAVG`** | Kernel Average Latency | VMkernel Storage Stack | Total time (ms) an I/O spends inside the hypervisor stack (`KAVG` = `QAVG` + stack execution overhead). Should ideally be $< 1\text{ ms}$. |
| **`GAVG`** | Guest Average Latency | Guest OS / Virtual Device | Total round-trip latency (ms) experienced by the Virtual Machine. |

### Diagnostic Rule of Thumb for Storage Performance

* **High `DAVG` ($> 10\text{–}15\text{ ms}$), Low `KAVG`:** The physical storage drive or hardware controller is saturated or experiencing physical bottlenecks.
* **High `KAVG` / `QAVG` ($> 2\text{–}5\text{ ms}$), Low `DAVG`:** The hypervisor software queues are throttling requests. This usually occurs when the VM’s concurrent requests exceed configured device queue depths (e.g., `pvscsi` queue depth or `Disk.SchedNumReqOutstanding`).

