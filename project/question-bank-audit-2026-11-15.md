# Question bank audit (2026-11-15 to 2026-11-16)

Audit and improvement of the benchmark question bank against the knowledge base as updated by the author on 2026-11-15. For the author's review. Not indexed. Design rules: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (sections 3, 5, 6, 13.1). Plan entry: [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md), decision of 2026-11-16.

## 1. Result in brief
- 275 question files at the start (228 running, 47 awaiting screenshots); 299 at the end: 296 running, 3 deferred; 4 retired to [project/archive/benchmark-questions](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/benchmark-questions).
- No answer key was wrong against the current knowledge base. Every key a reviewer doubted (44 questions) was re-derived by an independent checker that had not seen the doubt: all 44 matched the file key.
- 44 practical halves now run as exports (CSV or tool text) from a seeded generator, [project/tools/export_generator](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/export_generator/README.md); no question waits for a screenshot.
- 28 new questions for knowledge the bank did not test (ids 0443-0470).
- Answer cues cut: the longest option is correct in 49.7% of questions (was 71.5%; chance 43.6%); strong length cues 16 (was 88).
- Every changed or new question was keyed again blind by an independent agent after the edits: 296 questions, 295 agreed at once; the one that differed (0351, a time window) was fixed so its key holds, and a final blind check of the 121 questions touched after that agreed on all 121.
- Ten author questions, Q244-Q253 ([project/author-questions.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/author-questions.md), Release 1.0).

## 2. Method
- Models: Opus for review, breaking, blind keys and rewriting; Sonnet for scripts and the generator. No gateway credit was spent; no benchmark round was run.
- Phase 0, baselines (section 7). Phase 1: [project/tools/question_scan.py](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/question_scan.py), a repeatable scan of cues, stem wording and knowledge coverage (`--ids` for a subset, `--json` for the data).
- Phase 2, review: 11 read-only reviewers by area (CPU two, memory two, storage two, network, Guest OS, tools, framework, cluster), 18-32 questions each. Each read the knowledge-engineering rules, the glossary, every cited knowledge file and its neighbours in full, and decided every option from the current files, not from the question's notes. Each wrong option was tagged: misconception, over-correction, wrong action, unit trap or throwaway.
- Second reviewers: 11 more agents tried to break every finding. Of 829 findings: 503 held, 222 were real with a wrong fix (the second reviewer gave the right one), 104 broke. Only held findings were applied.
- Blind keys: an agent that saw only the prompt, the evidence and the knowledge files keyed each question a reviewer doubted before reading the file's key.
- Phase 3, redundancy: one agent normalised the facts the reviewers listed per question into canonical facts and counted the questions that test each through a correct or misconception option (section 4).
- Phase 5: export conversion (7 agents) and generator cases (5 coders), rewriting by group (11 agents), gap questions (4 agents).
- Phase 6: an independent blind re-review of every changed and new question (12 agents), a fix pass on what it found (8 agents), and a last blind key check of the 121 questions the fix pass touched (4 agents).
- Safety rules kept: no key changed against an independent verdict; no file under `knowledge/` edited; knowledge-base gaps and contradictions went to the author list (section 8, appendix B).
- Interruptions: the account usage limit stopped all agents three times; every agent resumed where it stopped.

## 3. Findings of the review
| Finding | Count | What was done |
|---|---|---|
| Key wrong | 0 | - |
| Option not decidable from the knowledge base, or decidable only from a vendor document | about 25 questions | reworded so the cited files decide it, or replaced by an option of the same truth value; the rest cite the vendor page in Notes and go to the author (Q244, Q245, Q247) |
| Throwaway distractor (nobody at Level 300 picks it) | about 45 options | replaced by a misconception or over-correction a knowledge file names |
| Stale key points or notes after the knowledge update (ballooning, Q201, Q205, Q214, Q217, Q236, the judge) | about 60 questions | rewritten from the current files |
| Impossible values in a stem (0291, 0350, 0022, 0456) | 4 | recomputed |
| Stem copies a knowledge-base example or sentence (F5) | about 12 | rebuilt with own numbers |
| Hints or give-aways in stems | about 20 | removed or turned into raw values |
| Option pairs that negate each other | about 30 | one of the pair reworded to a different fact |
| Who-said-it in metadata ("Drafted by Claude") | all touched questions | `source_path` now "Synthetic, date" |
| Level labels | 20 changed | 15 from 400 to 300, 5 from 300 to 400 (appendix A) |

- Length and word cues: most correct options carried the reason, the hedge and the extra clause. Rewriters evened lengths and spread hedges, absolutes and "because" over correct and wrong options. Remaining: 16 strong length cues (list in the scan); Level 400 still shows the longest option correct in 55.8% (chance 44.9%).
- Imperative options: "Open a (support) case" was wrong in 9 of 9 options and "Add ..." in 18 of 19; no new option of either shape was added.
- Practical halves: the second reviewers held that the pairing plan sets them at Level 400 (design.md 3.9); relabels of 0401, 0431, 0438, 0440 broke. 0390 and 0403 went to 300 on the merits: Q251.

## 4. Redundancy (cap: two questions per fact)
- 60 canonical facts were tested by three or more running questions (counting only correct and misconception options). Largest: a rolled-up point is a mean, so a burst is diluted (13 questions); whether VMs wait is read per VM, not from utilization (9); limit time is inside Ready (7); swapped and compressed pages are past reclamation (7); admission control counts reservations, not usage (8 or more).
- Handled by replacing the over-cap option in place with a fact of the same truth value that no question tested twice (about 170 options), and by dropping 37 options where no such fact existed (letters re-lettered; every such key re-checked blind).
- One near-copy retired: 0185 repeated 0426 option for option. Deliberate pairs (theory and practical) keep their fact.
- Facts still at three: 0023 D (latency misconception; every untested wrong belief in that file is already used), 0454 E and H (the kernel reservation, a third time through the Utilization formula). Listed for the author.

## 5. Coverage
### By tag (running set; before: 228 running plus 47 waiting)
| Axis | Before (running) | After |
|---|---|---|
| Levels 100 / 200 / 300 / 400 | 8 / 18 / 71 / 131 | 8 / 18 / 105 / 165 |
| Input text / table / screenshot | 185 / 36 / 8 | 214 / 75 / 8 |
| Task: troubleshoot / read-metric / decide-capacity / explain-mechanism / judge-setting | 60 / 55 / 37 / 47 / 29 | 84 / 80 / 48 / 46 / 38 |
| Technology: CPU / memory / storage / network / system / Guest OS layer | 90 / 75 / 58 / 37 / 66 / 55 | 119 / 99 / 70 / 46 / 75 / 77 |
| Object: VM / ESXi / cluster / resource pool / datastore / network / Guest OS | 171 / 106 / 32 / 12 / 23 / 20 / 43 | 227 / 141 / 43 / 12 / 29 / 22 / 57 |
| Tool: vCenter / VCF Operations / esxtop / Guest OS tools | 126 / 74 / 21 / 33 | 175 / 97 / 41 / 47 |
| Misconception type label-read-as-model | 0 | 5 |
| Knowledge files cited by no running question | 81 of 288 | 58 of 288 |

- `python3 project/tools/question_coverage.py` shows no zero except the archived `judged` answer type. M2's exception for `label-read-as-model` is no longer needed.
- Network stays the thinnest area (46 questions against 119 for CPU); 3 of the 28 new questions are network. GPU stays at one question (after 1.0).

### Knowledge files still with no question (58)
- 41 SP5 framework files and the vCommunity models and scores (cluster-performance, cluster-consumption, cluster-risk, close-for-business, esxi-performance, guest-os-performance, inter-host-imbalance, idle-vm): fairness rules F1 and F2 block them.
- Availability (cluster/metrics/availability, guest-os-availability): after 1.0.
- VCF Operations dashboards and reports (capacity-summary-dashboard, configuration-dashboards, report-suite): names and design opinion, no mechanism an operator misreads; the gap writer rejected them.
- cluster/metrics/vm-operations: its key line has an open review note (whether the counters are cumulative).
- memory/configuration/memory-hardware (a guideline, no mechanism) and memory/metrics/cluster/consumed (its meaning is unsettled: vSphere 9.1 disagrees with itself about the VMkernel).
- glossary: read by every answer through the up-front block; not a question target.

### New questions (28)
| Id | Title | Knowledge it covers |
|---|---|---|
| 0443 | Side-Channel-Aware Scheduler turned on after an L1TF audit | side-channel-scheduling |
| 0444 | Sum of VM CPU Usage above host CPU Usage | host used, host consumption metrics, the HT ramp test |
| 0445 | Host CPU Wait and thread Idle after a VDI move | host wait, host idle, CPU utilization for resources |
| 0446 | NPS-4 on an AMD EPYC 9005 cluster of mixed VM sizes | cpu-topology, numa-settings |
| 0447 | Fewer cycles for the same job on a new CPU generation | run-time-vs-run-quality |
| 0448 | BIOS and power settings on new hosts | bios-settings, power-states, hardware-assisted virtualization |
| 0449 | Latency Sensitivity High with Hyperthreading on a Java service | latency-sensitivity |
| 0450 | Balloons that do not empty | balloon-target |
| 0451 | Host Granted above physical memory | host granted, VM shared |
| 0452 | Compressed memory and the Consumed drop | host compressed |
| 0453 | PowerCLI memory report of a SQL Server VM | entitlement (as defined since Q230), QuickStats |
| 0454 | Memory Demand far below Consumed | host utilization, memory-capacity |
| 0455 | Batch VM pages under a memory limit | swap-and-compression, double paging |
| 0456 | HA admission green on a tiered cluster | memory-tiering and HA before 9.1.1 |
| 0457 | Direct device access for four packet-heavy VMs | passthrough-and-offload |
| 0458 | Backup repository receives on one uplink | nic-teaming (transmit only) |
| 0459 | Static interrupt coalescing on a trading VM | rss-and-interrupt-coalescing |
| 0460 | Template datastore never returns space to the array | thin on thin, VMFS 6 unmap |
| 0461 | Datastore virtual disk space below the sum of its VMs | datastore virtual-disk |
| 0462 | Highest disk latency above every device | kernel latency, NVMe memory-tier device |
| 0463 | Shared disk IOPS drop to zero on one cluster node | multi-writer disks |
| 0464 | vCLS Retreat Mode on a vCenter 9.1 cluster | vcls |
| 0465 | Patching one host of a five-host cluster | can-cluster-take-a-host-out |
| 0466 | DRS ignores bursts and incompatible VMs | drs-migration-levels |
| 0467 | esxtop Ready against the VM Performance dashboard | vm-performance-dashboard |
| 0468 | Guest OS run queue alert on a 16-vCPU VM | guest-os-alerts, run-queue |
| 0469 | vSphere documentation guidance as a checklist | performance-guidance |
| 0470 | Three small clusters or one large one | cluster-configuration-review |

## 6. Practical halves as exports
- 44 converted as decided on 2026-11-15 ([project/practical-questions-as-exports-2026-11-15.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/practical-questions-as-exports-2026-11-15.md)): prompt rewritten as the operator's situation with the export linked, `## Input to supply` removed, status draft; keys unchanged. 0389 and 0419 retired; 0435 and 0015 deferred.
- Generator: one seeded case per question in [project/tools/export_generator/question_exports](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/export_generator/question_exports); writers for the real formats from project/sources/export-templates; `check` re-reads each file and asserts the condition behind every option it can (`python3 -m project.tools.export_generator check all`; 45 unit tests). Tool text (esxtop panels, `top`, `sar`, `mpstat`, `ip -s link`, `systeminfo`, PowerCLI output) sits in a fenced `text` block in the prompt, written by the generator.
- CSV cap 24,000 characters (`question_csv_max_chars`); the largest export is about 18,500 characters.
- vCenter exports carry no units; prompts that need them state the chart legend's units as the operator sees them.
- Formats assumed, not captured: VCF Operations List view, `/proc/pressure/memory`, `mpstat`, the vSphere VM DRS score grid, vCenter column names beyond Usage and Readiness, the stamp position of vCenter rollups. Recorded in the generator README; worth one capture each.

## 7. Checks before and after
| Check | Before (2026-11-15) | After (2026-11-16) |
|---|---|---|
| Lint | 0 problems | 0 problems |
| Harness tests | pass | 101 pass |
| Runner tests | 59 pass | 59 pass |
| Generator tests | - | 45 pass; `check all` clean |
| Retrieval, BM25, with options | 275 questions: recall 91%, complete 207 (75%), main file missing 8 | 299 questions: recall 92%, complete 228 (76%), main file missing 4 |
| Retrieval, BM25, stem only | recall 74%, complete 133 (48%), main file missing 34 | recall 77%, complete 158 (53%), main file missing 34 |
| Same 271 questions in both runs, with options | recall 91.3%, complete 205 | recall 91.2%, complete 203 |
| Same 271 questions, stem only | recall 73.9%, complete 132 | recall 76.3%, complete 139 |
| Longest option correct | 71.5% (strict 64.0%) | 49.7% (strict 42.6%); chance 43.6% |
| Hedges in correct / wrong options | 13.3% / 6.2% | 9.2% / 7.1% |
| "because" in correct / wrong options | 4.0% / 8.3% | 2.5% / 4.2% |

- The retrieval check changed with the question text (options and stems), not with any knowledge or harness change: kept.

## 8. Left for the author
- Author questions Q244-Q253: three vendor facts for HA percentage admission control (0330 deferred until then); alert cycles, criticality and Child/Descendant (0274, 0275, 0340); adapter Highest latency weighting (0072); a Linux memory file (0272, 0387, 0079); the 0345 reviewer disagreement; two contradictions in memory-tiering; overhead and VM logging (0017); the level labels to confirm; the guest-os-sizing "Active shows the limit" line (0079); the reversed esxtop units misconception line (0412).
- Basics guard: eight Level 100-200 questions read as Level 300 to the reviewers (0187, 0039, 0041, 0043, 0045, 0049, 0271, 0273); labels kept as decided; Q251 asks how to keep them basic.
- Review before they count: 293 questions are draft and 3 reviewed; 0018, 0042, 0050 and 0266 were reviewed and are draft again after changes in substance.
- Knowledge-base issues found by the audit (no file under knowledge/ was edited): appendix B, 54 contradictions, 21 missing facts a key rests on, 15 open review notes under a key.
- Remaining minor defects the last checks noted, not fixed: some option pairs close to negation (0453 A/B, 0456 B/H, 0188 A/B, 0414 A/B, 0298 A/K, 0027 C/D, 0111 A/H, 0114 G/H); 0406 D needs a statistics-level condition; 0046's export rows are round disk sizes (the author's own export); 0444-0470 levels are the writers' calls.
- Per-question items: appendix C.

## Appendix A. Change list
Every question touched, by id: file name now, the change, level, key (only where it changed). Base commit 039c463. Change text is a summary from the change logs; git history has each edit.

| id | file now | change | level | key |
|---|---|---|---|---|
| 0001 | L3-001-cpu-wait-includes-idle.md | hedge words removed; option lengths evened; key points rewritten | 300 |  |
| 0002 | L4-001-cpu-latency-frequency.md | Options added J; replaced H; stem reworded; option lengths evened; key points rewritten | 400 | A,C,D -> A,C,D,J |
| 0003 | L4-002-hyperthreading-vm-vs-esxi.md | Options replaced B,D,F,G,I; stem reworded; option lengths evened; key points rewritten | 400 |  |
| 0004 | L4-003-esxi-true-utilization-from-usage-core-utilization-and-utilization.md | Options added G; replaced D; stem reworded; option lengths evened; key points rewritten | 400 | C -> C,G |
| 0005 | L4-004-likely-vcpu-speed-on-a-busy-hyper-threaded-cluster.md | Options added F; stem made plural; numbers recomputed; key points rewritten | 400 |  |
| 0006 | L4-005-esxi-cpu-capacity-threads-not-hertz.md | stem reworded; numbers recomputed; key points rewritten | 400 |  |
| 0007 | L3-002-reading-an-intel-xeon-specification-base-all-core-turbo-tdp.md | numbers recomputed; option lengths evened; key points rewritten | 300 |  |
| 0008 | L4-006-which-counter-to-size-vm-cpu.md | Options replaced B,D; stem reworded; hedge words removed; key points rewritten | 400 |  |
| 0009 | L3-003-counters-where-a-vcpu-cannot-run-at-all.md | Options replaced E,F; stem reworded; key points rewritten | 300 |  |
| 0010 | L3-004-guest-os-run-queue-context-switch-windows-thread-states.md | Options replaced B; stem made plural; key points rewritten; notes cleaned | 300 |  |
| 0011 | L3-005-cpu-reservation-behaviour.md | Options added H; stem reworded; key points rewritten; notes cleaned | 300 |  |
| 0012 | L4-007-utilization-50-and-core-utilization-50.md | Options replaced E,H | 400 |  |
| 0013 | L3-006-reclaiming-vcpus-from-an-idle-vm.md | Options added G; replaced A; stem reworded; key points rewritten; notes cleaned | 300 |  |
| 0014 | L3-007-reservation-cpu-vs-memory.md | Options dropped B,G; replaced A; stem reworded; key points rewritten; notes cleaned | 300 | A,H -> A,F |
| 0015 | L3-008-vm-availability.md | Deferred: availability is outside release 1.0 | 300 |  |
| 0016 | L3-009-provider-consumer-ready-demand.md | stem reworded; key points rewritten; notes cleaned | 300 |  |
| 0017 | L3-010-overhead-classification.md | key points rewritten; notes cleaned | 300 |  |
| 0018 | L4-008-vm-vs-guest-os-metrics.md | Options replaced C; back to draft; stem reworded; option lengths evened; key points rewritten | 400 |  |
| 0019 | L3-011-performance-vs-capacity-view-of-utilization.md | Options added I,J; hedge words removed; key points rewritten; notes cleaned | 300 |  |
| 0020 | L3-012-usage-vm-vs-esxi.md | Options added I; dropped B; key points rewritten; notes cleaned | 400 -> 300 | B,D,G,H -> C,F,G |
| 0021 | L3-013-which-counter-to-size-vm-memory.md | stem reworded; hedge words removed; key points rewritten | 300 |  |
| 0022 | L3-014-relationship-between-vm-and-guest-os-memory-metrics.md | Options replaced E; stem reworded; key points rewritten | 300 |  |
| 0023 | L3-015-actual-vs-potential-memory-contention.md | Options replaced B; key points rewritten | 400 -> 300 |  |
| 0024 | L4-009-memory-reservation-behaviour.md | Options added F; replaced C; stem reworded; option lengths evened; key points rewritten | 400 | A,B -> A,B,F |
| 0025 | L4-010-balloon-0-while-swapped-and-compressed-are-not-0.md | Options added E,F,G,H; replaced D; stem made plural; option lengths evened; key points rewritten | 400 | B,C -> B,C,G |
| 0026 | L4-011-guest-queue-invisible.md | Options dropped H; stem reworded; hedge words removed; key points rewritten | 400 | A,D,H,I -> A,D,H |
| 0027 | L3-016-disk-latency-threshold.md | hedge words removed; key points rewritten; notes cleaned | 300 |  |
| 0028 | L3-017-latency-and-outstanding-io.md | Options added J; hedge words removed; key points rewritten; notes cleaned | 300 |  |
| 0029 | L1-001-network-units-vcenter-vs-esxtop.md | stem reworded; title changed; key points rewritten | 100 |  |
| 0032 | L1-002-esxtop-device-latency-davg.md | stem made plural; key points rewritten; notes cleaned | 100 |  |
| 0034 | L1-003-vcenter-virtual-disk-latency-counters.md | key points rewritten; notes cleaned | 100 |  |
| 0035 | L1-004-real-time-sample-interval.md | Options replaced D; stem reworded; key points rewritten; notes cleaned | 100 |  |
| 0036 | L1-005-cpu-ready-applies-to.md | Options replaced D; stem made plural; key points rewritten; notes cleaned | 100 |  |
| 0038 | L1-007-balloon-driver-in-guest-os.md | stem clue removed; title changed; key points rewritten | 100 |  |
| 0039 | L2-001-vm-dropped-vs-guest-os-counters.md | option lengths evened; notes cleaned | 200 |  |
| 0040 | L2-002-full-duplex-port-capacity.md | key points rewritten; notes cleaned | 200 |  |
| 0041 | L2-003-set-vnic-speed.md | Options replaced I; hedge words removed; key points rewritten; notes cleaned | 200 |  |
| 0042 | L2-004-vcenter-host-network-contention-counters.md | Options replaced C,D; back to draft; option lengths evened; key points rewritten; notes cleaned | 200 |  |
| 0043 | L2-005-gavg-formula.md | Options added I; hedge words removed; key points rewritten; notes cleaned | 200 |  |
| 0044 | L2-006-total-latency-weighted-by-commands.md | Options replaced C; key points rewritten; notes cleaned | 200 |  |
| 0045 | L2-007-datastore-read-iops-above-virtual-disk.md | Options added J; key points rewritten; notes cleaned | 200 | A,D -> A,D,J |
| 0046 | L2-008-datastore-provisioned-vs-used.md | stem reworded; key points rewritten; notes cleaned | 200 |  |
| 0047 | L2-009-rollup-dilutes-peaks.md | key points rewritten; notes cleaned | 200 |  |
| 0048 | L2-010-admission-control-counts-reservations.md | Options replaced B; stem reworded; hedge words removed; option lengths evened | 200 |  |
| 0049 | L2-011-totals-do-not-reconcile.md | Options added H; replaced D; option lengths evened; key points rewritten; notes cleaned | 200 | A,B,D,E -> A,B,D,E,H |
| 0050 | L3-018-esxtop-disk-device-where-is-latency.md | Options added E; back to draft; stem reworded; key points rewritten | 300 |  |
| 0051 | L2-012-vcf-operations-guest-vs-vm-metrics.md | key points rewritten | 200 |  |
| 0052 | L2-013-balloon-above-zero.md | Options replaced C; stem reworded; hedge words removed; key points rewritten | 200 |  |
| 0053 | L2-014-co-stop-multi-vcpu.md | stem made plural; option lengths evened; key points rewritten | 200 |  |
| 0054 | L4-012-is-overcommit-affecting-this-vm.md | Options replaced A,C,E; hedge words removed; option lengths evened; key points rewritten | 400 |  |
| 0056 | L4-013-host-consumed-with-no-vms.md | Options added H; key points rewritten; notes cleaned | 400 | A,C -> A,C,H |
| 0057 | L4-014-memory-tiering-candidate.md | Options added F; option lengths evened; key points rewritten; notes cleaned | 400 |  |
| 0058 | L4-015-host-demand-130-is-it-overloaded.md | Options dropped J; replaced C,F,G; numbers recomputed; key points rewritten; notes cleaned | 400 | A,C,F,G,J,K -> A,C,F,G,J |
| 0059 | L4-016-cpu-contention-vs-latency.md | Options added H; stem reworded; option lengths evened; key points rewritten | 400 |  |
| 0060 | L4-017-firewall-vm-receive-drops.md | Options replaced G; stem reworded; key points rewritten; notes cleaned | 400 |  |
| 0061 | L4-018-dropped-packets-95-percent-spike.md | key points rewritten; notes cleaned | 400 |  |
| 0062 | L4-019-high-latency-at-low-iops.md | Options replaced D,H,L; option lengths evened; key points rewritten; notes cleaned | 400 |  |
| 0063 | L4-020-wide-vm-numa-placement.md | hedge words removed; key points rewritten; notes cleaned | 400 |  |
| 0065 | L3-019-contention-on-one-host-drs-enabled.md | Options replaced D; stem reworded; key points rewritten; notes cleaned | 400 -> 300 |  |
| 0066 | L4-021-esxtop-ready-from-a-limit.md | Options replaced C; key points rewritten; notes cleaned | 400 |  |
| 0067 | L4-022-esxtop-numa-remote-memory.md | stem clue removed; hedge words removed; key points rewritten | 400 |  |
| 0068 | L4-023-esxtop-zip-vs-unzip.md | Options added I; key points rewritten; notes cleaned | 400 |  |
| 0069 | L3-020-esxtop-network-findings.md | Options added F; stem reworded; key points rewritten; notes cleaned | 400 -> 300 |  |
| 0070 | L4-024-esxtop-adapter-errors-and-paths.md | Options added K; key points rewritten; notes cleaned | 400 |  |
| 0072 | L4-025-vcenter-adapter-highest-latency.md | key points rewritten; notes cleaned | 400 |  |
| 0073 | L4-026-vcenter-resource-pool-tree-invalid.md | notes cleaned | 400 |  |
| 0074 | L3-021-vcenter-vm-transmit-drops-no-complaints.md | Options replaced C; stem reworded; key points rewritten; notes cleaned | 400 -> 300 |  |
| 0077 | L3-022-vmotion-downtime-units.md | stem reworded; option lengths evened; title changed | 400 -> 300 |  |
| 0079 | L4-027-memory-reclaim-from-40-vms.md | Options replaced G,I,K; key points rewritten; notes cleaned | 400 |  |
| 0080 | L4-028-datastores-running-out-of-space.md | key points rewritten; notes cleaned | 400 |  |
| 0082 | L4-030-which-vm-first-for-network-drops.md | duplicate facts reworded; key points rewritten; notes cleaned | 400 |  |
| 0083 | L4-031-vm-footprint-for-migration.md | attachment edited; stem reworded; numbers recomputed; option lengths evened | 400 |  |
| 0084 | L4-032-iscsi-network-vs-storage-bytes.md | attachment edited; stem clue removed; option lengths evened; key points rewritten | 400 |  |
| 0085 | L4-033-power-on-fails-at-low-usage.md | key points rewritten; notes cleaned | 400 |  |
| 0086 | L4-034-esxtop-batch-device-queue-full.md | Options added F; replaced D; option lengths evened; key points rewritten; notes cleaned | 400 | A,E -> A,E,F |
| 0088 | L4-035-bad-packets-which-host.md | Options replaced C; option lengths evened; key points rewritten; notes cleaned | 400 |  |
| 0089 | L4-036-disk-latency-peak-vs-average.md | Options added L; replaced D; option lengths evened; key points rewritten; notes cleaned | 300 -> 400 |  |
| 0090 | L4-037-erp-slow-after-change-window.md | Options replaced N; stem made plural; key points rewritten; notes cleaned | 400 |  |
| 0094 | L3-023-collect-every-metric-at-20-seconds.md | Options replaced G; key points rewritten; notes cleaned | 300 |  |
| 0095 | L3-024-windows-in-use-vs-vm-consumed.md | Options added K; key points rewritten; notes cleaned | 300 |  |
| 0097 | L4-038-how-many-silver-vms-fit-at-planning.md | stem reworded; numbers recomputed; key points rewritten | 400 |  |
| 0100 | L4-039-used-vm-vs-vcpu-instance.md | Options added J; replaced B; option lengths evened; key points rewritten | 400 |  |
| 0101 | L4-040-low-average-high-disparity.md | Options replaced C,F; option lengths evened; key points rewritten | 400 |  |
| 0102 | L4-041-demand-up-usage-down.md | Options replaced G; stem clue removed; option lengths evened; key points rewritten | 400 |  |
| 0104 | L4-043-run-above-used-more-vcpus.md | Options added L; hedge words removed; option lengths evened; key points rewritten | 400 |  |
| 0105 | L3-025-ready-summation-to-percent.md | Options dropped E; key points rewritten; notes cleaned | 300 |  |
| 0106 | L4-044-same-ready-quiet-vs-busy-vm.md | attachment edited; hedge words removed; option lengths evened; key points rewritten | 400 |  |
| 0107 | L3-026-oversized-vm-ready-and-co-stop.md | Options replaced D; hedge words removed; option lengths evened; key points rewritten | 300 |  |
| 0108 | L4-045-other-wait-after-backup.md | Options added L,M; stem reworded; option lengths evened; key points rewritten | 400 | A,B,C,I,J -> A,B,C,I,J,L |
| 0109 | L4-046-swap-wait-in-cpu-states.md | Options added F,G; dropped C; stem reworded; key points rewritten; notes cleaned | 400 | A,D,E -> A,C,D,F |
| 0110 | L3-027-overlap-from-other-vms-io.md | Options added I,J; stem reworded; option lengths evened; key points rewritten | 300 | A,C,E -> A,C,E,I |
| 0111 | L4-047-power-policy-latency-sensitive-app.md | Options added L; replaced B; hedge words removed; key points rewritten; notes cleaned | 300 -> 400 |  |
| 0112 | L4-048-latency-sensitivity-high.md | Options added G,H; option lengths evened; key points rewritten; notes cleaned | 400 |  |
| 0113 | L4-049-vnuma-after-move-to-older-host.md | Options replaced D; stem reworded; hedge words removed; key points rewritten | 400 |  |
| 0114 | L3-028-scale-up-vs-scale-out.md | Options replaced D; stem reworded; hedge words removed; key points rewritten | 300 |  |
| 0115 | L4-050-host-ready-average-hides-one-vm.md | attachment edited; option lengths evened; key points rewritten; notes cleaned | 400 |  |
| 0140 | L4-051-memory-limit-swap-and-compress.md | Options added L,M; replaced E; stem reworded; option lengths evened; key points rewritten | 400 |  |
| 0141 | L4-052-does-a-limit-cause-ballooning.md | Options added F; key points rewritten; notes cleaned | 400 |  |
| 0142 | L4-053-swap-target-vs-swapped.md | Options dropped I; replaced G; key points rewritten; notes cleaned | 400 | A,C,E,F,G,I -> A,C,E,F,G |
| 0143 | L4-054-swapped-is-not-swap-out-minus-swap-in.md | hedge words removed; key points rewritten; notes cleaned | 300 -> 400 |  |
| 0144 | L3-029-host-memory-state-at-6-gb-free.md | Options replaced E; key points rewritten; notes cleaned | 300 |  |
| 0145 | L3-030-page-sharing-between-identical-vms.md | Options replaced A; hedge words removed; notes cleaned | 300 |  |
| 0146 | L4-055-sharing-jumps-as-free-memory-falls.md | Options added O; hedge words removed; notes cleaned | 400 | A,B,C,J,M -> A,B,C,J,M,O |
| 0147 | L4-056-which-vm-waits-on-the-nvme-tier.md | Options added G; stem reworded; hedge words removed; key points rewritten | 400 | B,D,F -> B,D,F,G |
| 0148 | L4-057-granted-near-configured-on-a-new-vm.md | Options added G,H; stem reworded; notes cleaned | 400 | A,D,E -> A,D,E,G |
| 0149 | L2-015-what-memory-contention-counts.md | key points rewritten; notes cleaned | 200 |  |
| 0150 | L4-058-adding-vgpu-vms-to-an-overcommitted-cluster.md | Options replaced B,H; key points rewritten; notes cleaned | 400 |  |
| 0151 | L3-031-vm-memory-usage-100-after-an-agent-install.md | Options replaced B; stem reworded; notes cleaned | 300 |  |
| 0152 | L4-059-fully-reserved-vm-will-not-power-on.md | Options added H; key points rewritten; notes cleaned | 400 |  |
| 0153 | L4-060-vm-with-1-gb-pages.md | Options added F; option lengths evened; key points rewritten; notes cleaned | 400 |  |
| 0180 | L4-061-large-reads-at-high-latency.md | Options replaced D,F; option lengths evened; key points rewritten; notes cleaned | 400 |  |
| 0181 | L3-032-swap-space-for-a-mass-power-on.md | hedge words removed; duplicate facts reworded; key points rewritten | 300 |  |
| 0182 | L3-033-guest-deleted-data-datastore-unchanged.md | key points rewritten; notes cleaned | 300 |  |
| 0183 | L4-062-protect-a-database-from-a-noisy-vm.md | Options added K,L; stem reworded; key points rewritten; notes cleaned | 400 | C,E,H,J -> C,E,H,J,K |
| 0184 | L4-063-datastore-average-hides-one-vm.md | Options replaced E; hedge words removed; key points rewritten; notes cleaned | 400 |  |
| 0185 | archive/L3-031-rdm-io-missing-from-datastore-counters.md | Retired: near-copy of 0426; moved to archive | 300 |  |
| 0186 | L4-064-nfs-datastore-latency-in-esxtop.md | Options added G,H; stem reworded; key points rewritten; notes cleaned | 400 | A,C,D,E -> A,C,D,E,G |
| 0187 | L1-008-keep-a-two-week-old-snapshot.md | Options replaced G; stem reworded; title changed; key points rewritten | 100 |  |
| 0188 | L4-065-array-iops-above-datastore-iops.md | stem reworded; numbers recomputed; hedge words removed | 400 |  |
| 0210 | L3-034-uplink-team-one-port-saturated.md | Options replaced F; stem reworded; hedge words removed; option lengths evened | 400 -> 300 |  |
| 0211 | L3-035-small-packets-low-bandwidth.md | key points rewritten; notes cleaned | 300 |  |
| 0212 | L4-066-receive-processing-on-one-vcpu.md | Options replaced J; stem reworded; hedge words removed; notes cleaned | 400 |  |
| 0213 | L3-036-jumbo-frames-mtu-mismatch.md | Options added G; key points rewritten; notes cleaned | 300 |  |
| 0214 | L3-037-network-latency-in-vsphere.md | stem reworded; hedge words removed; option lengths evened | 300 |  |
| 0215 | L4-067-network-io-control-during-mass-vmotion.md | Options replaced E; notes cleaned | 400 |  |
| 0216 | L4-068-broadcast-storm-across-hosts.md | stem clue removed; duplicate facts reworded; key points rewritten | 400 |  |
| 0217 | L4-069-uplink-load-vs-sum-of-vm-traffic.md | Options replaced B; key points rewritten; notes cleaned | 400 |  |
| 0230 | L4-070-resource-pool-share-dilution.md | Options added F,G,H; key points rewritten; notes cleaned | 400 |  |
| 0231 | L3-038-counter-missing-from-history.md | Options replaced C; key points rewritten; notes cleaned | 300 |  |
| 0232 | L3-039-cluster-drs-score-high-one-vm-slow.md | Options dropped F; hedge words removed; key points rewritten | 300 | A,C,D,F,G -> A,C,D,F |
| 0233 | L3-040-usable-capacity-ha-and-maintenance.md | stem reworded; option lengths evened; key points rewritten | 300 |  |
| 0234 | L3-041-overcommit-per-thread-or-per-core.md | hedge words removed; option lengths evened; key points rewritten | 400 -> 300 |  |
| 0235 | L4-071-capacity-forecast-averages-hide-month-end.md | Options added N; key points rewritten; notes cleaned | 400 |  |
| 0236 | L4-072-cpu-usage-dropped-after-downsize.md | Options replaced D; option lengths evened; key points rewritten; notes cleaned | 400 |  |
| 0237 | L3-042-api-export-vs-chart-values.md | Options dropped D; hedge words removed; key points rewritten; notes cleaned | 400 -> 300 | A,D,G -> A,F |
| 0238 | L4-073-dpm-morning-ready.md | notes cleaned | 400 |  |
| 0239 | L4-074-monday-web-slow-pool-limit.md | Options added O; dropped M; hedge words removed; key points rewritten; notes cleaned | 400 | A,B,C,F,G,H,I,M,O -> A,B,C,F,G,H,I,N |
| 0240 | L4-075-ha-performance-degradation-warning.md | Options dropped C; replaced E; stem clue removed; option lengths evened; notes cleaned | 400 | A,C,D -> A,C |
| 0260 | L4-076-linux-load-average-tasks-waiting-on-io.md | option lengths evened; key points rewritten; notes cleaned | 400 |  |
| 0261 | L4-077-windows-processor-queue-with-idle-vcpus.md | Options added G; stem reworded; option lengths evened; key points rewritten | 400 |  |
| 0262 | L4-078-slow-windows-application-where-to-start.md | Options replaced G; option lengths evened; key points rewritten; notes cleaned | 400 |  |
| 0263 | L3-043-linux-free-memory-near-zero.md | Options added G; notes cleaned | 300 | B -> B,G |
| 0264 | L4-079-windows-free-low-standby-high.md | Options replaced D; key points rewritten; notes cleaned | 400 |  |
| 0265 | L4-080-guest-paging-with-no-vm-swap.md | hedge words removed; key points rewritten; notes cleaned | 400 |  |
| 0266 | L4-081-linux-steal-time-and-windows-busy-time.md | Options replaced A,C; back to draft; stem clue removed; hedge words removed; option lengths evened | 400 |  |
| 0267 | L4-082-two-sockets-one-numa-node.md | hedge words removed; option lengths evened; key points rewritten | 400 |  |
| 0268 | L4-083-tcp-retransmits-with-no-vsphere-drops.md | hedge words removed; notes cleaned | 300 -> 400 |  |
| 0269 | L4-084-sql-server-holds-its-memory.md | Options replaced A,D; stem reworded; numbers recomputed; key points rewritten | 400 |  |
| 0270 | L3-044-windows-commit-limit-without-page-file.md | Options replaced E; hedge words removed; key points rewritten; notes cleaned | 300 |  |
| 0271 | L2-016-vmware-tools-not-running.md | key points rewritten; notes cleaned | 200 |  |
| 0272 | L4-085-linux-oom-kill-from-a-cgroup-limit.md | key points rewritten; notes cleaned | 400 |  |
| 0273 | L2-017-gpu-memory-used-on-an-idle-host.md | notes cleaned | 200 |  |
| 0274 | L4-086-alert-wait-cycles-symptom-and-alert-level.md | Options added F; stem made plural; key points rewritten; notes cleaned | 400 |  |
| 0275 | L3-045-one-alert-warning-and-critical-symptoms.md | stem made plural; key points rewritten; notes cleaned | 400 -> 300 |  |
| 0277 | L4-087-getting-2-second-esx-top-data.md | stem reworded; hedge words removed; option lengths evened | 400 |  |
| 0279 | L3-046-keeping-a-business-application-current.md | Options replaced K; hedge words removed; key points rewritten; notes cleaned | 400 -> 300 |  |
| 0290 | L4-088-ha-slot-policy-one-large-reservation.md | Options added F; key points rewritten; notes cleaned | 400 | A -> A,F |
| 0291 | L4-089-memory-limit-balloons-on-an-idle-host.md | Options added N; replaced L; stem reworded; option lengths evened; key points rewritten | 400 |  |
| 0292 | L4-090-full-reservations-stop-drs-migrations.md | Options added F; stem clue removed; key points rewritten; notes cleaned | 400 |  |
| 0293 | L4-091-cpu-hot-add-and-the-numa-topology.md | Options added I,J; stem reworded; notes cleaned | 400 | A,E,F,G -> A,E,F,G,J |
| 0294 | L4-092-dense-mode-below-the-cpu-threshold.md | Options replaced A; key points rewritten; notes cleaned | 400 |  |
| 0295 | L3-047-splitrx-on-vmxnet3-and-e1000e.md | stem reworded; option lengths evened; notes cleaned | 400 -> 300 |  |
| 0296 | L4-093-swap-file-space-at-power-on.md | Options added F,G; stem made plural; key points rewritten; notes cleaned | 400 |  |
| 0297 | L4-094-host-local-swap-and-vmotion.md | Options replaced A,E; stem reworded; notes cleaned | 400 |  |
| 0298 | L4-095-over-allocated-memory-and-overhead.md | Options replaced D,E,F,I; stem clue removed; key points rewritten; notes cleaned | 400 |  |
| 0310 | L4-096-storage-drs-full-datastore-in-a-healthy-cluster.md | Options added J; stem reworded; key points rewritten; notes cleaned | 400 |  |
| 0311 | L4-097-windows-disk-queue-length-of-48.md | Options replaced B,E; stem reworded; key points rewritten | 400 |  |
| 0313 | L4-098-peak-transmitted-packet-dropped-percent.md | Options added H; dropped G; key points rewritten; notes cleaned | 400 | B,C,E,F,G -> B,C,E,F |
| 0314 | L4-099-population-alert-value-type-for-a-host.md | Options added F; stem made plural; key points rewritten | 400 |  |
| 0330 | L4-100-ha-failover-percentage-uneven-hosts.md | Deferred: key needs vendor facts missing from the knowledge base | 400 |  |
| 0331 | L4-101-esxtop-load-average-at-full-utilization.md | Options replaced G; stem clue removed; hedge words removed; key points rewritten | 400 |  |
| 0340 | L4-102-resource-pool-alert-nested-pool.md | stem reworded; option lengths evened; key points rewritten | 400 |  |
| 0341 | L4-103-resource-pool-alert-microbursts-and-the-5-minute-average.md | Options dropped B; replaced H; stem clue removed; key points rewritten; notes cleaned | 400 | B,C,F,H,I,J -> B,E,G,H,I |
| 0342 | L4-104-datastore-latency-alert-from-vm-latency.md | Options replaced E; option lengths evened; key points rewritten; notes cleaned | 400 |  |
| 0343 | L4-105-datastore-space-alert-fired-what-next.md | Options replaced B; option lengths evened; key points rewritten; notes cleaned | 400 |  |
| 0344 | L4-106-distributed-switch-alert-request.md | Options added F; replaced E; stem made plural; option lengths evened; key points rewritten | 400 | A -> A,F |
| 0345 | L4-107-port-group-drops-received-or-transmitted.md | Options replaced E; stem reworded; key points rewritten; notes cleaned | 400 |  |
| 0346 | L4-108-port-group-drops-tcp-and-udp-red-only.md | Options replaced C,D,G,H,J,K; stem clue removed; key points rewritten; notes cleaned | 400 |  |
| 0347 | L4-109-vm-cpu-alert-activity-gate-in-ghz.md | Options added F,G; replaced D; stem made plural; title changed; key points rewritten | 400 | A -> A,F,G |
| 0350 | L4-110-vm-night-job-health-check-findings.md | Options dropped A,B,D,F; stem clue removed; key points rewritten | 400 | B,C,F,G,H,K,N -> A,C,D,G,J |
| 0351 | L3-048-vcenter-only-contention-history-at-default-level.md | Options added F,G,H; replaced D; stem made plural; option lengths evened; key points rewritten | 400 -> 300 | C -> C,F |
| 0352 | L4-111-host-health-check-which-host-opens-a-flow.md | Options dropped D; replaced A; option lengths evened; key points rewritten; notes cleaned | 400 |  |
| 0353 | L4-112-busy-healthy-hosts-and-one-host-failure.md | Options dropped D,F,G,H,J; stem reworded; key points rewritten; notes cleaned | 400 | A,C,E,G,I,K,N -> A,C,D,E,F,I |
| 0354 | L4-113-cluster-percentile-hides-one-hot-host.md | Options added F,G; option lengths evened; key points rewritten; notes cleaned | 400 | C -> C,F |
| 0355 | L4-114-cluster-take-12-reserved-vms.md | Options dropped H,J; replaced D; stem reworded; key points rewritten; notes cleaned | 400 | A,C,E,G,J,K,L,M,N -> A,C,E,G,I,J,K,L |
| 0356 | L4-115-nine-day-old-20-second-peak.md | key points rewritten | 400 |  |
| 0357 | L4-116-same-vm-two-tools-two-numbers.md | Options replaced A,C,M; hedge words removed; option lengths evened; key points rewritten | 400 |  |
| 0358 | archive/L4-126-vm-size-requests-across-report-set.md | Retired: options not decidable from the knowledge base; moved to archive | 400 |  |
| 0359 | L4-117-windows-disk-queue-of-300-with-low-virtual-disk-latency.md | Options added F,G; replaced D; stem reworded; option lengths evened; key points rewritten | 400 | B -> B,F |
| 0360 | L4-118-linux-two-disks-same-queue-and-utilization.md | Options replaced E,H; stem reworded; numbers recomputed; key points rewritten | 400 |  |
| 0361 | L4-119-two-queue-limits-on-one-virtual-disk.md | Options replaced C,H; stem reworded; key points rewritten; notes cleaned | 400 |  |
| 0362 | L3-049-esxi-cpu-demand-vcenter-vs-vcf-operations.md | Options replaced B,E; stem reworded; option lengths evened; key points rewritten | 300 |  |
| 0363 | L4-120-esxi-cpu-demand-differs-between-tools.md | Options replaced C,D; stem made plural; option lengths evened; key points rewritten | 400 |  |
| 0364 | L3-050-ready-read-against-run.md | Options replaced A; hedge words removed; option lengths evened; key points rewritten | 300 |  |
| 0365 | L3-051-default-shares-follow-vcpu-count.md | Options replaced I; option lengths evened; key points rewritten | 300 |  |
| 0366 | L3-052-vcpu-usage-disparity-two-vms.md | Options replaced B,C; hedge words removed; option lengths evened; key points rewritten | 300 |  |
| 0367 | L3-053-swap-wait-cpu-state-memory-cause.md | Options added J; stem reworded; option lengths evened; key points rewritten | 300 |  |
| 0368 | L4-121-task-manager-full-vcenter-ready-high.md | Converted from screenshots to 2 generated export files; option lengths evened; key points rewritten | 400 |  |
| 0369 | L3-054-ready-ms-burst-on-two-charts.md | Converted from screenshots to 2 generated export files; Options replaced E; hedge words removed; option lengths evened; key points rewritten | 300 |  |
| 0370 | L4-122-month-chart-vs-vcf-operations-batch.md | Converted from screenshots to 6 generated export files; Options dropped C,I; replaced B; stem reworded; option lengths evened | 400 | A,E,G,I -> A,D,F |
| 0371 | L4-123-usage-near-100-net-run-lower.md | Converted from screenshots to 3 generated export files | 400 |  |
| 0372 | L3-055-cpu-wait-on-a-quiet-vm-chart.md | Converted from screenshots to 1 generated export file; option lengths evened; key points rewritten | 300 |  |
| 0373 | L4-124-wide-vm-ready-co-stop-few-cpus-busy.md | Converted from screenshots to 2 generated export files; hedge words removed; option lengths evened; key points rewritten | 400 |  |
| 0374 | L4-125-host-usage-above-100-alert.md | Converted from screenshots to 2 generated export files; Options dropped A,J; replaced D,F; option lengths evened; key points rewritten | 400 | A,D,F,G,J -> C,E,F |
| 0375 | L3-056-esxtop-co-stop-on-a-half-busy-host.md | Converted from screenshots to 0 generated export files; Options replaced C,G; hedge words removed; option lengths evened; key points rewritten | 300 |  |
| 0376 | L3-057-esxtop-time-a-vcpu-could-not-run.md | Converted from screenshots to 0 generated export files; Options replaced E,G,H; key points rewritten | 300 |  |
| 0377 | L4-126-esxtop-load-average-above-three.md | Converted from screenshots to 0 generated export files; Options dropped H; replaced E,F | 400 | A,D,E,F,H -> A,D,E,F |
| 0378 | L3-058-host-average-hides-one-busy-thread.md | Options replaced D; option lengths evened; key points rewritten | 300 |  |
| 0379 | L4-127-one-thread-saturated-host-under-15.md | Converted from screenshots to 2 generated export files; Options added I; replaced F,H; option lengths evened; key points rewritten | 400 |  |
| 0380 | L3-059-linux-steal-time-needs-the-steal-clock.md | option lengths evened; key points rewritten | 300 |  |
| 0381 | L4-128-linux-st-zero-vcenter-ready-high.md | Converted from screenshots to 1 generated export file; option lengths evened; key points rewritten | 400 |  |
| 0382 | L2-018-windows-available-standby-modified-free.md | Options replaced H; key points rewritten | 200 |  |
| 0383 | L3-060-windows-paging-unseen-by-vm-counters.md | option lengths evened; notes cleaned | 300 |  |
| 0384 | L3-061-vm-wait-on-the-nvme-memory-tier.md | Options added I; key points rewritten; notes cleaned | 300 |  |
| 0385 | L3-062-host-memory-usage-high-without-balloon.md | Converted from screenshots to 2 generated export files; notes cleaned | 300 |  |
| 0386 | L4-129-windows-in-use-falls-consumed-stays.md | Converted from screenshots to 2 generated export files; stem reworded; numbers recomputed; key points rewritten | 400 |  |
| 0387 | L3-063-linux-guest-free-memory-low-all-week.md | Converted from screenshots to 1 generated export file; Options replaced D; key points rewritten | 300 |  |
| 0388 | L4-130-vm-balloon-flat-for-days.md | Converted from screenshots to 2 generated export files; Options added H; key points rewritten | 300 -> 400 |  |
| 0389 | archive/L4-140-esxtop-which-vms-wait-on-swapped-memory.md | Retired: partner 0068 already gives the same text; moved to archive | 400 |  |
| 0390 | L3-064-vsan-host-consumed-in-maintenance-mode.md | Converted from screenshots to 1 generated export file; Options replaced G; hedge words removed; notes cleaned | 400 -> 300 |  |
| 0391 | L3-065-host-compressed-flat-with-balloon-at-zero.md | Converted from screenshots to 1 generated export file; Options replaced C; key points rewritten; notes cleaned | 300 |  |
| 0392 | L3-066-vm-memory-contention-follows-swap-in.md | Converted from screenshots to 1 generated export file; key points rewritten | 300 |  |
| 0393 | L3-067-windows-commit-limit-in-task-manager.md | Converted from screenshots to 1 generated export file; hedge words removed; key points rewritten; notes cleaned | 300 |  |
| 0394 | L3-068-vm-memory-usage-vcenter-vs-vcf-operations.md | stem reworded; key points rewritten; notes cleaned | 300 |  |
| 0395 | L4-131-vm-memory-usage-differs-between-tools.md | Converted from screenshots to 2 generated export files; option lengths evened; duplicate facts reworded; notes cleaned | 400 |  |
| 0396 | L3-069-vm-memory-usage-without-guest-data.md | stem reworded; notes cleaned | 300 |  |
| 0397 | L4-132-vm-memory-usage-dips-for-half-an-hour.md | Converted from screenshots to 6 generated export files; key points rewritten | 400 |  |
| 0398 | L3-070-esxtop-mem-overcommit-average.md | Options added J; replaced F; hedge words removed; key points rewritten | 300 |  |
| 0399 | L3-071-esxtop-memory-overcommit-on-a-quiet-host.md | Converted from screenshots to 0 generated export files; Options replaced C; key points rewritten; notes cleaned | 300 |  |
| 0400 | L3-072-guest-free-memory-after-a-downsize.md | Options added H; replaced F; stem reworded; key points rewritten | 300 |  |
| 0401 | L4-133-guest-memory-four-weeks-across-a-downsize.md | Converted from screenshots to 1 generated export file; Options replaced E; option lengths evened; key points rewritten; notes cleaned | 400 |  |
| 0402 | L3-073-esxi-memory-latency-and-its-vms.md | stem reworded | 300 |  |
| 0403 | L3-074-one-vm-waits-while-host-latency-stays-low.md | Converted from screenshots to 2 generated export files | 400 -> 300 |  |
| 0404 | L3-075-vm-transmit-packets-dropped.md | Options replaced F,G,H; numbers recomputed; option lengths evened | 300 |  |
| 0405 | L3-076-rank-hosts-by-latency-percentile.md | Options added I; key points rewritten; notes cleaned | 300 |  |
| 0406 | L3-077-storage-adapter-highest-latency.md | Options added H; replaced B; stem reworded; option lengths evened; key points rewritten | 300 |  |
| 0407 | L3-078-uplink-load-vs-vm-traffic.md | Options replaced G; option lengths evened | 300 |  |
| 0408 | L3-079-array-lun-iops-vs-datastore-iops.md | stem reworded; option lengths evened; key points rewritten | 300 |  |
| 0409 | L3-080-esxi-vmnic-error-counters.md | hedge words removed; option lengths evened; duplicate facts reworded | 300 |  |
| 0410 | L3-081-iscsi-storage-io-as-network-traffic.md | option lengths evened; key points rewritten | 300 |  |
| 0411 | L3-082-broadcast-flood-in-a-vlan.md | Options dropped G; replaced F; key points rewritten | 300 |  |
| 0412 | L3-083-esxtop-and-vcenter-vm-transmit-rate.md | Converted from screenshots to 1 generated export file; Options added L; key points rewritten | 300 | A,C,H -> A,C,H,L |
| 0413 | L3-084-vmnic-usage-above-link-speed.md | Converted from screenshots to 1 generated export file; Options replaced G; numbers recomputed; notes cleaned | 300 |  |
| 0414 | L3-085-command-latency-hides-slow-writes.md | Converted from screenshots to 1 generated export file; Options dropped G; replaced H; key points rewritten; notes cleaned | 300 | A,C,G,H -> A,C,G |
| 0415 | L4-134-small-packets-telemetry-vm.md | Converted from screenshots to 1 generated export file; Options replaced H; stem clue removed; key points rewritten; notes cleaned | 400 |  |
| 0416 | L3-086-outstanding-reads-at-low-latency.md | Converted from screenshots to 1 generated export file; duplicate facts reworded | 300 |  |
| 0417 | L3-087-datastore-iops-vs-one-host.md | Converted from screenshots to 2 generated export files; Options replaced G,I; option lengths evened; key points rewritten | 300 |  |
| 0418 | L4-135-windows-disk-time-above-1000-percent.md | Converted from screenshots to 2 generated export files; Options replaced L; stem reworded; key points rewritten | 400 |  |
| 0419 | archive/L4-148-linux-util-near-100-at-low-await.md | Retired: partner 0360 already gives the same text; moved to archive | 400 |  |
| 0420 | L3-088-vm-receive-drops-linux-shows-none.md | Converted from screenshots to 1 generated export file; Options replaced H | 300 |  |
| 0421 | L4-136-peak-transmit-drop-percent-one-cycle.md | Converted from screenshots to 4 generated export files; Options dropped A; key points rewritten | 400 | A,C,G,H -> B,F,G |
| 0422 | L3-089-vm-disk-latency-aggregate-and-one-disk.md | Options replaced G; hedge words removed; key points rewritten | 300 |  |
| 0423 | L4-137-one-slow-disk-behind-low-vm-latency.md | Converted from screenshots to 3 generated export files; duplicate facts reworded; key points rewritten | 400 |  |
| 0424 | L3-090-virtual-disk-iops-limit-latency.md | Options replaced H; key points rewritten | 300 |  |
| 0425 | L4-138-slow-scan-under-an-iops-limit.md | Converted from screenshots to 1 generated export file | 400 |  |
| 0426 | L3-091-vm-virtual-disk-datastore-and-disk-charts.md | duplicate facts reworded; key points rewritten | 300 |  |
| 0427 | L4-139-vm-storage-charts-do-not-match.md | Converted from screenshots to 4 generated export files | 400 |  |
| 0428 | L3-092-linux-load-average-what-it-counts.md | hedge words removed | 300 |  |
| 0429 | L3-093-resource-pool-cpu-limit-across-hosts.md | Options dropped A,E; key points rewritten; notes cleaned | 300 | A,C,E,G -> B,E |
| 0430 | L3-094-capacity-remaining-what-it-measures.md | Options added K; option lengths evened; key points rewritten; notes cleaned | 300 |  |
| 0431 | L4-140-cluster-cpu-above-90-request-for-hosts.md | Converted from screenshots to 2 generated export files; Options replaced H; option lengths evened; key points rewritten; notes cleaned | 400 |  |
| 0432 | L3-095-two-minute-burst-real-time-vs-past-day.md | Converted from screenshots to 2 generated export files; option lengths evened; key points rewritten | 300 |  |
| 0433 | L3-096-drs-score-high-one-vm-low.md | Converted from screenshots to 2 generated export files; Options added G,H; dropped G; notes cleaned | 300 | B,D,G -> B,D |
| 0434 | L3-097-perfmon-queue-on-a-4-vcpu-vm.md | Converted from screenshots to 1 generated export file; Options added J; key points rewritten | 300 | A,D,E -> A,D,E,J |
| 0435 | L3-098-powered-on-vm-with-a-crashed-windows.md | Deferred: availability is outside release 1.0 | 300 |  |
| 0436 | L4-141-two-sockets-in-windows-one-numa-node.md | Converted from screenshots to 0 generated export files; option lengths evened | 400 |  |
| 0437 | L3-099-cluster-cpu-peak-and-the-busiest-host.md | option lengths evened; duplicate facts reworded; key points rewritten | 300 |  |
| 0438 | L4-142-cluster-at-70-one-host-near-100.md | Converted from screenshots to 1 generated export file; Options replaced G,H; numbers recomputed; option lengths evened; key points rewritten | 400 |  |
| 0439 | L3-100-six-minute-job-across-two-cycles.md | stem reworded; option lengths evened; key points rewritten | 300 |  |
| 0440 | L4-143-five-minute-job-shows-as-two-half-points.md | Converted from screenshots to 2 generated export files; Options added H; replaced G; hedge words removed; option lengths evened | 400 | B,C,F -> B,C,F,H |
| 0441 | L3-101-what-a-vm-memory-reservation-changes.md | Options replaced I; key points rewritten; notes cleaned | 300 |  |
| 0442 | L4-144-vm-memory-chart-flat-after-reservation-change.md | Options added J; replaced H; numbers recomputed; key points rewritten | 400 | B,D,F,I -> B,D,F,I,J |
| 0443 | L4-145-side-channel-aware-scheduler-after-l1tf-audit.md | New question, 10 options: Side-Channel-Aware Scheduler turned on after an L1TF audit | 400 |  |
| 0444 | L4-146-vm-cpu-usage-sum-above-host-usage.md | New question, 10 options: Sum of VM CPU Usage above host CPU Usage | 400 |  |
| 0445 | L3-102-host-cpu-wait-and-thread-idle-after-vdi-move.md | New question, 10 options: Host CPU Wait and thread Idle after a VDI move | 300 |  |
| 0446 | L4-147-epyc-nps4-on-a-mixed-size-cluster.md | New question, 10 options: NPS-4 on an AMD EPYC 9005 cluster of mixed VM | 400 |  |
| 0447 | L4-148-fewer-cycles-on-a-new-cpu-generation.md | New question, 9 options: Fewer cycles for the same job on a new CPU | 400 |  |
| 0448 | L3-103-bios-and-power-settings-on-new-hosts.md | New question, 9 options: BIOS and power settings on new hosts | 300 |  |
| 0449 | L4-149-latency-sensitivity-high-with-hyperthreading.md | New question, 9 options: Latency Sensitivity High with Hyperthreading on a Java service | 400 |  |
| 0450 | L4-150-balloons-that-do-not-empty.md | New question, 11 options: Balloons that do not empty | 400 |  |
| 0451 | L4-151-host-granted-above-physical-memory.md | New question, 10 options: Host Granted above physical memory | 400 |  |
| 0452 | L4-152-compressed-memory-and-the-consumed-drop.md | New question, 10 options: Compressed memory and the Consumed drop | 400 |  |
| 0453 | L4-153-powercli-memory-report-of-a-sql-vm.md | New question, 11 options: PowerCLI memory report of a SQL Server VM | 400 |  |
| 0454 | L4-154-memory-demand-far-below-consumed.md | New question, 11 options: Memory Demand far below Consumed | 400 |  |
| 0455 | L4-155-batch-vm-pages-under-a-memory-limit.md | New question, 10 options: Batch VM pages under a memory limit | 400 |  |
| 0456 | L4-156-ha-admission-green-on-a-tiered-cluster.md | New question, 9 options: HA admission green on a tiered cluster | 400 |  |
| 0457 | L4-157-direct-device-access-for-packet-heavy-vms.md | New question, 12 options: Direct device access for four packet-heavy VMs | 400 |  |
| 0458 | L4-158-backup-repository-receives-on-one-uplink.md | New question, 10 options: Backup repository receives on one uplink | 400 |  |
| 0459 | L3-104-static-interrupt-coalescing-on-a-trading-vm.md | New question, 9 options: Static interrupt coalescing on a trading VM | 300 |  |
| 0460 | L4-159-template-datastore-never-returns-space-to-the-array.md | New question, 9 options: Template datastore never returns space to the array | 400 |  |
| 0461 | L4-160-datastore-virtual-disk-below-the-vm-sum.md | New question, 9 options: Datastore virtual disk space below the sum of its VMs | 400 |  |
| 0462 | L4-161-highest-disk-latency-above-every-device.md | New question, 9 options: Highest disk latency above every device | 400 |  |
| 0463 | L4-162-shared-disk-iops-drop-to-zero-on-one-node.md | New question, 8 options: Shared disk IOPS drop to zero on one cluster node | 400 |  |
| 0464 | L3-105-vcls-retreat-mode-on-vcenter-9-1.md | New question, 8 options: vCLS Retreat Mode on a vCenter 9.1 cluster | 300 |  |
| 0465 | L4-163-patching-a-host-with-pinned-vms.md | New question, 9 options: Patching one host of a five-host cluster | 400 |  |
| 0466 | L4-164-drs-default-threshold-and-incompatible-vms.md | New question, 8 options: DRS ignores bursts and incompatible VMs | 400 |  |
| 0467 | L4-165-esxtop-ready-against-the-vm-performance-dashboard.md | New question, 8 options: esxtop Ready against the VM Performance dashboard | 400 |  |
| 0468 | L4-166-guest-os-run-queue-alert-on-a-16-vcpu-vm.md | New question, 9 options: Guest OS run queue alert on a 16-vCPU VM | 400 |  |
| 0469 | L3-106-vsphere-documentation-guidance-as-a-checklist.md | New question, 8 options: vSphere documentation guidance as a checklist | 300 |  |
| 0470 | L3-107-three-small-clusters-or-one-large.md | New question, 9 options: Three small clusters or one large one | 300 |  |

## Appendix B. Knowledge-base issues found by the audit
For the author and plan.md M1; no knowledge file was changed. Each item was checked against the file's text when the list was made.
Sources: 11 review reports, 11 break reports, 8 blind-key reports. BROKEN items dropped. Quotes re-checked by grep against knowledge/ on 2026-11-16. Question ids are numeric (L-ids mapped from benchmark/questions).

### Contradictions

Verdict is HOLDS for every row (a second reviewer held it, or nobody broke it).

| # | Files | Side A | Side B | Questions | Verdict |
|---|---|---|---|---|---|
| C1 | vsphere/object-types/cluster/concepts/admission-control-and-cluster-state | "A VM with no reservation passes CPU and memory admission control" | vendor 9.1 (p. 1971): 32 MHz default charged per unreserved VM; file has no 32 MHz | 0330 (B, E), 0290 | HOLDS |
| C2 | same file | State table: red only as Invalid | "A cluster also turns red when HA can no longer meet its failover capacity" | 0073 (stem must exclude the HA cause) | HOLDS (tidy-up) |
| C3 | vsphere/object-types/cluster/configuration/drs-migration-levels vs vsphere/object-types/cluster/cluster-health-check | "Score above 80%: no performance impact" | "DRS Score 80%+ means no contention" | 0354 D, 0232 B | HOLDS |
| C4 | vsphere/object-types/cluster/cluster-vm-contention | step 2: "A depth row not green with the breadth rows green: one VM deep" | several VMs on one host (14 of 200 on esx-04) belong in step 3 | 0354 | HOLDS |
| C5 | vsphere/technology/cpu/concepts/virtual-numa vs vSphere 9.1 docs p. 1939 | "ESXi rebuilds the topology at every power cycle" | docs: topology fixed once initialised unless vCPU count changes (numa.autosize.once); Q216 open | 0113, 0267 (avoid it) | HOLDS |
| C6 | vsphere/technology/cpu/metrics/host/demand | "Demand above Usage can be reservation alone" (unscoped) | same file scopes it: "in VCF Operations the gap can be reservation alone" | 0058 (key point E) | HOLDS |
| C7 | vsphere/technology/cpu/concepts/cpu-frequency | "The gap between base and highest Turbo is about 2x" | same file: Single-Core Turbo 7%-77% above base | none named | HOLDS |
| C8 | vsphere/technology/cpu/metrics/virtual-motherboard/run, net-run vs overlap | "Remove Overlap first: Net Run = Run - Overlap" | overlap, Effect on the Guest OS: "Include Overlap in Guest OS sizing"; overlap.md also says "removes it from Run" | 0008, 0110 E, 0371 D | HOLDS |
| C9 | glossary (Other Wait "Also called: VM Wait") vs vsphere/tools/esxtop/cpu | alias VM Wait = Other Wait | "%VMWAIT includes %SWPWT. VCF Operations uses a VM Wait that excludes Swap Wait" | 0376 | HOLDS |
| C10 | vsphere/tools/esxtop/cpu vs vsphere/technology/cpu/metrics/virtual-motherboard/wait | "%WAIT - %IDLE (= %VMWAIT) of the vCPU worlds estimates guest IO wait" | "VM Wait equals Guest OS IO Wait" is a misconception | 0376 (option %VMWAIT) | HOLDS |
| C11 | vsphere/tools/esxtop/cpu | "%CSTP \| Co-stop, 100% per vCPU" | "%RDY \| Ready, summed over vCPUs: can exceed 100%" (group rows sum %CSTP too) | 0375 | HOLDS |
| C12 | vsphere/technology/cpu/metrics/virtual-motherboard/used vs sp5-framework/capacity/vm-footprint-sizing | "Not capacity ... Run is the capacity counter" | "Used, not Run, carries the work" (capacity sizing) | 0083 | HOLDS |
| C13 | vsphere/architecture/overhead vs sp5-framework/capacity/overcommit | "Overcommit: total vCPUs on the host exceed total physical cores" | "CPU: per physical thread, not per core" | none named | HOLDS |
| C14 | sp5-framework/concepts/performance-vs-capacity vs sp5-framework/observability/collection-interval | capacity interval "Hourly or daily average" | capacity "15 minutes, the average, not the peak" | 0094 K | HOLDS (minor: collection vs reading) |
| C15 | vsphere/technology/storage/troubleshooting/host-storage-latency, metrics/host/adapter-and-path vs sp5-framework/observability/aggregation | "Use the 95th or 99th percentile, not the maximum" | "The 95th percentile alone does not separate the two" | none named | HOLDS (minor) |
| C16 | sp5-framework/capacity/rightsizing | heading "Cost of an oversized VM" | bullets "Lower Co-stop and Ready", "Faster snapshots" are benefits of a smaller VM | none named | HOLDS (editorial) |
| C17 | vsphere/tools/esxtop/cpu vs vsphere/technology/cpu/images (hyper-threading, cpu-measurement-levels) | text: ESXi 500/1,000 MHz; Usage = average of thread Usage | images: 625/1,250 MHz; Utilization reads 200% | none named | HOLDS (already in review_notes) |
| C18 | guest-os/memory/windows-memory | "read free memory against the Guest OS KPI row" (poor at low Free) | "Near-zero free memory with healthy other metrics is ideal: no waste" | 0382 E/H, 0264 F | HOLDS |
| C19 | guest-os/cpu/metrics/processor-time vs run-queue, guest-os-alerts, ms-windows-slow | "The split is of little use" | Privileged Time high and User Time low read as driver or locking issue | 0261 D, 0434 | HOLDS |
| C20 | guest-os/system/troubleshooting/ms-windows-slow | step 6: "No Windows counter is confirmed to carry the ring-full count" | Flow box: "6. Network: receive discards" | 0262 D | HOLDS |
| C21 | guest-os/cpu/windows-cpu-scheduling vs guest-os/cpu/metrics/run-queue | Ready "Should be near 0"; "All 3 indicate a CPU problem" | KPI green 0-2 per processor; PerfMon under 10 acceptable | 0010 H | HOLDS |
| C22 | vsphere/object-types/vm/configuration/vm-configuration-review vs vsphere/technology/cpu/concepts/virtual-numa | "CPU hot add deactivates vNUMA, so memory is interleaved" | hardware 20+ with numa.allowHotadd keeps vNUMA | none named | HOLDS |
| C23 | vsphere/technology/memory/concepts/memory-tiering | "one fetch at a high latency on an idle device does not [slow a VM]" | "NVMe read latency of 900 µs on an idle device can be ignored" is wrong: "never zero" | 0384 H | HOLDS |
| C24 | vsphere/technology/memory/decision-tree/is-overcommit-affecting-vm (step b) vs metrics/virtual-motherboard/active | "Consumed above Active: the guest is currently getting all the memory it requires" | Active: "none for capacity, sizing, performance or Guest OS need" | 0054 | HOLDS (step a part BROKEN, dropped) |
| C25 | vsphere/technology/memory/concepts/memory-layers vs memory-limit, swap-and-compression | "Proactive. Means ESXi Consumed is very high, not that VMs contend" | "A limit is enforced at all times, also on a host in the High state" | 0291, 0140 | HOLDS |
| C26 | memory-layers vs host-memory-states | "ESXi uses 4 levels: TPS, memory tiering, balloon, compress/swap" | "ESX uses five mechanisms" (host cache, no tiering) | 0038 | HOLDS |
| C27 | vsphere/technology/memory/concepts/host-memory-states | Hard row: "ballooning stops inflating" | Low row: "All of the above" (includes balloon); ballooning has no stop in Hard; no source | none named | HOLDS |
| C28 | vsphere/technology/memory/metrics/host/ballooned vs concepts/ballooning, host-memory-states | "Balloon is slower to act than swap and compress" | balloon first in reclamation order | none named | HOLDS (wording) |
| C29 | vsphere/technology/memory/metrics/virtual-motherboard/swap-target vs concepts/swap-and-compression | "Compare it with Swapped; do not add the two" | target = "compressed plus swapped memory" (pre-compression base) | 0142 | HOLDS |
| C30 | vsphere/technology/memory/concepts/ballooning | "when the Balloon Target falls below the balloon size, the VMkernel deflates the balloon" | "The VM initiates the reallocation, so Balloon Target can be 0 while Ballooned is still above 0" | 0052, 0388 (new options blocked) | HOLDS |
| C31 | vsphere/technology/memory/metrics/virtual-motherboard/latency vs memory-tiering | "The only ESXi counter for memory speed"; no tiering caveat | NVMe fetch is a wait Latency may not count (vm-memory-latency-high step 5) | 0384 | HOLDS |
| C32 | vsphere/technology/memory/metrics/virtual-motherboard/latency vs memory-tiering | "DIMM access takes about 200 ns" | "about 100-200 µs against about 100 ns" | none named | HOLDS |
| C33 | vsphere/architecture/overhead vs vsphere/technology/memory/metrics/virtual-motherboard/overhead | "Small. Operationally negligible." | "several percent of the VM's memory, and lowers the reservable memory" | none named | HOLDS (part) |
| C34 | vsphere/technology/memory/concepts/swap-and-compression (line 76) vs memory-limit | "Consumed flat just under the effective limit" | "Consumed stays under the effective limit by at least the overhead" | 0291 | HOLDS |
| C35 | vsphere/object-types/vm/vmotion, Stun time | "A checkpoint stun ... device reset, disk branching ... snapshot" | "Stun time is the switch-over: the VM is paused while its last memory pages ... are copied" (= Downtime) | 0077 (stun-time option) | HOLDS |
| C36 | guest-os/memory/windows-memory | "no conversion possible" (pages to MB) | same file converts pages x 4 KB (lines 55, 58) | none named | HOLDS |
| C37 | vsphere/technology/network/concepts/nic-teaming | "LBT (it moves the other ports away, not the big flow)" | "It moves the port with the highest IO"; "busiest port moved" | 0210 C | HOLDS |
| C38 | vsphere/technology/network/metrics/virtual-motherboard/packets-dropped vs concepts/packet-drop-accounting | "Received packets are dropped before reaching the Guest OS ... do not match Guest OS counters" | "A full receive ring is counted here ... and by the guest" | 0420 | HOLDS |
| C39 | vsphere/technology/network (vnic-rx-drops) | Interpretation: "check whether the VM requests NetQ RSS" | Single receive queue: "The fix is Receive Side Scaling (RSS) in the Guest OS" | 0060 H, 0212 H | HOLDS (wording risk) |
| C40 | vsphere/technology/storage/metrics/host/adapter-and-path, host/datastore, virtual-motherboard/disk-latency, tools/esxtop/storage | "averages read and write per adapter first"; "a normalized average of read and write" | "Total latency is not (read + write) / 2. It is the average over all commands" | 0072 A/C/E (key flips if command-weighted), 0406 | HOLDS |
| C41 | vsphere/technology/storage/metrics/virtual-motherboard/disk-latency vs concepts/esxi-storage-io-path | "each layer in the stack has its own queue (process, Guest OS storage subsystem, VM driver ...)" | "GAVG starts at the virtual device. The wait in the guest queue is outside it" | none named | HOLDS |
| C42 | vsphere/technology/storage/troubleshooting/vm-storage-performance-checks (step 4) vs storage-layers | "array-side IO (replication, snapshots)" | "array snapshots" (VM snapshots are counted by vCenter) | 0408 G, 0188 J | HOLDS |
| C43 | vsphere/architecture/resource-controls vs sp5-framework/performance/noisy-neighbour, storage-io-control | "Disk: an IOPS limit and shares per virtual disk" (no caveat) | "Share: ignored from VCF 9.0, which keeps only the IOPS limit" | 0183 B | HOLDS |
| C44 | vsphere/technology/storage/metrics/virtual-motherboard/disk-space ("Provisioned Space for VM") vs author export | "thin disks count at their configured size, not their actual use" | export 0046: Provisioned 1,000 GB beside an 88.92 GB snapshot; round disk sizes | 0046 | HOLDS |
| C45 | vsphere/technology/storage/metrics/virtual-motherboard/disk-space | line 20: RDM "counted at configured size, unless the array thin-provisions the LUN" | vm-files: RDM "Always counts as thick ... A thin LUN on the array is transparent to ESXi" | none named | HOLDS (second reviewer, missed by the first) |
| C46 | vsphere/technology/storage/metrics/virtual-motherboard/disk-space | Snapshot: "Reclaimable by removing the snapshot" | thin base disk: consolidation writes the delta's new blocks into the base, net return smaller | 0187 (option on "frees only part above 1.1 TB") | HOLDS |
| C47 | vsphere/technology/storage/concepts/esxi-storage-latency-stack | line 19: "High QAVG: check queue depths at each level of the stack" | esxi-storage-io-path: guest PVSCSI depth adds nothing to QAVG | 0425 G | HOLDS |
| C48 | project/practical-questions-as-exports-2026-11-15.md row 0425 vs esxi-storage-latency-stack | generator relation "QAVG <= KAVG" | "QAVG cannot exceed KAVG" is a misconception: QAVG includes kernel IO | 0425 | HOLDS (project file) |
| C49 | vsphere/tools/esxtop/storage | "VAAI offload raises KAVG" (settled in text) | own review note: KB 342563 says nothing on KAVG | 0043 G | HOLDS |
| C50 | vsphere/tools/vsphere-client/vcenter-statistics vs memory/swap-and-compression, vm-memory-metrics | "Contention counters stored at the default level 1: ... balloon, swap-in and swap-out rates" | "Swap out: ... Not contention by itself"; balloon "past reclamation, not a wait" | 0351 C | HOLDS |
| C51 | glossary (Capacity) vs vcf-operations/features/capacity-forecast, sp5-framework/capacity/supply | "Usable capacity: Total capacity minus HA, buffer and hypervisor overhead" | "total capacity minus what vSphere HA admission control reserves ..., minus the policy buffer"; hypervisor not subtracted | 0430 I | HOLDS |
| C52 | vsphere/tools/esxtop/memory | "CNSM \| Consumed: memory the VM uses now, minus sharing savings and minus compression savings" | line 52: "Consumed = GRANT - SHRDSVD" (no compression term); glossary Consumed is not "uses now" | none named | HOLDS |
| C53 | vsphere/tools/esxtop/memory vs vsphere/technology/cpu/concepts/numa | "always has remote memory, even with one home node" (settled) | numa review note: "Needs a lab test on a 9.1 host" | 0067 (A, E, G, H, M) | HOLDS |
| C54 | vcf-operations/features/peak-20-second-metrics vs catalog/thresholds-alerts, vm-alerts | pair: "Peak Transmitted Packet Dropped within collection cycle" (count, no %) | sym-vm-network-tx-dropped-above-4 is a % ("share of the packets it transmitted") | 0313, 0421 | HOLDS |

### Missing facts that a question key rests on

| # | Knowledge file (where it belongs) | Fact | Vendor source named | Questions / options |
|---|---|---|---|---|
| M1 | vsphere/object-types/cluster/concepts/admission-control-and-cluster-state | 32 MHz CPU default (0 MB memory) per powered-on VM without a reservation; slot CPU default 32 MHz; slot sizes "rounded down" | vSphere 9.1 Availability, Computing the Current Available Capacity p. 1971; Slot Size Calculation pp. 1970-1972 (project/sources/vmware-vsphere-9-1.pdf) | 0330 A-E (B and E keyed false on it); 0290 key points |
| M2 | same file | Manual percentage below the computed one raises "Insufficient Failover Resources"; power-on tested against the configured value; the 1/N misconception line names only slot and tier-aware policies | vSphere 9.1 Availability, Cluster Resources Percentage Admission Control (pp. 1969-1990; warning text not found in the PDF, public docs) | 0330 A, C, D |
| M3 | same file (slot policy) | A VM above the slot size takes several slots (das.slotmeminmb cap) | vSphere 9.1 Slot Size Calculation pp. 1970-1972 | 0290 (proposed options) |
| M4 | vcf-operations/alert-definitions | Alert-level Wait Cycle and Cancel Cycle, how they stack on symptom cycles, meaning of symptom cancel cycle, value types (Count, Percent, Any, All) on child-object sets, Symptom Based criticality (most critical triggered symptom); body line 12 merges symptom wait and alert wait | VCF Operations 9.1 TechDocs Alert Definition Best Practices; API 9.1.1 alert-condition (source.path in file); catalog/thresholds-alerts review note | 0274 A, C, E; 0275 C vs D; 0314 |
| M5 | vcf-operations/alert-definitions | Symptom-set relationships Child (one level below) and Descendant; resource-pool-alerts says "does not work with nested resource pools" with no reason | vendor definition of Child/Descendant (grep finds neither word in the file) | 0340 (L4-110) |
| M6 | vcf-operations/features/real-time-metrics | Retention of 2-second data (question assumes it covers 10:15 viewed at 14:30) | none named | 0277 C |
| M7 | vsphere/technology/network/concepts/netioc, vsphere/architecture/resource-controls | VM adapter reservations draw on the bandwidth reserved for virtual machine system traffic on the host's uplinks; at 0, no adapter reservation can be granted | vSphere 9.1 Networking, Configure Bandwidth Allocation for a Virtual Machine (URL in 0215 Notes) | 0215 J |
| M8 | vsphere/technology/network (new line in a loss-impact file, e.g. network-characteristics or vm-alerts) | TCP throughput against loss (Mathis: rate ~ MSS/RTT x 1.22/sqrt(p)); voice loss tolerance of about 1-3% | public TCP model, public VoIP guidance (blind check) | 0346 D, H |
| M9 | vsphere/technology/network/metrics/distributed-switch/packets-dropped | Definition of the VCF Operations port group drop metric (name, dropped / packets or dropped / (dropped + delivered)); vCenter has no port group counter | vSphere Web Services API 9.1 network counters; VCF Operations metric list | 0345 (15% against 13%), 0344 |
| M11 | vsphere/technology/cpu/metrics/host/peak-core-usage or virtual-motherboard/usage-disparity | A single-threaded job is bound by one core's clock; free threads or another host do not speed it up | public knowledge (F3 reading) | 0378 F; 0379 F, G |
| M12 | vsphere/technology/cpu/metrics/virtual-motherboard/usage-disparity | Which of Peak / Min / Max - Min the VCF Operations metric "vCPU Usage Disparity (%)" is (example implies Max - Min) | VCF Operations 9.1 metric definitions | 0366 A, 0101 F |
| M13 | guest-os-vs-vm-cpu, Linux metrics | sar `%guest` is time the kernel spent running nested guests (distractor "no CPU went to the hypervisor") | Linux sar man page | 0381 (export plan distractor) |
| M14 | vsphere/technology/storage/metrics/host/adapter-and-path | How Highest latency averages read and write (plain mean or command-weighted) | vSphere Web Services API 9.1, storage adapter counters (maxTotalLatency) | 0072 A, C, E (key flips if weighted); 0406 A not affected |
| M15 | vsphere/technology/storage (snapshot-impact or reclamation) | 72-hour snapshot rule | Broadcom KB 318825 (reviewer); KB 1025279 (blind check, "Do not use a single snapshot for more than 72 hours") | 0187 I |
| M16 | same | Deleting a snapshot commits the delta into the base disk; only Revert rolls back (near-throwaway option) | Broadcom KB 371714 | 0187 G |
| M17 | vsphere/technology/storage/metrics/virtual-motherboard/iops or disk-latency | Per-IO latency grows with IO size ("7 ms on 512 KB reads" is not a slow array) | none named (storage-io-control Normalized Latency discounts large IOs) | 0180 B, C, D |
| M18 | vsphere/technology/storage/concepts/guest-os-vs-vm-storage, vsphere/object-types/vm/vm-performance | Weighting of the VM-level virtual disk latency aggregate (IOPS-weighted?) and of datastore latency "average of the VMs" | VCF Operations 9.1 metric definitions | 0422, 0423 (row 0423 of the export plan says IOPS-weighted), 0184 |
| M19 | guest-os/system/guest-os-sizing, guest-os/memory/windows-memory | Linux derivation of Guest\|Needed Memory (MemAvailable?); the file defines it from Windows page lists only | VCF Operations 9.1 metric definitions, Guest\|Needed Memory (techdocs.broadcom.com) | 0387, 0079 (Linux rows), 0401 |
| M20 | guest-os/memory (new linux-memory file) | Linux available vs free, page cache, cgroup v2 memory.max/high, "Memory cgroup out of memory" OOM text, /proc/vmstat swap counters cumulative since boot | Linux kernel docs | 0272 (A and 5 more options), 0263 |
| M21 | vsphere/technology/memory/concepts/ballooning | Whether adding memory to a ballooned VM stops the balloon (balloon follows host pressure; default shares scale with memory) | none named | 0054 E |
| M22 | vsphere/technology/memory/concepts/memory-tiering | Tiering is transparent to the VM memory counters (option rests on it); a VM excluded from tiering without full reservation can be host-swapped | vSphere 9.1 docs p. 1869-1871 | 0025 D |

### Open review notes that a key rests on

| File | Note | Questions |
|---|---|---|
| vsphere/object-types/resource-pool/resource-pool-design | Scalable Shares multiplier 4, 2, 1 not stated by vSphere 9.1 docs or Performance Best Practices 9.1 | 0230 D (and key point) |
| vsphere/object-types/cluster/configuration/drs-migration-levels | Whether VCF Operations 9.1 still offers the Predictive DRS data provider (also dpm, Power-on lag) | 0238 J |
| vsphere/technology/cpu/metrics/virtual-motherboard/demand | VM CPU Demand under a limit: file says equals Usage; Web Services API 9.1 defines cpu.demand without limit | 0102 I, 0103 B, 0371 E (decided by Ready or Max Limited, keys hold) |
| vsphere/technology/cpu/concepts/numa | Remote memory for a VM whose vCPUs fit one node but memory does not: "Needs a lab test on a 9.1 host" | 0067 A, E, G, H, M |
| vsphere/technology/cpu/concepts/virtual-numa | Rebuild at every power cycle vs docs p. 1939 (Q216, Future release) | 0113, 0267 (avoid it) |
| vsphere/tools/esxtop/storage | VAAI offload raises KAVG: KB 342563 says nothing on KAVG | 0043 G |
| vcf-operations/features/real-time-metrics | Object type that carries ESX Top state: policy page says Virtual Machine, Workbench page says Host System and Virtual Machine | 0277 C |
| vcf-operations/features/peak-20-second-metrics | Key of Peak Transmitted Packet Dropped (net\|droppedTxPct_max vs net\|droppedTx_summation) | 0313, 0421 |
| vcf-operations/dashboards/business-applications | "one group can hold VMs of several vCenter instances (adapter instances)" unchecked | 0279 G |
| vcf-operations/features/capacity-forecast | Aggressive risk level = mean of upper and lower bounds comes from the pre-9.1.1 TechDocs page | 0235 G |
| vsphere/technology/network/concepts/packet-drop-accounting | Distributed Firewall drop section rests on Broadcom KB 449113 (ESXi 8.x, NSX 4.x), not checked on 9.1 | 0420 |
| vsphere/technology/network/concepts/network-characteristics | Whether vCenter 9.1 has a counter that shows NIOC capping bandwidth | 0041 L |
| vsphere/technology/memory/concepts/memory-tiering | Whether VM memory contention (%LAT_M) counts tier-1 fetch waits; whether host memory states count tier 1 as free | 0384 H, 0025 |
| catalog/thresholds-alerts.yaml | Wait cycles sit on the alert or the symptom (Alert Definition Best Practices) | 0274, 0275, 0314 |
| vsphere/object-types/vm/vmotion (stun time) | Not a note; blocks any `vmw_esxi_vmprecopystuntime` question until C35 is fixed | 0077 |

### Stale cross-references in question files

Q214 (a limit balloons first, e42d026), Q201 and Q205 (deda489), Q217 (26d511c) and Q202 are settled; these Notes still call them open or speak the old reading.

| Question | File (benchmark/questions) | Stale text |
|---|---|---|
| 0052 | L2-013-balloon-above-zero.md line 39 | "open author question Q214" |
| 0014 | L3-007-reservation-cpu-vs-memory.md line 37 | "open author question Q201" |
| 0140 | L4-055-memory-limit-swap-and-compress.md line 46 | "No option on ballooning under a limit (open author question Q214)" |
| 0239 | L4-080-monday-web-slow-pool-limit.md line 56 | "whether a limit causes ballooning is open (Q214)" |
| 0291 | L4-096-memory-limit-balloons-on-an-idle-host.md line 51 | Q214 open; Notes state the old reading "a limit causes Compressed and Swapped, not Balloon directly" |
| 0350 | L4-118-vm-night-job-health-check-findings.md line 56 | "open question Q214" |
| 0403 | L4-145-one-vm-waits-while-host-latency-stays-low.md line 48 | "open author questions Q205 and Q214" (Q205 settled) |
| 0390 | L4-141-vsan-host-consumed-in-maintenance-mode.md line 39 | cites Q201 as a reason for wording; check against deda489 |
| 0018 | L4-008-vm-vs-guest-os-metrics.md | still shows "Guest OS CPU Run Queue 25" on an 8-vCPU VM; Q217 made the VCF Operations value per vCPU |
| 0365 | L3-043-default-shares-follow-vcpu-count.md | Notes say a knowledge line on per-VM shares is being corrected; ready.md line 45 is corrected |
| 0264 | L4-085-windows-free-low-standby-high.md line 34 | names its pair as 0263; metadata says 0382 |
| 0360 | L4-128-linux-two-disks-same-queue-and-utilization.md line 88 | `pair: "0419"` while the export plan drops 0419 |
| 0090 | L4-042-erp-slow-after-change-window.md | cites Broadcom KB 85393 (legacy number of KB 338438, fixed in 8.0 U3j) and says no file states the consolidation stun (vsphere/object-types/vm/vmotion now does) |
| 0186 | L4-067-nfs-datastore-latency-in-esxtop.md | calls 0050 deferred; 0050 is reviewed |
| 0343 | L4-113-datastore-space-alert-fired-what-next.md | still speaks to a judge (judge archived, Q199) |
| 0187 | L1-008-keep-a-six-week-old-snapshot.md | "six-week-old" against prompt "two weeks ago" |
| 0074, 0212, 0214 | Notes (not a Q214 item) | assume VM net.droppedRx/droppedTx history at the default statistics level; vcenter-statistics says VMs keep no network drops there; level not stated in the stems and the counters are absent from catalog/vcenter-api-counters.yaml |

## Appendix C. Per-question items left for the author
- 0003: the question was reviewed as free text and converted on 2026-11-14; with five options replaced it needs a full review.
- 0006: key check note: Q236's "capacity at base clock" wording makes A arguable under "give the CPU capacity"; the key point avoids calling 20 GHz a capacity.
- 0007: the reviewer-only images in Notes show the original quiz numbers (6520P; 20 cores at 1 GHz vs 10 at 2 GHz). Replace them if the images should match the prompts.
- 0008: the knowledge base contradicts itself on Overlap in Guest OS sizing (net-run, run: remove; overlap, guest-os-sizing: keep inside Run); the key holds either way.
- 0008: Q0008 level 400: the reviewer reads it as generous; noted, not changed.
- 0009: key unchanged (A, B, C, D, I), author-approved; please confirm the two new distractors.
- 0017: the key (A, B, F, K) rests on the knowledge base's own overhead definition, not stated in the prompt (F3). The second reviewer shows that stating "only what cannot be avoided" does not fix it: vSphere 9.1 lets VM logging be turned off (Virtual Machine...
- 0018: re-review of the reviewed question (C changed in substance; key letters unchanged A, C, E).
- 0022: the case values (104% Utilization with 64 of 96 GB usable and 50 GB in use) are synthetic; realism check by the author.
- 0023: D (the only misconception) is also over the cap (cluster 38); the redundancy report asks the author to pick an untested latency misconception, and both misconception lines of latency are already tested in three or more questions. D stays.
- 0039: E rests on fleet data in the knowledge base (3,938 VMs); a frontier model can only infer it from the general pattern (F3, borderline).
- 0042: re-approve (was reviewed).
- 0043: the relabel of a Level 200 basics item to 300 (it now holds a threshold option); revert I and the label if he wants 0043 kept as a 200 guard.
- 0046: Provisioned Space for VM counts non-disk files at actual size (disk-space) but the author's CSV shows round disk sizes (row 009: 1,000 GB with an 88.92 GB snapshot); check against a VCF Operations 9.1 export.
- 0050: review of the reviewed question's new C and E.
- 0052: the deflate option ("stays ballooned until Linux asks for it back") is not added: balloon-target and ballooning, Mechanism still say "The VM initiates the reallocation, so Balloon Target can be 0 while Ballooned is still above 0", which makes it...
- 0056: level 400 rests on one mechanism option (H); the reviewer proposed two for 400, second reviewer allowed one.
- 0060: vnic-rx-drops step 5 and Interpretation name NetQ RSS where the Single receive queue section names guest RSS (review KB issue 5, a wording risk for 0060 H and 0212 H).
- 0067: numa review note (lab test on 9.1) under A, E, G, H, M; esxtop/memory states the same reading as settled.
- 0069: Level labels the reviewer called off (noted, not changed): file names L4 with level 300 for Q0069, Q0237, Q0275, Q0279, Q0351; Q0089 file L3 with level 400.
- 0072: knowledge-base issue 1: the key reads Highest latency as the plain mean of read and write per adapter; adapter-and-path does not state the weighting, and disk-latency says total latency is command-weighted. If maxTotalLatency is command-weighted, A, C and...
- 0077: the review's replacement of G (precopy stun time and downtime measure the same pause) was not applied: vmotion.md, Stun time, describes stun time both as a checkpoint stun and as the switch-over pause, so no stun-time option is decidable until the file is...
- 0077: file name prefix L4-032 does not match level 300 (lint asks for renumber_questions.py); not renamed.
- 0079: the review's ballooned column for a donor (new misconception option) was not added: it needs a new CSV column, and second reviewer did not cover it.
- 0079: Q0079 L / knowledge base: guest-os/system/guest-os-sizing, section "Applications that manage their own memory", line 109: "Windows In Use, the process working set and VM Active then show the limit, not the need." This contradicts...
- 0086: regenerating the CSV with real `esxtop -b` perfmon headers waits for the esxtop template's header/data field-count mismatch.
- 0106: Q0106 level 400 rests on one rule of thumb (read Ready against Run), per the reviewer; not changed.
- 0110: Overlap in Guest OS sizing (knowledge base contradiction, see Q0008).
- 0113: the power-cycle remedy stays out of the options until Q216 (topology rebuild on power cycle) is answered.
- 0114: misconception_type is empty at Level 300: no listed type fits B ("same vCPU total, same performance").
- 0142: the Swap target base of comparison (Swapped alone, or Swapped + Compressed) is still two ways in the knowledge base; no option depends on it.
- 0144: file name says 6 GB while the title says 11 GB (rename when the lead renumbers)
- 0151: the file name ("after-an-agent-install") no longer matches the case; rename when convenient.
- 0152: misconception_type [consumption-as-contention, provider-vs-consumer] fits A loosely (usage read as reservable capacity); no listed type fits better, so it stays.
- 0180: KB gap: no knowledge file states as a mechanism line that per-IO latency grows with IO size; B, C, D rest only on the Normalized Latency size adjustment (proposed home: iops Values or disk-latency, misconception "7 ms on 512 KB reads means the array is slow").
- 0183: the review's true option "an IOPS limit of 3,200 on rpt-07 caps its 512 KB reads at about 200 per second" was not added: the mClock fact is already tested by the pair 0424/0425 (cap of two).
- 0187: the level label may be his (status comment "reviewed as a free-text question"); confirm 300. Option I is decided only by Broadcom KB 318825 (72 hours), which no knowledge file states: add the rule to snapshot-impact or reclamation, or accept a vendor-only...
- 0210: nic-teaming contradicts itself on what LBT moves ("it moves the other ports away, not the big flow" against "it moves the port with the highest IO"); C is keyed on moving the busy port (review KB issue 1).
- 0212: the vCenter statistics level of the VM counters net.droppedRx and net.droppedTx is not in the catalog (review KB issue 6); "raised to 3" is safe whether they are level 2 or 3.
- 0215: J is true only by the vSphere 9.1 Networking document (VM adapter reservations draw on the virtual machine system-traffic reservation); netioc does not state it (review KB issue 4).
- 0216: misconception_type stays [] at Level 400; no listed type fits E (victim read as source) or F (move the VM).
- 0230: D (and F) rest on the Scalable Shares multiplier (x 4, 2, 1) that resource-pool-design's open review note says neither the vSphere 9.1 documentation nor Performance Best Practices 9.1 states.
- 0235: G rests on the risk-level mapping with an open review note in capacity-forecast.
- 0238: J is keyed true on Predictive DRS with VCF Operations as data provider; drs-migration-levels has an open review note on whether VCF Operations 9.1 still offers that provider. If not, J flips to false.
- 0238: Q0238 J and Q0230 D, F: decided by knowledge text that carries open review notes (Predictive DRS provider in VCF Operations 9.1, drs-migration-levels; Scalable Shares multiplier, resource-pool-design). Fixing needs the KB review, not the question.
- 0262: L (VM latency fine, so no storage delay in Windows) repeats the disk-queue misconception tested in 0311/0359; it is a plain distractor (not in `misconception`), so it does not count against the cap and was kept.
- 0262: level 400 partly L300 by the reviewer; not changed.
- 0266: re-review (was reviewed).
- 0272: the knowledge base has no Linux memory file (available vs free, page cache, cgroup v2 memory.max/high, OOM messages); 6 of 10 options rest on vendor documents (declared in Notes). A guest-os/memory/linux-memory file would let Agent E2 help here.
- 0274: the alert-definitions body should state the alert-level Wait/Cancel Cycle and the cancel-cycle meaning; A, C, E are decided from vendor pages until then.
- 0274: stay as they are (author question Q245: alert-level Wait/Cancel Cycles, Cancel Cycle meaning, Symptom Based criticality and Any/All between sets are not in the vcf-operations/alert-definitions body).
- 0275: Symptom Based criticality is not in the KB body (C vs D decided from vendor pages).
- 0277: real-time-metrics gives no retention for 2-second data (C assumes 10:15 is still there at 14:30).
- 0277: "2-second data starts at activation (no back-fill)" is not stated in the knowledge base (Notes admit it). Not changed.
- 0279: G rests on the unchecked line "one group rule matches VMs of several vCenter adapter instances" (business-applications review note).
- 0279: Q0279 G and Q0235 G, I: rest on knowledge lines with open review notes (rule across vCenter adapter instances; risk-level mapping). Not changed.
- 0291: knowledge_main moved to memory-limit; per CLAUDE.md a retrieval-scoring change needs a before and after number from the retrieval check, done for the whole set (section 7).
- 0293: Q216 (a), the lab check of `numa.allowHotadd`, is still open; I stays false on hardware 19 whatever it finds. Knowledge-base issue 7: vm-configuration-review (knowledge_main) states the hot-add rule with no hardware-version qualifier.
- 0294: Level labels the re-review reads as generous (not changed): Q0294 (300), Q0111 F is Level 200.
- 0295: misconception_type [layer-confusion] does not fit (per-adapter against host-wide is a scope, not a layer); the review proposed [] or same-name-other-object, neither fits clearly, so it is left as is.
- 0296: misconception_type stays empty on a Level 400 question; no listed type fits a sizing-formula question.
- 0297: M rests on an inference (a running VM's swap file moves only at power-on or a vMotion copy), as the Notes say.
- 0298: option I (a swap file above 100 GB slows power-on) rests on the vSphere 9.1 documentation, Using Swap Files (p. 1875), not on a knowledge file; adding the line to host-level-swapping would close the gap. misconception_type [reclamation-as-contention] fits...
- 0313: D ("no pattern within the cycle") kept: second reviewer proposed dropping it, but the redundancy report counts it as a plain distractor, so the fact is not over the cap.
- 0330: the key (A) rests on vendor facts the knowledge base lacks: the 32 MHz CPU / 0 MB default for a powered-on VM without a reservation, the Insufficient Failover Resources warning for a manual percentage below the N largest hosts, and the power-on test...
- 0330: deferred (key rests on vendor facts not in the knowledge base).
- 0331: the "load of 1 or more is overloaded" option was not added.
- 0340: confirm on a VCF Operations 9.1 instance that the nested pool's VMs are not Child objects of the outer pool; vcf-operations/alert-definitions does not define Child and Descendant (key A rests on the Aria Operations 8.18 definition).
- 0340: Child vs Descendant population of the resource pool alert is not in the knowledge base (vcf-operations alert definitions); the outcome for Prod rests on vendor knowledge.
- 0345: the review judged the old A false ("so the network is healthy"; 15% depended on an unstated formula), the blind key check judged it true. Key kept [A]; A and stem reworded so A is true as keyed. Also: the port group drop metric has no formula in the...
- 0346: coverage-gap sketch 4 (port group values are aggregates, no vCenter port group counters) would now be a third question on that fact (0214 I, 0346 J).
- 0350: the review's proposed true option "Consumed sits about 15 GB under configured" was not added. The memory row now feeds only I; the author may want one memory option back once a fact under the cap exists.
- 0351: the level of cpu.costop, mem.latency and net.droppedRx in the 9.1 Data Counters tables (Notes); vcenter-statistics still calls balloon and swap rates contention counters (KB issue 2).
- 0358: whether the report-suite convention is worth a question at all (design 11.7).
- 0359: the review's I ("the 5-minute average can hide bursts above the depth") was not added: that fact is over the two-question cap.
- 0363: Notes name a frontier model run ("Gemini Hydrogen"); keep or drop.
- 0364: level 300 -> 400. KNOWLEDGE-ENGINEERING.md section 4 uses this exact reading (2% Ready on 10% Run) as its Level 400 example, and second reviewer holds the relabel, but the pairing plan labels item B1 Level 300: the author decides.
- 0372: the stem relies on ESXi 9.1 being outside the KB 338438 accounting issue; the knowledge base names only ESXi 8.0 Update 3j as the fixed build (other-wait, Known issue). Worth one line in other-wait stating that 9.x carries the fix, if Broadcom confirms it.
- 0374: the export check in specs/0374.md asserts conditions by the old letters (A, D, E, F, G); the coder must remap them (new C has its own condition, see above).
- 0376: export check in specs/0376.md asserts old E and H conditions; new E and H rest on the spec's own relations. Generator note: vcpu worlds show %USED above %RUN on a busy Hyper-Threading host, against hyper-threading/esxtop text (%USED falls below %RUN while...
- 0377: the case check asserts neither new E (dw-etl-01 %RUN 200-300) nor new F (%VMWAIT "-" on every non-VM row); a coder may add both.
- 0378: F (and 0379 F, G) rest on a fact no knowledge file states: a single-threaded job is bound by one core's clock; add a line to peak-core-usage or usage-disparity.
- 0378: Knowledge-base gap: no file states that a single-threaded job runs at the speed of its one thread, so free threads or another host do not speed it up. Q0378 F still rests on it (not in this fix list); Q0379 no longer does.
- 0379: F and G rest on the unstated single-thread fact (see 0378). specs/0379.md asserts the old H condition (Usage in MHz for 0 > 3,000); new H rests on the hot-thread move.
- 0382: the true judgment "low Free with high Standby means Windows wastes no memory" was not added: the Free memory (MB) row of the threshold catalog scores that state as poor, against windows-memory "Near-zero free memory with healthy other metrics is ideal"...
- 0384: H rests on memory-tiering Misconceptions ("never zero") while Touching a page on NVMe says "one fetch at a high latency on an idle device does not" slow a VM; second reviewer proposes rewording that knowledge line ("adds one wait, too small to slow the...
- 0387: Linux Needed Memory is still undefined in the knowledge base (review knowledge-base issue 6); E reads the export value.
- 0394: the misconception "VCF Operations 9.1 has no VM Memory Usage (%)" is not added: the stem must say the metric is enabled to show its value.
- 0399: the case check asserts neither rclmtgt = 0 nor PSHARE saving > 0 (both guaranteed by the generation rules); a coder may add them.
- 0412: knowledge/vsphere/tools/esxtop/network-units-vs-vsphere-client.md line 11, misconception "esxtop shows 125 times more traffic than vCenter, so one tool is wrong" points the wrong way: the vCenter value (KBps, ~364,000) is about 125 times larger than the...
- 0414: the generator case project/tools/export_generator/question_exports/q0414_command_latency_hides_slow_writes.py labels the old I condition "I" in its failure message; it is now option H (cosmetic, not my file).
- 0415: the review proposes 400 -> 300 (same arithmetic as 0211 at 300), which conflicts with question-pairing-2026-11-14.md C20 (400); kept at 400 pending the author.
- 0420: the review and second reviewer judge it Level 400 on the merits (pkts rx OOB against rx_dropped, drops before delivery, a two-tool disagreement), which conflicts with question-pairing-2026-11-14.md C26 (300); not relabelled. B and J rest on the Distributed...
- 0430: knowledge/glossary.md Usable capacity line adds hypervisor overhead, against capacity-forecast and supply (affects I).
- 0431: the file name `L4-153-cluster-cpu-above-90-request-for-hosts.md` still states the level the title no longer gives; rename with the next renumber if wanted.
- 0433: the generator case project/tools/export_generator/question_exports/q0433_drs_score_high_one_vm_low.py has comments "# B, H" and "# H" (lines 143, 152) for the rpt-batch-09 check, which is now option G (comment only; not edited here).
- 0454: E and H lean on the kernel-reservation fact already in L4-015 C and L4-141 E (overlap noted by the reviewer, not changed).
- 0464: with C replaced, the "DRS needs vCLS" misconception is tested only through true options A and B; misconception metadata is now F. Author may prefer a different misconception option.
