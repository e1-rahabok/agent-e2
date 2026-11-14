# Question pairing: audit and plan (2026-11-14)

The theory and practical pairing of benchmark/design.md, section 3.9, applied to every question. Phase 1 (audit, read-only): 8 independent read-only agents; the leaks, the 0022 key and the 0104 base re-checked by hand. Phase 2: the changes, after the author's decisions in section 1. Not indexed. Status of each item: project/plan.md, M2.
Rules: T1 one fact per option; T2 no A / not-A (also a clause that negates another option); T3 no vague option; T4 Level 300 misconception and its over-correction; T5 a wrong-action option; T6 count of correct options (reported); T7 decidable from the knowledge files; T8 no hint, plural stem; T9 public vocabulary.

## 0. Numbers
- Theory audit: 77 text questions (Level 200-300, plus Level 400 explain-mechanism or read-metric).
  - Pass: 4 (0001, 0181, 0230, 0266).
  - Fail: 73. Key changes: 17 (up to 20 if 0111, 0276, 0278 are kept).
  - 26 are not theory questions (a setting or a capacity decision): only T1-T3 and T7-T9 apply.
  - Most common breaks: T2 in 35 (the true option is written as the negation of the misconception); T4 missing in 40; T5 missing in 33.
- Pair candidates: 82 pairs.

| Group | Pairs | New questions | Screenshots the author captures |
|---|---|---|---|
| A. Both halves exist: set `pair` after fixes | 16 | 0 | 1 recapture (0050) |
| B. Practical exists: write the theory half | 18 (+1 held) | 18 | 0 |
| C. Theory exists: write the practical half | 35 | 35 | 35 |
| D. New from the knowledge base: both halves | 13 | 26 | 13 |
| Total | 82 | 79 | 48 + 1 recapture |

- By field frequency: high 26, medium 51, low 5 (section 6).

## 1. Decisions (author, 2026-11-14)
1. Scope: every change of this plan, the author's questions included (book, quiz, real ticket). Executed as one change set: writers per technology in parallel, each reading this whole plan; one independent review; lint, tests and the retrieval check before and after.
2. Retired: 0276 (same fact as 0277), 0278 (inside 0279).
3. Leaks: each CSV whose values a knowledge file states (0081, 0085, 0102, 0103, 0142) or copies (0089, 0101, 0140, 0151) is regenerated with new numbers; the knowledge examples stay. 0104: its knowledge example (run-vs-used-gap) loses its number instead, since 0104's base is an open question (item 6).
4. Facts over the two-question cap: as recommended (0002 with 0102; 0003 with 0104; 0059 keeps what Contention counts; 0066 with 0103; 0331 J dropped; 0356 with 0089; option-level copies removed from the weaker question).
5. 0022: the author says the balloon driver comes from the VMware Tools service, so "Tools not running" stops ballooning. The knowledge base (ballooning, Broadcom KB 313773) says the driver is a kernel driver (Linux `vmw_balloon` is in the kernel; open-vm-tools does not contain it). Option D is reworded to the case both agree on (VMware Tools not installed on a Windows VM); key A,B,D,E holds. Raised as an author question.
6. 0104: the author says its base is right (300,000 ms per vCPU in a 5-minute point). collection-interval and aggregation say a VCF Operations 5-minute ms value averages the 15 values of 20 seconds (100% = 20,000 ms per vCPU). 0104's base is not changed; raised as an author question; pair D1 is held until the answer.
7. 0004: the values come from the chart, not the typed approximations. 0016 and 0140: changed as proposed.
8. Masking: every VM name is masked, in existing and new screenshots.
9. Lint: the singular stems ("What is its", "By how much", "How is ... related", "What is the relationship") join `question_prompt_hints`.

## 2. Theory audit (77)
Key: "no" or old → new letters. NT = not a theory question (setting or capacity).

### CPU
| id | file | broken | fix | key |
|---|---|---|---|---|
| 0001 | L3-01 cpu-wait-includes-idle | passes | - | no |
| 0007 | L3-02 xeon specification (NT) | T1 D, E | one fact each: A "All 24 cores at 3.4 GHz at once"; D "With OS Controlled and Balanced every workload loses performance" (F); E "At 4 GHz the CPU draws more than 210 W" (F) | no |
| 0009 | L3-03 counters where a vCPU cannot run | T4, T5 | add H "CPU Latency" (F: also counts HT and frequency); add I "CPU Swap Wait" (T) | A,B,C,D → A,B,C,D,I |
| 0010 | L3-04 run queue, context switch | T1 B, C; T2 B/D, C/E; T4; T5 | B "Processor queue length has no bearing on application performance" (F); C "High context switch rate: add vCPUs" (F); D "Windows Processor Queue Length leaves out running threads; Linux counts them" (T) | no |
| 0011 | L3-05 CPU reservation (NT) | T1 F; T3 G | F "The ESXi kernel holds no CPU reservation of its own" (F); G "The kernel's CPU use never exceeds its reservation" (F); G is a copy of 0024 E | no |
| 0013 | L3-06 reclaiming vCPUs (NT) | T1 B, C; T3 C | split B and C into single facts ("frees allocation, not cycles") | no |
| 0016 | L3-09 provider-consumer Ready, Demand | T2 B/C, D/F, E/G; T5; T7 D, G ("dashboard" names no tool); T9 F, H, I (knowledge-base terms) | stem names the vSphere Client host chart; C "Every host CPU counter is a sum over its VMs" (F); G "Host CPU Usage includes vSAN and NSX kernel work" (T) | A,C,D,G,I → A,D,G,I |
| 0019 | L3-11 performance vs capacity view | T6 5/5 all true; T1 A-D; T4 no false option; T5 | split A-D; add F "A cluster at 95% CPU usage has a VM performance problem" (F); G "Utilization plays no part in troubleshooting" (F, over-correction); H "95% and no contention: add hosts now" (F) | no (5 of 8) |
| 0053 | L2-14 co-stop | T4, T5 | C "Co-stop comes from ESXi being short of CPU, like Ready" (F); E "Co-stop and Ready are independent counters" (F); F "High Co-stop: add vCPUs" (F) | no |
| 0105 | L3-20 Ready summation to % | T4, T5 | F "A 5-minute point cannot become a percentage" (F); G "4% per vCPU in one sample: add 2 vCPUs" (F) | no |
| 0107 | L3-21 oversized VM (NT) | T2 A/B | B "Add 8 vCPUs: Net Run 9% per vCPU shows saturation" (F) | no |
| 0110 | L3-22 overlap | T4, T5, T7 E | E "For the guest, Overlap is time frozen on that vCPU" (T); F "Used counts Overlap too" (F); G "Move the disks to a faster datastore to cut Overlap" (F) | no |
| 0111 | L3-23 power policy (NT) | T2 A/G; T7 J (power-states Turbo conflict) | G "Under High Performance an idle core stops at C1"; J restated; L, M copy 0112 | no (C..I if L, M go) |
| 0362 | L3-41 ESXi Demand, model question | T1 C; T2 C/D, H/I; T5 (G is a reading, no action); T7 E/J (demand.md line says "adds") | C "VCF Operations Demand includes the host's CPU System Resource Reservation"; E "Per running VM, VCF Operations counts the higher of demand and reservation"; G "Demand far above Usage: add a host" (F); I "VCF Operations Usage also adds the reservation" (F); fix the demand.md line | no |
| 0002 | L4-01 CPU Latency, frequency | T2 B/D; T5 | D "Ready and Co-stop count time waiting for a thread"; add I "Add two vCPUs to bring Latency back" (F) | no |
| 0003 | L4-02 HT, VM vs ESXi | T1 B; T2 G/H; T4 | H "62.5% is the share of the core charged to each thread"; add L "Each VM does as much work as with the core to itself" (F) | no |
| 0012 | L4-07 Utilization 50, Core 50 | T1, T2, T3 C ("Nothing"), T4, T5, T7 (HT not stated), T8 | stem states HT on; 8 single-fact options (A every running core runs both threads T; C half the threads are free T; F with HT off they always match T; H running vCPUs show up to 37.5% Latency T) | A → A,C,F,H |
| 0100 | L4-44 Used VM vs vCPU instance | T1 B; T2 A/E; T4; T5; T8 "(VM only)" | drop the hint; B "VM Used equals the sum of its vCPU instances" (F); H "The gap is Turbo counted again" (F); I "Add a vCPU" (F) | no |
| 0266 | L4-87 steal time, Windows busy | passes | - | no |
| 0267 | L4-88 two sockets, one NUMA node | T2 A/B, D/H; T4 | A "Two sockets in Task Manager mean two physical NUMA nodes" (F); D positive; add L "Cores per socket only affects licensing" (F) | no |
| 0293 | L4-100 CPU hot add, NUMA (NT) | T1, T2, T8 (allowHotadd line touches Q216) | drop that line; single facts A, B, E, G true | B → A,B,E,G |
| 0331 | L4-111 esxtop load average | T2 D/I; T4 | D positive; add L "Load 2.60: every VM waits 60%" (F) | no |
| 0357 | L4-127 same VM, two tools | T1 B; T2 A/B, E/H; T4; T5; T8 ("no counter called Contention") | remove the clause; reword A, B, E; add O "VCF Operations CPU Usage has its own formula" (F); P "9.8% Contention: add a host" (F) | no |

### Memory
| id | file | broken | fix | key |
|---|---|---|---|---|
| 0014 | L3-07 reservation CPU vs memory | T1 D; T2 A vs B, C, E; T5 | A "A memory reservation is backed only as pages are touched" (T); D "Lower the CPU reservation: it keeps 4 GHz from others now" (F) | no |
| 0017 | L3-10 overhead classification (NT) | T1 I; T2 G ("all of the above") | G and I one fact each | no |
| 0021 | L3-12 counter to size VM memory (NT) | T3 E ("In some cases") | E "Guest memory in use plus part of its cache" | no |
| 0022 | L3-13 VM vs Guest OS memory | T1 A, B, E; T3 B; T7 A, D (D false by ballooning.md); T4; T5 | A "The guest runs its memory as on a physical server, blind to host memory"; B "ESXi cannot see which guest pages are Standby or Free"; D "On Linux, ballooning continues while vmtoolsd is stopped" (T) | A,B,D,E → A,B,E (as written) |
| 0023 | L4-10 actual vs potential contention | definition prompt at Level 400 (F5); T1; T4; T5 | stem with values (Ballooned 6 GB, Swapped 1.2 GB flat, Contention 0 except 0.8% at 02:05); 7 single-fact options | C → A,B,C |
| 0052 | L2-13 balloon above zero | T1 A; T2 A/C; T4 | A "Ballooned 2 GB shows the VM waits now" (F); add I "Ballooning cannot slow it" (F, over-correction); J "Add memory" (F) | no |
| 0056 | L4-15 host Consumed with no VMs | T4; T5; stem copies the consumed.md example | new numbers (512 GB host, 41 GB); add F "Without vSAN Consumed reads 0" (F); G "Reboot before leaving maintenance" (F) | no |
| 0057 | L4-16 memory tiering candidate (NT) | T1 E | E one fact | no |
| 0095 | L3-19 Windows In Use vs Consumed | T4; T5; T8 (the owner's line states the key) | drop that line; add J "Consumed is of no use once guest counters exist" (F); K "Consumed near configured: add 8 GB" (F) | no |
| 0143 | L3-25 Swapped is not out minus in | T2 A/B; T4; T5 | B positive; F "A flat Swapped total is history only" (F: swap-in 2,000 KBps); G "ESXi brings the pages back by itself" (F) | no |
| 0144 | L3-26 host state at 6 GB free | T4; T5; stem copies the host-memory-states example | 2 TB host, new numbers; F "Ballooning never slows a VM" (F); G "Move VMs off now" (F) | no |
| 0145 | L3-27 page sharing (NT) | T1/T7 A (case fact not in stem) | A "ESXi shares pages only within one resource pool" (F) | no |
| 0146 | L4-58 sharing jumps | T2 I/J; T4 | J positive; add N "Turn off 2 MB pages so sharing works from the start" (F) | no |
| 0149 | L2-15 what memory contention counts | T4; T5 | F "Same measure as CPU Swap Wait" (F); G "2%: add memory" (F); H "Waits for decompression" (T) | A → A,H |
| 0181 | L3-29 swap space, mass power-on (NT) | passes | - (fact also in 0296) | no |
| 0263 | L3-38 Linux free near zero (NT) | T2 B vs C, D | B "Keep 32 GB: memory pressure stayed at 0" | no |
| 0270 | L3-40 commit limit, no page file | T4 | A one fact; add F "Adding RAM is the only fix" (F) | no |
| 0020 | L4-09 Usage VM vs ESXi | T2 E/G, E/I; T4; key point I lists balloon as contention | G "Host Consumed near 100% is the normal state of a used host" (T); I "Shortage is read from VM contention and swap-in" (T); add J "Host Memory Usage has no use in capacity" (F) | no |
| 0068 | L4-26 esxtop ZIP vs UNZIP | T1 B, D; T2 B/C; T4; T5 | B, C, D one fact each; G "vm-d's swapped pages carry no risk" (F); H "Move vm-d first" (F) | no |
| 0273 | L2-17 GPU memory, idle host | T1 A; T2 F/G; T4 | F "A vGPU frame buffer sits on one GPU" (T); J "Compute below 5%: room for another vGPU VM" (F); K "Buy GPUs" (F) | no |

### Storage
| id | file | broken | fix | key |
|---|---|---|---|---|
| 0027 | L3-14 disk latency threshold (NT) | T2 A/B, C/D; T3 E, I; T7 G | drop B, D; E "Read and write get separate thresholds"; I "A low threshold gives red with no complaints"; G restated | B,C,E,G,I → B,C,E,G (relettered) |
| 0028 | L3-15 latency and outstanding IO | T1/T3 A; T4; T5; T8 singular | plural stem; A "Not linked by any formula" (F); E "High OIO means high latency whatever the IOPS" (F); F "OIO 32: move the VM" (F) | no |
| 0043 | L2-05 GAVG formula | T1 A, D; T2 A/D; T7 A (QAVG can exceed KAVG); T4; T5; T8 | plural stem; A "GAVG = KAVG + DAVG"; C "QAVG can never exceed KAVG" (F); D "GAVG is what the guest measures" (F); E "KAVG 2.1, DAVG 1.0: ask the array team" (F) | no |
| 0044 | L2-06 total latency weighted | T4; T5; T8 singular | plural stem; C "Command latency equals read latency whenever reads dominate" (F); E "3.6 ms: no LUN problem" (F) | no |
| 0045 | L2-07 datastore read IOPS above vdisk | T5; T7 H (derivable) | add J "Move to a faster datastore" (F) | no |
| 0049 | L2-11 totals do not reconcile | T2 C/D; T3 D; T7 ("disk IOPS" is three counters); T4; T5 | "virtual disk IOPS"; D "Snapshot IO counts in the datastore sum only" (T); E, F false | no |
| 0182 | L3-30 guest deleted data | T2 A/B; T4 | A "Shrinks only when Windows sends TRIM or unmap" (T); G "Gives space back only after Storage vMotion" (F) | no |
| 0185 | L3-31 RDM IO missing | T4; T5; T7 F (mode not named) | G "Datastore IOPS include other VMs' IO" (F); H "Only 50 IOPS: LUNs have room" (F); fix F or the file | no |
| 0310 | L4-106 Storage DRS (NT) | T1/T2 (whole outcomes); T8; knowledge_main should be storage-drs | 10 single-fact options | B → A,B,G,J |
| 0237 | L4-78 API export vs chart | T1 B; T4; T5 | B "The API returns Consumed in MB" (F); F "API network usage is in kilobits" (F); G "Report 1 Day max as the worst of each 5 minutes" (F) | no |

### Network
| id | file | broken | fix | key |
|---|---|---|---|---|
| 0039 | L2-01 VM dropped vs guest | T1 C; T5; T7 D, E (not in the knowledge base) | C "Linux has no counter for ring-full drops" (F); D "The guest and ESXi count the same packets" (F); E "Raise the ring in Linux" (F) | no |
| 0040 | L2-02 full-duplex capacity (NT) | T2 A/B; T8 singular | plural; B "Usage can exceed 25 Gbps with no fault" (T); D "Judge each direction against 25 Gb" (T); E "30 Gbps: add a port" (F) | B → B,D |
| 0041 | L2-03 set vNIC speed (NT) | T2 B/C; T7 L | C "VMXNET3 reports the uplink speed" (F); L "vCenter has a counter for NIOC caps" (F) | B,D,E,F,I,L → B,D,E,F,I |
| 0061 | L4-20 dropped 95% spike | T2 B/D; T4; T5; T8 (formula in stem); stem mirrors the file | give counters instead; D restated; F "Read only the count" (F); G "Open an outage ticket" (F) | no |
| 0077 | L4-32 vMotion downtime units | T4; T5 | F "1.45 s is too short to notice" (F); G "Exclude from DRS" (F) | no |
| 0211 | L3-32 small packets | T4; T5 | F "Throughput counters are of no use" (F); G "Move to faster uplinks" (F) | no |
| 0213 | L3-33 jumbo frames (NT) | T7 B, E, C (vmkping, 28-byte header not in the knowledge base) | add the facts to network-configuration-review from the Broadcom KB | no |
| 0214 | L3-34 network latency | T2 A/B; T4 | B "The delay must come from the physical switches" (F) | B,C,E,F,G,H,K → C,E,F,G,H,K |
| 0268 | L3-39 TCP retransmits | T2 H/N, D/G, E/F; T4 | H "vSphere counters rule out nothing here" (F); G, F positive | A,C,F,G,H,J,K,M → A,C,F,G,J,K,M |
| 0295 | L4-102 SplitRx (NT) | T1/T2 (VM sets); T7 (restart rule not in splitrx-mode); T8 | one option per VM; add the restart rule to the file | B → A,C,E |
| 0313 | L4-108 peak Tx dropped | T2 E/F; T4; T5; T8 (formula in stem) | delete the two lines; B "about 3%"; I, J false | no |

### System, VCF Operations, Guest OS
| id | file | broken | fix | key |
|---|---|---|---|---|
| 0015 | L3-08 VM availability | T2 A/B; T4; T5 | A "Count this crash as VM downtime" (F); K "The applications count as available" (F) | A,C,D,E,F,G → C,D,E,F,G |
| 0047 | L2-09 rollup dilutes peaks | T4; T5; T8 singular | plural; A "In 1 Week the burst is diluted 90x" (T); E, F false | B → A,B |
| 0048 | L2-10 admission control (NT) | T2 A/C; copies the file | A, C restated | no |
| 0094 | L3-18 collect every metric at 20 s (NT) | T9 J ("context metrics"); B, C, D, E, H copy metric-volume | paraphrase; J restated | no |
| 0114 | L3-24 scale up vs out (NT) | T2 B/C; T3 C; T7 A, F | C NUMA fact; A, F restated | no |
| 0231 | L3-35 counter missing from history (NT) | T2 A/C | C "Real-time can still be opened for 3 days ago" (F) | no |
| 0232 | L3-36 DRS score high, one VM slow | T2 A/E; T4 | A weighted average of VM scores (T); E "VM score below 80% means waiting now" (F) | no |
| 0233 | L3-37 usable capacity, HA (NT) | T7 A, B (supply.md table conflicts) | fix the supply.md table | no |
| 0271 | L2-16 Tools not running | T7 D, F (not in the knowledge base) | D "Guest disk queue length"; F "Guest context switch rate" | no |
| 0356 | L4-126 nine-day-old peak | T1 B, D, E; T2; T4 | 8 single-fact options | D → B,D,E |
| 0230 | L4-74 pool share dilution (NT) | passes | - | no |
| 0276 | L4-93 Top N 20 s (NT) | duplicate of 0277 | retire | (B → A,B,D if kept) |
| 0278 | L4-95 manual business application (NT) | inside 0279 | retire | (B → B,C,F if kept) |

## 3. Pairs from existing questions

### A. Both halves exist: set `pair` after the fixes (16)
| # | Theory | Practical | Fact | Fix first | Freq |
|---|---|---|---|---|---|
| A1 | 0012 | 0004 (screenshot) | ESXi Utilization vs Core Utilization vs Usage | 0012 rewrite; 0004: delete the value bullets (hint, and they disagree with the chart: about 75/46%, not 70/40%) | h |
| A2 | 0020 | 0151 | vCenter VM memory Usage is Active | 0151 near-copy of an example: new scenario | h |
| A3 | 0016 | 0115 | host Ready is the VMs' sum; one VM hides | 0115 stem states the mechanism ("averaged over its 110 vCPUs") | h |
| A4 | 0021 | 0079 | size memory from guest needed memory | - | h |
| A5 | 0343 | 0080 | rank datastores by thin space and snapshots, not used % | - | h |
| A6 | 0062 | 0184 | datastore average hides one VM | 0184 A not in the knowledge base | h |
| A7 | 0002 | 0102 | CPU Latency counts frequency and HT | 0102 CSV leak | m |
| A8 | 0003 | 0104 | Run vs Used: HT and power saving | 0104 base and leak | m |
| A9 | 0066 | 0103 | limit time inside Ready; Demand = Usage | 0103 CSV leak | m |
| A10 | 0048 | 0085 | admission control counts reservations | 0085 CSV leak | m |
| A11 | 0143 | 0142 | Swapped is a current amount; target vs result | 0142 CSV leak | m |
| A12 | 0356 | 0089 | VCF Operations peak within collection cycle | 0089 near-copy: new numbers | m |
| A13 | 0061 | 0082 | Packets Dropped (%) high at low traffic | - | m |
| A14 | 0291 | 0140 | memory limit swaps on a host with free memory | 0140 A rests on Q205: drop it | m |
| A15 | 0186 | 0050 | esxtop NFS: DAVG is beyond the NFS client | 0050 image has drawn marks on the answer row: recapture or mask the marks | m |
| A16 | 0043 | 0086 | full device queue: wait in KAVG/QAVG, DAVG low | 0043 rewrite; 0086 stem reads the CSV for the candidate | m |

### B. Practical exists: write the theory half (18 new, complete)
| # | Practical | Theory half (level, deciding file) | Freq |
|---|---|---|---|
| B1 | 0106 | Ready read against Run, not a flat threshold (L300, ready) | h |
| B2 | 0264 | Windows Available = Standby + Free; Modified is not available (L200, windows-memory) | h |
| B3 | 0260 | Linux load average counts runnable and D-state tasks (L300, linux-os-slow; needs a source: the file's review note) | h |
| B4 | 0239 | a pool CPU limit holds VMs cluster-wide; time shows in Ready and Max Limited (L300, resource-pool-design) | m |
| B5 | 0235 | Capacity Remaining = usable minus highest projected point in 3 days (L300, capacity-forecast) | m |
| B6 | 0074 | VM transmit drops are real loss TCP resends (L300, packets-dropped) | m |
| B7 | 0081 | rank by percentile, not maximum (L300, aggregation + adapter-and-path); CSV leak | m |
| B8 | 0072 | adapter Highest latency averages read and write, then takes the worst adapter (L300, adapter-and-path); 0072 stem reads the CSV | m |
| B9 | 0217 | vmnic load is not the sum of VM traffic (L300, network-observability) | m |
| B10 | 0188 | array IOPS count every initiator; datastore only its hosts (L300, storage-layers) | m |
| B11 | 0088 | vmnic error counters: 0 at all times; average hides one port (L300, host/errors); 0088 D-G not in the knowledge base | m |
| B12 | 0236 | default shares scale with vCPUs: a downsize lowers the VM's total shares (L300, ready + resource-controls); knowledge contradiction first (section 5) | m |
| B13 | 0265 | Windows paging to its own page file is invisible to VM counters (L300, windows-memory) | m |
| B14 | 0101 | vCPU Usage Disparity: peak minus minimum; Turbo can pass 100% (L300, usage-disparity); near-copy | l-m |
| B15 | 0084 | IP storage read arrives as network Receive; frames carry headers (L300, ip-storage-network-accounting) | l |
| B16 | 0109 | Swap Wait is a memory cause in a CPU state (L300, swap-wait) | l |
| B17 | 0147 | a VM waits on the NVMe tier in proportion to its reads (L300, memory-tiering) | l |
| B18 | 0216 | a broadcast reaches every VM in its VLAN (L300, distributed-switch packets) | l |
| held | 0141 | Granted vs limit: rests on Q214 | - |
- No pair: 0034, 0037, 0042, 0051 (Level 100-200 recognition: the screen matches expectation; remove the stale `## Input to supply`), 0046 (provisioned vs used; the fact sits in 0080 and 0343), 0083 (capacity decision).

### C. Theory exists: write the practical half (35, awaiting-input: the author's screenshots)
Each: tool, screen, counters, time range; condition the key depends on. All masked; none a knowledge-base image.

High
| # | Theory | Capture | Level |
|---|---|---|---|
| C1 | 0266 | Windows 4-vCPU VM on an overcommitted host, 10 min: Task Manager > CPU near 100%; vSphere Client VM > Advanced > CPU, Real-time: Run, Ready, Co-stop (ms), Readiness. Condition: Readiness 25-40% while Task Manager stays near 100%; no limit | 400 |
| C2 | 0105 | 8-vCPU VM, vSphere Client Advanced > CPU, Ready (ms), VM object: Real-time with one sample near 4,000 ms, and Last day with the 5-minute point holding it. Condition: the 1 Day point about 15 times the burst's share | 300 |
| C3 | 0144 | vSphere Client host > Advanced > Memory, Past week: Usage (%) at 94% or more, Ballooned 0, Swap in rate 0; plus a VCF Operations list of the host's VMs with max Memory Contention below 0.5% | 300 |
| C4 | 0095 | Windows VM, Past day: Task Manager > Memory (In use falls after an application restart) and vSphere Client VM Consumed (flat near configured) and Active | 400 |
| C5 | 0357 | one VM, same 30 minutes: vSphere Client CPU Usage (%) on the Last week chart; VCF Operations CPU Usage (%) and CPU Contention (%) | 400 |
| C6 | 0008 | VCF Operations 4-vCPU VM, 7 days: CPU Usage (%) 90-110%, Net Run 70-80%, Ready below 1% (Turbo headroom, Balanced) | 400 |
| C7 | 0019 | VCF Operations cluster, 7 days: CPU Usage (%) 90-95%, CPU Contention (%) below 1%, worst-VM contention low | 400 |
| C8 | 0047 | one VM: vSphere Client CPU Usage (%), Real-time with a 2-minute burst near 100%, and Last day with the same time near its average | 300 |
| C9 | 0001 | 4-vCPU mostly idle VM, Advanced > CPU, Real-time: Wait, Idle, Run, Ready, Co-stop (ms). Condition: Wait about 70,000-75,000 ms, Idle within 1,000 ms of Wait, Ready below 400 ms | 300 |
| C10 | 0263 | VCF Operations Linux VM, 7 days: Guest Free Memory about 1%, Guest Needed Memory about 30%, swap rates 0 | 300 |
| C11 | 0107 | VCF Operations 24-vCPU VM, 7 days: Peak vCPU Ready, Co-stop, Net Run per vCPU; plus Task Manager with 3 of 24 CPUs busy | 400 |
| C12 | 0052 | vSphere Client VM, Past week: Ballooned flat at 15% or more of configured for 3 days, Balloon target 0 at the end, Swap in rate and Latency 0 | 300 |
| C13 | 0029 | same minute, steady iperf: esxtop `n` MbTX/s for the VM port; vSphere Client VM network Data transmit rate. Condition: esxtop ≈ vCenter × 8 × 1,024 / 10^6. Knowledge unit fix first (section 5) | 300 |

Medium
| # | Theory | Capture | Level |
|---|---|---|---|
| C14 | 0058 | host, Turbo on, Balanced: Usage (%) 105-120%, Core Utilization 85-95%, Utilization 50-65%; VMs' peak Ready below 2% | 400 |
| C15 | 0068 | esxtop `m` with MCTLSZ, SWCUR, SWR/s, SWW/s, ZIP/s, UNZIP/s; the VM with the largest SWCUR shows SWR/s = 0, another shows SWR/s above 0 | 400 |
| C16 | 0056 | vSAN host across entering maintenance, 2-3 days: Consumed stays above 10 GB with 0 VMs; Configure > System Resource Reservation | 400 |
| C17 | 0025 | host 90 days: Compressed (or Swap consumed) flat above 0, Balloon 0, Usage below 90% | 300 |
| C18 | 0040 | one vmnic, Real-time: Usage above link speed, receive at 90% of line rate, transmit 30-60%; Physical adapters page | 300 |
| C19 | 0044 | one device, Real-time 1 h: read, write, command latency; reads 8x writes, writes 5x slower; command within 25% of read | 300 |
| C20 | 0211 | VM network Real-time: Packets received (count per 20 s) and Data receive rate; small packets | 400 |
| C21 | 0028 | virtual disk Real-time: outstanding reads 16 or more at 1 ms or less; OIO ≈ IOPS × latency | 300 |
| C22 | 0049 | VCF Operations datastore Read IOPS and each host's Datastore:DS Read IOPS, 24 h; host A at 40% or less | 300 |
| C23 | 0311 | PerfMon PhysicalDisk report: % Disk Time 1,000% or more, queue = transfers × sec/transfer; vCenter virtual disk latency | 400 |
| C24 | 0360 | Linux `iostat -xd 5` with %util 99, aqu-sz 30, await 3 ms or less; vCenter virtual disk latency same minutes | 400 |
| C25 | 0232 | cluster Summary DRS Score above 90%; VM DRS Score list with one VM low; that VM's Ready chart | 300 |
| C26 | 0039 | vSphere Client VM Receive packets dropped above 0, Real-time 1 h; Linux `ip -s link` and `ethtool -S` at 0 | 300 |
| C27 | 0149 | VCF Operations VM 24 h: Memory Contention follows Swap In Rate, not Balloon | 300 |
| C28 | 0053 | esxtop CPU, one 16-24 vCPU VM expanded: %CSTP on siblings, PCPU UTIL about 50% | 300 |
| C29 | 0009 | esxtop CPU, VM expanded: %RDY, %CSTP, %SWPWT above 0 while %WAIT is mostly %IDLE | 300 |
| C30 | 0010 | PerfMon 1 h, 4-vCPU VM: Processor Queue Length above 2 per vCPU, Context Switches/sec, % Processor Time near 100% | 300 |
| C31 | 0270 | Task Manager > Memory (Committed at 95% of a limit ≈ RAM, Available 1 GB or more); Virtual memory dialog with no paging file | 300 |
| C32 | 0015 | VM Summary powered on, Tools not running; console showing the crash | 300 |
| C33 | 0313 | VCF Operations VM 1 day: Peak Transmitted Packet Dropped (%) about 3% in one cycle, 5-minute share about 0.2% | 400 |
| C34 | 0331 | esxtop CPU panel: load average about 2.6, PCPU UTIL 100, VM rows with %RDY and one %MLMTD | 400 |
| C35 | 0267 | Task Manager CPU (2 sockets, 16 processors), coreinfo (1 NUMA node), esxtop NUMA fields (NHN 1, N%L 100) | 400 |
- Not proposed (low frequency or no screen adds anything): 0007, 0011, 0014, 0041, 0045, 0057, 0059 (cap), 0077 (log metric), 0100, 0108, 0110, 0112, 0146, 0182, 0185, 0214, 0230, 0231, 0237, 0261, 0268, 0273, 0293, 0310.

## 4. New pairs from the knowledge base (both halves new; 13)
| # | Fact | Deciding file | Misconception / over-correction / wrong action | Levels | Capture | Freq |
|---|---|---|---|---|---|---|
| D1 | VCF Operations ms metrics: 100% is 20,000 ms per vCPU (mean of 15 samples); vCenter Last day sums: 300,000 ms | collection-interval, aggregation | 3,000 ms is 1% / "VCF Operations ms is already per vCPU" / open a case over the 15x gap | T300, P400 | 4-vCPU VM under contention: VCF Operations CPU Ready (ms) and (%) at one 5-minute point; vSphere Client Last day Ready (ms) at the same time. Condition: vCenter ≈ 15 × VCF Operations; % = ms / (20,000 × 4) | h |
| D2 | VM memory Usage (%): vCenter = Active / configured; VCF Operations = guest Needed Memory / total | vm memory usage | one tool is wrong / every memory counter differs / cut to vCenter Active | T300, P400 | Windows VM, 24 h: vSphere Client Usage, Active, Consumed; VCF Operations Memory Usage (%), Guest Needed Memory, Total Capacity, Contention. Condition: vCenter Usage 15% or less, VCF Operations 60% or more; trim 0020 H | h |
| D3 | cluster CPU Usage averages hosts: the busiest host per point is the risk | aggregation, performance-vs-capacity | cluster peak 80% so every host below 80% / plan capacity on the busiest host / add a host | T300, P400 | VCF Operations cluster CPU Usage 7 days (peak 65-70%) plus host CPU Usage per host; one host at 95-100% (VM-host rule) | h |
| D4 | VCF Operations VM disk latency averages the disks: one slow disk with few IOs hides | vm-storage-performance-checks, peak-20-second-metrics | VM 2 ms so every disk is fine / no VM metric can show it / close the case | T300, P400 | VCF Operations VM 24 h: aggregate and per-disk read latency and IOPS (6+ disks), Peak Latency within collection cycle; one disk at 15 ms+ for 1 h at under 10% of IOPS. Options do not compute the aggregate (weighting not stated) | h |
| D5 | host CPU Usage averages all threads: one saturated thread is invisible | peak-core-usage | host 15% so no core is busy / scheduler misbalance / add a host | T300, P400 | vSphere Client host, Real-time, Utilization per PCPU instance with Max column; host below 20%, 1-3 instances at 90-100% (1-thread burner) | m |
| D6 | an IOPS limit on a virtual disk holds IO in the kernel: QAVG and KAVG up, DAVG normal, IOPS flat | virtual-motherboard/iops | array slow / high QAVG always means a limit / array case | T300, P400 | virtual disk Real-time (IOPS flat at about 250, latency 30 ms+); esxtop `u` (DAVG below 1 ms, KAVG 10x DAVG); 1,000 IOPS limit, 128 KB reads | m |
| D7 | one VM, three storage levels: virtual disk, datastore, disk (NFS absent from Disk; Disk is this VM only) | virtual-motherboard/disk, storage-layers | Disk is the whole LUN / they never match / collection fault | T300, P400 | VM Real-time: Virtual disk (VMFS and NFS disks), Datastore, Disk charts, plus the host device chart | m |
| D8 | without guest data, VCF Operations Memory Usage falls back to Active, Workload to Consumed | vm memory usage, guest-os-sizing | app freed memory / history corrupt / downsize on the dip | T300, P400 | VCF Operations VM, 2 h around a 20-30 minute stop of the Tools service: Usage, Workload, Guest Needed Memory, Active, Consumed | m |
| D9 | a 5-minute burst offset by half a cycle shows as two points at half height | collection-interval (fix the example first) | 50% load for 10 minutes / bursts under 5 minutes leave no trace / support case | T300, P400 | 300 s burner starting 2.5 min into a cycle: Real-time plateau about 100%; VCF Operations two points about 50% | m |
| D10 | esxtop MEM overcommit avg is requested over managed minus 1; above 0 is not pressure | esxtop/memory | host short or swapping / no level can cause swapping / migrate until 0 | T300, P300 | esxtop `m` header (overcommit 0.3+ at all three averages, state high, MEMCTL, SWAP, ZIP 0) | m |
| D11 | after a memory downsize, guest Free falls by design; too far shows as sustained page-out or contention | rightsizing, guest-os-sizing | undo the downsize / paging never matters / restore on Free alone | T300, P400 | VCF Operations VM 4 weeks across 32 → 16 GB: Guest Free, Needed, Usage, page-in/out, Contention | m |
| D12 | Linux `st` reports Ready only with the steal clock enabled | guest-os-vs-vm-cpu | st 0 means never frozen / Linux never reports steal / add vCPUs | T300, P400 | Linux VM, default advanced settings, host contention: `top` with 0.0 st; vCenter Readiness 10%+ same window. Needs a vSphere source (only KB 434983, written for Tanzu) | m |
| D13 | host Memory Latency averages its VMs: one waiting VM hides | host/latency | host 0.3% so no VM waits / rises only when all wait / close the ticket | T300, P400 | host Latency (%) Past day 0.5% or less; one VM at 5%+ for 30 min (limit below its working set) | m |
- Deferred: knowledge gap or open author question. vSphere Client "Guest memory" label (consumed.md vs the vSphere API); Reclaimable Idle vs Idleness Indicator (idle-vm review notes); VCF Operations "Total" packet metrics (labels); ESXi Memory Utilization (Q215, Q221); cluster Consumed vs the sum of hosts (review note); VM Used above the vCPU sum (system.md note); Other Wait on an idle VM (needs a field screenshot).
- Not proposed (cap reached): host Ready as a sum (0016 + 0115); Latency vs Contention (four questions); 20-second peaks (0089 + 0356).

## 5. Defects found on the way
- Leaks (section 1, item 2).
- 0004: the stem types Core about 70% and Utilization about 40%; the chart shows about 75/46% (Latest 84.94/54.38). Key C ("40%") fails on the image. The typed values also equal the utilization.md example.
- Stems that read the evidence for the candidate (design 6.2): 0004, 0072, 0086, 0115; stems that define a formula: 0061, 0313; stems that state the key: 0095, 0100, 0357.
- Stale `## Input to supply` in 0034, 0037, 0042, 0050, 0051.
- Stems or options copied from a knowledge file (recall, not reasoning): 0027, 0048, 0056, 0061, 0094, 0144.
- Knowledge contradictions, fixed as general facts in Phase 2 after a vendor check:
  - host/demand misconception line says VCF Operations "adds" the VMs' reservations; its table and your Q218 answer say "the higher of".
  - collection-interval, Short problems: the 08:00 point covers 07:55-08:00 (idle); only 08:05 and 08:10 are half busy.
  - vcenter-statistics: "charts convert network usage to Mbps" and "labelled Kbps but measured in KBps" in the same section; 0029 and throughput say KBps.
  - supply.md usable-capacity table reads as the HA host covering maintenance; 0233's key says otherwise.
  - power-states: "turning off C-states does not disable Turbo" vs its table row "0 | 1: no Turbo" (already a review note).
  - consumed.md: "Guest | Memory Usage is the same as Consumed"; the vSphere API quickStats guestMemoryUsage is active guest memory.
  - splitrx-mode lacks the restart rule (Performance Best Practices); network-configuration-review lacks the vmkping and 28-byte header facts (Broadcom KB).
  - disk.md: Requests (summation) and requests per second "basically the same".
- Contradictions that may need you (raised only if vendor documents do not settle them):
  - esxtop/cpu: "%RUN can be twice %USED" on Hyper-Threading vs used.md and hyper-threading (Used 62.5% at Run 100%). Close to Q220.
  - noisy-neighbour: "shares are per VM, not per vCPU" vs ready.md and vcpu-states (default shares per vCPU). 0107 D and B12 depend on it.
  - Consumed called "the main capacity counter" (host/ballooned, host-memory-metrics) and "too conservative" (host/utilization).

## 6. Ranking by field frequency
- High (26): A1-A6; B1-B3; C1-C13; D1-D4.
- Medium (51): A7-A16; B4-B13; C14-C35; D5-D13.
- Low (5): B14-B18. Held: 0141 (Q214).
- Total: 82 pairs (16 ready, 66 to write). New questions: 79. The author's screenshots: 48 new, plus 1 recapture (0050).

## 7. Phase 2: writers
One change set. Each writer reads this whole plan, writes only its own files and the knowledge files listed for it, and reports. New files take temporary names `L<level>-9NN-<slug>.md` in the writer's range; `project/tools/renumber_questions.py` numbers them at the end. New ids in the writer's range; gaps are closed before the commit.

| Writer | Questions | Knowledge files it may edit | New ids | Temp numbers |
|---|---|---|---|---|
| W1 CPU fixes | rewrites 0007, 0009, 0010, 0011, 0013, 0016, 0019, 0053, 0105, 0107, 0110, 0111, 0362, 0002, 0003, 0012, 0100, 0267, 0293, 0331, 0357; A1 (0004), A3 (0115), A7 (0102), A8 (0104), A9 (0103); 0059 trim; `pair` on 0001, 0066, 0266 as their partners arrive | sp5-framework/performance/noisy-neighbour, vsphere/tools/esxtop/cpu, vsphere/technology/cpu/concepts/power-states, vsphere/technology/cpu/troubleshooting/run-vs-used-gap | - | - |
| W2 CPU new | B1, B12, B14 (and the 0101 CSV), B16; C1, C2, C5, C6, C9, C11, C14, C28, C29, C34; D5, D12 | - | 0364-0389 | 900-924 |
| W3 Memory fixes | rewrites 0014, 0017, 0021, 0022, 0023, 0052, 0056, 0057, 0095, 0143, 0144, 0145, 0146, 0149, 0263, 0270, 0020, 0068, 0273; A2 (0151), A4 (0079), A11 (0142), A14 (0140) | vsphere/technology/memory/metrics/host/consumed, vsphere/technology/memory/metrics/virtual-motherboard/consumed | - | - |
| W4 Memory and Guest OS new | B2, B13, B17; C3, C4, C10, C12, C15, C16, C17, C27, C31; D2, D8, D10, D11, D13 | - | 0390-0414 | 925-949 |
| W5 Storage and network fixes | rewrites 0027, 0028, 0043, 0044, 0045, 0049, 0182, 0185, 0310, 0237, 0039, 0040, 0041, 0061, 0077, 0211, 0213, 0214, 0268, 0295, 0313; A5 (0080), A6 (0184), A12 (0089), A13 (0082), A16 (0086); option overlap in 0060, 0212, 0345 | vsphere/technology/network/configuration/splitrx-mode (or its file), vsphere/technology/network/configuration/network-configuration-review | - | - |
| W6 Storage and network new | B6, B7 (and the 0081 CSV), B8 (and the 0072 stem), B9, B10, B11 (and 0088 D-G), B15, B18; C13, C18-C24, C26, C33; D4, D6, D7 | vsphere/tools/vsphere-client/vcenter-statistics, vsphere/tools/esxtop/units-vs-vsphere-client | 0415-0444 | 950-979 |
| W7 System, VCF Operations, Guest OS | rewrites 0015, 0047, 0048, 0094, 0114, 0231, 0232, 0233, 0271, 0356; retire 0276, 0278; A10 (0085); A15 (0050: stale section, marks masked); stale sections and VM names masked in 0034, 0037, 0042, 0051; new B3, B4, B5; C7, C8, C25, C30, C32, C35; D3, D9 | sp5-framework/capacity/supply (or the file with the usable-capacity table), guest-os/system/troubleshooting/linux-os-slow | 0445-0469 | 980-999 |
- `pair` lines are set at the end from the writers' reports, so no writer edits another writer's file.
- Then: an independent review of every changed and new question (each option decided from the knowledge files before the key is read); fixes or author questions; lint, tests, retrieval check; project/plan.md; one pull request.
