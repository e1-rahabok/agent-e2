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

## Book extraction
- [x] Metrics Nuances (Chapter 1): re-extracted.
- [ ] Chapter 2 (CPU): waiting for the corrected `.docx` upload. The copy on main is the pre-correction version.
- [ ] Memory, Storage, Network chapters: waiting for upload.
- [ ] Clear `[author-correction]` markers once the corrected book is uploaded.

## Evaluation
- [ ] Convert book quizzes (Chapter 2 has five) into golden cases.
- [ ] Run baseline (no knowledge base) and knowledge-base runs. Record in `evaluation/results/results.csv`.
- [ ] Add `status: reviewed` only after author review.

## Structure (after the re-organization of 2026-11-02)
- [ ] Review the tags assigned during migration (pillar, object, metric_class). Pillar values were assigned by Claude.
- [ ] metric_class for Wait, Idle, Swapped, Swap Used, Ballooned: set provisionally. Author to confirm.
- [ ] Pillar example re-mapping in `foundations/metric-perspectives`: Compliance Score under Security, Month-to-Date Cost under Value. Author to confirm.
- [ ] `cluster-resource-management/` sits outside the technology-first rule. Author to confirm the placement.
- [ ] Legacy files in `docs/legacy/` (old `cpu.usage.average` files): decide whether to rewrite as metric files or remove.
- [ ] `vsphere/system/diagnosis/host-not-responding` is not from the book. Decide whether to keep.
- [ ] Add a script that generates per-tag index files and checks front matter and links.
