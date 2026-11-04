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

## Restructure (holistic review 2026-11-04)
- [x] Decisions 1, 4, 5, 6, 7 carried out; 2 and 3 declined. Record: `project/review-2026-11-04.md`, section 9.
- [ ] Thin files (review section 5): fill from the book or merge into the parent file.
- [ ] Re-check `vsphere/technology/cpu/configuration/side-channel-scheduling` against Performance Best Practices 9.1.
- [ ] Shorten `vsphere/object-types/cluster/concepts/vcls` to the 9.1 status.
- [x] Metric catalog (`knowledge/catalog/`) and harness tools: catalog lookup, calculator, flow executor, answer verifier (2026-11-04).

## Structure (author review 2, 2026-11-04)
- [x] Moved 174 files and 161 images: `vsphere/technology/`, `vsphere/object-types/`, `operations-management/`; `system/` and `resource-management/` dissolved. Ids repointed everywhere; lint enforces the folders.
- [x] `vcf-operations/` created with `concepts/vcf-operations-role`. Glossary: storage vs disk, vCenter vs VCF Operations.
- [x] Screen template (`knowledge/_templates/screen.md`) and lint rules for `screens/` (release 1.1).
- [x] Overview file per object folder: what to monitor, in priority order (vm, esxi, cluster), 2026-11-04.
- [ ] Review `operations-management/capacity/capacity-model`: it holds vSphere cluster capacity. Split the vSphere-specific part into `vsphere/object-types/cluster/` if it is not cross-product.
- [ ] VCF Operations knowledge: map its objects, engines and metric groups; fetch the VCF Operations 9.1 metric reference; ask the author for the VCF Operations book chapters.

## Product (from the vCommunity Ask demo, 2026-11-04; see `project/product-requirements.md`)
- [x] Section "Host CPU monitoring" moved from `vsphere/foundations/overhead` to `vsphere/object-types/esxi/overview-what-to-monitor`, with the knowledge base reading next to it.
- [x] Overview files for VM, ESXi and cluster. Next: datastore and resource pool when their content grows.
- [ ] Benchmark case: "most important CPU metrics on an ESXi host" (trap: utilization and load average first).
- [ ] The shipped app uses `harness/` for retrieval, tools, prompt and verifier, and the benchmarked embedding model.
- [ ] Store prompt version, settings, model and index version with every answer; mark answers from a UI-edited prompt as untested.
- [ ] Rate and flag buttons with cause tags, feeding the review queue.
- [ ] Release gate: every knowledge file `status: reviewed` (D1). Remove the draft rule from the answer prompt before release.
- [ ] Offline bundle import for dark sites; local viewer as the default source link.
- [ ] Screenshot upload (1.1, D2): prepare the screen library structure in 1.0; recognition, read-back of values, multi-image comparison in 1.1.
- [ ] Data file upload (1.2, D3): document each export format and its traps first, then parse in code.
- [ ] Guided troubleshooting UX: step progress and branch shown, user enters values.
- [ ] After 1.0: connect to VCF Operations (read-only service account). Find objects, read metrics and properties, run the flows on live values, cite live data with timestamps. Needs the VCF Operations 9.1 metric reference in the catalog first.

## Catalog and tools follow-up
- [ ] Catalog rows without a `kb` file: cluster and resource pool memory, datastore space, DPU charts. Add files or map to existing ones.
- [ ] Counter group unclear for the per-host and per-VM-disk datastore charts (deviceLatency, maxQueueDepth, totalReadLatency, ...): confirm in the vSphere API reference (developer.broadcom.com).
- [ ] Map esxtop fields to knowledge files (esxtop comparison files) so a catalog hit on %RDY also returns the file.
- [ ] VCF Operations metrics in the catalog (needs the VCF Operations 9.1 metric reference).
- [ ] After the next benchmark run: check `verify_flags` against wrong answers. Promote a soft check to a repair trigger only if it predicts errors.
- [ ] After the next benchmark run: check `tools_used`. If models skip catalog and calculate on unit questions, strengthen the prompt rule or add a router.
- [ ] Add benchmark cases that need the catalog, calculator and object paths (units, statistics levels, summation to %, multi-hop).
- [ ] Merge `project/philosophy-and-structure.md` into `project/solution-design.md`; split `project/design-kb-test-site.md` into harness design and benchmark plan.

## Source reading (VMware vSphere 9.1 product documentation, PDF built 2026-11-02)
- [x] vSphere Monitoring and Performance, pp. 2025-2184: extracted 2026-11-03.
  - New: `vsphere/foundations/vcenter-statistics`, `vsphere/foundations/vsphere-client-performance-guidance`, `vsphere/technology/storage/metrics/datastore/storage-io-control`.
  - Updated: esxtop-cpu, esxtop-memory, system/concepts/esxtop, memory-tiering, storage host datastore; links in ready, host memory usage, host-storage-latency, metric-sources.
  - Left out as not relevant to performance monitoring: UI click steps, alarm and event configuration, preconfigured alarm list, SNMP, log files, vimtop, Solutions Manager, host hardware health, Configuration Maximums checker, Fault Tolerance charts, DPU charts, PMem Memory Mode, GPU chart details beyond their statistics level.
  - Questions: Q044-Q046.
- [x] GPU monitoring (Monitoring and Performance + Resource Management): `vsphere/technology/gpu/concepts/gpu-monitoring`, 2026-11-03.
- [x] vSphere Resource Management, pp. 1824-1959: extracted 2026-11-03.
  - New: `resource-management/concepts/admission-control-and-cluster-state`, `resource-management/diagnosis/vm-insufficient-resources-in-drs-cluster`.
  - Updated: memory-tiering (mechanism, sizing, DRAM-only VMs, interactions, NVMe bandwidth threshold), memory-overhead, swap-and-compression, foundations/resource-management (memory allocation, default CPU shares), numa (scheduler mechanics), hyper-threading, latency-sensitivity (vHT), large-memory-pages (1 GB pages), drs-migration-levels (DRS Score), storage-io-control (deprecation).
  - Left out: configuration steps, power policy parameters, affinity rule and span limit setup, DPM setup, HA and FT, PMem and vMMR, storage policies and I/O filters, Storage DRS setup, swap file location setup, memory tiering setup and NVMe failure handling, DRS fault definitions, reliable memory, EVC.
  - Question: Q047.

## Open points to verify
- [ ] vCLS status in vCenter 9.1: official VCF 9.1 Product Support Notes or release notes (currently third-party only).
- [ ] Side-channel content: not in the 9.1 document. Confirm where it moved (KB 55806 and others).
- [ ] Power policy name: "Maximum performance" (9.0 and 9.1 p. 53) vs "High Performance" (p. 31).
- [ ] Hyper-Threading penalties (37.5% VM, 50% ESXi): not in the source. Book figures need author confirmation.
- [ ] `numPCPUs` in the dense mode trigger: not defined in the source.
- [ ] KB number for the ESXi CPU Usage 100% cap (author correction, pending).
- [ ] Cluster-level share scope: marked `[claude-knowledge]` in `vsphere/foundations/resource-controls`.
- [ ] Memory reservation headroom: source gives no percentage. Does the book?
- [ ] Predictive DRS and DPM require vRealize Operations 6.4 or later per the source. Check the current equivalent (VCF Operations).
- [ ] Existing `cpu/counters/*/cpu.usage.average.md` uses an unsourced "~80-85%" threshold. Replace or source it.
- [ ] `troubleshooting/host-not-responding.md` has no front matter and is not from the book.

## Open points from book extraction
- [ ] Questions for the author: `project/author-questions.md` (25 open).
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
- [x] Consumer Objects > Performance: VM & Guest OS: extracted 2026-11-02. New: system/concepts/performance-kpi-design; system/metrics/virtual-motherboard vm-performance, guest-os-performance, vmotion; comparisons/peak-20-second-metrics. Updated: cpu/configuration/latency-sensitivity.
- [x] Consumer Objects > Capacity: Guest OS: extracted 2026-11-02. New: system/concepts rightsizing, guest-os-sizing, vm-footprint-sizing. Validator: allow list for book metric names containing Needed.
- [x] Provider Objects > Overview: extracted 2026-11-02. New: system/concepts/cluster-operations; system/metrics/cluster/vm-operations; cpu/metrics/cluster/inter-host-imbalance.
- [x] Provider Objects > Performance: extracted 2026-11-02. New: system/concepts/cluster-utilization-vs-contention; system/metrics/cluster cluster-performance, cluster-sla-sli; system/diagnosis/cluster-vm-contention.
- [x] Provider Objects > Capacity: extracted 2026-11-02. New: system/concepts capacity-model, hypervisor-overhead; cpu/concepts/cpu-capacity; memory/concepts/memory-capacity.
- [x] Provider Objects > Other Metrics: extracted 2026-11-02. New: system/metrics/cluster cluster-consumption, cluster-risk; system/metrics/comparisons/availability.
- [x] Provider Objects > esxtop (Overview, CPU, Memory): extracted 2026-11-02. New: system/concepts/esxtop; cpu/metrics/comparisons/esxtop-cpu; memory/metrics/comparisons/esxtop-memory.
- [x] Provider Objects > esxtop (Storage, Network): extracted 2026-11-02. Provider Objects complete. New: storage/metrics/comparisons/esxtop-storage; network/metrics/comparisons/esxtop-network.
- [x] MS Windows (Introduction, CPU, Memory, Storage): extracted 2026-11-02. Book extraction complete. New: cpu/concepts/windows-cpu-scheduling; cpu/metrics/virtual-motherboard guest-run-queue, guest-context-switch, guest-processor-time; memory/concepts/windows-memory; storage/metrics/virtual-motherboard/guest-disk-queue.
- [ ] Create VM metric files for Co-stop, Demand, Overlap, System, VMX, Idle when the book's VM section is extracted.
- [x] 24 unlinked book images linked under the sections they explain. Validator now fails on any unlinked image.
- [ ] Clear `[author-correction]` markers once the corrected book is uploaded.

## Evaluation
- [x] Case vendor-neutral-general-001 (hyperscaler VM cost): removed 2026-11-04. Cost and price are out of scope (author, Q039).
- [x] Author quiz (vSphere Metric Quiz.docx): 18 golden cases added 2026-11-03 (vsphere cpu-004 to cpu-013, vsphere general-001, vendor-neutral general-001, memory-002 to 006, storage-003). Q034-Q037 raised.
- [ ] Convert book quizzes (Chapter 2 has five) into golden cases.
- [ ] Add golden cases for Chapter 2 Architecture traps: Ready vs Run context, ms vs % normalization, Demand 170% and adding vCPUs, Windows vs vSphere 100% vs 50%, Balanced vs High Performance Turbo.
- [ ] Add golden cases for MS Windows traps: Windows 100% on a shared core vs VM CPU Usage 62.5%, queue excludes running threads on Windows but includes them on Linux, 100% utilization with a low queue, Available = Standby + Free, guest disk queue invisible to VM latency.
- [ ] Add golden cases for Chapter 2 VM traps: Demand equals Usage under a limit, Latency excludes limit, Co-stop chain from one vCPU in Ready, System on vCPU 0, Usage 39 GHz vs 57.6 GHz, 20-second vs 5-minute Ready.
- [ ] Add golden cases for Chapter 2 ESXi traps: Usage 100% vs Thread Utilization 47%, Core Utilization duplicated per thread, Demand 315% on a host, host with no VMs showing Demand, Thread Utilization 50% with all cores busy.
- [ ] Add golden cases for Chapter 3 Memory traps: Active stuck at 100%, Windows In Use 7.2 GB on an idle VM, Granted above limit, Swapped is not swap in - swap out, balloon 63% flat for weeks, only Latency measures memory performance.
- [ ] Run baseline (no knowledge base) and knowledge-base runs. Record in `benchmark/results/results.csv`.
- [ ] Add `status: reviewed` only after author review.
- [ ] Next Auto Test run, after more questions are added: try `--concurrency 16`. Keep 16 if errors stay at 0 and answers per minute rise. At 100 questions (about 12,700 answers, about US$ 11) the run takes about 4 hours at 12 and about 3 hours at 16 if speed scales: above the 2-hour command limit either way. Plan `--resume` once, or split by model.
- [ ] Close the agentic gap (run 20261103-081849: agentic below classic for 7 of 8 models):
  - [ ] Better agentic prompt: example lookups; keep going until linked files (`same_name`, `related`) are read.
  - [ ] Hybrid mode: start from the classic results, then let the model follow links.
  - [ ] Test a larger local model if hardware allows; tool use improves with size.
  - [ ] Raise `agent_max_calls` and `agent_tool_tokens` once models use the calls they have.
  - [x] Frontier model as a reference ceiling: run 20261103-093742 (claude-opus-5.5). Baseline 75%, classic 67%, agentic 67%.
- [ ] Frontier run findings for the author: Q038-Q043 in `project/author-questions.md` (prompt rule, cost case, 4 golden cases wrong for all models). Re-run the frontier model after the answers are applied.

## Structure (after the re-organization of 2026-11-02)
- [ ] Review the tags assigned during migration (pillar, object, metric_class). Pillar values were assigned by Claude.
- [ ] metric_class for Wait, Idle, Swapped, Swap Used, Ballooned: set provisionally. Author to confirm.
- [ ] Pillar example re-mapping in `foundations/metric-perspectives`: Compliance Score under Security, Month-to-Date Cost under Value. Author to confirm.
- [x] Placement of `resource-management/`: split 2026-11-04 (resource controls → `vsphere/foundations/`, DRS and cluster mechanisms → `vsphere/object-types/cluster/`).
- [ ] Terminology: author to provide the book terminology for `glossary`.
- [x] Validator: `tools/lint.py`, run before every merge.
- [ ] Legacy files in `project/legacy/` (old `cpu.usage.average` files): decide whether to rewrite as metric files or remove.
- [ ] `vsphere/system/diagnosis/host-not-responding` is not from the book. Decide whether to keep.
- [ ] Add a script that generates per-tag index files and checks front matter and links.

## Troubleshooting flows
- Rule: README, section Troubleshooting flow diagrams. Each file gets: Symptom, Flow (Mermaid), numbered Checks with metric, object, threshold with source, next step per outcome; Why this order.
- Source: the author's draw.io flows when available; otherwise derive from the file's current checks and flag in `review_notes`.
- [ ] `vsphere/technology/cpu/diagnosis/vm-cpu-contention-high`: add flow.
- [ ] `vsphere/technology/cpu/diagnosis/vm-other-wait-high`: add flow.
- [ ] `vsphere/technology/cpu/diagnosis/run-vs-used-gap`: add flow.
- [ ] `vsphere/technology/cpu/diagnosis/host-cpu-capacity-headroom`: add flow.
- [ ] `vsphere/technology/cpu/diagnosis/oversized-vm-downsizing`: add flow.
- [ ] `vsphere/technology/memory/diagnosis/vm-memory-latency-high`: add flow.
- [ ] `vsphere/technology/memory/diagnosis/overcommit-indicators`: add flow.
- [ ] `vsphere/technology/storage/diagnosis/vm-storage-performance-checks`: add flow.
- [ ] `vsphere/technology/storage/diagnosis/host-storage-latency`: add flow.
- [ ] `vsphere/technology/network/diagnosis/vnic-rx-drops`: add flow.
- [ ] `vsphere/object-types/cluster/diagnosis/cluster-vm-contention`: add flow.
- [ ] `vsphere/system/diagnosis/host-not-responding`: add flow.
- [ ] New flows for symptoms with no diagnosis file yet: list to be agreed with the author.

## Diagrams
- [ ] Convert the author's draw.io troubleshooting flows to Mermaid plus numbered steps in `diagnosis/` files. Keep the `.drawio` source and an exported `.png` next to them. Rule: README, section Troubleshooting flow diagrams.

## Test site
- [ ] Author decisions: audience, scoring (hosting and model decided 2026-11-03). See `project/design-kb-test-site.md`, section Decisions for the author.
- [x] Build phase 1 (Auto Test) runner: `benchmark/runner/` (2026-11-03). Tested offline with --mock.
- [ ] First real Auto Test run: needs AI_GATEWAY_API_KEY in the environment.
- [ ] Grow the golden question set from 30 to 100 multiple-choice questions: 20% recall, 50% Level 400, 20% multi-hop, 10% screenshot; at least 10 per area; about 10 out-of-scope questions.
- [x] "Not covered" option and fixed answer format: added by the runner. Answer keys (`answer`, `trap`, `level`, `format`) added to 17 quiz cases.
- [ ] Case vsphere-cpu-006 (two hosts, two answers): split into two multiple-choice cases to make it auto-scorable.
