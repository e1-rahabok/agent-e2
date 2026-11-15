# Practical questions as exports, not screenshots (2026-11-15)

Review of the 47 practical halves that wait for screenshots ([question-pairing-2026-11-14.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/question-pairing-2026-11-14.md), section Screenshots to capture). Read-only so far: no question, design rule or tool is changed yet. Not indexed. Status: waiting for the export templates (section 8), then one change set (section 9).

## 1. The question
- The author: a practical question does not need a screenshot. Practical means a case to apply the fact to, not an image. The readers are AI only; humans need screenshots because they cannot digest much text, a model can.
- Example: [0368](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-131-task-manager-full-vcenter-ready-high.md) (Task Manager at 100%, vCenter Ready high) and its theory half [0266](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-087-linux-steal-time-and-windows-busy-time.md). The key of 0368 needs the values, not the pixels.
- The author added: customers send long CSV files with dozens of columns, so that the expert does not have to ask again. A screenshot carries one screen; customers rarely take extra ones. A CSV carries the misleading counters in the same file.

## 2. Design considerations
1. One construct per question. The practical half tests two things at once: applying the fact and reading the image. A wrong answer cannot tell which failed; design.md 3.9 names three causes for "right on theory, wrong on practical". Item-writing practice calls the image part construct-irrelevant variance when the item targets the fact ([ASC Item Writing Guide 2025](https://assess.com/docs/ASC_Item-Writing-Guide_2025.pdf)).
2. Screen reading is a real capability, but not the one these questions target. Model size is not a requirement (up to about 500B is acceptable, author 2026-11-15; benchmark/models.md: parameter count is not a limit). Large open vision models read screens far better than the 2024 models measured by [CharXiv](https://arxiv.org/abs/2406.18521) (open 29%, GPT-4o 47%, humans 80% on chart reasoning). The benchmark chooses the cheapest model that passes, which can be a small one, so screen reading is checked separately (section 7).
3. A question its evidence does not need is not a test of that evidence. [MMMU-Pro](https://arxiv.org/abs/2409.02813) removed every question a text-only model answered without the image. All 47 keys rest on values; none on pixels (section 4).
4. Prose gives the reading away; a product export does not. "Ready about 10% per vCPU" (0266) has done the hard step. An export shows `Readiness` for the VM, and knowing it is per vCPU is the trap. So the practical form is raw tool output with the product's names and units, never a summary in words.
5. Wide exports add a trap that prose and screenshots cannot. With Readiness, Ready (ms), Run, Co-stop, Wait, Usage and Demand side by side, the model must choose the counter: the Level 400 skill the theory half tests in the abstract. A misleading counter (Wait includes idle; Usage includes the Hyper-Threading charge) is the misconception of the theory half, present as a column.
6. Screenshots in the field are few and often incomplete: one or two images, frequently without the counter that settles the case. A screenshot question fits "the decisive counter is missing, ask for it" (MISSION.md: ask when one missing fact changes the answer), not a complete set.
7. Cost and control. 47 lab captures need exact conditions (0368: Readiness between 22% and 35% all window) and masking, and the author's time is the constraint (design.md 4). A seeded generator meets the condition exactly and is checked against the key.

## 3. Method
- Four read-only review agents, 11 to 12 practical halves each, with the theory partner of each.
- Per question: the facts its key rests on, each marked (a) same fact as the theory partner, (b) a reading of the evidence only, (c) a fact the partner does not test, with any other question that already tests it (searched in benchmark/questions); whether any option needs something only a screen shows; the real export path; a verdict (CSV, TEXT, KEEP-SCREENSHOT, DROP); the effect on the theory partner; for a CSV, the columns, distractors, rows and the relations a generator must keep.
- Not checked: the exact column names of each export. The agents wrote them from memory; section 8 collects the real ones.

## 4. Result per question
Format: CSV = generated export; TEXT = tool text (esxtop panel, `top`, `sar`, `iostat`, PowerCLI, `esxcli`); CSV + TEXT = both. Theory effect: "none" unless stated.

### CPU
| Practical | Theory | Format | Evidence | Notes |
|---|---|---|---|---|
| [0369](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-046-ready-ms-burst-on-two-charts.md) | 0105 | CSV | vCenter Real-time and Past day | Leave Readiness (%) out: it gives away the arithmetic of A and D. Past day row = sum of its 15 Real-time samples |
| [0372](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-047-cpu-wait-on-a-quiet-vm-chart.md) | 0001 | CSV | vCenter Real-time | Almost all partner facts. Run + Ready + Co-stop + Wait = vCPUs × 20,000 ms; Wait = Idle + Swap wait + rest |
| [0375](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-048-esxtop-co-stop-on-a-half-busy-host.md) | 0053 | TEXT | esxtop CPU panel, one VM expanded | Group row = sum of its worlds; %MLMTD ≤ %RDY |
| [0376](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-049-esxtop-time-a-vcpu-could-not-run.md) | 0009 | TEXT | esxtop CPU panel | Add %VMWAIT: %WAIT = %VMWAIT + %IDLE (tested only here) |
| [0368](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-131-task-manager-full-vcenter-ready-high.md) | 0266 | CSV | `typeperf` per processor; vCenter Real-time | Task Manager has no export: keep "Task Manager shows 100%" in the prompt. Not a duplicate: B, G, J test facts 0266 does not |
| [0370](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-132-month-chart-vs-vcf-operations-batch.md) | 0357 | CSV | vCenter Last month; VCF Operations | Weakest practical half: partner facts plus reading |
| [0371](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-133-usage-near-100-net-run-lower.md) | 0008 | CSV | VCF Operations | 7 days at 5 minutes is 2,016 rows: one afternoon plus a 7-row daily peak view |
| [0373](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-134-wide-vm-ready-co-stop-few-cpus-busy.md) | 0107 | CSV + TEXT | VCF Operations hourly; guest `mpstat -P ALL` | Busy CPUs in mpstat ≈ Net Run × 16 |
| [0374](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-135-host-usage-above-100-alert.md) | 0058 | CSV | vCenter Real-time; VCF Operations list | Usage ≥ Core Utilization ≥ Utilization; Usage > 100 only with Turbo |
| [0377](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-136-esxtop-load-average-above-three.md) | 0331 | TEXT | esxtop CPU panel | Load average 3.2-4.0; per VM %RUN + %RDY + %CSTP + %WAIT ≈ 100 × vCPUs |
| [0379](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-137-one-thread-saturated-host-under-15.md) | 0378 | CSV + TEXT | vCenter, all instances; host hardware text | 49 columns: cut to 30 rows |
| [0381](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-138-linux-st-zero-vcenter-ready-high.md) | 0380 | CSV + TEXT | `sar -u`, `top`; vCenter | sar `%guest` is a strong distractor (nested guests, not the hypervisor) |
| [0434](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-088-perfmon-queue-on-a-4-vcpu-vm.md) | 0010 | CSV | `typeperf` | 60 rows at 1 minute; distractor % Processor Utility (can pass 100) |
| [0431](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-153-cluster-cpu-above-90-request-for-hosts.md) | 0019 | CSV | VCF Operations hourly; VM list | Top VM contention below 1% |
| [0436](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-154-two-sockets-in-windows-one-numa-node.md) | 0267 | TEXT | `Get-CimInstance Win32_Processor` or Coreinfo; esxtop memory panel NUMA fields | Task Manager "Sockets" label carried as text |
| [0438](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-155-cluster-at-70-one-host-near-100.md) | 0437 | CSV | VCF Operations hosts and cluster | Cluster = mean of identical hosts in every row |
| [0440](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-156-five-minute-job-shows-as-two-half-points.md) | 0439 | CSV | vCenter Real-time; VCF Operations | Each half point = mean of its 15 samples; time stamps show the boundary |
| [0433](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-087-drs-score-high-one-vm-low.md) | 0232 | CSV + TEXT | cluster score text; VM DRS Score grid; VM chart | A low-score VM with low Readiness (memory-bound) as distractor |

### Memory
| Practical | Theory | Format | Evidence | Notes |
|---|---|---|---|---|
| [0385](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-054-host-memory-usage-high-without-balloon.md) | 0144 | CSV | vCenter Past week (daily rows); VCF Operations list | C tests the same fact as 0391 C and L4-058 K |
| [0387](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-055-linux-guest-free-memory-low-all-week.md) | 0263 | CSV + TEXT | VCF Operations list; `uptime`, `/proc/vmstat`, `/proc/pressure/memory` | Needed + Free < Total |
| [0388](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-056-vm-balloon-flat-for-days.md) | 0052 | CSV | vCenter Past week (daily rows) | Key risk: VM memory Latency is not kept at statistics level 1 (section 6) |
| [0391](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-057-host-compressed-flat-with-balloon-at-zero.md) | 0025 | CSV | VCF Operations list with First, Last, Min, Max | Remove C (third question on one fact). Theory 0025 needs a rewrite (section 6) |
| [0392](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-058-vm-memory-contention-follows-swap-in.md) | 0149 | CSV | VCF Operations, 15-minute rows | Contention > 0 only where Swap In > 0 |
| [0393](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-059-windows-commit-limit-in-task-manager.md) | 0270 | CSV + TEXT | `typeperf`; `systeminfo`, `Win32_PageFileUsage` | Rewrite B (perfmon has no "In use") and C ("no paging file is configured"). `systeminfo` "Virtual Memory: In Use" means commit: a good misleading label |
| [0399](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-063-esxtop-memory-overcommit-on-a-quiet-host.md) | 0398 | TEXT | esxtop memory header | Overcommit = requested / managed − 1; state matches free against minfree |
| [0386](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-139-windows-in-use-falls-consumed-stays.md) | 0095 | CSV | `typeperf`; vCenter, about 6 hours | Rewrite A to perfmon counters. The Task Manager screenshot version is deferred (section 5) |
| [0389](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-140-esxtop-which-vms-wait-on-swapped-memory.md) | 0068 | DROP | - | 0068 is already the esxtop text; 0068 loses its pair |
| [0390](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-141-vsan-host-consumed-in-maintenance-mode.md) | 0056 | CSV + TEXT | vCenter Past month; reservation as text | Overhead to about 0 at the evacuation; Consumed > 10 GB and flat |
| [0395](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-142-vm-memory-usage-differs-between-tools.md) | 0394 | CSV | vCenter, 12 hours; VCF Operations | vCenter Usage = Active / configured; VCF Operations Usage = Needed / Total |
| [0397](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-143-vm-memory-usage-dips-for-half-an-hour.md) | 0396 | CSV | VCF Operations, 24 rows | The chart gap becomes blank cells |
| [0401](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-144-guest-memory-four-weeks-across-a-downsize.md) | 0400 | CSV | VCF Operations, daily Max, 28 rows | Total Capacity halves at the downsize |
| [0403](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-145-one-vm-waits-while-host-latency-stays-low.md) | 0402 | CSV | vCenter host and VM, 12 hours | At least 20 running VMs (a count column) |

### Storage
| Practical | Theory | Format | Evidence | Notes |
|---|---|---|---|---|
| [0414](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-076-command-latency-hides-slow-writes.md) | 0044 | CSV | vCenter host disk | Command latency = read and write latency weighted by requests. Its stated capture condition could not be met; the generator can |
| [0416](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-077-outstanding-reads-at-low-latency.md) | 0028 | CSV | vCenter virtual disk | Little's law: IOPS × latency ≈ outstanding |
| [0417](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-078-datastore-iops-vs-one-host.md) | 0049 | CSV | VCF Operations list, one row per host | Host values sum to the datastore within 10% |
| [0418](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-147-windows-disk-time-above-1000-percent.md) | 0311 | CSV | `typeperf` PhysicalDisk; vCenter | % Disk Time = queue × 100 (tested only here) |
| [0419](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-148-linux-util-near-100-at-low-await.md) | 0360 | DROP | - | 0360 already gives the iostat columns as text; 0360 loses its pair |
| [0423](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-150-one-slow-disk-behind-low-vm-latency.md) | 0422 | CSV | VCF Operations, 8 disks, 6 hours | Aggregate is IOPS-weighted; the slow disk under 10% of IOPS |
| [0425](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-151-slow-scan-under-an-iops-limit.md) | 0424 | CSV + TEXT | vCenter; esxtop disk panel; limit as PowerCLI text | GAVG = DAVG + KAVG; QAVG ≤ KAVG |
| [0427](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-152-vm-storage-charts-do-not-match.md) | 0426 | CSV | 4 vCenter exports | Rewrite H ("one line per disk" becomes the instance column) |

### Network
| Practical | Theory | Format | Evidence | Notes |
|---|---|---|---|---|
| [0412](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-074-esxtop-and-vcenter-vm-transmit-rate.md) | 0029 | CSV + TEXT | esxtop network panel; vCenter Real-time | Rewrite D: the chart title "Network Rate (Mbps)" exists only on screen; the owner quotes it in the prompt |
| [0413](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-075-vmnic-usage-above-link-speed.md) | 0040 | CSV + TEXT | vCenter vmnic; `esxcli network nic list` | G (units) becomes free: the header says KBps |
| [0420](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-079-vm-receive-drops-linux-shows-none.md) | 0039 | CSV + TEXT | vCenter VM network; `ip -s link`, `ethtool -S` | Guest text is native: better than a picture |
| [0415](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-146-small-packets-telemetry-vm.md) | 0211 | CSV | vCenter Real-time | Replace H (KBps is in the header). Bytes per packet 120-250 |
| [0421](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-149-peak-transmit-drop-percent-one-cycle.md) | 0313 | CSV | VCF Operations, 12 hours | Total and non-Total drop metrics as distractors |

### System and VCF Operations
| Practical | Theory | Format | Evidence | Notes |
|---|---|---|---|---|
| [0432](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-086-two-minute-burst-real-time-vs-past-day.md) | 0047 | CSV | vCenter Real-time and Past day | Past day point = mean of its 15 Real-time samples |
| [0435](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-089-powered-on-vm-with-a-crashed-windows.md) | 0015 | DEFER | - | Availability is not in 1.0 (author, 2026-11-15); 0015 deferred with it |

## 5. Impact
### Practical halves (47 questions, 90 images)
| Outcome | Questions |
|---|---|
| CSV | 28 |
| TEXT | 5 |
| CSV + TEXT | 11 |
| Drop | 2 (0389, 0419) |
| Defer: availability | 1 (0435) |
| Need a screenshot for the key | 0 |

- No lab capture is needed. 44 questions run in 1.0 as exports.
- 0386 runs as CSV (author, 2026-11-15). A Task Manager screenshot question is deferred: the knowledge-base images of that screen cannot be reused (an attachment is never a knowledge-base image, and the knowledge files state those images' values), and it needs a Windows VM in the lab, not a laptop.

### Theory partners (47)
| Effect | Questions |
|---|---|
| No change | 43 |
| Loses its pair, metadata only | 2 (0068, 0360) |
| Rewrite: existing defect, not caused by this change | 1 (0025) |
| Defer: availability | 1 (0015) |

- The 34 pairs that already run are not affected.
- Screenshot questions that run: 8, with 12 images. They stay.

## 6. Defects found on the way
- 0388: VM memory Latency is probably not kept at statistics level 1, so a Past week capture as written may lack it. The input must state level 2 or higher. Checked by the export templates (section 8).
- 0385 C, 0391 C and L4-058 K test the same fact (balloon from host pressure at about 99%): three questions, over the cap of two. Remove 0391 C.
- 0025 (theory) has 4 options, no over-correction and no wrong action: it breaks the option rules of design.md 3.9.
- 0414: its stated capture condition could not be met as written.
- 0370 rests almost wholly on its partner's facts; allowed (two questions per fact), but the weakest practical half.

## 7. Work the conversion needs
1. CSV cap. `question_csv_max_chars` goes from 12,000 to 24,000 characters (about 6K tokens), and each period is cut to the event. The distractor columns are the trap; rows after the event add nothing. Budget at a 32K window: 3K prompt and blocks, 16K retrieved text, 2K answer, about 11K left. Multi-day cases use a VCF Operations list view with Max, Min, First, Last instead of thousands of 5-minute rows.
2. Options that become free once a value is a cell: units in vCenter headers (0412 D, 0413 G, 0415 H); a column that does the arithmetic (Readiness in 0369). The trap moves to columns with near names: Readiness vs Ready (ms), Command latency vs Highest latency, Usage (%) vs Usage (MHz), sar `%guest` vs `%steal`, Memory\Cache Bytes vs Task Manager "Cached", Total vs non-Total drop metrics, esxtop batch names ("Average Driver MilliSec/Command") vs DAVG.
3. Wording. "Chart", "legend", "hover", "line", "screen" become columns or values in all 44. Screen-only labels are rewritten from what the export prints: 0386 A, 0393 B and C, 0412 D, 0427 H.
4. Generator. One seeded model of counter relations per object type; every derived value recomputed on every row; the key checked against the rows, not against the stated condition. Relations named by the review: Ready + Run + Co-stop + Wait = vCPUs × 20,000 ms; Readiness = Ready / (vCPUs × 20,000); command latency weighted by reads and writes; Little's law; vmnic Usage = receive + transmit; rollup point = mean of its 15 samples; GAVG = DAVG + KAVG; esxtop group row = sum of its worlds; VCF Operations Contention from its parts; cluster = mean of identical hosts.
5. Screen reading, tested separately: stage 1 of the harness reads each image into a fixed schema (harness/AGENT.md); compare that output with the true values of each image. No answer key, no model judge. Starts with the 8 running screenshot questions and the author's field screenshots.
6. Duplicate guard. Each practical half has at least one option only its evidence decides, and tests no fact beyond its partner's and the cap of two. A search over stems and options (BM25) flags near-copies before a question is added.

## 8. Export templates (in progress)
- The author collects one real export per tool from the lab with a local Claude Code session, read-only: vCenter chart CSV (Real-time, Past day, Past week), the vCenter statistics levels, VCF Operations metric export, list view and API names, `esxtop -b` and the interactive panels as text, `typeperf`, `systeminfo`, Linux `top`, `sar`, `iostat`, `free`, `ip -s link`, `ethtool -S`.
- Saved under project/sources/export-templates/, with HEADERS.md: exact headers, units, time stamp format, delimiter, quoting, and every place where the export name differs from the screen name.
- Only names and formats are used. Lab values do not enter questions or knowledge files.

## 9. Decisions and the change set
Decided (author, 2026-11-15):
1. Practical halves become exports (CSV or tool text), not screenshots.
2. 0386 runs as CSV; the Task Manager screenshot question is deferred.
3. 0435 and 0015 deferred: availability is not in 1.0.
4. CSV cap: decided by Claude on the author's leave: 24,000 characters, periods cut to the event (section 7.1).

Conflicts with earlier decisions, changed by the change set:
- design.md 3.9 (2026-11-14): practical input "Screenshot, sometimes a table" becomes "an export: CSV or tool text; a screenshot only where the trap is visual".
- design.md 13 (2026-11-14): "1.0 grows the screenshot set" with the practical halves. Screenshots stay few, as customers send them; screen reading is tested in stage 1 (section 7.5).

The change set, after the templates are on main:
- design.md 3.9, 13 and 13.1; `question_csv_max_chars` in tags.yaml.
- 44 questions converted (prompt, options, `input`, `attachments`, `## Input to supply` removed, status draft); 0389 and 0419 retired; 0435 and 0015 deferred; pairs of 0068 and 0360 removed; 0391 C removed; 0025 rewritten; 0388 input fixed.
- The generator and its unit tests; every CSV checked against its key.
- question-pairing-2026-11-14.md: Screenshots to capture replaced by a link here.
- Lint, the two test suites, and the retrieval check before and after.
