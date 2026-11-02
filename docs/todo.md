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
- [ ] Memory, Storage, Network chapters: present in the uploaded `.docx` (pp. after CPU). Not started.
- [ ] Chapter 2 ESXi: open questions for the author, with verbatim search strings:
  - ESXi Demand: provider or consumer? Your correction (2026-11-02) says provider. Search: "Demand is consumer-view, while Usage is provider view". Also: "The value you see at ESXi is the summation of all the VMs".
  - ESXi Usage cap. Your correction says capped at 100% (KB pending). Search: "Usage no longer capped at 100% of total capacity at the nominal frequency". Is the cap only in vCenter, and removed in VCF Operations since Aria Operations 8.18?
  - ESXi CPU Imbalance: built-in VCF Operations metric or your own? Search: "ESXi CPU Imbalance = Count of Running Threads / Count of Running Cores".
- [ ] Chapter 2 VM: open questions for the author, with verbatim search strings:
  - Steal Time. Search 1 (Chapter 1): "Steal Time in Linux only includes CPU Ready". Search 2 (VM > Overlap): "Linux Guest OS tracks this as Stolen time". Does Linux Steal include Ready only, Overlap only, or both?
  - System charged to vCPU 0. Search 1: "this is charged to the VM CPU 0". Search 2 (diagram text): "Charged at VM level, not at vCPU 1". Chapter 1 also says per-vCPU Used excludes System. Which is right?
  - Run for sizing. Search 1: "suitable as input to size the Guest OS and not the VM". Search 2: "This counter is suitable for VM Capacity sizing". Guest OS sizing, VM sizing, or both?
  - Contention formula. Search: "Other Wait (if less than 1%)". What does the condition mean?
  - Contention and limit. Search 1: "Unlike CPU Ready, it does not account for Limit". Search 2: "Why does the counter include Ready by Limit?". Is the first about the pre-July-2024 Contention (mapped to Latency)?
  - Used above Run. Search: "Why is Used consistently 41% higher than Run?". How does Ready make Used higher than Run?
  - Ready and VM size. Search 1 (VM): "CPU Ready tends to be higher, ceteris paribus, in larger VMs". Search 2 (Architecture): "You can reduce Co-stop by reducing the VM size". Does downsizing reduce Ready too?
  - Ramp test. Search: "ESXi CPU Core Utilization (%) matches VM Run. Both went 2x." Core Utilization stayed at 100%. Should this be Utilization (%)?
- [ ] Create VM metric files for Co-stop, Demand, Overlap, System, VMX, Idle when the book's VM section is extracted.
- [ ] Clear `[author-correction]` markers once the corrected book is uploaded.

## Evaluation
- [ ] Convert book quizzes (Chapter 2 has five) into golden cases.
- [ ] Add golden cases for Chapter 2 Architecture traps: Ready vs Run context, ms vs % normalization, Demand 170% and adding vCPUs, Windows vs vSphere 100% vs 50%, Balanced vs High Performance Turbo.
- [ ] Add golden cases for Chapter 2 VM traps: Demand equals Usage under a limit, Latency excludes limit, Co-stop chain from one vCPU in Ready, System on vCPU 0, Usage 39 GHz vs 57.6 GHz, 20-second vs 5-minute Ready.
- [ ] Add golden cases for Chapter 2 ESXi traps: Usage 100% vs Thread Utilization 47%, Core Utilization duplicated per thread, Demand 315% on a host, host with no VMs showing Demand, Thread Utilization 50% with all cores busy.
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
