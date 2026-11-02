# vSphere Golden Questions

These questions are used to evaluate how well the AI retrieves and answers from the knowledge base.

Add real questions that matter to experienced vSphere administrators.

## How to use

1. **Baseline:** ask each question to the AI *without* the knowledge base. Record the answer.
2. **With KB:** ask the same question with retrieval from `knowledge/`. Record the answer.
3. **Score** each answer against the key points (see rubric). Compare.

Each question is written so a generic AI is likely to fall into the listed trap.
The question text must not be changed to hint at the answer.

### Scoring rubric (per question, 0–3)

| Score | Meaning |
|-------|---------|
| 0 | Falls into the trap, or wrong |
| 1 | Avoids the trap, but cannot explain why |
| 2 | Correct, with the right reason (vantage point / mechanism) |
| 3 | Correct, right reason, and states what to check next |

Max score: 30.

---

## Set 1 — Metrics Nuances

Source: *PART 3 – Counters*, Chapter "The World of Metrics", section "Metrics Nuances".

### Q1 — Memory usage: VM vs ESXi

**Q:** Every VM on an ESXi host shows Memory Usage below 25% in vCenter. The host itself shows Memory Usage at 95%. The customer wants to buy more RAM. Is the host running out of memory?

**Tests:** Same name, different formula per object (distinction).
**Likely wrong answer:** "Yes, the host is nearly full, buy RAM" — or "the numbers are inconsistent, something is broken".
**Expected key points:**
- VM Memory Usage maps to **Active**. ESXi Memory Usage maps to **Consumed**. Cluster maps to Consumed + Overhead.
- Reason: 2-level memory hierarchy. VM level = what is actively used (performance). Host level = what VMs have claimed (capacity).
- High Consumed is not proof of shortage. Memory is a cache; near 100% is expected and is good use of money.
- This confusion has led customers to buy more RAM than needed.
- Check contention metrics, not Usage, to decide.

**Source:** Naming Complexity; Architecture Complexity (Memory).

---

### Q2 — High CPU Wait

**Q:** A VM shows CPU Wait at 90%. The application owner says the VM must be stuck waiting on disk or memory. Are they right?

**Tests:** Confusing name (distinction).
**Likely wrong answer:** "Yes, high wait means IO or memory bottleneck."
**Expected key points:**
- VM CPU Wait **includes idle time**.
- Most VMs do not run at 100%, so Wait is naturally high.
- The name is correct from the kernel scheduler's viewpoint: the vCPU is waiting to be used.
- High Wait alone does not indicate a bottleneck. Need other evidence (e.g. disk latency, memory contention).

**Source:** Naming Complexity (Confusing name).

---

### Q3 — CPU Latency without contention

**Q:** After a host BIOS power policy change, VM CPU Latency went up by about 15%. CPU Ready and Co-Stop are unchanged. Is the VM now suffering CPU contention?

**Tests:** Same name, different meaning (CPU Latency vs Disk / Memory Latency).
**Likely wrong answer:** "Yes, latency means the VM is waiting for CPU."
**Expected key points:**
- CPU Latency is affected by **CPU frequency**. Lower frequency raises it.
- The VM is running at a lower speed, but it is **not waiting to be served**. Like running on an older CPU.
- Unlike Disk Latency and Memory Latency, CPU Latency does not *always* mean a performance problem.
- Contrast: Linux Steal Time only includes CPU Ready. VM CPU Latency includes more factors, including frequency.
- Ready and Co-Stop being flat supports "no contention".

**Source:** Naming Complexity (Same name, different meaning; Same name, same purpose, different formula).

---

### Q4 — Hyper-Threading and two vantage points

**Q:** Two single-vCPU VMs are both fully busy, running on the two hardware threads of the same physical core. Each VM shows CPU Usage around 62.5%, not 100%. Is each VM only using 62.5% of what it needs? What does the host report for that core?

**Tests:** Same name, different meaning (consumer vs provider vantage point).
**Likely wrong answer:** "The VMs are under-utilised" — or "it's a reporting bug".
**Expected key points:**
- VM Used is HT-aware: when both threads run, the VM is charged with a **37.5% penalty**, so it shows ~62.5%.
- ESXi sees the core as fully busy (100%). ESXi Used is also HT-aware, with a different penalty (50%).
- Different numbers come from different vantage points: consumer (VM) vs provider (ESXi). Both are correct.
- ESXi Core Utilization shows 100% whether 1 or 2 threads run. Check **Thread Utilization** to tell which.

**Source:** Naming Complexity; Other Nuances (Formula).

---

### Q5 — Memory reservation vs CPU reservation

**Q:** A 16 GB VM with a 10 GB memory reservation and a 4 GHz CPU reservation is powered on and sits at the BIOS screen (no OS booted). What do its Memory Consumed and CPU usage metrics show?

**Tests:** Same name, different behaviour (principle: CPU vs memory are different in nature).
**Likely wrong answer:** "Both near 0, nothing is running" — or "both show the reserved amounts".
**Expected key points:**
- **Memory:** Consumed jumps to ~10 GB. Reservation is counted even though the pages are not actually used, because ESXi has set the space aside.
- Once a reserved page has been used, ESXi keeps it locked to the VM, even if the VM is idle for days.
- **CPU:** reservation is on-demand. Run, Used, Demand and Usage stay at 0 or near 0. CPU reservation does not affect utilization metrics.

**Source:** Resource Management.

---

### Q6 — Guest queue invisible to the hypervisor

**Q:** Oracle on a Windows VM is slow. Windows shows a high Disk Queue Length. In vCenter, the VM's disk IOPS and disk latency look normal. The storage team says storage is fine, so it is not an infrastructure problem. Is that conclusion valid?

**Tests:** Visibility layers (principle + diagram).
**Likely wrong answer:** "Yes, vSphere metrics are normal so the storage path is healthy."
**Expected key points:**
- Queues inside the Guest OS (layer A: disk queue, driver queue, etc.) are **not visible to the hypervisor**. The IO has not yet been sent down.
- So VM-level IOPS can **under-report** real demand.
- Normal vSphere metrics do not prove the IO path is healthy end to end. Look inside the Guest OS too.
- Mental model: Guest OS view Demand = A + B; VM view Demand = B + C + D.

**Source:** Visibility (layers A–D diagram).

---

### Q7 — VM availability

**Q:** A VM is powered on, but Windows inside it has crashed and is stuck on a blue screen. Is the VM available? How would you measure VM availability vs Guest OS availability?

**Tests:** Principle: a VM is a virtual motherboard, not the OS.
**Likely wrong answer:** "No, the VM is down."
**Expected key points:**
- A VM is a **virtual motherboard**, not a complete machine and not the OS.
- VM is unavailable in only 2 states: **powered off**, or **frozen** (clock paused, e.g. vMotion switchover, ~0.2 s when healthy).
- So the VM is available. The **Guest OS** is not.
- Guest OS availability needs OS-level checks, e.g. `sc query RpcSs` (Windows), `systemctl is-system-running` (Linux).
- OS-level metrics (processes, threads, system calls) do not apply to a VM.

**Source:** What, exactly, is a VM?

---

### Q8 — Provider vs consumer metrics

**Q:** A dashboard shows "CPU Ready" for an ESXi host. What does that number actually represent? Can a physical core itself have Ready time?

**Tests:** Principle: provider vs consumer; provider metric vs sum-of-consumer metric.
**Likely wrong answer:** "It's the host's own CPU Ready — time the host waited for CPU."
**Expected key points:**
- Virtualization splits the stack into **provider** and **consumer**.
- Provider has 2 kinds of metrics: true **provider metrics** (don't exist on the consumer) and **sum of consumer** metrics.
- Ready is a consumer concept. A physical core/thread is always ready. Host-level Ready can only be an aggregate of its VMs.
- The metric name does not say which kind it is. You must know the mechanism.
- ESXi ≠ sum of VMs + kernel. Host metrics are more complex than a sum.

**Source:** Virtualization Impact; Architecture Complexity (VM vs ESXi; ESXi ≠ VMs + Kernel).

---

### Q9 — Setting a disk latency threshold

**Q:** Microsoft says SQL Server disk latency should consistently stay below 10–15 ms. Should we set a vSphere VM disk latency alert at 15 ms averaged over 5 minutes?

**Tests:** Judgment / interpretation (heuristic, "it depends").
**Likely wrong answer:** "Yes, use 15 ms as the threshold."
**Expected key points:**
- The 10–15 ms guidance is at the **SQL layer**. Windows layer must be lower, and the VM layer lower still, to leave room for processing and queues higher in the stack.
- Read vs write may need different thresholds.
- "Consistently": IO is measured per second, so 5 minutes is 300 samples. A 5-minute window tends to give many alerts but few real complaints.
- No universal threshold: tolerance varies by application, use case and end user. Too low = noise, too high = missed problems.

**Source:** Interpretation Challenge.

---

### Q10 — What counts as overhead

**Q:** A capacity report lists the following as "virtualization overhead": VM snapshots, the spare host kept for vSphere HA, vSAN FTT=1 storage, ESXi kernel memory, and VM log files. Is this classification correct?

**Tests:** Principle: overhead vs not overhead.
**Likely wrong answer:** "Yes, all of these are overhead."
**Expected key points:**
- **Overhead** = mandatory (cannot be avoided) **and** has negative impact.
- **Not overhead** = optional, and brings a capability you choose to use.
- Overhead: ESXi kernel, VM log files (also VMM overhead, vSAN processes' CPU/memory).
- Not overhead: VM snapshots, HA spare host, vSAN FTT policy.
- Buffers (capacity, cost, DR, security) are a separate category again.
- Bonus: vMotion is not overhead, but can raise VM Consumed on the destination (swap or compressed pages become regular pages).

**Source:** Overhead vs Not Overhead.

---

## Results log

| Date | Model | Mode (baseline / KB) | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 | Total /30 |
|------|-------|----------------------|----|----|----|----|----|----|----|----|----|-----|-----------|
|      |       |                      |    |    |    |    |    |    |    |    |    |     |           |
