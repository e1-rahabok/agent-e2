# VMware ESXi 9.1 Memory Reclamation & State Machine Technical Manual

## 1. Executive Summary & Overview

VMware ESXi relies on the VMkernel memory manager (`VMKMEM`) to handle host physical memory allocation and reclamation dynamically. To prevent hypervisor thrashing and ensure stable virtual machine performance, ESXi enforces a state-driven memory reclamation model based on threshold percentages of the minimum free memory limit ($\text{minFree}$).

Beginning in ESXi 6.0 and maintained through ESXi 7.x, 8.x, and 9.1, ESXi incorporates **hysteresis logic** into its memory state transitions. State boundaries are asymmetric: entering a higher-pressure state occurs at a lower percentage threshold, while exiting back to a lower-pressure state requires memory recovery to a higher percentage threshold.

---

## 2. Mathematical Definition of $\text{minFree}$

The parameter $\text{minFree}$ represents the baseline amount of physical RAM that VMkernel reserves exclusively for its critical system processes. It is calculated automatically during host boot based on total host capacity.

For modern hosts, $\text{minFree}$ is computed non-linearly across memory tiers (roughly $890\text{ MB}$ for the first $4\text{ GB}$, plus $1\%$ to $2\%$ of additional capacity up to scaling caps).

### Example Reference Table (1 TB Host)
For a host equipped with $1\text{ TB}$ ($1,024\text{ GB}$) of physical RAM:
$$\text{minFree} \approx 10.8\text{ GB}$$

---

## 3. The State Machine & Hysteresis Thresholds

The state machine consists of five discrete operational states: **High**, **Clear**, **Soft**, **Hard**, and **Low**. 

Hysteresis ensures that temporary memory allocation spikes do not cause rapid oscillation ("flapping") between memory states.

```
       [ HIGH STATE ]  (Normal Execution)
             |
   Free RAM  | Drop below 300% minFree
   Decreases v
       [ CLEAR STATE ] (Page Splitting Active)
             |
   Free RAM  | Drop below 64% minFree
   Decreases v
       [ SOFT STATE ]  (Ballooning Active)
             |
   Free RAM  | Drop below 32% minFree
   Decreases v
       [ HARD STATE ]  (Compression & Hypervisor Swapping Active)
             |
   Free RAM  | Drop below 16% minFree
   Decreases v
       [ LOW STATE ]   (Allocations Blocked)

=======================================================
RECOVERY REVERSE PATH (Requires higher % to step up):
- LOW   --> HARD:  Recovery above 24% minFree
- HARD  --> SOFT:  Recovery above 48% minFree
- SOFT  --> CLEAR: Recovery above 100% minFree
- CLEAR --> HIGH:  Recovery above 400% minFree
=======================================================
```

---

## 4. State Matrix & Actionable Thresholds

| State | Entry Threshold (Increasing Pressure) | Exit Threshold (Decreasing Pressure) | Threshold Volume (1 TB Host, $\text{minFree} = 10.8\text{ GB}$) | Active Reclamation Mechanisms |
| :--- | :--- | :--- | :--- | :--- |
| **High** | $\text{Free} > 300\%\text{ of }\text{minFree}$ | $\text{Free} > 400\%\text{ of }\text{minFree}$ | $> 43.2\text{ GB}$ (To enter High from Clear) | None. 2 MB large pages mapped directly. |
| **Clear** | $\text{Free} \le 300\%\text{ of }\text{minFree}$ | $\text{Free} \le 400\%\text{ of }\text{minFree}$ | $32.4\text{ GB} \le \text{Free} \le 43.2\text{ GB}$ | Breaks $2\text{ MB}$ large pages into $4\text{ KB}$ small pages. TPS candidate scanning begins. |
| **Soft** | $\text{Free} \le 64\%\text{ of }\text{minFree}$ | $\text{Free} \le 100\%\text{ of }\text{minFree}$ | $6.9\text{ GB} \le \text{Free} \le 10.8\text{ GB}$ | Active Memory Ballooning (`vmmemctl`) inside guest operating systems. |
| **Hard** | $\text{Free} \le 32\%\text{ of }\text{minFree}$ | $\text{Free} \le 48\%\text{ of }\text{minFree}$ | $3.5\text{ GB} \le \text{Free} \le 5.2\text{ GB}$ | Memory Compression Engine active. Hypervisor swap (`.vswp`) initiated. Ballooning stops inflating. |
| **Low** | $\text{Free} \le 16\%\text{ of }\text{minFree}$ | $\text{Free} \le 24\%\text{ of }\text{minFree}$ | $< 1.7\text{ GB}$ | All previous mechanisms active + New VM memory allocation requests blocked. |

---

## 5. Key reclamation Mechanisms Explained

### 5.1 Large Page Breaking & Transparent Page Sharing (TPS)
* **Trigger State:** Clear
* **Operation:** ESXi default behavior prioritizes allocating $2\text{ MB}$ backing pages for guest performance. When memory transitions to **Clear**, the host stops backing new requests with large pages and breaks existing unused large pages into $4\text{ KB}$ small pages to facilitate inter-VM and intra-VM deduplication (TPS).

### 5.2 Memory Ballooning (`vmmemctl`)
* **Trigger State:** Soft
* **Operation:** The VMkernel inflates the balloon driver inside virtual machines. The guest OS selects unallocated memory pages and hands them to the driver, allowing ESXi to reclaim those underlying physical host pages without guest performance impact.

### 5.3 Memory Compression Engine
* **Trigger State:** Hard
* **Operation:** If guest pages cannot be reclaimed via ballooning, candidate pages are compressed and stored in a designated memory compression cache within host RAM. Decompression is significantly faster than swapping to disk.

### 5.4 Hypervisor Swapping (`.vswp`)
* **Trigger State:** Hard / Low
* **Operation:** As a last resort before memory exhaustion, ESXi writes uncompressed guest pages directly to the VM's `.vswp` file on storage. This introduces major disk latency penalties.

---

## 6. Verification and Diagnostics Commands

To inspect the host memory state, calculate exact thresholds, and monitor active state transitions in ESXi 9.1:

### 6.1 `vsish` VMkernel Shell Query
Interrogate the internal VMkernel memory structure directly:

```bash
# Query total memory, minFree, and active state
vsish -e get /memory/memInfo
```

**Sample Output Snippet:**
```text
Memory Information {
   Physical Memory:274877906944 bytes (256.0 GB)
   Min free:2831155 KB (2.7 GB)
   State: High
}
```

### 6.2 `esxtop` Interactive Monitor
Launch `esxtop` to view real-time state flags:

1. SSH into the ESXi host.
2. Run `esxtop`.
3. Press `m` to switch to the **Memory Panel**.
4. Check the top summary header:

```text
PMEM /MB: 262144 total, 245000 used, 17144 free, state: high
```

---

## 7. Operational Best Practices

1. **Maintain Host Utilization Below Clear Threshold:** Target host baseline memory consumption to remain above $400\%\text{ of }\text{minFree}$ free memory to maintain $2\text{ MB}$ backing performance benefits.
2. **Avoid Hypervisor Swapping:** If host logs report **Hard** or **Low** memory states, add physical host capacity, migrate workloads via vMotion, or lower VM memory reservations.