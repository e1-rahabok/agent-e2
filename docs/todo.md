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
- [ ] Chapter 2 Architecture questions for the author (details in each file's `review_notes`):
  - Impacts on ESXi table shows ESXi Usage (%) at 120% and 150%. Conflicts with the 100% cap correction in `host/usage`.
  - Same table: meaning of the "My Recommendation" column (values = Core Utilization × 0.8), and Core Utilization 125%.
  - Fair Share Scheduler: "Used increases run time on a shared core" vs the CPU Efficiency example (Used 62.5% < Run 100%).
  - ESXi ≠ VM + Kernel: "a thread is consumer" read as provider.
  - State of a VM vCPU: Co-stop listed as a sub-case of IO wait.
  - Power states: C/P combination table (P-states off = no Turbo) vs "highest available frequency" vs Turbo at 129% under static high performance.
  - Typos assumed: remote L3 "80 ms" = 80 ns; "812 GHz" = 812 MHz (image confirms); "CPCC" = CPPC.
  - Linux Steal applies to VMs only ("I think"), and Idle "correlates with run queue".
  - "14 grades" of P-states: processor-specific?
  - "Run – Overlap – VMX – System": formula or list?

## Book extraction
- [x] Metrics Nuances (Chapter 1): re-extracted.
- [x] Chapter 2 (CPU) > Architecture (pp. 52-78): extracted 2026-11-02 from the pre-correction `.docx` on main.
  - New: `cpu/concepts/` guest-os-vs-vm-cpu, cpu-measurement-levels, cpu-topology, vcpu-states, run-time-vs-run-quality, cpu-efficiency, cpu-frequency, power-states, frequency-and-ht-impact-on-vm.
  - Updated: VM run, ready, wait, used, usage, latency; host core-utilization, utilization.
- [ ] Chapter 2 (CPU) > Architecture: re-check all files above when the corrected `.docx` is uploaded.
- [ ] Chapter 2 (CPU) > VM and later sections: not started.
- [ ] Create VM metric files for Co-stop, Demand, Overlap, System, VMX, Idle when the book's VM section is extracted.
- [ ] Memory, Storage, Network chapters: waiting for upload.
- [ ] Clear `[author-correction]` markers once the corrected book is uploaded.

## Evaluation
- [ ] Convert book quizzes (Chapter 2 has five) into golden cases.
- [ ] Add golden cases for Chapter 2 Architecture traps: Ready vs Run context, ms vs % normalization, Demand 170% and adding vCPUs, Windows vs vSphere 100% vs 50%, Balanced vs High Performance Turbo.
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
