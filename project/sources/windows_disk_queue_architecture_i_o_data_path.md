# Windows Storage I/O Subsystem Architecture: Control Plane vs. Data Plane

## 1. Executive Summary & Core Answer

**Yes, your observation is mathematically and physically correct.** 

For unbuffered I/O (such as standard database writes performed by Microsoft SQL Server via `FILE_FLAG_NO_BUFFERING`), the actual **payload data block** (the raw bytes of data being written) is copied/transferred exactly **two times** across physical spaces:

1. **Transfer 1 (Host RAM $\rightarrow$ Storage Controller Cache):** Direct Memory Access (DMA) transfer over the PCIe/SATA bus from system RAM directly into the onboard SRAM/DRAM buffer of the storage controller.
2. **Transfer 2 (Storage Controller Cache $\rightarrow$ Physical Media):** Internal firmware transfer from the controller's onboard RAM onto the physical non-volatile media (NAND Flash cells or magnetic disk platters).

The 12 software layers often cited in Windows storage documentation represent the **Control Plane** (processing instructions, metadata, address translation, and queue management). They do **not** touch or move the underlying payload data. 

---

## 2. Fundamental Distinction: Control Plane vs. Data Plane

To understand Windows storage performance and metrics, the system architecture must be split into two decoupled concepts:

| Dimension | Control Plane (Metadata & Instructions) | Data Plane (Payload Data Movement) |
| :--- | :--- | :--- |
| **What moves?** | Memory addresses, Logical Block Addresses (LBAs), I/O Request Packets (IRPs), SCSI/NVMe command blocks. | The actual $8\text{ KB}$ database block (or data payload bytes). |
| **Where does it execute?** | Host CPU registers and system RAM allocated for OS kernel drivers. | PCIe bus, Direct Memory Access (DMA) engines, controller DRAM, and non-volatile media. |
| **Physical movement count** | Traverses 8–12 kernel driver modules via function calls. | **2 physical hops** (RAM $\rightarrow$ Controller $\rightarrow$ Media). |
| **Data copying involved?** | Zero payload data copying. Drivers manipulate standard kernel descriptors (Memory Descriptor Lists / MDLs). | DMA hardware engine moves bytes asynchronously without host CPU involvement. |

---

## 3. Physical Spaces (The Data Plane Path)

There are only **three distinct physical spaces** where the data block resides during the lifetime of a write operation.

```
+-------------------------------------------------------+
| SPACE 1: Host System Memory (RAM)                     |
| [ SQL Server Buffer Pool Memory (Pinned by OS MDL) ]  |
+-------------------------------------------------------+
                           |
                           |  Physical Hop #1: PCIe Bus DMA Read
                           v
+-------------------------------------------------------+
| SPACE 2: Storage Controller Memory                    |
| [ Onboard NVMe / Controller SRAM / DRAM Cache ]      |
+-------------------------------------------------------+
                           |
                           |  Physical Hop #2: Internal Write Execution
                           v
+-------------------------------------------------------+
| SPACE 3: Physical Storage Media                       |
| [ Non-Volatile NAND Flash Cells / Magnetic Platters ] |
+-------------------------------------------------------+
```

### Space 1: Host System RAM (User Buffer Pool)
* **Location:** System Main Memory (DRAM).
* **State:** SQL Server allocates and prepares the $8\text{ KB}$ block in its process buffer pool. When issuing unbuffered I/O (`FILE_FLAG_NO_BUFFERING`), the OS Kernel locks these virtual memory pages into physical RAM using a **Memory Descriptor List (MDL)**. This prevents the OS from paging out or moving the physical RAM pages while I/O is active.

### Hop 1: PCIe Bus Direct Memory Access (DMA) Transfer
* **Mechanism:** The host storage controller (e.g., NVMe host controller) reads the Physical Region Page (PRP) or Scatter Gather List (SGL) provided by the driver. The storage controller's onboard DMA engine pulls the data directly across the PCIe bus into device memory.
* **CPU Involvement:** $0\%$ CPU usage during the byte transfer.

### Space 2: Storage Controller Internal Cache
* **Location:** Onboard SRAM/DRAM of the NVMe SSD or SATA controller.
* **State:** The data resides transiently in volatile or battery/capacitor-backed controller RAM while the flash translation layer (FTL) determines physical target blocks, wear-leveling, and ECC calculations.

### Hop 2: Physical Media Flush
* **Mechanism:** Internal device bus transfers data from device cache into non-volatile storage elements.

### Space 3: Physical Non-Volatile Storage Media
* **Location:** Floating-gate / charge-trap NAND flash cells or magnetic platter domains.
* **State:** Permanent physical storage.

---

## 4. Software Execution Path (The Control Plane)

While the data payload resides statically in Space 1 waiting for the DMA engine, the host CPU executes software logic down the Windows driver stack to build the instructions required by the storage controller.

```
[ User Space ]
  └── 1. sqlservr.exe               -> Calls WriteFile() with buffer pointer & offset
[ Kernel Space ]
  ├── 2. ntdll.dll / ntoskrnl.exe    -> System Call Transition & IRP Allocation
  ├── 3. I/O Manager                -> Creates IRP, locks memory pages (MDL)
  ├── 4. ntfs.sys / refs.sys        -> File offset -> Logical Cluster Number (LCN)
  ├── 5. volmgr.sys                 -> LCN -> Volume Logical Block Address (LBA)
  ├── 6. partmgr.sys                -> Tracks queue metric! Partition LBA -> Disk LBA
  ├── 7. disk.sys                   -> Builds SCSI / Storage Request Block (SRB)
  ├── 8. storport.sys               -> Adapter queue management & protocol binding
  └── 9. stornvme.sys               -> Translates SRB to NVMe SQ entry & rings Doorbell
```

### Component Breakdown: Program vs. Space

| Step | Software Component (Program) | Memory / Context Space | Operation Performed on Instruction / Descriptor |
| :---: | :--- | :--- | :--- |
| **1** | `sqlservr.exe` | User Mode Process Address Space | Prepares data block in memory; passes buffer pointer, file handle, and size to `WriteFile API`. |
| **2** | `ntdll.dll` / Syscall | CPU Register / System Call Space | Executes CPU trap (`syscall`), transitioning thread state from User Mode to Kernel Mode. |
| **3** | I/O Manager (`ntoskrnl.exe`) | Kernel Space (Paged Pool) | Allocates an **I/O Request Packet (IRP)** header. Pins the buffer memory pages using a **Memory Descriptor List (MDL)**. |
| **4** | `ntfs.sys` | Kernel Space | Reads file allocation tables; translates file byte offset into Logical Cluster Number (LCN). |
| **5** | `volmgr.sys` | Kernel Space | Translates LCN to a Volume Logical Block Address (LBA). Handles RAID/software striping if present. |
| **6** | `partmgr.sys` | Kernel Space | Translates Volume LBA to Disk Physical LBA. **Applies Performance Counters tracking here.** |
| **7** | `disk.sys` | Kernel Space | Converts generic kernel IRP into a standardized **Storage Request Block (SRB)**. |
| **8** | `storport.sys` | Kernel Space | Handles OS-level queue management per device controller. Ensures driver queue depths are respected. |
| **9** | `stornvme.sys` | Kernel Memory / Device Register Space | Formats SRB into a 64-byte NVMe Command Descriptor. Writes physical RAM address to Submission Queue (SQ) and writes to hardware **Doorbell Register** via MMIO. |

---

## 5. Precise Location of `Avg. Disk Queue Length`

The Microsoft Windows metric **`Avg. Disk Queue Length`** is calculated at the **Partition Manager (`partmgr.sys`)** layer.

### What the Metric Tracks
`partmgr.sys` keeps an active count of all IRPs that pass down through it but have not yet returned an I/O completion status from below.

$$\text{Active IRPs at } \texttt{partmgr.sys} = \text{IRPs queued in software} + \text{IRPs actively in flight on hardware}$$

### Why Windows Uses Little's Law
Rather than sampling the instantaneous queue size continuously (which incurs high CPU overhead), Windows samples the stack state or computes the counter dynamically using **Little's Law**:

$$\text{Avg. Disk Queue Length} = \text{Disk Transfers/sec} \times \text{Avg. Disk sec/Transfer}$$

Where:
* **$\text{Disk Transfers/sec}$ ($\lambda$):** The arrival rate (IOPS) of IRPs passing through `partmgr.sys`.
* **$\text{Avg. Disk sec/Transfer}$ ($W$):** The average time elapsed (latency) between an IRP entering `partmgr.sys` and its completion back at `partmgr.sys`.

### Why the Metric Can Be Misleading
* **It does not mean files are waiting in a line:** A high queue length (e.g., Queue Length = 32 on modern NVMe drives) usually means the storage controller's hardware interface (which can handle 64,000 parallel queues) is executing 32 requests concurrently in hardware.
* **It measures instruction metadata concurrency, not data size:** An IRP for a $4\text{ KB}$ write and an IRP for a $1\text{ MB}$ write both equal exactly $1.0$ in queue length count while active.
```

I have completed generating the technical documentation detailing the Windows I/O path, clarifying the physical spaces versus software control components, and explaining the exact layer for the disk queue length metric. 

Let me know if you would like to explore any specific driver layer or NVMe hardware mechanics further!