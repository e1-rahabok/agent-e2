# To Do

Open work for this repository. Not indexed. Update when items close.

## Source reading (vSphere 9.1 performance PDF, revision 20260624)
- [ ] Read p. 19: network hardware considerations.
- [ ] Read p. 46: Enhanced Data Path (EDP) and network traffic shaping.
- [ ] Read pp. 39-45: storage considerations (not started).
- [ ] Read pp. 66-75: vCenter, vSphere management, vMotion and Storage vMotion.
- [ ] Read pp. 82-95: Storage DRS, HA, FT, vSAN, Lifecycle Manager, content library, Kubernetes (only what the knowledge base needs).
- [ ] Read p. 59: guest OS memory considerations (2 MB pages cross-check).
- [ ] Read KB 316514 (Retreat Mode) and KB 55806 (scheduler options).

## Open points to verify
- [ ] vCLS status in vCenter 9.1: official VCF 9.1 Product Support Notes or release notes (currently third-party only).
- [ ] Side-channel content: not in the 9.1 document. Confirm where it moved (KB 55806 and others).
- [ ] Power policy name: "Maximum performance" (9.0 and 9.1 p. 53) vs "High Performance" (p. 31).
- [ ] Hyper-Threading penalties (37.5% VM, 50% ESXi): not in the source. Book figures need author confirmation.
- [ ] `numPCPUs` in the dense mode trigger: not defined in the source.
- [ ] KB number for the ESXi CPU Usage 100% cap (author correction, pending).
- [ ] Cluster-level share scope: marked `[claude-knowledge]` in `vsphere/foundations/resource-management`.
- [ ] Memory reservation headroom: source gives no percentage. Does the book?
- [ ] Predictive DRS and DPM require vRealize Operations 6.4 or later per the source. Check the current equivalent (VCF Operations).
- [ ] Existing `cpu/counters/*/cpu.usage.average.md` uses an unsourced "~80-85%" threshold. Replace or source it.
- [ ] `troubleshooting/host-not-responding.md` has no front matter and is not from the book.

## Open points from book extraction
- [ ] Questions for the author: `docs/author-questions.md` (29 open).
- [ ] Author to update the book: Use P States off vs Turbo. Strings: "When deactivated, the ESX configures to use the highest available frequency"; "Rigid Base / Sleep Only"; "Turbo can still kick in despite the BIOS setting". Then update `cpu/concepts/power-states`.
- [ ] Author to elaborate in the book: idle CPU lowers frequency below base (string: "Frequency will go lower than base clock speed"). Then update `cpu/concepts/power-states`.
- [ ] Author to correct the book: wait sub-cases are IO wait, memory wait, other wait (string: "There are 3 sub cases here (Co-stop, VM Wait and memory wait)"). Knowledge base already updated.
- [ ] Later: add the author's "My Recommendation" column (single-counter recommendation) from the Impacts on ESXi table to `cpu/concepts/cpu-frequency`.

## Book extraction
- [x] Metrics Nuances (Chapter 1): re-extracted.
- [x] Chapter 2 (CPU) > Architecture (pp. 52-78): extracted 2026-11-02.
  - New: `cpu/concepts/` guest-os-vs-vm-cpu, cpu-measurement-levels, cpu-topology, vcpu-states, run-time-vs-run-quality, cpu-efficiency, cpu-frequency, power-states, frequency-and-ht-impact-on-vm.
  - Updated: VM run, ready, wait, used, usage, latency; host core-utilization, utilization.
- [ ] Re-check extracted chapters when the author uploads the corrected `.docx` (author uploads when enough corrections accumulate).
- [x] Chapter 2 (CPU) > VM (pp. 78-118): extracted 2026-11-02.
  - New VM metric files: co-stop, overlap, other-wait, swap-wait, idle, contention, net-run, demand, system, usage-disparity.
  - New comparisons: vm-contention-metrics, vm-vs-esxi-ht-ramp-test. New diagnosis: vm-cpu-contention-high, run-vs-used-gap, oversized-vm-downsizing, vm-other-wait-high.
  - Updated: VM ready, run, used, usage, wait, latency; comparisons/consumption-metrics.
- [x] Chapter 2 (CPU) > ESXi: extracted 2026-11-02. Chapter 2 CPU complete.
  - New: `cpu/concepts/esxi-thread-core-accounting`; host metric files peak-core-usage, reserved-capacity, imbalance, wait, cpu-utilization-for-resources; comparisons host-consumption-metrics, host-contention-metrics; diagnosis host-cpu-capacity-headroom.
  - Updated: host utilization, core-utilization, idle, usage, used, demand.
- [x] Chapter 3 (Memory) > Architecture: extracted 2026-11-02. New: `memory/concepts/` memory-as-storage, memory-layers, guest-os-vs-vm-memory. Updated: VM latency, consumed, ballooned; host consumed.
- [x] Chapter 3 (Memory) > VM: extracted 2026-11-02.
  - New concepts: ballooning, swap-and-compression. New VM metric files: granted, shared, zero-pages, active, compressed, swap-target, swap-in-rate, swap-out-rate, balloon-target, entitlement, overhead, utilization.
  - New: comparisons/vm-memory-metrics, diagnosis/vm-memory-latency-high. Updated: VM latency, ballooned, consumed, swapped, usage; CPU swap-wait.
- [x] Chapter 3 (Memory) > ESXi: extracted 2026-11-02. Chapter 3 Memory complete.
  - New: `memory/concepts/host-memory-states`; host metric files ballooned, state, latency, compressed, granted, shared, utilization, reservation; comparisons/host-memory-metrics.
  - Updated: host consumed, swap-used, usage.
- [x] Chapter 4 (Storage) > Architecture: extracted 2026-11-02. New: `storage/concepts/` storage-dimensions, storage-layers, guest-os-vs-vm-storage; `storage/diagnosis/vm-storage-performance-checks`. Updated: VM disk-latency.
- [x] Chapter 4 (Storage) > VM: extracted 2026-11-02. New: concepts vm-files, snapshot-impact; VM metric files outstanding-io, disk, datastore, virtual-disk-used, disk-space-used, provisioned-space, snapshot-space. Updated: virtual-disk, disk-latency, iops.
- [x] Chapter 4 (Storage) > ESXi: extracted 2026-11-02. Chapter 4 Storage complete. New: concept esxi-storage-latency-stack; host metric files disk, adapter-and-path, datastore; diagnosis host-storage-latency. Updated: memory-tiering.
- [x] Chapter 5 (Network) > Architecture: extracted 2026-11-02. New: concepts network-characteristics, network-observability.
- [x] Chapter 5 (Network) > VM: extracted 2026-11-02. New: comparisons/vm-network-metrics; VM metric files packets-dropped, packets, throughput.
- [x] Chapter 5 (Network) > ESXi: extracted 2026-11-02. Chapter 5 Network complete. New: host metric files errors, packets-dropped, throughput; diagnosis vnic-rx-drops.
- [x] Consumer Objects > Performance: VM & Guest OS: extracted 2026-11-02. New: system/concepts/performance-kpi-design; system/metrics/virtual-machine vm-performance, guest-os-performance, vmotion; comparisons/peak-20-second-metrics. Updated: cpu/configuration/latency-sensitivity.
- [x] Consumer Objects > Capacity: Guest OS: extracted 2026-11-02. New: system/concepts rightsizing, guest-os-sizing, vm-footprint-sizing. Validator: allow list for book metric names containing Needed.
- [x] Provider Objects > Overview: extracted 2026-11-02. New: system/concepts/cluster-operations; system/metrics/cluster/vm-operations; cpu/metrics/cluster/inter-host-imbalance.
- [ ] Provider Objects (Performance, Capacity, Other Metrics, esxtop); MS Windows: not started.
- [ ] Create VM metric files for Co-stop, Demand, Overlap, System, VMX, Idle when the book's VM section is extracted.
- [ ] Clear `[author-correction]` markers once the corrected book is uploaded.

## Evaluation
- [ ] Convert book quizzes (Chapter 2 has five) into golden cases.
- [ ] Add golden cases for Chapter 2 Architecture traps: Ready vs Run context, ms vs % normalization, Demand 170% and adding vCPUs, Windows vs vSphere 100% vs 50%, Balanced vs High Performance Turbo.
- [ ] Add golden cases for Chapter 2 VM traps: Demand equals Usage under a limit, Latency excludes limit, Co-stop chain from one vCPU in Ready, System on vCPU 0, Usage 39 GHz vs 57.6 GHz, 20-second vs 5-minute Ready.
- [ ] Add golden cases for Chapter 2 ESXi traps: Usage 100% vs Thread Utilization 47%, Core Utilization duplicated per thread, Demand 315% on a host, host with no VMs showing Demand, Thread Utilization 50% with all cores busy.
- [ ] Add golden cases for Chapter 3 Memory traps: Active stuck at 100%, Windows In Use 7.2 GB on an idle VM, Granted above limit, Swapped is not swap in - swap out, balloon 63% flat for weeks, only Latency measures memory performance.
- [ ] Run baseline (no knowledge base) and knowledge-base runs. Record in `evaluation/results/results.csv`.
- [ ] Add `status: reviewed` only after author review.

## Structure (after the re-organization of 2026-11-02)
- [ ] Review the tags assigned during migration (pillar, object, metric_class). Pillar values were assigned by Claude.
- [ ] metric_class for Wait, Idle, Swapped, Swap Used, Ballooned: set provisionally. Author to confirm.
- [ ] Pillar example re-mapping in `foundations/metric-perspectives`: Compliance Score under Security, Month-to-Date Cost under Value. Author to confirm.
- [ ] Parked until Chapter 6 of the book: placement of `cluster-resource-management/` (outside the technology-first rule).
- [ ] Terminology: author to provide the book terminology for `vsphere/glossary/terminology`.
- [x] Validator: `scripts/validate.py`, run before every merge.
- [ ] Legacy files in `docs/legacy/` (old `cpu.usage.average` files): decide whether to rewrite as metric files or remove.
- [ ] `vsphere/system/diagnosis/host-not-responding` is not from the book. Decide whether to keep.
- [ ] Add a script that generates per-tag index files and checks front matter and links.
