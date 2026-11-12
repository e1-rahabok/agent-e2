# Questions for the author

Not indexed. One entry per question.

How to answer:

- Write your reply after `Answer:` under each question. Any length.
- Leave `Answer:` empty to skip a question for now.
- Then tell Claude the file is updated. Claude applies each answer to the knowledge base and moves the entry to Resolved.
- `Final answer:` (2026-11-12) is the answer proposed for your review. It replaces the drafts of 2026-11-10 and 2026-11-11 and the partly-settled notes: it is checked against the knowledge base as it is now, the decisions in project/plan.md and your answers up to Q179. Its status says how it was reached: settled (by an earlier answer or decision, named), expert call, or needs you. `For you:` names what only you can give; "nothing" means accept or change. In `Answer:`, write accept, accept with changes, or your own answer.

Each entry has:

- Section: book chapter and Heading 3.
- Files: knowledge-base files affected.
- Search: verbatim strings to find in the book.
- Written as now: what the knowledge base currently says.

## Open

### Q088 · Part 1 > Observability > Symptom | Alert | Insight · Thresholds in the prevention window image

- Files: [Alerts, symptoms and insights](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/alerts-and-insights.md) (section Prevention window); [VM CPU Co-stop](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/co-stop.md); [VM CPU Other Wait](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/other-wait.md); [ESXi storage latency stack: GAVG, KAVG, QAVG, DAVG](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/concepts/esxi-storage-latency-stack.md).
- Search 1: "In the following example, the alerts use the SLA metrics and threshold."
- Search 2: "Correct means the SLA is measured on each paying VM, and not at the infrastructure level."
- Image text (not searchable): "SLA: VM CPU Ready > 5%", "SLA: VM Disk Latency > 10 ms", "Cluster average CPU Ready.", "VM CPU Co-Stop > 2.5%", "VM CPU IO Wait > 1%", "ESXi VMkernel queue > 1 ms", "vMotion stun time > 0.2 second".
- Question:
  - (a) SLA VM CPU Ready above 5%: which is the threshold?
  - (b) Co-stop 2.5% as an insight threshold; the Co-stop file says below 1% in a high-performing environment. Is 2.5% right?
  - (c) VMkernel queue above 1 ms: QAVG or KAVG?
  - (d) Cluster average CPU Ready and memory contention as alerts: cluster worst VM, or provider-side alerts?
  - (e) VM CPU IO Wait: VM Other Wait (vCenter), or Guest OS IO wait?
- Written as now: the text dropped "SLA" ("Alert examples: VM CPU Ready and VM disk latency; cluster average CPU Ready; cluster average memory contention"). It still says "VM CPU IO wait" and "cluster average". The alt text still says "SLA VM CPU Ready, SLA VM disk latency" and the image metadata lists "VM CPU IO Wait". No image number is in the text or the catalog.
- Final answer (2026-11-12; (a) settled by the 2026-11-11 SLA decision and Q106; (e) by the other-wait file; vMotion by Q030; (b)-(d) expert call):
  - (a) Neither. Operations use no SLA (2026-11-11); an alert reads a KPI metric with its own values (Q106). The shipped VM alert rows: VM CPU Ready orange 4%, red 8%; VM disk latency orange 40 ms, red 80 ms (thresholds-alerts.yaml). The image's 5% and 10 ms are not used.
  - (b) Drop 2.5%. "Insight before alert" means earlier in time, not a lower number. The insight reads the KPI row VM Peak CPU Co-stop (20 s): yellow 1%, orange 2%, red 4%, which matches the Co-stop file. Comparing Co-stop with Ready says nothing: on a wide VM one vCPU in Ready co-stops its siblings, so Co-stop can exceed Ready.
  - (c) QAVG (vSphere Client: Queue command latency): the time a command waits in a full device or adapter queue inside the VMkernel. Block storage only; NFS has no QAVG. The earlier draft argued that KAVG contains QAVG; the latency stack file states QAVG can exceed KAVG (QAVG covers VM and kernel IO, KAVG VM IO only), so that argument is dropped. No catalog row: 1 ms has no five-number band yet (modelling, Setting thresholds).
  - (d) Provider-side alerts, read on the VM population, not an average: the infrastructure CPU alert fires when 25% of the cluster's VMs are above a per-VM value (cpu-alerts). An average hides the victim; the worst VM is the VM alert's job.
  - (e) VM CPU Other Wait, once labelled IO Wait (other-wait file). Not the Guest OS iowait. 1% is not kept: it would catch the accounting issue of Broadcom KB 85393.
  - vMotion stun time above 0.2 second matches your Q030 answer (cluster-performance, section vMotion): keep it as the insight example.
  - Change if accepted: alerts-and-insights, Prevention window: "VM CPU IO wait" → VM CPU Other Wait; "cluster average CPU Ready; cluster average memory contention" → share of the cluster's VMs above a per-VM value; alt text without "SLA" and with Other Wait; image metadata `VM CPU IO Wait` → `VM CPU Other Wait`; delete the review note. The image stays (Agent E2 reads the alt text).
  - For you: nothing.
- Answer:

### Q108 · Part 1 > Configuration Management > Resource Management, Share · Memory share unit and the share example

- Files: [Resource settings: when and how](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/configuration/resource-settings-guidance.md) (sections Review: how each control affects operations, Review: share values).
- Search 1: "10 per GB" (default VM memory shares table)
- Search 2: "per VM GB of RAM = 10240"
- Search 3: "Both VMs want to consume 10 GHz"
- Search 4: "In this case, VM 1 gets 5 GHz and VM 1 gets 5 GHz"
- Image text (not searchable): "A 2000 worth of reservation depends on the value of other VMs reservation" (VM Share row).
- Question: (a) memory shares per GB or per MB? (b) a 1-vCPU VM cannot consume 10 GHz on 2-3 GHz cores: change the example or keep it with the cap? (c) "VM 1" twice should read VM 2; the image says reservation where it means share. (d) a resource pool is 4x a VM for CPU and 16x for memory: is it a Normal pool weighing as much as a Normal 4-vCPU, 16 GB VM?
- Written as now: (a) per MB (5, 10, 20 per MB; 10,240 per GB at Normal). (b) "a 10 GHz host, a 1-vCPU VM (1,000 shares) and a 2-vCPU VM (2,000 shares) … 3.33 and 6.67 GHz, but a 1-vCPU VM cannot take more than one physical core's worth". (c) the text no longer names VM 1 twice; the alt text says share is relative to other VMs. (d) "A Normal resource pool weighs as much as a Normal VM with 4 vCPU and 16 GB."
- Final answer (2026-11-12; (a), (c) settled by the 2026-11-08 rule that a wrong fact is fixed in the file; (b), (d) expert call):
  - (a) Done: per MB. CPU 500, 1,000, 2,000 per vCPU.
  - (b) Replace the example. With 2.5 GHz cores, a 1-vCPU VM tops out near 2.5 GHz and a 2-vCPU VM near 5 GHz: 7.5 of 10 GHz, no contention, so shares never act, and the example shows a cap instead of shares. New example: 4 cores × 2.5 GHz, Hyper-Threading off. VM A 2 vCPU (2,000 shares), VM B 4 vCPU (4,000 shares); both demand all their vCPUs (15 GHz). Split 1:2: 3.33 and 6.67 GHz, 1.67 GHz per vCPU for both. Default shares give every vCPU the same runtime; only custom shares per class change that. When total demand is 10 GHz or less, each VM gets its demand.
  - (c) Done in the text and alt text. The image pixels still say reservation; the alt text is what Agent E2 reads.
  - (d) Agree, and add one line: 4,000 = 4 × 1,000; 163,840 = 10 × 16,384 MB. "4x and 16x" holds only against a 1-vCPU, 1 GB VM. One 8-vCPU, 32 GB sibling VM carries twice a Normal pool's shares, and the pool's weight is split among all its VMs: why pools and VMs are not siblings (Q110 c).
  - Sources: vSphere Web Services API, SharesInfo.Level; vSphere 9.1 documentation, Create a Resource Pool.
  - Change if accepted: resource-settings-guidance, Review: share values (new example; sibling line); delete the four Q108 review notes.
  - For you: nothing.
- Image for (c), asked 2026-11-12: [knowledge/vsphere/object-types/vm/images/vm-limit-reservation-share-impact-table.png](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/images/vm-limit-reservation-share-impact-table.png). It renders in resource-settings-guidance, section Review: how each control affects operations. VM Share row, second bullet: "A 2000 worth of reservation depends on the value of other VMs reservation". Both "reservation" words should read share. The alt text already says "relative to other VMs".
- Answer:

### Q109 · Part 1 > Configuration Management > Limit · Is there a network limit

- Files: [Resource settings: when and how](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/configuration/resource-settings-guidance.md) (section Limit); [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/noisy-neighbour.md) (section Network); [Network characteristics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/concepts/network-characteristics.md) (section Coarse allocation).
- Search: "There is no network limit"
- Question: with Network I/O Control each VM network adapter has share, reservation and limit, and port groups have traffic shaping. Change to: a network limit exists per vNIC but is not recommended?
- Written as now: resource-settings-guidance: "VM limits exist for CPU, memory and disk IOPS". noisy-neighbour: "Each VM network adapter has share, reservation and limit"; the 8 Gb/s limit and 100 Mb/s reservation withdrawn (Q083). network-characteristics: "NIOC and traffic shaping exist, but are not VM configuration properties."
- Final answer (2026-11-12; settled: Q083 for the advice, vSphere 9.1 documentation for the fact):
  - Yes. "There is no network limit" is wrong. Two controls exist:
    - Network I/O Control v3 on a distributed switch: each VM network adapter has shares (1-100), a reservation (Mbps) and a limit, set in the VM's network adapter settings. This is a VM configuration property, so the network-characteristics line is wrong for NIOC.
    - Traffic shaping per port group or port: average, peak, burst. A distributed switch shapes in and out; a standard switch outbound only. This one is a port group policy, not a VM property.
    - The lower of the two wins: a 200 Mbps adapter limit under a 100 Mbps shaping average gives 100 Mbps.
  - Advice (Q083): no limit or reservation on a VM, network included.
  - Two more reasons: a vNIC reservation is checked by the distributed switch, DRS and HA admission control (HA restarts a VM only on a host that meets its vNIC reservation); a limit is invisible to the Guest OS, as with CPU.
  - Edge cases: Network I/O Control is off when Network Offloads compatibility is on; SR-IOV is not available with Network I/O Control v3.
  - Text: "VM limits exist for CPU, memory, disk IOPS and network adapter bandwidth, plus traffic shaping per port group. Do not use them on VMs."
  - Sources: vSphere 9.1 documentation (What is vSphere Network I/O Control; Defining Bandwidth Requirements for a Virtual Machine; Traffic Shaping Policy; Factors Considered for Virtual Machine Restarts).
  - Change if accepted: resource-settings-guidance (Limit); network-characteristics (Coarse allocation: NIOC per vNIC is a VM property, shaping a port group policy); delete the review note.
  - For you: nothing.
- Answer:

### Q110 · Part 1 > Configuration Management > Reservation, Cluster, Resource Pool · Admission control, slot size and siblings

- Files: [Cluster configuration review: HA, DRS, DPM and cluster variants](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/configuration/cluster-configuration-review.md) (section HA); [Resource settings: when and how](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/configuration/resource-settings-guidance.md); [Admission control, expandable reservations and cluster state](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/admission-control-and-cluster-state.md); [Scalable Shares and resource pool siblings](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/resource-pool/configuration/scalable-shares.md).
- Search 1: "Reservation is respected only when Admission Control is enabled"
- Search 2: "this will impact the HA Slot Size"
- Search 3: "Resource Pool with VM as sibling is a common mistake"
- Question: (a) reservations are enforced at power-on whether or not HA admission control is on: reword to "with HA admission control off, reservations are not protected after a host failure"? (b) reservations change the slot size only under the slot policy: add that condition? (c) with Scalable Shares, is a pool with VMs as siblings still a mistake?
- Written as now:
  - (a) cluster-configuration-review: "Admission control disabled: failover capacity for the VMs' reservations is no longer kept." admission-control-and-cluster-state covers power-on and reservation or pool changes; it does not say host and DRS admission control cannot be turned off, nor what happens at restart.
  - (b) resource-settings-guidance: reservations "raise the HA slot size and narrow DRS placement", no policy condition. memory-tiering: do not use the slot policy on a tiered cluster.
  - (c) scalable-shares: "resource pools and VMs can be siblings … without the dilution problem"; misconception "Resource pools and VMs can always be siblings → only with Scalable Shares active". resource-settings-guidance: "a pool with VMs as siblings is a common mistake". Default (on or off) not stated.
- Final answer (2026-11-12; expert call from the vSphere 9.1 documentation):
  - (a) Keep the current line and add the mechanism. Host and DRS admission control check reservations at every power-on, reservation change and pool change, and cannot be turned off. HA admission control only keeps failover capacity. With it off, VMs power on into that capacity; after a host failure HA restarts a VM only where its CPU, memory and vNIC reservations plus overhead fit, so the reserved VMs are the first to stay down.
  - (b) Add the condition. Slot policy: the largest CPU and the largest memory reservation (plus overhead) set one slot size for every VM; one large reservation cuts the slot count (cap with das.slotcpuinmhz, das.slotmeminmb). Cluster resource percentage (the default): reservations are summed against the failover capacity; each costs only its own size. Tiered clusters: not the slot policy (memory-tiering, already written).
  - (c) Keep the rule "pools and VMs are not siblings" with Scalable Shares on or off; only the reason changes. Off (the default; set per cluster or per pool, inherited): a sibling VM dilutes the pool. On: a pool's shares are the sum of its VMs' shares × 4, 2 or 1 (High, Normal, Low), so dilution inside the pool is gone; but a Normal pool's VMs then weigh twice a sibling Normal VM, and that weight moves with every VM added to the pool. Recommend Scalable Shares on for clusters with pools, and no siblings.
  - The scalable-shares misconception reads siblings as fine once Scalable Shares is on; it is reworded to the reason above.
  - Sources: vSphere 9.1 documentation (Admission Control; vSphere HA Admission Control; Cluster Resources Percentage; Slot Size Calculation; DRS Scalable Shares); Performance Best Practices for VMware vSphere 9.1 (revision 20260624), p. 77.
  - Change if accepted: admission-control-and-cluster-state (host and DRS admission control always on; restart after a failure); resource-settings-guidance (Reservation: slot policy condition); scalable-shares (multiplier, default off, misconception); delete the Q110 review notes.
  - For you: nothing. Optional: whether your designs turn Scalable Shares on by default.
- Answer:

### Q111 · Part 1 > Configuration Management > Compute-related, ESXi · Cores or threads, and 48 or 64 cores

- Files: [VM configuration review](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/configuration/vm-configuration-review.md) (section Compute); [ESXi configuration review](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/esxi/configuration/esxi-configuration-review.md) (sections Memory, Capacity); [VM size](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/vm-size.md); [ESXi host specification from class of service and VM profile](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/host-spec-from-class-of-service.md). Related: Q079, Q099, Q100, Q125, Q176.
- Search 1: "do not count the logical processors"
- Search 2: "So a machine with 64 cores 128 threads get 512 GB of RAM"
- Search 3: "Aim for 48 to maximise software license"
- Question: (a) maximum VM size by physical cores or by logical CPUs? (b) host RAM per core or per thread? (c) 48 cores here, 64 in Price & SLA, both to maximize the licence: drop both?
- Written as now:
  - vm-size: technical maximum at 1:1 = ESXi physical threads − hypervisor overhead, ÷ 2 at 2:1, ÷ 3 at 3:1; size per class (Q176) counted in physical cores of one CCD or compute tile: Gold 2×, Silver 1×, Bronze 0.5×, 4 GB per vCPU. Its last section still says "the maximum VM size of a class follows from its ratio in the table above". class-of-service lists both: "CPU cap per class, by logical CPUs and the overcommit ratio" and "Size per class … Gold up to 2 CCDs".
  - vm-configuration-review: "count physical cores, not logical processors"; "Keep it within a socket"; "A VM above 8 vCPUs spans chiplets".
  - esxi-configuration-review: "64 cores with 128 threads maps to 512 GB (1 vCPU per thread)", with a pointer to host-spec. Licence reason removed from the body.
  - host-spec: 16-core licence minimum per CPU; "No core count above 16 per CPU has a licence advantage; keep Hyper-Threading on". 64 cores, 2.5 GHz: Gold 520 GB, Silver 839 GB, Bronze 660 GB.
- Final answer (2026-11-12; (a) settled by Q176; (b) by Q079, Q174 and the six-number model; (c) expert call):
  - (a) Two limits, both already in vm-size. The technical maximum counts threads (what ESXi can schedule). The class size counts physical cores of one CCD or compute tile (Q176: "Cores, not threads"). The class size binds far below the technical maximum, so no separate ceiling at the physical cores is needed. Two lines contradict this and change: vm-size, Size as a class of service fence ("follows from its ratio in the table above" → follows from Size per class); class-of-service, Size limit ("CPU cap per class by logical CPUs" → the technical ceiling; the class size is Size per class).
  - vm-configuration-review: "count physical cores" stays (it matches Q176). "Keep it within a socket" → within one NUMA node, and within one CCD or compute tile where the class allows (Q100, Q176). "A VM above 8 vCPUs spans chiplets" → Q125.
  - (b) Settled: per thread, 4 GB per vCPU, and the host RAM from the six-number model in host-spec (Gold 520 GB, Silver 839 GB, Bronze 660 GB on 64 cores). The 512 GB line in esxi-configuration-review ignores the hypervisor share and the class: replace it with the pointer to host-spec. The 768 GB host in class-of-service-planning and host-spec is the spreadsheet's example host, not a rule; it stays.
  - (c) Drop 48 and 64. The licence floor is written in host-spec. Above the floor the core count per host is decided by:
    - cost per sellable vCPU (hardware and licence);
    - failure domain: VMs lost per host failure, and the HA share of a cluster of few large hosts;
    - the class size against the host's CCDs or compute tiles (Q176);
    - per-core application licences (Windows Server Datacenter, SQL Server, Oracle): a dedicated cluster with fewer, faster cores.
  - Change if accepted: vm-size (fence section line); class-of-service (Size limit wording); vm-configuration-review (Compute); esxi-configuration-review (Memory: pointer only; Capacity: the four reasons); delete the Q111 review notes in vm-size, esxi-configuration-review and vm-configuration-review.
  - For you: nothing.
- Answer:

### Q124 · Part 1 > Reclamation > TRIM and Unmap · Per datastore

- Files: [ESXi Datastore metrics (host view)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/host/datastore.md) (section Unmap); [esxtop storage counters](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/tools/esxtop/storage.md).
- Search: "but you can’t aggregate them per datastore"
- Question: the knowledge base reads this as: the metrics are on the ESXi host with one instance per datastore, and no datastore-wide total across hosts exists. Correct?
- Written as now: "Two metrics on the ESXi host, one instance per datastore"; "Per host and datastore only: a datastore total across hosts is not available. Sum the hosts that mount it." Counter keys only in a review note ("likely datastore.unmapIOs and datastore.unmapSize"). esxtop storage lists the VAAI unmap fields (DELETE, DELETE_F, MBDEL/s), not linked from the Unmap section.
- Final answer (2026-11-12; expert call; one live check):
  - Correct, with four precisions.
  - Keys: vCenter `datastore.unmapIOs.summation` (count) and `datastore.unmapSize.summation` (MB), per host, one instance per datastore. They are not in the 9.1 API counter pages or the chart tables. ESXi keeps the same counts per volume (vsish) and per device (esxtop VAAI: DELETE, DELETE_F); both reset at reboot.
  - Total: the datastore object has no unmap counter. Sum the hosts that mount it, same interval. The sum is complete: each unmap command comes from exactly one host. The space reclamation hosts setting limits how many hosts send automatic unmap, so most hosts read 0.
  - Units: one value per 20 seconds. VCF Operations averages the 15 values of a 5-minute point: MB released in 5 minutes = value × 15; MB/s = value / 20.
  - Scope: VMFS6, and NFS through the VAAI unmap primitive.
  - Sources: vSphere 9.1 documentation (Space Reclamation); https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/datastore_counters.html (no unmap counter); Broadcom KB 374191.
  - Change if accepted: host datastore, Unmap (keys, conversions, reclamation hosts, link to the esxtop fields); close the plan item on the unmap keys (M1, VCF Operations line).
  - For you: in a live VCF Operations 9.1, confirm the Datastore object has no unmap metric, and give the Host System metric keys.
- Answer:

### Q125 · Part 1 > Rightsizing > Best Practices · 8-core block, 8 and 16 vCPU

- Files: [Rightsizing VMs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/rightsizing.md) (section Practices); [Cluster Risk (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md) (section Monster VM); [VM configuration review](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/configuration/vm-configuration-review.md) (section Compute); [VM size](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/vm-size.md); [Terminology](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md) (CCD). Related: Q111, Q176.
- Search: "AMD EPYC and Intel Xeon use an 8-core block"
- Question: (a) limit the 8-core block to AMD? (b) why does a VM above 8 vCPU risk the Hyper-Threading effect? (c) is above 16 vCPU about the CCD (L3) effect inside a socket, not NUMA?
- Written as now:
  - rightsizing: "a VM above 8 vCPU risks the Hyper-Threading effect; above 16 vCPU risks the NUMA effect. Both depend on the host CPU".
  - cluster-risk, Monster VM: "most Xeon and EPYC use 8-core CCDs; a 16-vCPU threshold would flag too many VMs".
  - vm-configuration-review: "a 64-core CPU of 8 chiplets of 8 cores … A VM above 8 vCPUs spans chiplets"; misconception "16 vCPUs span two 8-core chiplets".
  - vm-size (Q176): class size counted in physical cores of one AMD CCD or Intel compute tile; the unit is the L3 cache domain (on Zen 4c the 8-core CCX); "Aim to run within the physical CPU package (AMD EPYC CCD or Intel Xeon Compute Tile) to avoid NUMA".
  - numa-settings: defaults are NPS-1 with CCX as NUMA Domain off. Glossary CCD: "A group of cores sharing one L3 cache inside an AMD socket".
- Final answer (2026-11-12; (a), (c) settled by Q176; (b) expert call):
  - (a) Settled: there is no fixed 8-core block. The unit is the host's CPU building block (Q176): an AMD L3 domain (the CCD; the CCX on Zen 4c) or an Intel compute tile. Two precisions for vm-size:
    - Zen 5c: one 16-core CCX per CCD, so the CCD is the unit again.
    - Intel: a compute tile is its own L3 domain and NUMA node only with sub-NUMA clustering (SNC) on. With SNC off the socket shares one L3 and one NUMA node, so the tile is a softer boundary than an AMD CCD. To check against the Intel Xeon 6 documentation before it is written.
  - (b) Remove the 8-vCPU Hyper-Threading rule. VM size against a CCD does not cause the Hyper-Threading effect. A vCPU pays it when its sibling thread is busy: under host load, or when the VM has more vCPUs than its NUMA node has cores (numa.vcpu.preferHT). vm-size already states the mechanism ("a vCPU on a busy sibling thread pays the Hyper-Threading penalty"). Above the L3 domain a VM pays a cache cost instead.
  - (c) Settled: the 16-vCPU NUMA rule goes. With the default BIOS (NPS-1, CCX as NUMA off) an AMD NUMA node is the whole socket, up to 128 cores (Zen 5) or 192 (Zen 5c). Rule: above the L3 domain → cache cost; above the cores of the NUMA node → remote memory. Both are read from the host, not fixed at 8 and 16. vm-size "to avoid NUMA" → "to stay within one L3 domain and one NUMA node": at default the CCD is an L3 boundary, not a NUMA boundary.
  - Sources: Performance Best Practices for VMware vSphere 9.1 (revision 20260624), BIOS and NUMA sections, preferHT; vSphere 9.1 documentation (llc.multiLLCPerSocket, llc.size.vcpu); AMD EPYC 9005 Architecture Overview (doc 58462).
  - Change if accepted: rightsizing (Practices: the two host-derived limits, link vm-size); vm-configuration-review (Compute and its misconception); cluster-risk (Monster VM: CCDs hold 8 to 32 cores by generation, Xeon has none); vm-size (Zen 5c, Intel SNC, "to avoid NUMA"); glossary CCD (on Zen 4c a CCD holds two CCX, each its own L3); delete the Q125 review notes in the four files.
  - For you: nothing, unless the 8-vCPU rule came from a test you ran: then its setup.
- Answer:

### Q128 · Glossary · Proposed terms from Capacity Management

- Files: [Terminology](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md) (section Capacity); [Demand](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/demand.md).
- Search: "Stop Provisioning (Yes/No)"
- Question: three glossary proposals: (a) "Closed cluster" (also called stop provisioning); (b) pair "Demand (capacity) vs ESXi CPU Demand"; (c) pair "Idle vs oversized vs unused VM". Keep, rename or drop?
- Written as now: glossary entry **Closed cluster** ("A cluster that accepts no new VM and no VM upsize, decided from Cluster Consumption (%), Cluster Performance (%) and Cluster Risk (%)"; Also called: Stop provisioning; File: can-cluster-take-more-vms). Entry **Demand (capacity)** with "Not to confuse with ESXi CPU Demand". (c) removed by your glossary edit of 2026-11-11. demand.md still says "Stop Provisioning (yes or no): … decided from Performance (%), Capacity Remaining (%) and Risk (%)".
- Final answer (2026-11-12; (c) settled by your edit; (a), (b) expert call):
  - (a) Rename the entry to **Close for Business**: 1 = closed (no new VM, no VM upsize), 0 = open, decided from Cluster Consumption, Cluster Performance and Cluster Risk. Also called: Closed cluster, Stop provisioning. File: close-for-business, then can-cluster-take-more-vms. Reason: one word per concept, and the pack metric (`vCommunity|Periodic Cluster Check|Close for Business`), the file title and the plan already use it.
  - Fix demand.md: Cluster Consumption replaced Capacity Remaining in the closure (Q121).
  - (b) Keep, and widen Not to confuse with to CPU Demand (VM and ESXi): VM CPU Demand is the same confusion. A third use exists: VCF Operations names a capacity setting Capacity Buffer (Demand) (cluster-consumption).
  - (c) Settled: you removed the pair. Nothing to do.
  - Change if accepted: glossary (Close for Business entry; Demand entry); demand.md (Stop Provisioning line).
  - For you: nothing.
- Answer:

### Q129 · VCF Operations 9.1 · Prometheus access for scripts

- Files: [Real-time metrics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/features/real-time-metrics.md).
- Search: not from the book. TechDocs "Real-time Data in the Workbench": "Use the Add Query input field to enter and run your PromQL query."
- Question: you say 2-second metrics are for programmatic use, with native Prometheus compatibility. The 9.1 docs show PromQL only in the Workbench Custom Query sub-tab. How do scripts reach it (endpoint, auth, doc link)?
- Written as now: "Designed for programmatic consumption: data is queried with PromQL"; "Custom Query: PromQL". No API section; sources are TechDocs pages only.
- Final answer (2026-11-12; settled by vendor documentation; one live check):
  - The statement holds. Broadcom publishes Real-Time Metrics APIs for VCF 9.1 and 9.1.1: Prometheus-compatible APIs for real-time metrics from vCenter (https://developer.broadcom.com/xapis/realtime-metrics-api/latest/). Usable as a Grafana data source, down to 2-second granularity.
  - Endpoints: GET `/api/v1/query`; GET `/api/v1/query_range` (start, end, step); GET `/api/v1/metadata`; PUT `/api/v1/vcenters/{vcId}/metrics_config` (STANDARD or VERBOSE profile; the ESXi hosts for esxtop collection). Responses in Prometheus format.
  - Not stock Prometheus: `sourceId` (vCenter instance UUID, NSX id) is required; `externalTagsFilter` is optional.
  - Auth: POST `/suite-api/api/auth/token/acquire` → OpsToken; read the integration services list and take the service of type VCF_VODAP; POST `/suite-api/api/auth/token/exchange` → JWT, sent as Bearer.
  - Change if accepted: real-time-metrics, new section API for scripts (endpoints, sourceId, auth, URL); delete the review note; keep the corrections entry (the Workbench page still omits the API).
  - For you: one call in your lab: which host answers `{api_host}` (the VCF Operations FQDN or the real-time metrics component), and whether the esxtop feature returns 2-second data through the API.
- Answer:

### Q130 · Benchmark · Retrieval check: what number is good enough to release

- Files: [benchmark/retrieval-check.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/retrieval-check.md) (section What is a good number); [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md) (M3 exit criteria).
- Search: not from the book.
- Question: (a) the release levels for classic mode; (b) should each question mark its main file, so the check reports main-file misses separately?
- Written as now: retrieval-check.md gives the proposal in counts of 90 questions ("bad. 53-57 of 90 complete"), marked as not agreed (Q130). Plan M3: "every needed file in the context for at least 90% of questions and context recall at least 95% (proposal, Q130)". Latest numbers (2026-11-11): search recall 60%, classic context recall 78%, 61 of 95 complete (64%). No question has a main-file key.
- Final answer (2026-11-12; expert call):
  - (a) Levels in percent, since the question count moves from 95 to 100. Classic mode, the shipped search mode; BM25 and hybrid both reported.
    - Release gate: the main file in context for 100% of the visible questions (each miss is a defect, fixed or explained); context recall at least 95%; complete questions at least 90%.
    - Target: 97% complete, 98% recall.
    - Held-out or sealed set (Q165) within 5 points of the visible set; a larger gap means retrieval is fitted to the visible questions.
  - Reasons: 0.90 × 0.95 ≈ 0.85 ties the gate to the release score. "Complete" punishes multi-file questions hardest. A missing main file drives confident-wrong answers, so it gets its own number.
  - (b) Yes, an explicit key, `knowledge_main` (also listed in `knowledge`; lint checks it). Not the list order: on 2026-11-10, 10 questions missed their first-listed file, but first was never written to mean main. The retrieval check reports main-file misses as a fourth number.
  - Change if accepted: retrieval-check.md (levels in percent, today's numbers); plan M3 exit criteria; question template; retrieval_eval.py; lint; project/terms.md (`knowledge_main` as a proposal).
  - For you: the main file of each question, during the one-go question review.
- Answer:

### Q131 · VCF-vCommunity-Adapter · KPI is performance only: names in the adapter documentation

- Files: [Cluster Risk (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md), [Cluster Consumption (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-consumption.md), [Close for Business](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/close-for-business.md); [Terminology](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md).
- Search: adapter docs/reference/metrics/README.md: "KPIs: Cluster Performance, Cluster Risk, Cluster Consumption, ESXi Performance, VM Performance, Guest OS Performance"; periodic-cluster-check.md: "the three cluster KPIs".
- Question: KPI is strictly performance; capacity and risk are models (2026-11-08). (a) The adapter documentation still lists Cluster Risk and Cluster Consumption as KPIs: rename them there, or keep a synonym in the knowledge base? (b) Where does Cluster SLA and SLI go?
- Written as now: both models in `vsphere/object-types/cluster/models/`. Glossary: Cluster Risk (%) entry without an Also called line; no Cluster Consumption entry; the Model entry says "Cluster Risk is a model, not a KPI". cluster-risk Purpose: "The only score of the pack read this way" (higher is worse), while cluster-consumption says "The same direction as Cluster Risk (%)"; cluster-risk also says "the ones driving the KPI".
- Final answer (2026-11-12; (a) settled for the knowledge base by the 2026-11-08 decision; (b) settled 2026-11-11):
  - (a) Both. In the knowledge base now: Also called "Cluster Risk KPI" on the Cluster Risk (%) entry; a new entry Cluster Consumption (%), Also called "Cluster Consumption KPI", "a model, not a KPI". Users read the pack pages and will keep saying KPI. In the adapter: rename the pages with the other pack fixes after 1.0 (Q151, Q179).
  - Fix cluster-risk: Cluster Consumption is higher-is-worse too, so "the only score of the pack read this way" goes; "driving the KPI" → "driving the score".
  - (b) Settled: no SLA or SLI in operations (2026-11-11); cluster-sla-sli is archived and its old ids point to Cluster Performance. Nothing to move.
  - Change if accepted: glossary (two Also called lines, one new entry); cluster-risk (Purpose, one line); plan After 1.0 (adapter page names with the pack fixes); delete the Q131 review notes in cluster-consumption and close-for-business.
  - For you: whether the adapter pages are renamed with the after-1.0 pack fixes.
- Answer:

### Q132 · VCF-vCommunity-Adapter vs Part 1 > Cluster Closure · Which closure thresholds does Agent E2 apply

- Files: [Close for Business](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/close-for-business.md); [Can this cluster take more VMs?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms.md) (steps 5 and 6); [thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml) (rows closure-*). Related: Q121, Q122.
- Search: book table after "Implementing the above with actual threshold"; adapter periodic-cluster-check.md, section The rule.
- Question: (a) when a user asks "is this cluster closed", which set applies? (b) is the pack the current version of your table?
- Written as now: two band sets live side by side.
  - close-for-business (the pack): band edges 25, 50, 75 on each score; Performance read at the 5th percentile, Consumption and Risk at the 95th; Risk orange closes every cluster.
  - can-cluster-take-more-vms steps 5-6 and the 6 catalog rows (your Q121 table): Consumption red above 80, orange above 60; Performance red below 20, orange below 40; Risk production above 60, non-production above 80; all at the 95th percentile of 24 hours.
  - close-for-business misconception still quotes the retired book table (Performance 40 and 20, Risk 50 and 75). The decision-tree chart is fixed (no Capacity Remaining); its review notes use old step numbers.
- Final answer (2026-11-12; expert call, needs your choice):
  - (a) Agent E2 reads the pack's published Close for Business when present: 1.0 reads published scores (2026-11-10). It reports the rule that fired and the worst-end value of each score.
  - (b) One band set, and the recommendation is the score colours: 25, 50, 75.
    - Reason: Consumption, Performance and Risk are scores whose colours are fixed by the scoring model (green 100-75, yellow 75-50, orange 50-25, red 25-0; mirrored for the higher-is-worse scores). The Q121 edges cut across the colours the user sees: Consumption 78 shows red and is orange under Q121; Performance 22 shows red and is orange under Q121. A closure rule that disagrees with the colour of its own input must be explained every time.
    - Keep from Q121 what the colours do not fix: the Risk split by environment (production closes at Risk orange, non-production at Risk red). The pack applies orange to every cluster: a pack change after 1.0, like Q151.
    - If you keep the Q121 edges instead: the pack changes to them after 1.0, and close-for-business states the difference until then.
  - Either way:
    - Performance is higher-is-better, so its worst end is the 5th percentile, not the 95th: step 5 and the two Performance rows change.
    - The close-for-business misconception quoting the retired book table is replaced.
    - The decision-tree review notes move to the new step numbers (Risk is step 6).
  - Change if accepted: can-cluster-take-more-vms (steps 5-6, image alt text, review notes); the 6 closure-* rows; close-for-business (misconception, review note); plan After 1.0 (pack: Risk split by environment). With the score colours, your closure table image is replaced.
  - For you: which set wins (score colours 25/50/75, or Q121 20/40/60/80); whether the pack gets the non-production Risk split.
- Answer:

### Q134 · Part 3 > Metric Mastery > Triple See Method · Why not USE, RED, Golden Signals

- Files: [Triple See Method](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/observability/triple-see-method.md) (section Why not USE, RED or Golden Signals); [Terminology](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md) (Triple See Method).
- Search: "Based on their strengths and weaknesses, I came up with The Triple See Method"
- Question: the book does not say what each method lacks. The knowledge base says: USE starts from utilization, which does not show who waits in an overcommitted cluster; RED and the Golden Signals are request-centric and a VM has no request to time; none has a context type; none maps metric types to pillars. Correct, and anything to add?
- Written as now: the section as above, unchanged. Misconceptions: "Apply the USE Method: high utilization means a problem"; "Monitor the four Golden Signals on the VMs". The file opens "Designed for Broadcom VCF by Iwan 'e1' Rahabok, after studying the USE Method …". The glossary entry says "Not based on the USE, RED or Golden Signals", against the file's "after studying".
- Final answer (2026-11-12; expert call: two corrections, three additions):
  - Correction 1: USE has a wait type: saturation is queue length, and USE is applied to hypervisor limits in the cloud. The real gaps: USE reads saturation per resource inside one OS; inside the Guest OS it cannot see Ready (the vCPU's frozen time is invisible to the guest run queue); at ESXi, saturation averages the VMs and hides the victim. Contention per consumer is what USE lacks.
  - Correction 2: "a VM has no request to time" is wrong for storage. The virtual disk is request-shaped (IOPS, latency, aborted commands), and RED fits it. CPU and memory are time-shared: Ready and memory contention are shares of time, with no request.
  - Add: RED and the Golden Signals belong to the application layer (realms-and-layers); there they are right, and Triple See does not replace them.
  - Add: none of the three has allocation or reservation as kinds of consumption, by which overcommitted capacity is managed.
  - Add: the Golden Signals do separate symptom from cause (Google SRE book, Monitoring Distributed Systems, "Symptoms Versus Causes"), the same idea as primary vs secondary metrics. Do not claim otherwise.
  - Keep "no context type", and "no pillar mapping" as scope, not a flaw.
  - Glossary: "Not based on" → built after studying their strengths and weaknesses.
  - The author's name in the file's first line is a who-said-it tag (repository rule): drop it; `source.document` cites the book.
  - Sources: brendangregg.com/usemethod.html; sre.google/sre-book/monitoring-distributed-systems/; grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/.
  - Change if accepted: triple-see-method (section, first line, new misconception "apply USE inside the Guest OS"); glossary entry; delete the review note.
  - For you: nothing.
- Answer:

### Q135 · Why a New Framework? > Complexity · ITIL 4 or ITIL 5

- Files: [Why SP5 and not ITIL](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/why-a-new-framework.md) (section Complexity).
- Search: "ITIL 5 has 34 management practices"
- Question: the 34 practices are ITIL 4 (the linked list is ITIL 4). Is "ITIL 5" a typo, or does ITIL 5 keep the same 34?
- Written as now: "ITIL 4 has 34 management practices: 17 service management, 3 technical management, 14 general management." "ITIL merges capacity and performance into one practice."
- Final answer (2026-11-12; expert call, from PeopleCert):
  - Not a typo any more: ITIL (Version 5) exists. Foundation exam since February 2026; PeopleCert plans to retire the ITIL 4 modules on 31 December 2027.
  - It keeps 34 practices: "For ITIL (Version 5), the 34 ITIL management practices will remain largely the same" (https://www.peoplecert.org/help-and-support/faq-itil).
  - The grouping changed: ITIL 4 had service (17), technical (3), general (14); ITIL (Version 5) has product and service management, and general management (22 and 12 per a secondary source; the full list is for PeopleCert Plus members).
  - Capacity and performance management is still one practice, so the Complexity point stands.
  - Text: "ITIL (Version 5), like ITIL 4, has 34 management practices, in two groups: product and service management, general management." Drop the 17/3/14 split or label it ITIL 4.
  - Change if accepted: why-a-new-framework (Complexity; PeopleCert source); delete the review note.
  - For you: nothing.
- Answer:

### Q136 · Part 3 > Modelling > Calculation · KPI colours and a timeline

- Files: [Modelling a pillar into one number](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/modelling.md) (sections Setting thresholds, Misconceptions); [Alerts, symptoms and insights](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/alerts-and-insights.md).
- Search: "The threshold maps to a timeline."
- Question: the book maps KPI colours to a timeline (red within a few hours, orange today, yellow tomorrow). Your Q089 answer: alert colours have a timeline, KPI colours do not. Remove the timeline from Modelling?
- Written as now: modelling, Setting thresholds: "Red is not an emergency: look within hours." Misconception: "Red means drop everything" → look within hours. alerts-and-insights: "an alert colour is a deadline … A KPI colour band is proactive and carries no deadline", and the same misconception "Red means drop everything" → red is attended within 1-2 hours. One misconception, two answers.
- Final answer (2026-11-12; settled by Q089):
  - Remove the timeline. An alert colour carries a deadline because time has started (red within 1-2 hours, orange by the end of the day); a KPI or model colour is proactive and carries none.
  - Setting thresholds: replace the bullet with "A KPI or model colour says how bad, not by when. The daily health check reads red first, then orange, then how often a value enters red and its trend."
  - Misconceptions: replace "Red means drop everything → look within hours" with "KPI red: act within hours" → a KPI colour has no deadline; the alert carries it. "Red means drop everything" stays only in alerts-and-insights, where it is about alerts.
  - The same holds for the models (Cluster Consumption, Cluster Risk).
  - Change if accepted: modelling (Setting thresholds, Misconceptions); delete the review note.
  - For you: nothing.
- Answer:

### Q137 · Metric Mastery > Aggregation > The Problem with Average · ESXi CPU Ready (%)

- Files: [Aggregation](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/observability/aggregation.md) (section Divide summed counters correctly).
- Search: "ESXi CPU Ready (%) = ESXi CPU Ready (ms) / Sum (vCPU of running VMs)"
- Question: the formula divides milliseconds by a vCPU count, which gives ms per vCPU, not %. Correct to ESXi CPU Ready (ms) / (20,000 ms × vCPUs of running VMs)?
- Written as now: "ESXi CPU Ready (%) = ESXi CPU Ready (ms) / (20,000 ms × vCPUs of running VMs)"; example 149,116 ms, 67 VMs, 195 vCPUs, no result given; "Divide by running vCPUs, not by physical cores."
- Final answer (2026-11-12; expert call; Broadcom KB 306576 confirms):
  - Yes. The denominator needs the sample length.
  - General form: ESXi CPU Ready (%) = ESXi CPU Ready (ms) / (sample length in ms × vCPUs of running VMs) × 100.
  - Sample length: vCenter real time 20,000 ms; VCF Operations 20,000 ms, also for its 5-minute points (it averages the 15 20-second values); vCenter rollups are sums: 300,000 (past day), 1,800,000 (past week), 7,200,000 (past month), 86,400,000 (past year).
  - Divide by vCPUs, not cores or threads: Ready is a state of each vCPU, and each vCPU's states add up to the sample length.
  - Example result: 149,116 / (20,000 × 195) × 100 = 3.8%.
  - Limits: a VM powered on or moved in during the sample counts only part of it. The result is an average that hides the worst VM; read ESXi Performance (%) (worst VM and 90th percentile).
  - Sources: https://knowledge.broadcom.com/external/article/306576; https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/cpu_counters.html
  - Change if accepted: aggregation (general formula, sample lengths, example result); delete the review note (it cites the old section name Summed counters).
  - For you: nothing.
- Answer:

### Q139 · Part 2 > Proactive Operations > Business Applications > vSphere Folder Structure · Diagram label

- Files: [Business applications in VCF Operations](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/dashboards/business-applications.md) (section vSphere folder structure, image).
- Search: "This is why I only have 2 levels of organisation in the above"
- Question: in the folder diagram, the third application under Department 2 is labelled C.3: Application C. Should it be C.2: Application C?
- Written as now: the image still shows C.3; the alt text says Department 2 owns Applications A, B and C.
- Final answer (2026-11-12; expert call): C.2: Application C.
  - Every label starts with the business unit letter and the department number ("C.2: Application A", "C.2.B: Web Tier"). C.3 would sit under Department 3; its arrow comes from Department 2.
  - Agent E2 reads the alt text, which is already right.
  - Change if accepted: business-applications, delete the review note; relabel the image when convenient.
  - For you: nothing.
- Answer:

### Q140 · Part 2 > Proactive Operations > Alert > Threshold Design · Red vs orange scale

- Files: [Alert design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/alert-design.md) (sections Threshold design, What not to alert); [Alert definitions in VCF Operations](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/alerts/alert-definitions.md).
- Search 1: "For example, Red is always 4x of orange. You can make red 2x as bad by modifying any 2 of the following"
- Search 2: "going up from the usual 0.2s to 0.6x second"
- Question: (a) is red 4x orange (two factors doubled) or 2x orange (one factor doubled)? (b) 0.2 s to 0.6 s is 3x as long; the text says 300% longer. Which is right?
- Written as now: alert-design: "Set the acute threshold at 4x the sustained one"; three ways to make red worse than orange (2x threshold, 2x population, 2x time); "3x as long over 12 hours (0.2 s to 0.6 s)". No "4x orange" and no "300%". alert-definitions: "a 20-second peak above 4x the 5-minute threshold".
- Final answer (2026-11-12; expert call; the 4x part settled by Q152):
  - (a) Red = 2x orange, on every threshold of a set (thresholds-alerts.yaml, peak / average):
    - infrastructure CPU: orange 12% / 3%, red 24% / 6%;
    - VM memory: orange 12% / 3%, red 24% / 6%;
    - infrastructure memory: orange 8% / 2%, red 16% / 4%;
    - VM disk: orange 160 / 40 ms, red 320 / 80 ms.
  - Exception: VM CPU orange keeps the red peak and contention (Q144). VM network has red only.
  - Doubling peak and average together is one factor: an episode twice as bad crosses both. "Red is always 4x of orange" reads as the peak-to-average guide (about 4x inside one colour) put in the wrong place.
  - 4x inside a colour is a guide for choosing the 20-second value, never a formula (Q152). alert-design ("Set the acute threshold at 4x the sustained one") and alert-definitions ("above 4x the 5-minute threshold") state it as a rule: reword both to a guide.
  - (b) Done: 3x as long, 0.2 s to 0.6 s (200% longer). "0.6x second" means 0.6 second.
  - Change if accepted: alert-design, Threshold design: "In the recommended set red is 2x orange on every threshold. Inside one colour the 20-second peak is set near 4x the 5-minute value: a guide, not a formula." alert-definitions, one line. Delete both review notes.
  - For you: nothing.
- Answer:

### Q141 · Part 2 > Proactive Operations > Alert > Class of Service: The What · Class names

- Files: [Alert design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/alert-design.md) (sections Class of service, What to alert); [Class of service](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/class-of-service.md); [Terminology](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md) (Class of service, Crown jewels).
- Search: "Mission Critical: VM Disk Latency > 30 ms for 5 minutes."
- Question: Part 2 names the classes mission critical, standard production, test and development; Part 1 names them Gold, Silver, Bronze. Map them one to one? Are 30, 60, 120 ms per class the same idea as a performance SLA per class?
- Written as now: alert-design: "Use 3 classes: mission critical, standard production, test and development", example 30 ms / 5 min, 60 ms / 10 min, 120 ms / 10 min; "Align with the KPI levels, the internal baseline." class-of-service: "Gold: … mission-critical applications"; "Silver: most production workloads. Bronze: test and development." Glossary: Class of service (Also called: Tier); "Mission-critical applications" is an Also called of Crown jewels. The two SLA lines were fixed on 2026-11-11.
- Final answer (2026-11-12; settled by class-of-service, Q089, Q106, the 2026-11-10 and 2026-11-11 decisions):
  - Mapping: Gold = mission critical, Silver = standard production, Bronze = test and development. Write Gold, Silver, Bronze in alert-design.
  - Glossary: add "standard production" (Silver) and "test and development" (Bronze) to the Also called line of Class of service. Do not make "mission critical" a name of Gold: it is already a name of Crown jewels, which always run in Gold (2026-11-09) but are not all of Gold.
  - 30/60/120 ms: an alert threshold per class is allowed, because an alert colour is urgency plus importance (Q089). The KPI has no class (2026-11-10), and there is no performance SLA (2026-11-11). An alert scores nothing, so the KPI objection does not apply.
  - alert-design "Align with the KPI levels, the internal baseline" contradicts "KPI and alert are independent" (2026-11-10): reword to "Alerts read KPI metrics with their own values; KPI levels and alert values are set apart."
  - Change if accepted: alert-design (class names; the KPI line); glossary (Class of service, Also called); delete the review note.
  - For you: nothing.
- Answer:

### Q142 · Part 2 > Proactive Operations > Alert > Design · Alert count table vs the alert sections

- Files: [Alert design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/alert-design.md) (section Design the alerts as a set); [Guest OS alerts](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/configuration/guest-os-alerts.md); [Storage alerts](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/configuration/storage-alerts.md).
- Search 1: "Not yet = I’ve not implemented it yet."
- Search 2: "There is no alert defined, as it could result in false positive."
- Search 3: "Not yet implemented. The reason is the many:many relationship"
- Question: the count table shows (a) Guest OS disk consumption 1, but the Guest OS section says no alert; (b) datastore cluster disk contention 2, but the storage section says not implemented. Which is current?
- Written as now: count table: Guest OS disk consumption 1; disk contention datastore 0, datastore cluster 2. guest-os-alerts, Consumption: daily checks, no alert: "Low disk space: not implemented". storage-alerts, Datastore latency: "Not implemented. VMs and datastores are many-to-many". The catalog has no Guest OS disk-space row and no datastore latency row.
- Final answer (2026-11-12; expert call, one item needs you):
  - Rule: where a table cell and a section disagree, the section that gives a reason wins. The table summarises the sections.
  - (a) No Guest OS disk consumption alert: swap partitions sit near 100%, and low disk space cannot be read at the virtual disk layer. Cell → Not yet.
  - (b) No datastore latency alert: VMs and datastores are many-to-many, and a datastore cluster is the same (a VM's disks can sit on several). Cells datastore and datastore cluster → Not yet. The datastore cluster consumption alert (above 90% used) is a different row and stays.
  - Change if accepted: alert-design, three table cells; delete the Q142 review notes in alert-design, guest-os-alerts and storage-alerts.
  - For you: whether your shipped set has a Guest OS disk-space alert or datastore cluster latency alerts. If yes, the sections change instead.
- Answer:

### Q143 · Part 2 > Proactive Operations > Alert > Threshold Design > Conditions · Condition vs symptom

- Files: [Alert definitions in VCF Operations](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/alerts/alert-definitions.md) (section Symptom and condition: one test, two names); [project/design-thresholds.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/design-thresholds.md) (section 9).
- Search: "Do not use Symptoms. Instead, use Conditions."
- Question: is a condition a test written inside the alert definition, as opposed to a reusable symptom definition? Is the reason only that symptoms are reserved for minor issues, or also a technical one?
- Written as now: rewritten after Q154: "A symptom and a condition are the same thing"; "A symptom definition is stored on its own and reused … A condition is written inside one alert definition"; "A symptom that triggers without its alert is a minor issue". The book's advice (use conditions, not symptoms) is no longer stated; cycles and the isolation reason are not written. design-thresholds section 9 (a proposal waiting for approval) puts wait and cancel cycles on symptoms only.
- Final answer (2026-11-12; settled by Q154 for the definition; expert call for the rest):
  - Yes: a condition is a test inside one alert definition; a symptom definition is stored and reused. One test, two names (Q154).
  - Not a technical limit on cycles: a condition has its own wait cycle, cancel cycle and severity, like a symptom definition (VCF Operations API 9.1.1, data structure alert-condition: waitCycles, cancelCycles, severity; https://developer.broadcom.com/xapis/vcf-operations-api/9.1.1/data-structures/alert-condition/).
  - Two reasons hold: meaning (a symptom triggered alone is a minor issue for the daily health check; an alert's own tests are not); isolation (editing a shared symptom definition changes every alert that uses it, vendor alerts included; editing a condition changes one alert).
  - Put the advice back as one line with both reasons: "Write an alert's tests as conditions, not as shared symptom definitions."
  - design-thresholds section 9: "symptom" → "symptom or condition" in each line about wait and cancel cycles (R1 and the lines above it).
  - Change if accepted: alert-definitions (advice line; cycles line); design-thresholds section 9; delete the review note (it cites the old section name).
  - For you: nothing.
- Answer:

### Q144 · Part 2 > Proactive Operations > Alert > CPU Alerts > VM Contention · Orange values and the missing diagram

- Files: [CPU alerts](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/configuration/cpu-alerts.md) (sections VM CPU contention, Infrastructure CPU contention); [VM CPU contention is high](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/troubleshooting/vm-cpu-contention-high.md).
- Search 1: "Peak vCPU Ready > 32%"
- Search 2: "This is complex. See the diagram at the start of CPU Alert section."
- Question: (a) orange keeps Peak vCPU Ready above 32% and CPU Contention above 8%, the same as red; only CPU Ready drops to 4%. Should orange be 16% and 4%? (b) the diagram at the start of CPU Alerts is not in the document: link vm-cpu-contention-high instead?
- Written as now:
  - cpu-alerts and catalog row `alert-vm-cpu-ready-orange`: orange CPU Ready above 4% with Peak vCPU Ready above 32%, CPU Contention above 8%, CPU Usage above 1 GHz (the red conditions). cpu-alerts: the VM owner gets an alert "at a higher CPU Ready than the infrastructure team (8% against 6%)", while the infrastructure alert's 6% is CPU Contention.
  - vm-cpu-contention-high: Mermaid chart present (2026-11-11). Step 1 still stops when Contention is not above 37.5%; Ready is read only after that. No resource pool limits or shares, no VM size against the host, no DRS.
- Final answer (2026-11-12; (b) diagram done; the rest expert call, one item needs you):
  - (a) Yes: orange = Peak vCPU Ready above 16%, CPU Ready above 4%, CPU Contention above 4%, CPU Usage above 1 GHz. Every other set halves each threshold from red to orange (Q140). As written, orange needs a red-level burst and red-level contention, so it fires almost only when red does.
  - Contention beside Ready: from VCF Operations 8.18, VM CPU Contention = Overlap + Co-stop + Ready + Other Wait (when below 1%), so Contention ≥ Ready. A Contention condition at the Ready value adds nothing. Drop it, or give it its own value if it is meant to catch Co-stop and Overlap.
  - cpu-alerts "8% against 6%" compares VM CPU Ready with the infrastructure alert's CPU Contention: name both metrics.
  - (b) The flow has its diagram. What remains is the flow logic: step 1 tests Contention against 37.5% (CPU Latency logic before 8.18), so a VM raised by the 8% Ready alert stops at step 1. Fix: step 1 reads Contention with the 8.18 formula against the KPI levels; add a Ready branch: VM limit, resource pool limits and shares, vCPU-to-thread overcommit at the time, VM size against the host (Co-stop), DRS.
  - Change if accepted: cpu-alerts (orange values; the 8% against 6% line); catalog row `alert-vm-cpu-ready-orange` (condition); vm-cpu-contention-high (step 1, Ready branch, chart); delete the Q144 review notes.
  - For you: what your shipped orange definition holds; whether Contention stays beside Ready after 8.18.
- Answer:

### Q145 · Part 2 > Proactive Operations > Alert > Memory Alerts · Wait, example and instance

- Files: [Memory alerts](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/configuration/memory-alerts.md); [Alert design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/alert-design.md); [Alert definitions in VCF Operations](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/alerts/alert-definitions.md); [ESXi Memory Latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/host/latency.md).
- Search 1: "10 minutes is used instead of 5 to reduce false positive. Take note this means you get notified later."
- Search 2: "VM 001 has 51% memory contention"
- Question: (a) the infrastructure consumption red has no duration in its condition; is the wait 10 minutes? (b) the 51% example lists 5 MB, 1 MB, 2 MB and shares; MB values cannot make 51%. Keep it as an illustration? (c) for ESXi and cluster, is Peak Memory Contention the worst VM, and Memory Contention the average of VMs?
- Written as now: (a) "Wait 10 minutes instead of 5 to reduce false positives" under Memory consumption; alert-design and alert-definitions still say "consumption: 15 minutes". (b) the 51% example with 5 MB, 1 MB, 2 MB. (c) infrastructure contention on ESXi, resource pool, cluster ("Cluster: measured on its VMs"); no instance, no population rule. Catalog rows `alert-infra-memory-contention-*`: no `instance`, no `interval`. ESXi Memory Latency is "a normalized average of the Memory Latency of the running VMs … Use the maximum VM Memory Contention across the host's VMs instead."
- Final answer (2026-11-12; (a), (b) expert call; (c) needs your confirmation):
  - (a) 10 minutes: the design note on this alert says so. Infrastructure CPU consumption also waits 10 minutes, VM CPU consumption 15. Write the wait on each alert; the general line in alert-design and alert-definitions becomes "consumption: 10-15 minutes, per alert".
  - (b) Keep the idea, drop the numbers. MB and % of time are different units: Memory Contention is the share of time a vCPU waits on memory (Q015, Q097). 1 MB of hot swapped pages can stall a VM more than 10 GB of cold ones. Rewrite: a limit, swap-in, decompression and low shares can act at once; the metric gives the total wait, not each cause's share.
  - (c) Neither worst VM nor average. Both are per-VM readings on each VM of the ESXi host, resource pool or cluster: Peak Memory Contention is the VM's highest 20-second value in the 5-minute interval (Q048); Memory Contention its 5-minute value. The alert fires on the population, as the CPU alert does (25% of VMs). Not the host's own Memory Latency: it is a normalized average of the running VMs and hides the victim. This is why the per-VM values (16% / 4%) sit below the VM alert's (24% / 6%).
  - Change if accepted: memory-alerts (three sections); the wait line in alert-design and alert-definitions; `instance` on the `alert-infra-memory-*` rows; delete the Q145 review notes.
  - For you: confirm the infrastructure memory alert uses 25% of VMs, as the CPU alert does.
- Answer:

### Q146 · Part 2 > Proactive Operations > Alert > Storage Alerts > VM Contention · 80 ms vs class of service

- Files: [Storage alerts](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/configuration/storage-alerts.md) (section VM disk latency); [Alert design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/alert-design.md) (section Class of service); [thresholds-alerts.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-alerts.yaml).
- Search: "Average Read Latency > 80 ms"
- Question: the VM disk latency alert is red above 80 ms average (orange 40 ms), while the class example gives standard production 60 ms for 10 minutes. Which class is the 80 ms alert for?
- Written as now: storage-alerts: "These are the standard production values" and the misconception "this set uses 80 ms average and 320 ms peak for standard production". alert-design: example 30 / 60 / 120 ms per class. Catalog alert rows have no class field.
- Final answer (2026-11-12; expert call, one item needs you):
  - The 80 ms alert belongs to no class. It is the recommended set for one policy over all VMs, set from field reality (the design note raises the value and waits 10 minutes because lower values draw hardly any complaints).
  - It matches no class anyway: orange 40 ms is below the standard production 60 ms and red 80 ms above it. The shape also differs: average plus a 20-second peak plus the 1 GHz and 100 IOPS gates, against one average and a duration.
  - 30/60/120 ms is an example of the step between classes (each 2x the one above). A site with classes makes one VCF Operations policy per class and sets each class's values.
  - Remove "These are the standard production values" and "for standard production" in the misconception: no source supports them.
  - The earlier draft's `class: all` on alert rows is dropped: alert rows have no class field. One line in the thresholds-alerts meta says the alert rows are one policy for every VM.
  - Change if accepted: storage-alerts (VM disk latency, misconception); alert-design (Class of service: an example, not shipped values); thresholds-alerts meta; delete the review note.
  - For you: whether your shipped set has per-class policies. If yes, their values are needed; none are in the knowledge base.
- Answer:

### Q147 · Part 2 > Proactive Operations > Alert > Network Alerts · VM dropped packets

- Files: [Network alerts](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/configuration/network-alerts.md); [VM Network Packets Dropped](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/metrics/virtual-motherboard/packets-dropped.md).
- Search 1: "Transmitted packet drop > 4% and"
- Search 2: "So the ratio is always 100%."
- Question: (a) the condition ends with "and": is a second condition missing? (b) 4% is 1 in 25, not 1 in 40. (c) what does "the ratio is always 100%" mean? (d) port group: does "change to transmit only" mean received drops gave the false positives?
- Written as now: "Red: transmitted packets dropped above 4%" (no second condition); "1 packet in 25 dropped … measured within a 20-second period"; "Dropped packets are usually retransmitted, so users rarely feel a problem"; "Planned change: count transmitted packets only" (no reason). Catalog row `alert-vm-network-tx-dropped-red`: 4%, 20s, no condition. packets-dropped: the % "can jump above 95% for under 15 minutes. Driven by low throughput"; receive drops are left out of the VM KPI.
- Final answer (2026-11-12; (b) done; (c), (d) expert call; (a) needs you):
  - (a) A condition is missing. Every other VM contention alert has an activity gate (CPU Usage above 1 GHz; disk adds IOPS above 100). A drop ratio over few packets is unstable: 1 drop in 20 packets is 5%, and packets-dropped records jumps above 95% at low throughput. Likely gate: a floor of packets transmitted per second, or CPU Usage above 1 GHz.
  - (b) Done: 1 in 25.
  - (c) Read as: the data delivered reaches 100% in the end, because TCP resends dropped segments. The cost is time, not data: each loss cuts the congestion window or waits for a retransmit timeout. UDP is not resent. Rewrite the retransmission line and its misconception that way; do not copy "the ratio is always 100%".
  - (d) Yes. Received drops include packets not meant for the port and VMXNET3 receive-ring drops, a Guest OS problem (Q070, Q085). The VM KPI leaves receive drops out for the same reason (packets-dropped, vm-performance). Transmit only keeps the alert on what the infrastructure team owns. Write this reason under the planned change. (The earlier draft said "why the SLA excludes them": no SLA since 2026-11-11.)
  - Change if accepted: network-alerts (condition, retransmission line, port group reason, misconception); catalog row `alert-vm-network-tx-dropped-red` (condition); delete the Q147 review notes.
  - For you: the missing condition and its value; whether (c) meant the delivery ratio.
- Answer:

### Q149 · Term map · Wrong terms users write

- Files: [knowledge/catalog/user-terms.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/user-terms.yaml).
- Search: not from the book.
- Question: list the wrong terms VMware admins and architects write in tickets, forums and chats, each with what they mean (for example "steal time" means VM CPU Ready and Co-stop). Each becomes a row: the words, the knowledge-base terms, the file, the misconception.
- Written as now: 41 rows, none from real tickets. `sla-for-performance` was added on 2026-11-11.
- Final answer (2026-11-12; expert call for the seed rows; the real terms need you):
  - Ten seed rows, each backed by current knowledge-base text:
    - `latency-unqualified`: "latency" with no layer; answer the likely layer, name the others (clarify rule).
    - `network-latency`: a VM has no network latency counter; read transmitted dropped packets.
    - `host-ready`: "ESXi Ready" sums or averages its VMs; read the worst VM.
    - `ready-percent`: "Ready 5% / 10%" or "Ready 2000 ms": summed over vCPUs, read per vCPU and against Run (ready).
    - `vm-consumed`: "VM consumed memory high" or "memory leak": Consumed does not drop when the Guest OS frees memory (guest-os-vs-vm-memory).
    - `thin-provisioning`: provisioned space counts thin disks at full size.
    - `drs-score`: DRS Score is demand met per VM, not contention.
    - `load-average`: esxtop load average is a utilization level; confirm with VM contention.
    - `sioc`: Storage I/O Control is deprecated in VCF 9.0.
    - `memory-pressure`: three layers: Guest OS paging, VM memory contention, host memory state.
  - Reword three notes: `iowait` ("CPU wait" can also mean Ready); `overcommit` (per thread, not per core); `esxtop-cpu` (read %RDY against %RUN).
  - Change if accepted: user-terms.yaml (10 rows, 3 notes); retrieval check before and after.
  - For you: the wrong terms you see in real tickets.
- Answer:

### Q150 · URL questions · Pages with known Level 300 errors

- Files: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (section 3.4, URL questions); [L4-50, the first URL question](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-50-vm-contention-dashboard-deprecated.md).
- Search: not from the book.
- Question: list 5-10 public pages (Broadcom KB or TechDocs, VMware blogs, community posts, third-party blogs) that you know are wrong, each with the error. Each becomes a URL question where a frontier model tends to agree with the page.
- Written as now: one URL question (L4-50, id 0091, the VM Contention dashboard page). Plan M2 lists the page list as yours to do.
- Final answer (2026-11-12; expert call for two pages; the rest needs you):
  - Two pages verified (fetched 2026-11-10):
    - Broadcom KB 419238, Troubleshooting VM performance (https://knowledge.broadcom.com/external/article/419238): %RDY ≥ 10 for a VM, with no per-vCPU normalisation and no Run; MCTLSZ, CACHEUSD, SWCUR ≥ 1 read as current problems (they are past tense); ZIP/s and UNZIP/s both read as overcommitment (only UNZIP/s and SWR/s mean the VM waits now); %DRPTX and %DRPRX above 0 read as high network utilization (received drops usually mean the Guest OS did not drain the ring); "Increase the amount of CPU and memory" (more vCPUs can raise Ready and Co-stop).
    - Broadcom KB 386180, CPU Ready Time issues in ESXi environments running high I/O workloads (https://knowledge.broadcom.com/external/article/386180): Ready baseline 5% and warning 10% from an esxtop batch capture, not per vCPU, not against Run; CPU Latency 5% and 10% read as contention (Latency also rises with lower frequency and Hyper-Threading, with no wait).
  - Checked and rejected: KB 306576 (right apart from "cores" for vCPUs); KB 431027 (matches core-utilization).
  - Re-fetch each page when the question is written: the date renders by script, so the question key records the fetch date and quotes the lines it relies on.
  - The frontier reference runs with web search on (Q164), so URL questions test whether a model agrees with a page it reads. The benchmark runs after development (Q163), so the pages can still change.
  - Change if accepted: two URL questions (Level 300, troubleshoot).
  - For you: 3-8 more pages (blogs, community posts) you know to be wrong.
- Answer:

### Q162 · Class of service planning · "KPI (%), not SLA (%)" per class

- Files: [Class of service in capacity planning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/class-of-service-planning.md) (Contention); [Performance KPI design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/performance-kpi-design.md) (section Scoring); [Can this cluster take more VMs?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms.md) (Misconceptions); [thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml) (rows class-*-min-vm-performance). Related: Q175 (c).
- Search: your table image in Part 1, Capacity Management: row "Contention: Minimum Performance (%) threshold. KPI (%), not SLA (%)."
- Question: your table gives Gold ≥ 99.5%, Silver ≥ 99%, Bronze ≥ 98% and labels it KPI. On 2026-11-10 you said the KPI is never per class of service. (a) The reword is right: a capacity design expectation per class, read on VM Performance (%); the KPI itself has no class. (b) The KPI has a target per class after all. (c) Other.
- Written as now: class-of-service-planning, Contention: minimum VM Performance (%) Gold ≥ 99.5%, Silver ≥ 99%, Bronze ≥ 98%, "a capacity design expectation that sets the overcommit of the class. The KPI itself has no class of service"; and "The minimum Performance (%) leaves unmet demand of 0.5%, 1% and 2%." The image with "KPI (%), not SLA (%)" was archived on 2026-11-11; the new planning image has no contention row. Catalog rows give no interval or statistic. can-cluster-take-more-vms misconception: "the Gold minimum of 99.5%".
- Final answer (2026-11-12; expert call, needs your choice): (a), with a scale correction.
  - (a) holds: the KPI has no class (2026-11-10). The image question is moot (archived).
  - The numbers are not on the scale of today's VM Performance (%). It is a banded score: green 100-75, a straight line inside each band, worse scores weigh more (performance-kpi-design, Scoring). 99.5, 99 and 98 all sit in the top tenth of green. Example: one sub-metric at score 95 among six at 100 gives a KPI of about 99.2, a fail for Gold, while every metric is green.
  - "Leaves unmet demand of 0.5%, 1% and 2%" reads the score as 100 minus the share of time a VM waits. That was the scale of the older Performance (%). On today's score it is the modelling misconception "KPI at 75%, so 25% of the VMs are slow": scores, not shares.
  - Proposal: state the class expectation as unmet demand, not as a VM Performance (%) value: the share of time a VM waits for CPU or memory, at most Gold 0.5%, Silver 1%, Bronze 1.5%. Bronze 1.5% steps with the relative contention 1x, 2x, 3x of your new diagram (Q175 c); 2% would be 4x.
  - Reading it in the running stage: per VM, the monthly mean of VM CPU Contention (%) and VM Memory Contention (%), each against the class value. A design expectation, not an alert or a KPI band.
  - Change if accepted: class-of-service-planning (Contention: unmet demand per class; the unmet-demand line); catalog rows renamed `class-*-max-unmet-demand` with interval and statistic; can-cluster-take-more-vms misconception ("Gold design expectation"); delete the review note.
  - For you: (1) restate the class values as unmet demand, or keep them as VM Performance (%) scores with new numbers on the 0-100 score; (2) Bronze 1.5% or 2%; (3) the statistic and period (proposal: monthly mean per VM).
- Answer:

### Q165 · benchmark/design.md, sections 3-5 and 10 · Sealed claim set and knowledge_class tag

- Files: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md); [project/review-2026-11-11.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/review-2026-11-11.md) (section 5); [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md).
- Question: (a) a sealed claim set of 150-200 Level 300-400 questions, at least half from real tickets, written by you and 1-2 peers, never seen during development; tag `knowledge_class: public-mechanism | vendor-current | author-framework`; superiority claimed on public-mechanism; (b) current design; (c) other.
- Written as now: 95 questions: 68 synthetic, 17 quiz, 10 book, 0 real tickets; 71 draft, 23 awaiting input, 1 reviewed. design.md keeps a held-out set of about 20% kept by you; no sealed set, no `knowledge_class`; its status section is dated 2026-11-05 (90 questions). Since the review: no benchmark until M1-M3 are done (Q163); the frontier reference is Claude Opus 5.5 only, web search on, effort capped at medium (Q164).
- Final answer (2026-11-12; expert call): (a), adjusted to Q163 and Q164.
  - One sealed set replaces the 20% held-out cut: 150-200 questions, Level 300-400, at least half from real tickets, by you and 1-2 peers, never seen during development. Two separate holdbacks would split too few questions.
  - `knowledge_class` on every question. Superiority is claimed on public-mechanism, the class a frontier model can know. author-framework is scored and reported apart: a frontier model cannot know the SP5 Framework, so a win there proves the knowledge base, not the agent's reasoning.
  - Why: at 100 questions a 10-point gap is detected with about 68% power (review, section 5). With one frontier family as the reference (Q164) and 68 of 95 questions synthetic, questions written by people matter more.
  - The development set (the 100 questions) keeps its job: the release gate and M3.
  - Change if accepted: benchmark/design.md (sections 3-5 and 10; status section with today's counts); question template (`knowledge_class`); project/terms.md (proposal); plan M2.
  - For you: names of the peer authors; a source of real tickets.
- Answer:

### Q175 · Class of service · New relative-value diagram vs the reservation shares, VM size and minimum performance

- Files: [Class of service in capacity planning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/class-of-service-planning.md) (sections Promise vs technique, Example implementation); [VM size](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/vm-size.md); [Class of service](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/class-of-service.md) (sections Recommended SLA per class, Sample offering, Size limit per class); [IaaS SLAs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/sla-metrics.md) (section Compliance SLA).
- Search: not from the book; your relative-value diagram of 2026-11-11.
- Question: which values win for (a) reservation, (b) maximum VM size, (c) minimum VM Performance; will you update the planning image (d); is the Sample offering's (e) a Compliance SLA or a Security SLA, and at which number?
- Written as now:
  - Diagram and table: contention 1x, 2x, 3x; maximum VM size 3x, 2x, 1x; reservation 3x, 2x, 1x; share 4-8x, 2-4x, 1x; overcommit 1x, 2x, 3x. "The steps are a goal, not a rule."
  - (a) Reservation 50%, 25%, 12.5% CPU and 100%, 50%, 25% memory: 4x, 2x, 1x. You kept 12.5% for Bronze (Q173 b).
  - (b) Q176: class size Gold 2 × the cores of one CCD or compute tile, Silver 1 ×, Bronze 0.5 ×: 4x, 2x, 1x. vm-size and class-of-service still also call the technical maximum (threads ÷ ratio) the class cap.
  - (c) 99.5%, 99%, 98%: see Q162.
  - (d) Done 2026-11-11.
  - (e) Sample offering: "Security SLA | 100% | 100% | Perfect compliance for every class". Recommended SLA table: Compliance 99.95% for every class. sla-metrics: "do not put 100% in it; the contract value is 99.95%. The internal KSI is 100%". Glossary: Security SLA is the preferred term, also called Compliance SLA.
- Final answer (2026-11-12; (a), (b) settled by Q173 and Q176, the diagram follows; (c) in Q162; (e) settled by sla-metrics and the glossary):
  - (a) The values stay (Q173 b, the spreadsheet): a reservation guards against starvation and does not have to step with the ratio. The diagram row reads 4x, 2x, 1x.
  - (b) The values stay (Q176): 2, 1 and 0.5 CCDs or compute tiles. The diagram row reads 4x, 2x, 1x. Two lines change so that the technical maximum is not called the class cap: vm-size, fence section; class-of-service, Size limit (Q111).
  - So the diagram: contention 1x, 2x, 3x; overcommit 1x, 2x, 3x; reservation 4x, 2x, 1x; maximum VM size 4x, 2x, 1x; share 4-8x, 2-4x, 1x. The steps stay a goal, not a rule.
  - (c) Q162: restate as unmet demand; Bronze 1.5% steps with contention 3x.
  - (d) Done.
  - (e) A Security SLA (the glossary's term) at 99.95%, as the Recommended SLA table and sla-metrics state; 100% is the internal KSI. Sample offering row → "Security SLA | 99.95% | 99.95% | Same for every class; the internal KSI is 100%". The Recommended SLA table header "Compliance" → "Security", one word per concept.
  - Change if accepted: your diagram (two rows) and its alt text and table in class-of-service-planning; vm-size and class-of-service (cap wording); class-of-service (Sample offering row; table header); delete the Q175 review note.
  - For you: relabel the two diagram rows, or tell which value should change instead.
- Answer:

### Q180 · Resource controls · One home for share, limit and reservation

- Files: [Resource controls](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/resource-controls.md) (1,338 words, cited by 6 questions); [Resource settings: when and how](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/configuration/resource-settings-guidance.md) (1,617 words); [Scalable Shares and resource pool siblings](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/resource-pool/configuration/scalable-shares.md) (356 words). Neighbours: [Noisy neighbour](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/noisy-neighbour.md); [Admission control, expandable reservations and cluster state](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/admission-control-and-cluster-state.md).
- Search: not from the book; your request of 2026-11-12.
- Written as now (review, top down):
  - Mechanism is written three times. "Shares act only under contention" and "a reservation is a guarantee, so it cannot be overcommitted": in all three files. Default CPU shares: resource-controls (1:2:4 per vCPU) and resource-settings-guidance (table). A VM's shares split among its vCPUs: resource-controls and noisy-neighbour.
  - resource-settings-guidance holds two sources one after the other: Performance Best Practices 9.1 (Principle, Shares, Reservation, Headroom, Resource pools) and the book's review list (Review: three sections). The two halves repeat each other: reservation 3 times, resource pools 2 times, limit advice 2 times.
  - Pool design sits in two files: resource-settings-guidance (Resource pools; Review: resource pools; siblings) and scalable-shares (siblings, Scalable Shares). They disagree on siblings (Q110 c).
  - scalable-shares holds two generic sections that are not about pools: Reservations and shares; Reservations and limits in DRS.
  - Reservation headroom and DRS: resource-settings-guidance (Headroom), scalable-shares (DRS section) and admission-control-and-cluster-state (Headroom, with the 10% figure). The last is the only one with a number.
  - Missing in every file: the memory share defaults sit only in the guidance; the network limit (Q109); the slot policy condition (Q110 b).
- Proposal (expert call): one home per fact, by layer. Mechanism once, advice once, pool design once.
  - resource-controls (vsphere/architecture, how it works): what each control is and how ESXi applies it, for every resource. Gains: the default share tables (VM and pool, CPU and memory), what a Normal pool weighs, shares divide only what is left after reservations, resize recalculates default shares (vSphere Client only), network and disk controls exist (NIOC per vNIC, traffic shaping, disk IOPS limit; Q109). Keeps: entitlement, reservation CPU vs memory, limit, two scheduler levels.
  - resource-settings-guidance (VM, what to set): advice only, one section per control, in the order Limit, Reservation, Share, then the audit. Merges the Best Practices half and the review half into one list each. Keeps the impact image and the share audit. Mechanism lines are replaced by one link to resource-controls. Headroom moves out. New share example (Q108 b). Pools move out. Expected size about 800 words.
  - scalable-shares → renamed "Resource pool design" (resource-pool/configuration): when to use a pool (delegation, multi-tier service, sold as a service), Fixed vs expandable as a design choice (the mechanism stays in admission-control-and-cluster-state), siblings and Scalable Shares (Q110 c), cascading, pool settings are cluster-wide. Its two generic sections are deleted: they repeat resource-controls and admission-control-and-cluster-state. Id moves; moved.yaml maps the old id.
  - admission-control-and-cluster-state: stays the home of admission, headroom and DRS migration limits. Gains: host and DRS admission control cannot be turned off; restart after a host failure (Q110 a); slot policy condition (Q110 b).
  - noisy-neighbour: unchanged except one line. Its per-resource overcommit arithmetic stays; the busy-vCPU share point stays there and resource-controls links to it.
  - Misconceptions follow their fact: each file keeps only the misconceptions of what it holds.
  - Q108, Q109 and Q110 are applied in the same change if you accept them.
- Measure: retrieval check before and after (resource-controls is the second most-cited file).
- For you: accept, or name what stays where.
- Answer:

## Resolved

### Q096 · Part 1 > Service Level Agreement > Availability SLA · The database restore in Actual Availability

- Files: [IaaS SLAs: what each measures and how it is computed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/sla-metrics.md) (section Availability SLA, example).
- Search 1: "the large database took 45 minutes to fully restore"
- Search 2: "Actual Availability (%) = 717 / 720 = 99.58%"
- Search 3: "If it takes the application 15 minutes to become fully operational"
- Question: the definition counts the Guest OS only; application start-up is not counted. The example counts 15 minutes of Windows plus 45 minutes of database restore, 3 times: 99.58%. By the definition it is 3 × 15 = 45 minutes: 99.90%. Which is meant: (A) the IaaS Actual Availability is 99.90% and 99.58% is what the application owner sees; (B) 99.58%, because Actual Availability counts everything users see, including the application; (C) other?
- Written as now: sla-metrics gives both numbers ("counting the Guest OS only: 45 minutes, 99.90%"; "counting until the database is restored: … 99.58%"), neither labelled as the SLA value. Glossary Actual Availability: "Availability as it happened. Usually lower than Operational Availability."
- Final answer (2026-11-12; expert call): (A).
  - Actual and Operational Availability measure the same thing, the Guest OS answering. They differ only in which downtime counts (scheduled, customer-caused), not in which layer must be up. If Actual counted the application, the gap between the two would mix two effects.
  - IaaS Actual Availability: 3 × 15 = 45 of 43,200 minutes = 99.90%. Operational Availability: 100% (all three restarts inside the change window).
  - 99.58% (3 × 60 minutes; 717 of 720 hours) is the application owner's view. Database recovery is application layer, like application start-up, which the definition already excludes. It belongs to the application team's KAI or an application SLA.
  - fsck differs: it runs before the Guest OS is up, so it counts (sla-metrics misconception already says so).
  - Change if accepted: sla-metrics, Availability SLA example: 99.90% is the IaaS Actual Availability; 99.58% is the application view, outside the IaaS SLA. Glossary Actual Availability: add "same scope as the Availability SLA: the Guest OS". Delete the review note.
  - For you: nothing.
- Answer: Agree. Proceed (2026-11-12).
- Applied 2026-11-12: sla-metrics, Availability SLA example (99.90% is the IaaS Actual Availability and the SLA value; 99.58% is the application owner's view, outside the IaaS SLA; Actual and Operational Availability share the Guest OS scope); glossary Actual Availability ("Same scope as the Availability SLA: the Guest OS"); review note deleted.

### Q064 · Review · Which files to review first

- Files: the 25 most-cited knowledge files below. Review: [project/review-2026-11-06.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/review-2026-11-06.md), section 3.4.
- Search: not applicable.
- Question: 0 of 277 knowledge files are `status: reviewed`. Reviewing them in this order puts your review where the benchmark scores. Please confirm the rule, or name your own order.
- Written as now (recount 2026-11-12): 95 questions cite 131 of 277 files; moved ids resolved. Up front: M = a `See` id in knowledge/misconceptions.md; G = a glossary entry with a Not to confuse with line (the `terms` block).

| # | Cited by | Up front | File |
|---|---|---|---|
| 1 | 9 | M | [vsphere/architecture/vm-vs-guest-os](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/vm-vs-guest-os.md) |
| 2 | 6 | | [vsphere/architecture/resource-controls](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/resource-controls.md) |
| 3 | 6 | | [vsphere/technology/cpu/metrics/virtual-motherboard/ready](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/ready.md) |
| 4 | 6 | | [vsphere/technology/network/metrics/virtual-motherboard/packets-dropped](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/metrics/virtual-motherboard/packets-dropped.md) |
| 5 | 5 | | [vsphere/technology/storage/metrics/virtual-motherboard/disk-latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/virtual-motherboard/disk-latency.md) |
| 6 | 4 | G | [vsphere/technology/cpu/metrics/host/core-utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/core-utilization.md) |
| 7 | 4 | G | [vsphere/object-types/cluster/models/cluster-risk](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md) |
| 8 | 4 | G | [vsphere/technology/memory/concepts/guest-os-vs-vm-memory](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/guest-os-vs-vm-memory.md) |
| 9 | 4 | | [vsphere/technology/cpu/concepts/hyper-threading](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/hyper-threading.md) |
| 10 | 4 | | [vsphere/object-types/vm/kpis/vm-performance](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/kpis/vm-performance.md) |
| 11 | 4 | | [vsphere/technology/memory/metrics/virtual-motherboard/latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/latency.md) |
| 12 | 4 | | [vsphere/technology/storage/concepts/snapshot-impact](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/concepts/snapshot-impact.md) |
| 13 | 4 | | [vsphere/architecture/overhead](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/overhead.md) |
| 14 | 4 | | [vsphere/technology/memory/concepts/ballooning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/ballooning.md) |
| 15 | 4 | | [vsphere/tools/esxtop/storage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/tools/esxtop/storage.md) |
| 16 | 3 | M | [vcf-operations/features/peak-20-second-metrics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/features/peak-20-second-metrics.md) |
| 17 | 3 | M | [vsphere/technology/cpu/metrics/virtual-motherboard/usage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/usage.md) |
| 18 | 3 | M | [vsphere/technology/cpu/metrics/host/utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/utilization.md) |
| 19 | 3 | M | [vsphere/object-types/cluster/concepts/admission-control-and-cluster-state](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/admission-control-and-cluster-state.md) |
| 20 | 3 | M | [vsphere/technology/memory/metrics/virtual-motherboard/ballooned](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/ballooned.md) |
| 21 | 3 | | [vsphere/object-types/cluster/kpis/cluster-performance](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md) |
| 22 | 3 | | [vsphere/technology/cpu/concepts/cpu-frequency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/cpu-frequency.md) |
| 23 | 3 | | [vsphere/technology/network/troubleshooting/vnic-rx-drops](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/troubleshooting/vnic-rx-drops.md) |
| 24 | 3 | | [vsphere/technology/storage/concepts/esxi-storage-latency-stack](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/concepts/esxi-storage-latency-stack.md) |
| 25 | 3 | | [vsphere/technology/storage/troubleshooting/host-storage-latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/troubleshooting/host-storage-latency.md) |

- Just outside: memory/metrics/virtual-motherboard/active and storage/metrics/host/adapter-and-path (3 each). Then 28 files cited twice; three carry an up-front mark: vsphere/architecture/provider-consumer, sp5-framework/capacity/rightsizing, memory/metrics/virtual-motherboard/usage.
- Size: about 17,700 words for the top 25.
- Final answer (2026-11-12; expert call, you confirm the rule):
  - Rule: sort by the number of questions that cite the file. Ties: first a file an up-front block points to (its error reaches every question), then inbound links (link expansion pulls it into other contexts).
  - Item 0, before the table: knowledge/glossary.md and knowledge/misconceptions.md. No question cites them, yet every question reads them up front.
  - After the first benchmark run, the files behind wrong answers sorted to "knowledge" come first.
  - A substantive edit after review sets the file back to `status: draft`.
  - Changed since the 2026-11-10 draft: capacity-model was split (its citations now go to supply, demand and overcommit); cluster-sla-sli was archived (its citations moved to cluster-performance); vm-performance is new at 4.
  - Change if accepted: plan M1, exit criterion "the most-cited files reviewed", points to this rule and this table.
  - For you: confirm the rule.
- Answer: Close as outdated. The plan is for Claude Opus to review all the synthetic questions and generate the rest (2026-11-12).
- Closed 2026-11-12: no review order is applied; plan M2 records the question review.

### Q179 · Memory tiering rows for Cluster Consumption, Cluster Performance and Cluster Risk · Proposal for review
- Files: [Cluster Consumption (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-consumption.md); [Cluster Performance (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md); [Cluster Risk (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md); [Memory tiering](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-tiering.md); [Modelling](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/modelling.md) (section Setting thresholds).
- Search: not from the book; follows Q178.
- Every row has five numbers. Values are % unless stated; higher is worse.
- Cluster Consumption (cluster-wide, against usable capacity):

| Group | Sub-metric | Score 100 at | Green ends at | Yellow ends at | Orange ends at | Score hits 0 at | Change |
|---|---|---|---|---|---|---|---|
| Utilization | ESXi CPU Thread Utilization | 0 | 55 | 70 | 85 | 100 | None |
| Utilization | ESXi Memory Consumed, hosts without tiering (% of usable DRAM) | 0 | 70 | 80 | 90 | 100 | None |
| Utilization | ESXi DRAM Consumed, tiered hosts (tier 0, % of usable DRAM) | 0 | 80 | 85 | 90 | 100 | New: tiering starts at 80% of DRAM by design, so green runs to 80 |
| Saturation | Memory Tiering Consumption (tier 1, % of usable NVMe tier) | 0 | 25 | 50 | 75 | 100 | Was 4, 8, 16, 32 |
| Saturation | ESXi Memory Ballooned (% of usable DRAM) | 0 | 1 | 2 | 4 | 8 | None; on a tiered host any value is a configuration finding |
| Saturation | ESXi Memory Zip Swap (% of usable DRAM) | 0 | 0.25 | 0.5 | 1 | 2 | None; same |

- Cluster Performance (powered-on VMs; worst VM and 90th percentile):

| Sub-metric | Unit | Score 100 at | Green ends at | Yellow ends at | Orange ends at | Score hits 0 at | Change |
|---|---|---|---|---|---|---|---|
| Worst VM CPU Ready | % | 0 | 4 | 8 | 16 | 32 | None |
| Worst VM CPU Co-Stop | % | 0 | 2 | 4 | 8 | 16 | None |
| Worst VM Memory Wait (Memory Latency + NVMe Wait) | % | 0 | 1 | 2 | 4 | 8 | Was Memory Latency only |
| Worst VM Disk Latency | ms | 0 | 40 | 80 | 160 | 320 | None |
| 90th Percentile VM CPU Ready | % | 0 | 1 | 2 | 4 | 8 | None |
| 90th Percentile VM CPU Co-Stop | % | 0 | 0.5 | 1 | 2 | 4 | None |
| 90th Percentile VM Memory Wait (Memory Latency + NVMe Wait) | % | 0 | 0.5 | 1 | 2 | 4 | Was Memory Latency only |
| 90th Percentile VM Disk Latency | ms | 0 | 20 | 40 | 60 | 80 | None |
| Highest ESXi Bad Network Packets | % | 0 | Excluded (exactly 0) | 0.2 | 0.4 | 0.8 | None |

- Cluster Risk (worst host; tiering rows only):

| Sub-metric | Unit | Score 100 at | Green ends at | Yellow ends at | Orange ends at | Score hits 0 at | Change |
|---|---|---|---|---|---|---|---|
| Worst ESXi Active Memory, tiered hosts | % of DRAM | 0 | 50 (excluded while green) | 62.5 | 75 | 100 | New (Q178 a); replaces NVMe consumed ÷ DRAM consumed |
| Worst ESXi NVMe Read Latency | µs | 0 | 100 | 200 | 400 | 800 | Was 150, 300, 450, 600; no read floor (revised 2026-11-12) |

- Reasons:
  - DRAM consumed on a tiered host: Memory Consumed covers both tiers and goes above 100% of DRAM by design, so the tiered row reads tier 0 only. DRAM sits near 80% whenever the tier is in use, so green runs to 80; above that, hot pages are filling DRAM.
  - Tier consumption is saturation (Q178 d), measured against the usable NVMe tier. Linear bands, like the utilization rows: the tier is filled with cold pages on purpose, so its fill is the room left before swap. At the default 1:1 ratio, Broadcom's example at 2x VM density (1,600 GB of 2 TB) puts the tier near 60%, orange, as a host without tiering at 80% sits at the yellow-orange line. The stricter option, doubling like the other saturation rows (12.5, 25, 50, 100), turns designed use red.
  - Memory Wait: the VM does not care where it waits for memory (Modelling). NVMe Wait estimates the share of vCPU time a VM waits for pages fetched from NVMe (Little's law): NVMe Wait (%) = VM tier-1 read bandwidth (MB/s) × 256 pages per MB × host NVMe read latency (s) ÷ VM vCPUs × 100. Same bands as Memory Latency, so it reuses a scale that is already quantified.
  - NVMe read latency: doubling, as Setting thresholds asks; red starts at Broadcom's impact point (400 µs); Broadcom's "potential issues" zone (200-400 µs) is orange; its "good" zone splits into green and yellow. No read floor (revised after your remark): a device waking from a power-saving state is the why; the VM that read waited all the same.
  - Active memory: Broadcom's 50% (recommended) and 75% (significant loss) are the ends of green and orange; 62.5% splits the testing zone; 100% is active memory equal to DRAM. Excluded while green, like the other leading indicators of Cluster Risk.
- Data quality before use (your rule in Q178 c):
  - NVMe Wait rests on three assumptions to validate on a tiered lab host: each fetch is one 4 KB page (large pages are off on tiered hosts) and blocks one vCPU; reads include no prefetch; Memory Latency (%LAT_M) does not already count the fetches (if it does, the sum double counts and NVMe Wait is dropped). Until validated, show it and leave it out of the score.
  - Metric keys in VCF Operations for tier-0 consumed, per-VM tier-1 read bandwidth and host tier-1 read bandwidth: not yet found (vCenter: tier.consumed, bandwidth.read per tier, level 2; latency.read level 3).
  - Revised 2026-11-12: the 1 MB/s read floor is withdrawn. It removed a real wait because of its cause (the why), and the SP5 Framework scores the what. Memory Wait (reads × latency) already weighs a wake-up by how many reads it hit.
- Question: accept each table row, or give your numbers; and which tier-consumption bands (linear 25/50/75/100 or doubling 12.5/25/50/100)?
- For you: the three tables.
- Answer (partial, 2026-11-12): tier consumption bands linear 25/50/75/100. The metric is in between utilization and saturation: utilization starts green at a high number, saturation starts green at a low number and doubles quickly; linear blends the two natures.
- Applied 2026-11-12: catalog row cluster-consumption-cluster-memory-tiering-consumption 25/50/75/100; cluster-consumption reason and correction entry. Still open: the other rows of the three tables.
- Answer: accepted as proposed (2026-11-12).
- Applied 2026-11-12: catalog thresholds-capacity (tiered DRAM consumed row 80/85/90/100; active memory 50/62.5/75/100; NVMe read latency 100/200/400/800 µs) and thresholds-performance (cluster memory wait rows); cluster-consumption, cluster-performance (memory wait, NVMe wait formula, validation before scoring), cluster-risk (rows, correction entry), memory-tiering (section In the cluster models). The vCommunity pack follows (plan.md, After 1.0). Closed.

### Q178 · Memory tiering in the capacity and performance models · Review of the three closure conditions
- Files: [Memory tiering](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-tiering.md); [Is memory tiering slowing this host?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/decision-tree/is-memory-tiering-slowing-host.md); [Cluster Risk (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md); [Cluster Consumption (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-consumption.md); [Cluster Performance (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md); VCF-vCommunity-Adapter docs/reference/metrics/cluster-risk.md and cluster-consumption.md.
- Search: not from the book; your note of 2026-11-12 (three conditions that close capacity on a tiered cluster).
- Sources read 2026-11-12: Memory Tiering Performance, VMware Cloud Foundation 9.0 (performance study, July 2025), section Using and monitoring Memory Tiering; vSphere 9.1 documentation, Memory Tiering over NVMe and Memory Tiering and HA Admission Control; blogs by Broadcom staff and yellow-bricks.com. Written into the two knowledge files above.
- What the models do now:
  - Cluster Risk: Worst ESXi Memory Tiering Latency, NVMe read latency, bands 150/300/450/600 µs.
  - Cluster Consumption: Memory Tiering Consumption in the Saturation group, NVMe in use ÷ usable NVMe tier, bands 4/8/16/32%. Memory Consumed ÷ usable DRAM.
  - Cluster Performance: no tiering row.
- Review of your three conditions:
  - (1) NVMe read latency: right, and Broadcom gives the bands: below 200 µs good, 200-400 µs potential issues, above 400 µs workload impact. The pack's 150/300/450/600 differ. Latency alone gives false positives: an idle device shows high latency on sporadic reads (wake-up penalty, already in the knowledge base). Score it only while the host reads from NVMe.
  - (2) Reads from NVMe: right, and the most direct signal: each fetch is a vCPU waiting about 1,000x a DRAM access, at any latency. Broadcom gives 200 MB/s per host as the point to start watching latency, not an impact limit; per-VM read bandwidth shows which VMs pay. Writes: you are right for device writes (demotion of cold pages runs in the background, off the vCPU's path; it costs endurance, and heavy writes can raise read latency through garbage collection). Not for guest writes: a write to a cold page must bring the page back to DRAM first, so it waits like a read and shows as NVMe read bandwidth. Inferred from the architecture (NVMe is not byte-addressable); no Broadcom page states it.
  - (3) NVMe consumed ÷ DRAM consumed as risk: right that tier 1 is not actual consumption, since it holds cold pages. Weak as a risk signal: at the default 1:1 ratio a host used as designed sits near 1 and stays fast while its working set is small (VDI). The documented leading signal is active memory as % of DRAM: 50% or lower green, 50-75% test and monitor, above 75% significant loss.
- Missing from the three:
  - (a) Active memory ÷ DRAM, as above.
  - (b) DRAM for HA restart: a VM needs DRAM to power on. Before vSphere 9.1.1, admission control counted NVMe as DRAM and could stay green while a restart would fail. 9.1.1 reserves DRAM separately (cluster resource percentage and dedicated failover hosts policies; not the slot policy).
  - (c) Memory Consumed ÷ DRAM goes above 100% by design on a tiered host (consumed covers both tiers): Cluster Consumption scores a healthy tiered cluster red. Tier usage in the Saturation group at 4/8/16/32% does the same.
  - (d) Reclamation on a tiered host means a configuration problem: a non-tiered VM without a full reservation, a limit, or overcommit on top of tiering. The existing ballooned and swapped + zipped rows catch it.
  - (e) Large VMs: the performance study says no VMs above 32 vCPUs and 512 GB with tiering; the documentation says 64 vCPUs and 512 GB.
  - (f) Unknown: whether VM Memory Contention (%LAT_M) counts the wait for NVMe fetches. If not, no VM KPI sees tiering today.
  - (g) Your question on swap and compression: they can run while tier 1 has free space (non-tiered VMs without reservation, limits). Broadcom does not state that host-wide reclamation now waits until tier 1 is full; the host's total memory is tier 0 + tier 1 and new pages go to tier 1 after DRAM reaches 80%, so host-wide reclamation should start only when both are nearly full. Unverified.
- Proposed model (expert call):
  - Cluster Performance, actual: add NVMe read latency of the worst host, scored only while that host reads from NVMe above a floor; bands green below 200, yellow 200-300, orange 300-400, red from 400, 0 at 600 µs. Add worst-VM and 90th-percentile NVMe read bandwidth once you have field ranges. Tiering then closes a cluster through the existing rule (Performance red).
  - Cluster Risk, leading: replace condition (3) with active memory ÷ DRAM of the worst host: green to 50%, yellow 50-62.5%, orange 62.5-75%, red from 75%, 0 at 100%. Move the latency row to Cluster Performance. Add a DRAM failover check for clusters below 9.1.1, as configuration rather than a score.
  - Cluster Consumption, quantity: on tiered hosts, memory consumed ÷ (usable DRAM + usable NVMe tier). Drop Memory Tiering Consumption from the Saturation group, or score it with the memory consumed bands (70/80/90). Ballooned and swapped + zipped stay against DRAM.
  - Planning: no change; tiering stays out of the plan (Q177).
- Question:
  - (A) Replace (3) with active memory ÷ DRAM in Cluster Risk, at the bands above?
  - (B) Move NVMe read latency to Cluster Performance, gated by reads, at Broadcom's 200/400 bands?
  - (C) What floor of NVMe reads, and what per-VM read bandwidth bands? No source gives them; they need your field data.
  - (D) Cluster Consumption against DRAM + NVMe on tiered hosts?
- For you: (A)-(D). The pack's thresholds stay as built until you decide.
- Answer: (a) Yes. (b) Broadcom bands not used on purpose: operations need 4 bands, so 5 numbers per metric; Broadcom gives 3 zones. (c) A metric that cannot be quantified into [grey], green, yellow, orange is not used; real-world data is not reliable because it is real: quality first, then enough quantity to rule out outliers. (d) In the SP5 Framework, Consumption = Utilization + Saturation, more than the Memory Consumed counter. NVMe consumed must be measured explicitly as Saturation, as zip and swap become 0. Propose the model by improving the Cluster Consumption and Cluster Performance tables.
- Applied 2026-11-12: modelling (Setting thresholds): five numbers for four bands, convert vendor zones; quantify or leave out, data quality before quantity. cluster-consumption: on a tiered host the tier is the saturation signal. memory-tiering and the tiering decision tree: tier 1 consumed is saturation, not contention. Proposal: Q179.

### Q176 · Part 1 > Service Level Agreement > Size Limit · Memory cap per class after the socket rule
- Files: [Class of service](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/class-of-service.md) (section Size limit per class); [VM size](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/vm-size.md) (section Maximum VM size); [Cluster Risk (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md) (section Monster VM).
- Search: "Capping the size at each tier is a good way to prevent monster VMs"
- Image text (not searchable): "Tier 1 ≤ 1 socket 32 vCPU, 512 GB RAM", "Tier 2 ≤ 50% of a socket", "Tier 3 ≤ 25% of a socket".
- Written as now: your Q100 answer removed the socket basis. The CPU cap moved to vm-size (logical CPUs × 1, 0.5, 0.33 at 1:1, 2:1, 3:1). The memory caps (512, 128, 32 GB) were per socket, so they are withdrawn and no memory cap per class is stated. Cluster Risk still flags a monster VM above 40% of host DRAM or 256 GB, whichever is smaller.
- Question: what is the memory cap per class? (A) the same step as CPU: host DRAM × 1, 0.5, 0.33; (B) one rule for every class, below the Cluster Risk monster size; (C) the CPU cap × the class's GB per vCPU (4 GB in the plan); (D) no memory cap per class.
- Proposed answer (expert call): (C), bounded by (B). Memory is sold with vCPUs (host-spec-from-class-of-service), so the cap follows the CPU cap: 4 GB per vCPU gives Bronze 0.33 × 128 threads × 4 = 170 GB on a 64-core host. (B) keeps every class below the size Cluster Risk calls a monster (256 GB on that host), so Gold is capped by memory before CPU. (A) ignores that memory is sold with vCPUs; (D) leaves Bronze unbounded.
- For you: pick (A)-(D), or give the field rule.
- Answer: None of (A)-(D) as a fixed number: VM size per class depends on the CPU architecture. After 1.0, Agent E2 should have a VM size calculator (roadmap). General advice meanwhile: Gold up to 2x an EPYC CCD or Xeon compute tile in vCPUs, Silver 1x, Bronze 0.5x; RAM 4 GB per vCPU. NUMA optimization aligns vCPU threads with the nearest memory controllers; crossing a die boundary for remote memory wastes cycles on the fabric. Example: AMD EPYC 9996 (256 cores, 8 CCDs of 32 cores, 2 IODs, 16 DDR5 channels, NPS2): a 32 vCPU VM fits one CCD; a 64 vCPU VM spans two CCDs behind the same IOD, memory within the NUMA node, no vNUMA topology.
- Applied 2026-11-12: vm-size: section Size per class (table, NUMA reason, L3 domain unit, EPYC 9996 example); class-of-service: size limit points to it; plan.md After 1.0: VM size calculator. Two wording changes in the example, for the author to check: the unit is the L3 cache domain (on Zen 4c a 16-core CCD holds two 8-core CCX); and "memory fetches within the same CCD are instantaneous" is written as L3 hits stay inside the CCD while data shared between CCDs moves through the IOD (DRAM is always behind the IOD).

### Q177 · Capacity Planning Stage.xlsx · Memory tiering on top of the memory overcommit ratio
- Files: [Overcommit ratio](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/overcommit.md) (section Per resource); [Class of service in capacity planning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/class-of-service-planning.md) (sections Example implementation, Planning calculator); [Memory tiering](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-tiering.md) (section Capacity management); [harness/capacity.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/capacity.py) (functions vms_per_host, consumption).
- Search: not from the book; the spreadsheet input "memory tiering" and the knowledge base line "Memory tiering serves memory beyond 1:1".
- Written as now: class-of-service-planning says tiering serves the memory beyond 1:1 of Silver (1.2:1) and Bronze (1.4:1). The calculator adds the tiering capacity on top: allocation supply = DRAM × class ratio + tiering. memory-tiering (Performance Best Practices 9.1) says not to overcommit on top of tiering: the ratio counts DRAM only, and the NVMe tier exists to avoid overcommit. The calculator default is 0 GB of tiering, so the default numbers are not affected.
- Question: with tiering on, which is meant? (A) the class ratio is served by tiering: allocation supply = max(DRAM × ratio, DRAM + tiering), no overcommit on top; (B) the ratio applies to DRAM and tiering adds on top (the calculator today); (C) tiering hosts run the class at 1:1 against DRAM + tiering.
- Proposed answer (expert call): (A). The tier replaces the ESXi reclamation that a ratio above 1:1 would otherwise need, so it is the same memory counted once. (B) counts the beyond-1:1 memory twice and goes against the vendor guidance; (C) drops the class difference.
- For you: (A), (B) or (C).
- Answer: None of (A)-(C). Memory tiering is not part of the overcommit ratio: NVMe is much slower hardware, likely 1,000x slower than DRAM. Tiering is not used in the capacity planning stage, but must be used in the actual (running) stage.
- Applied 2026-11-12: overcommit (Per resource), class-of-service-planning (allocation text, calculator inputs, misconception, image note "RAM against DRAM. Memory tiering is not in the ratio."), host-spec-from-class-of-service, capacity README (Two stages row), memory-tiering (Capacity management); harness/capacity.py and the capacity_plan tool no longer take memory_tiering_gb. The running-stage model: Q178.

### Q166 · ARCHITECTURE.md, section Troubleshooting questions · Code evaluates flow branches

- Files: [harness/flows.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/flows.py), [project/design-thresholds.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/design-thresholds.md).
- What the knowledge base says now: the flow tool serves step text; the model compares values and picks the branch.
- Question: (a) executable steps: the model extracts values into a case state, code compares them with catalog thresholds and picks the branch, the model explains; (b) keep as is.
- Proposed answer: (a), for 1.0, starting with the VM slow flow.
- Answer: Yes, (a) for 1.0.
- Applied 2026-11-12: Recorded in project/plan.md, M1 open work: executable flow steps (the model extracts values into a case state, code compares them with catalog thresholds and picks the branch), starting with the VM slow flow.

### Q138 · Part 2 > Proactive Operations > System Engagement · Good For row

- Files: [How VCF Operations reaches its users](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/system-engagement.md) (section Alerts, dashboards and reports compared).
- Search: "Export to spreadsheet or PowerPoint"
- Question: the Good For row reads Exception for alerts, Exception and Analysis for dashboards, and Exception for reports. Is Exception right for reports, or did you mean Summary or Trend?
- Written as now: Exceptions for reports, as in the source.
- Proposed answer (expert call): Trends.
  - The report is a passive channel, weekly or longer, read by IT leaders and finance. They read trends over weeks.
  - Depth already says Summary; Summary in Good for would repeat it.
  - An exception needs action within the day. One found in a weekly report can be 7 days old; the daily dashboard covers it.
  - Audit exception lists are covered by the row "Dashboard + Report work together".
  - Change if accepted: system-engagement table, Good for / Report = Trends; delete the review note.
  - For you: confirm Trends is what the row meant.
- Answer: IT leaders deal with urgency and the big picture, not with urgent items. The exception in a report is the important type: "important exception". They also read trends: add Trends.
- Applied 2026-11-12: system-engagement, table row Good for, Report column: Important exceptions and trends; review note deleted.

### Q087 · Part 1 > Purpose-Driven Architecture > Day 0 | Day 1 | Day 2 · Host specification example

- Files: [ESXi host specification from class of service and VM profile](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/host-spec-from-class-of-service.md); [Purpose-driven architecture: Day 2 first, business context, automation last, two sides of VCF](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/purpose-driven-architecture.md) (section Day 2 → Day 0 → Day 1); [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/noisy-neighbour.md) (sections Avoiding it, Maximum VM size).
- Search 1: "If 1 CPU typically uses 4 GB RAM, then a 64-core ESXi host will only need 256 GB."
- Search 2: "If you buy a 64-core ESXi, you have 56 cores left and you will be able to sell 224 vCPU."
- Search 3: "For Silver, you plan to overcommit 4:1 for CPU and 2:1 for memory."
- Search 4: "I’ve seen multiple customers having 32-node production clusters running 1K – 2K VMs."
- Question:
  - (a) Basis. Your Q079 answer: overcommit is per physical thread. Silver here is 4:1 per core (56 cores × 4 = 224 vCPU), which is 2:1 per thread. If Silver is meant as 4:1 per thread: 112 threads × 4 = 448 vCPU, 448 × 4 GB / 2 + 64 = 960 GB. Which is meant?
  - (b) Gold keeps no cores or RAM for vSAN, NSX and replication; Silver keeps 8 cores and 64 GB. With the same share, Gold is 56 vCPU and 224 + 64 = 288 GB. Should Gold keep the share too? And is Gold 1 vCPU per core (as here) or per thread?
  - (c) Silver memory overcommit is 2:1 here and 1.5:1 in the Noisy Neighbour table. Keep both as examples, or align them?
  - (d) The 32-node clusters with 1,000-2,000 VMs: a counter-example to the cap of 300 VMs per cluster failure?
- Written as now: the book's numbers, with the basis stated (4:1 per core = 2:1 per thread); Gold with the share shown as Claude's arithmetic; both memory ratios kept as examples; (d) stated without a verdict.
- Proposed answer ((a) settled by Q079, Q115 e, Q151; (b)-(d) expert call):
  - (a) Per thread. Keep the arithmetic, restate the ratio: 56 cores = 112 threads × 2:1 = 224 vCPU. 4:1 per core is 2:1 per thread.
  - (b) Gold keeps the share: vSAN, NSX, replication and kernel IO run on every host. Gold is 1:1 per thread: 112 vCPU × 4 GB + 64 GB = 512 GB. Gold's protection is the reservation and the low expected Thread Utilization, not one vCPU per core. Drop 256 GB (per core, no share).
  - (c) Align. This Silver is the non-production class ("Silver: suitable for non-production workloads"); its 4:1 per core and 2:1 memory are the capacity plan's Bronze. Same host (64 cores, 128 threads), share kept:
    - Gold (CPU 1:1, RAM 1:1): 112 vCPU, 512 GB.
    - Silver (2:1, 1.5:1): 224 vCPU, 661 GB.
    - Bronze (4:1, 2:1): 448 vCPU, 960 GB.
  - (d) Not a counter-example: 300 VMs per cluster failure is an example value, not a rule. 1,000-2,000 VMs per cluster means no blast-radius limit, traded for a smaller HA share (1 host in 32, not 1 in 5). At about 74 VMs per host (the 32-host, 2,357-VM cluster in cluster-utilization-vs-contention), a 300 cap means about 4 + 1 hosts. State the trade-off.
  - Change if accepted: host-spec-from-class-of-service (per thread; the three-class list replaces the per-core examples; remove "(book example)" and "The book picks", Q159); purpose-driven-architecture Example 2 (trade-off line).
  - For you: nothing.
- Partly settled by the author's edit (2026-11-11): host-spec-from-class-of-service now states overcommit per physical thread ((a)), and the noisy-neighbour memory table is removed ((c) no longer applies). Still open: (b) whether Gold keeps the infrastructure share; (d).
- Partly settled (author, 2026-11-11): CPU overcommit per class is final: Gold 1:1, Silver 2:1, Bronze 3:1 per physical thread.
- Partly settled by the author's working model (Capacity Planning Stage.xlsx, 2026-11-11): (b) every class keeps the infrastructure share: hypervisor overhead (14 threads, 64 GB on a 64-core, 768 GB host) is subtracted per ESXi host before any class. Still open: (d).
- Settled 2026-11-11: (a), (b), (c) (memory ratios from the spreadsheet: 1:1, 1.2:1, 1.4:1).
- Answer: (d) settled by the author's edit of purpose-driven-architecture (2026-11-11): the cap is a policy, not a rule. One cluster failure may affect at most N mission-critical VMs; the architecture states N, because a cluster can host thousands of VMs. Closed.

### Q099 · Part 1 > Service Level Agreement > Price & SLA · Silver ratios, notation and the 64-core licence

- Files: [Class of service: price, overcommit, SLA numbers, size limit and cluster design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/class-of-service.md) (section Planning example); [ESXi host specification from class of service and VM profile](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/host-spec-from-class-of-service.md) (section Silver at 3:1 CPU).
- Search 1: "For Silver, you decide on 3:1 CPU overcommit and no RAM overcommit"
- Search 2: "(67% of Gold)" and the cells "CPU 1:2", "RAM 1:1.5" in the same table
- Search 3: "Buying 64 cores maximizes your vSphere license"
- Question:
  - (a) The table gives Silver CPU 1:2 and RAM 1:1.5 (price 58% of Gold by the 50/50 rule); the text gives 3:1 and 1:1 (67%). Which is Silver?
  - (b) The book writes overcommit both ways (1:2 in two tables, 2:1 and 4:1 in the sample offering). The knowledge base writes N:1 (consumer : physical). Keep that?
  - (c) 768 GB = 64 cores × 3 vCPU × 4 GB is per core. Per thread (your Q079 rule) it is 1,536 GB. Which basis?
  - (d) VCF 9 is licensed per core with a 16-core minimum per CPU (Broadcom KB 313548); 64 cores no longer maximizes a licence. Drop the reason in the next edition?
- Written as now: Silver from the text (3:1, 1:1, 67%); N:1 notation; per core, flagged; licence reason replaced with the per-core rule.
- Related (2026-11-08, Capacity Management session): Q119 and Q120 (the capacity plan states CPU per thread: Silver 2:1, Bronze 4:1; memory 1.5:1 and 2:1). One answer can settle (b), (c) and Q120.
- Proposed answer ((b) settled: N:1 in capacity-dimensions; (c) by Q079, Q115 e, Q151; (a), (d) expert call):
  - (a) Silver = the table, read per thread: CPU 2:1, RAM 1.5:1, the capacity plan's set. Its "(67% of Gold)" fails the 50/50 rule: 0.5 × 1/2 + 0.5 × 1/1.5 = 58%. Drop the 3:1 / 1:1 text example as Silver. Bronze 4:1, 2:1 gives 37.5%. The rule gives the cost share; the 2x price gap is a goal (Q119), so a half-price Silver earns a lower margin than Gold.
  - (b) Keep N:1 (consumer : physical). The table's 1:2 is written 2:1.
  - (c) Per thread. Drop 768 GB. Silver on 64 cores (128 threads): 256 vCPU × 4 GB / 1.5 = 683 GB without the share; 661 GB with 8 cores and 64 GB kept (Q087). At 3:1 per thread: 1,536 GB.
  - (d) Drop the reason. VCF 9 is licensed per physical core, 16-core minimum per CPU (Broadcom KB 313548, read 2026-11-10): no sweet spot above 16. What licensing still decides: avoid CPUs under 16 cores (paid as 16); keep Hyper-Threading on (the licence counts cores, capacity counts threads); VCF entitles 1 TiB of vSAN per licensed core. Core count above that: Q111 (c).
  - Change if accepted: class-of-service (Planning example: plan values, 58%, 37.5%; Sample offering per thread); host-spec-from-class-of-service (remove Silver at 3:1; licence bullet = 16-core floor and Hyper-Threading).
  - For you: nothing.
- Partly settled by the author's edit (2026-11-11): Example 3 is 1.5:1 per physical thread ((c), per thread). Still open: (a) which ratios are Silver; (d) the 64-core licence reason, still in host-spec-from-class-of-service.
- Partly settled (author, 2026-11-11): CPU overcommit per class is final: Gold 1:1, Silver 2:1, Bronze 3:1 per physical thread. Applied in class-of-service (planning example: Silver 58%, Bronze 42% of Gold). Still open: (d) the 64-core licence reason.
- Answer: Settled 2026-11-11: (a) Silver is CPU 2:1 per physical thread with memory 1.2:1 (the author's final ratios and the spreadsheet); (b) N:1 notation; (c) per thread; (d) the knowledge base states VCF 9 per-core licensing with a 16-core minimum per CPU in host-spec-from-class-of-service; the book's 64-core reason is for the next edition.

### Q168 · vCenter API counters · gpu.mem.used on vSphere 8.x

- Files: [GPU monitoring](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/gpu/concepts/gpu-monitoring.md) (section Reading the counters).
- Search: not from the book. Follow-up to Q053, point 2.
- Written as now: on vSphere 9.0 and 9.1 `gpu.mem.used` is the frame buffer workloads touch, at or below `gpu.mem.reserved`. On 8.x the knowledge base says only that the rule does not hold.
- Question: on vSphere 8.x, what does `gpu.mem.used` count? (a) the allocated frame buffer, equal to reserved; (b) something else (please name it); and from which 8.x update did it change, or only from 9.0?
- For you: the 8.x behaviour from field experience.
- Answer: Closed 2026-11-11 by the author's rule (Q172): no knowledge of outdated releases; Agent E2 covers vSphere 9.x, and older releases are after 1.0 (plan, After 1.0). The 9.0 and 9.1 behaviour stays in gpu-monitoring.

### Q172 · Guest OS · Linux pressure stall information vs "no memory latency"
- Files: [Guest OS Performance (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/metrics/guest-os-performance.md) (section Reasons); [Windows memory management](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/memory/concepts/windows-memory.md) (section Free memory guidance); [Linux is slow](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/troubleshooting/linux-os-slow.md) (steps 2, 4, 5).
- Search: "Linux and Windows track memory space, throughput and IOPS, but not memory latency"
- Written as now: the Guest OS files say Windows and Linux do not measure how long work waits for memory. Linux has pressure stall information (/proc/pressure/cpu, memory, io): the share of time tasks stalled on CPU, memory or IO (https://docs.kernel.org/accounting/psi.html). The new Linux flow uses it; VMware Tools does not collect it, so VCF Operations does not show it.
- Question: (a) keep the statement for Windows only and add pressure stall information as the Linux exception, not collected by VMware Tools; (b) other.
- Proposed answer (expert call): (a).
- For you: whether your customers' Linux teams read pressure stall information, and whether the Linux counters in the new flow match what they use.
- Answer: Author (2026-11-11): deferred to after 1.0, as Linux is after 1.0. Two kinds of knowledge: theory is not limited by VMware Tools (Linux, Windows, Kubernetes); practical advice follows what each product can do, so Agent E2 must know exactly what VMware Tools collects. Linux knowledge starts at release 5.0; no older releases.

### Q173 · Class of service · Price and reservation after Bronze 3:1
- Files: [Class of service](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/class-of-service.md) (section Generic guideline); [Class of service in capacity planning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/class-of-service-planning.md) (section Example implementation, its image).
- Search: not from the book.
- Written as now: CPU overcommit per class is final at 1:1, 2:1, 3:1 per physical thread (2026-11-11), applied everywhere. Three values were set for Bronze 4:1 and are unchanged: the Generic guideline price 0.25x ("each step halves the price"); the Bronze reservation 12.5% CPU (Gold 50%, Silver 25%: each step halves); the class image, which still shows Bronze CPU 4:1 (recorded in corrections). The relative-value table keeps contention 4x and VM size 1x for Bronze while overcommit is now 3x.
- Question: (a) Bronze price: 0.33x (follows 1/3 overcommit) or keep 0.25x (a business choice, more margin pressure)? (b) Bronze CPU reservation: keep 12.5% or 1/6 (about 17%)? (c) Will you update the image?
- Proposed answer (expert call): (a) 0.33x: price follows the overcommit, which is the reason the guideline gives. (b) Keep 12.5%: a reservation protects against starvation and is not tied to the ratio; a lower value keeps Bronze from reserving the cluster. (c) Yes; until then the correction stays.
- For you: (a), (b), (c).
- Partly settled by the author's working model (Capacity Planning Stage.xlsx, 2026-11-11): (b) Bronze CPU reservation stays 12.5% with CPU 3:1. (a) Its note says price follows overcommit ("Bronze is 4x cheaper than Gold because it has 4x overcommit"), which with 3:1 gives 0.33x; the note still says 4x (Q174). (c) open.
- Answer: Author (2026-11-11): (a) Bronze price 0.33x (class-of-service, Generic guideline); (b) Bronze CPU reservation stays 12.5% (the spreadsheet); (c) the relative-value image is replaced by the author's new diagram. The class planning values image (reservation, allocation, contention, utilization) still shows the old ratios: Q175 (d).

### Q174 · Capacity Planning Stage.xlsx · Conflicts with the knowledge base, and four formula errors
- Files: [project/sources/Capacity Planning Stage.xlsx](https://github.com/e1-rahabok/agent-e2/blob/main/project/sources/Capacity%20Planning%20Stage.xlsx) (read-only); [Class of service in capacity planning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/class-of-service-planning.md); [Class of service](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/class-of-service.md).
- Search: sheet Capacity Provider, cell C71 "Overcommit Ratio (against DRAM)"; sheet Capacity Consumer, cell B52 "Overall Planned Consumption"; sheet Read Me, cell B29 "How many VM will fit on a typical ESXi".
- Written as now: the knowledge base gives memory overcommit Silver 1.5:1 and Bronze 2:1 (class image); the spreadsheet gives 1.2:1 and 1.4:1.
- Question:
  - (a) Memory overcommit: the spreadsheet (Gold 1:1, Silver 1.2:1, Bronze 1.4:1) or the knowledge base (1:1, 1.5:1, 2:1)?
  - (b) Utilization model, rows Overall Planned Consumption (M52, N52, M61, N61, M70, N70): (demand + hypervisor overhead) / usable capacity. Usable capacity already excludes the overhead (114 = 128 − 14 threads; 704 = 768 − 64 GB), so the overhead is counted twice. Scenario 2 memory reads 102% instead of 93%; scenario 3 CPU 101% instead of 89%. Use demand / usable?
  - (c) Read Me, the 6-number answer: G36 (memory reservation) and G37 (memory utilization) divide the allocation-model memory (E35, 844.8 GB with 1.2:1 overcommit) instead of the reservation and utilization usable memory (704 GB). Corrected: G36 = 704 / 16 = 44; G37 = 704 / 27.2 = 25.9. The answer becomes 25.9 VMs, bound by memory utilization, not 26.4 by memory allocation.
  - (d) Capacity Provider B60 says Bronze is 4x cheaper because of 4x overcommit; F68 is 3.
  - (e) Read Me C14-C15 and the closure diagram say "Performance SLA". The 2026-11-11 decision: no performance SLA; performance is managed by the KPI. Reword to the KPI?
  - (f) The named range ESXi.CPU.Usable.Capacity.Allocation points to #REF! (unused).
- Proposed answer (expert call): (a) the spreadsheet: it is the newest model and already carries Bronze 3:1; then class-of-service and class-of-service-planning change to 1.2:1 and 1.4:1, and the price example becomes Silver 67%, Bronze 52% of Gold. (b), (c), (d), (f): fix in the spreadsheet. (e) KPI.
- For you: (a); fix the spreadsheet, since project/sources is read-only for Claude.
- Answer: Author (2026-11-11): the spreadsheet is fixed ((b) overhead no longer counted twice; (c) the Read Me answer reads 25.9; (d) B60 says 3x; (e) KPI, not Performance SLA; (f) broken name removed); memory overcommit follows the spreadsheet: Gold 1:1, Silver 1.2:1, Bronze 1.4:1, with CPU 1:1, 2:1, 3:1. Applied in class-of-service, class-of-service-planning, the catalog rows planning-*, and harness/capacity.py, which reproduces the spreadsheet's three scenarios and the Read Me answer.

### Q127 · Part 1 > Performance | Capacity vs Capacity Model > Demand · Reservation: supply or demand side

- Files: [Performance vs capacity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/performance-vs-capacity.md) (section Usable capacity exists only in capacity), [Capacity dimensions](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/demand.md) (section Demand).
- Search 1: "Demand = Max (Utilization, Reservation)"
- Search 2: Performance Management chapter, Performance | Capacity, the usable capacity diagram.
- Question: performance-vs-capacity says capacity subtracts HA, buffer, hypervisor overhead and reservation from total capacity. This chapter puts reservation on the demand side: demand = Max (utilization, reservation), per VM, against usable capacity. Subtracting it from supply as well counts it twice. Remove reservation from the usable capacity sentence?
- Written as now: both files as they are.
- Proposed answer (expert call): yes, remove reservation from the usable capacity sentence. Reservation is demand, not supply.
  - Demand = Max (Utilization, Reservation), per VM, then summed. Subtracting it from supply as well counts it twice. Example: 100 GHz usable; a VM uses 4 GHz with 5 GHz reserved. Demand side only: 95 GHz left. Both sides: 95 − 5 = 90; 5 GHz reserved takes 10 GHz of room.
  - Same logic as the hypervisor in the utilization model: its load is in demand, so it is not subtracted from supply.
  - Supply: Usable = Total − HA − Buffer; hypervisor overhead subtracted in the allocation model only. The pack's Usable Capacity leaves reservation out too.
  - Reservation keeps its own dimension, reserved against capacity (admission control; Cluster Risk reservation rows). The cluster is full at the first of utilization, allocation or reservation.
  - New text: "Capacity subtracts HA, buffer and hypervisor overhead from total capacity, and counts reservation in demand. Performance ignores all four."
  - Change if accepted: performance-vs-capacity, Usable capacity exists only in capacity.
  - For you: nothing.
- Answer: From the author's working model (project/sources/Capacity Planning Stage.xlsx, 2026-11-11): reservation is its own model, compared against the reservable capacity (CPU 64 cores × 2.5 GHz − 10 GHz system reservation = 150 GHz; memory DRAM minus hypervisor = 704 GB), not subtracted from the supply of the utilization model. Applied: performance-vs-capacity, section Usable capacity exists only in capacity.

### Q062 · Operations flows · Is this host or cluster healthy right now

- Files: [ESXi: what to monitor, in priority order](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/esxi/health-check/esxi-health-check.md); [vSphere cluster: what to monitor, in priority order](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/health-check/cluster-health-check.md).
- Search: not from the book.
- Question: what is your daily health check of an ESXi host and of a cluster, in order? The overview files list what to monitor, but not the order of checks with a stop at each step. With your order, a health-check flow can be written for each.
- Written as now (2026-11-08): the three overview files are now health checks ([ESXi: health check](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/esxi/health-check/esxi-health-check.md), [vSphere cluster: health check](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/health-check/cluster-health-check.md), [VM: health check](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/health-check/vm-health-check.md)) with numbered steps in the order of health-risk-efficiency. The order inside each pillar is still Claude's.
- Partial answer (author, in session, 2026-11-08): "what to monitor" is a health check; troubleshooting is part of the health check and comes only after an object fails it (monitor is the what, troubleshoot is the why); availability flows, security and compliance are future, after 1.0. Still open: your order inside each pillar, and Q133.
- Proposed answer (pillar order settled by Q104, Q105 b, Q133 b and the 2026-11-09 decisions; order inside each pillar: expert call):
  - Settled: availability, performance, security, capacity. Performance: contention, consumption, configuration, known bug, log. Capacity: consumption, configuration, contention, inventory. Configuration is the drill-down. About 5 minutes when there is no problem.
  - Stop rule: an availability failure stops that object's check. A performance failure opens its troubleshooting flow; the check then goes on to capacity.
  - ESXi: performance = ESXi Performance (%), the failing sub-metric, consumption (Core and Thread Utilization, memory state, path and vmnic throughput), configuration (power, BIOS). Capacity = memory state and hot host only, then hand over to the cluster (a host is sized as part of its cluster). Today's steps 4-6 move from capacity into performance consumption.
  - Cluster: performance = Cluster Performance (%), balance (hot host), contention flow, configuration (resource pools, limits). Capacity = Consumption, Risk, Close for Business, inventory, efficiency. Step 3 (SLA and SLI) removed 2026-11-11: no SLA or SLI in operations; the daily check reads the KPI. The cluster health check now has 7 steps.
  - VM: add consumption (VM, then Guest OS) after contention, as vm-slow step 4, so both share one performance order.
  - Daily run is top down: clusters worst first, then hosts, then VMs.
  - Stale text: proactive-operations, Day-to-day order, lists three pillars; add capacity (Q133 b).
  - Change if accepted: the three health checks (steps, diagrams); proactive-operations.
  - For you: which VCF Operations dashboards you open each morning, and in what order.
- Partly settled by the author's edit (2026-11-11): the ESXi health check has no efficiency step; waste is read on the cluster, because DRS and HA move VMs between hosts. Still open: the order inside each pillar.
- Answer: Author (2026-11-11): agrees with the proposed answer; the VCF Operations dashboards of the daily check are after 1.0. Applied: ESXi health check (performance = KPI, failing sub-metric, consumption, configuration; capacity = memory state and hot host, then the cluster); cluster health check (performance = KPI, balance, configuration; capacity = consumption and risk, closure, inventory and efficiency); VM health check (consumption after contention, 9 steps); sp5-framework/concepts/health-check, section Running the daily check (top down, stop rule); proactive-operations day-to-day order adds capacity.

### Q116 · Part 1 > 4 Dimensions of Capacity > Utilization · Zones vs Cluster Consumption bands

- Files: [Capacity dimensions](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/demand.md) (section Utilization), [Cluster Consumption (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-consumption.md), [thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml) (rows cluster-utilization-usable-wastage, cluster-utilization-usable-best).
- Search: "I divide the capacity into 10 equal chunks"
- Question: the book puts 40-80% of usable capacity in green and 80% as best. Cluster Consumption (%) has CPU green 0-55, yellow 55-70, orange 70-85, red 85-100, and memory green 0-70. A 10-host N+1 cluster at the best 80% of usable is 72% of total: orange on CPU in Cluster Consumption. (a) Is Cluster Consumption measured against total or usable capacity? (b) Which governs? (c) Give values for yellow, orange and red above 80%. (d) Should Cluster Consumption get a grey band (0-40%) for wastage? The plan lists grey values for capacity bands as open.
- Written as now: zones as rules (grey below 40%, best 80%); Cluster Consumption bands unchanged.
- Proposed answer ((a) settled by the pack's Cluster Consumption page; (b)-(d) expert call):
  - (a) Usable. Usable = Total − HA − Buffer; CPU in threads, memory in DRAM. 80% of usable reads 80, not 72.
  - The bands quoted are the sub-metric rows (catalog `cluster-consumption-*`), matching the pack. The score has its own bands: pack 25/50/75; closure since Q121 orange above 60, red above 80 (see Q132).
  - (b) In a running cluster, the pack's sub-metric bands set the colour. At 80% of usable: CPU orange, memory at the yellow edge. The 80% best fits memory (capacity plan: Gold RAM about 80%), not CPU threads (Gold about 50%, Silver below 70%). Keep 80% in prose; drop catalog row `cluster-utilization-usable-best` (two verdicts for one value).
  - (c) No new numbers: the pack has them. Memory orange 80-90, red 90-100. CPU threads orange 70-85, red 85-100.
  - (d) Yes, on the two utilization rows, not the score: below 40% of usable is dark grey (Q148). The score blends in saturation, so no score value means 40%. Exceptions: a growing new cluster, DR capacity. Grey is an efficiency reading; the pack still shows green.
  - Also: benchmark question 0076 computes 99% × 11/12 against total; the row is against usable.
  - Change if accepted: cluster-consumption (usable; score vs sub-metric bands); catalog (grey below 40 on the two utilization rows; remove `cluster-utilization-usable-best`); capacity-dimensions Utilization; question 0076.
  - For you: how long utilization stays below 40% before it counts as wastage; whether the 80% row leaves the catalog.
- Answer: Author (2026-11-11): capacity-dimensions fixed by the author: no 10 equal chunks, because zones depend on the object type and, within it, on what is sized (CPU, memory, storage); utilization renamed consumption (utilization and saturation); diagrams replaced. Applied: the zones image archived; catalog rows cluster-utilization-usable-wastage and cluster-utilization-usable-best archived (project/archive/catalog-rows-cluster-utilization-usable-2026-11-11.yaml); the planning and operating diagram and the closure diagram replaced; the stale review note in cluster-consumption deleted. Closed: (b) to (d) no longer apply; question 0076 computes the memory HA ceiling against host memory, which is correct for ballooning.

### Q061 · Operations flows · Can this cluster take more VMs: your order of checks

- Files: [Can this cluster take more VMs?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms.md) (sections Checks, in order; Why this order).
- Search: not from the book. Drafted from the capacity model, Cluster Performance, Cluster Risk, Cluster Consumption, admission control and host memory states.
- Question:
  1. Is this your order: cluster state and HA, contention today, Cluster Risk, room after HA and buffer, fit of the new VMs (reservations, overcommit, monster size), balance?
  2. Which resource do you find fills first in practice, and does that change the order?
  3. How do you state the answer to the requester: a yes/no, a number of VMs, or a date?
- Written as now: 6 steps, status draft.
- Proposed answer (steps 2-5 settled by Q120-Q122; the rest expert call):
  - (1) Order: steps 2-5 settled. Step 1 (cluster state, HA) stays first: if HA failover capacity is not met, usable capacity is wrong and every later number with it. Add a planning gate before step 2: a cluster with no running history uses the class-of-service overcommit ratios tied to price, not Cluster Risk (Q120). Step 6 adds storage (new VMs' provisioned disks against datastore free space): the flow tags storage but no step reads it. Balance stays last.
  - (2) Corrected 2026-11-11. The earlier answer ("memory, in most enterprise server clusters") read utilization as fullness: a Level 300 mistake. Memory is a cache: high Consumed is expected and wanted, and an ESXi host can show ballooned, compressed and swapped memory with 0% memory contention. A resource is full when its contention rises, not when its utilization or its reclamation counters do.
    - Overcommitted cluster: the binding resource is the one whose contention worsens first in Cluster Performance (%): CPU Ready and Co-stop, memory contention, disk latency, dropped packets. Not Consumed, ballooned or swapped memory.
    - Expected (expert call): CPU contention shows first. Ready and Co-stop appear as soon as vCPUs compete for threads; memory contention appears only when a reclaimed page is touched again.
    - Cluster without overcommit (1:1, Gold): allocation and reservation fill first, by design; utilization does not decide (step 3). Memory binds first here only because it is allocated, not because it is used.
    - Storage: datastore space and disk latency (vSAN after 1.0).
    - The order of steps does not change: each step reads all resources; the answer names the binding resource and the dimension (allocation or contention).
  - (3) State: yes or no; the number of VMs of the requested profile (vCPU, memory, disk, class) that fit before the binding resource reaches its limit, against usable capacity; the limiting resource and dimension; Time Remaining as a date (it ignores committed demand); what changes the answer (hosts, reclamation, VM design). In 1.0 the count comes from usable capacity arithmetic, not a what-if of the scores (2026-11-10).
  - Applied 2026-11-11: trap in can-cluster-take-more-vms (ballooned, compressed or swapped memory is not a full cluster).
  - Change if accepted: can-cluster-take-more-vms (planning gate, storage in step 6, How to read the result).
  - For you: which contention counter you see move first in your customers' overcommitted clusters.
- Answer: Author (2026-11-11): the flow depends on whether the customer maximizes utilization. Not maximizing: VCF Operations' built-in Capacity Remaining (%) and Time Remaining (days) are sufficient, the first and basic answer. Not maximizing and not trusting these numbers: why they differ is a VCF Operations product topic, outside Agent E2 1.0. Maximizing: the model in sp5-framework/capacity/capacity-dimensions. Applied: can-cluster-take-more-vms step 1 (goal); old steps 1-7 are steps 2-8; the new closure diagram and the impact of additional workload added to step 7.

### Q060 · Operations flows · Users say the VM is slow: your order of checks

- Files: [Users say the VM is slow: triage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/troubleshooting/vm-slow.md) (sections Checks, in order; Why this order). Review: [project/review-2026-11-06.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/review-2026-11-06.md), section 3.3.
- Search: not from the book. Drafted from the VM overview file and the per-resource flows.
- Question:
  1. Is this the order you follow in the field: time window, breadth (many VMs?), VM contention per resource, Guest OS queues, then context (limits, snapshots, vMotion)?
  2. What do you check that is missing, for example the application team's own evidence, or a recent change?
  3. Is the SLI bar (Ready 2.5%, memory contention 1%, disk latency 10 ms, transmit dropped 0%) the right first bar for one VM, or do you use other values?
- Written as now: 5 steps, status draft. It hands over to the existing CPU, memory, storage, network and cluster flows.
- Proposed answer (updated 2026-11-11: no SLA, no SLI; (1) settled by the 2026-11-09 rewrite; (3) by your 2026-11-11 decision; (2) expert call):
  - (1) Settled. vm-slow now runs: time window, breadth, contention (KPI), consumption (VM and Guest OS), configuration, known bug, log.
  - (3) Settled: no SLI. The first bar for one VM is the VM KPI: VM Performance (%) and the sub-metric that pulls it down, at the 20-second peak in the complaint window (VirtualMachine rows of `kpi` in [knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml): Ready, Co-stop and Overlap of the worst vCPU, memory contention, disk latency of the worst virtual disk, transmit dropped packets). The SLI rows and the Performance SLA are removed from the catalog. If the user cites an SLA, ask its metric and object: it does not change the bar, and it is often on the wrong object (the cluster, not the VM).
  - (2) Additions:
    - Step 1 adds "since when, and what changed": change records in the window, vCenter tasks and events (reconfigure, vMotion, upgrade, snapshot), against the same window on a normal day. Today a recent change surfaces only at step 7 (log), yet it is the cheapest lead.
    - Step 2 (breadth) adds the other tiers of the same application: an application is as slow as its worst tier, active node only (Q092). The VM the user names is often not the slow tier.
    - Symptom: unreachable or failing is down, the availability process, not this flow (Q105 c).
    - The application team's evidence (which transaction, its response time, its errors) is input to step 1.
  - Change if accepted: vm-slow (Symptom, steps 1 and 2, trap "the VM the user names is the slow one"); delete the review note.
  - For you: what you ask the application team first.
- Answer: Author (2026-11-11): users rarely tell the Guest OS from the VM, so the first step is to ask the application team to quantify the slowness in the Windows or Linux counters they can see; developers have no access to vSphere or Kubernetes metrics. Guest OS counters belong outside the VM, so they leave step 4 (consumption). Applied: vm-slow step 1 hands over to two new flows, guest-os/system/troubleshooting/ms-windows-slow and guest-os/system/troubleshooting/linux-os-slow; VM consumption reads VM counters only; 8 steps.

### Q171 · Scope · Generic public cloud in the SP5 Framework
- Files: [IaaS as a service](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/iaas-business.md) (lines on cost target, consumer layer, provider layer); [Class of service](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/class-of-service.md) (free tier); [Rightsizing VMs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/rightsizing.md) (cost row; public cloud providers and oversizing); [Capacity dimensions](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/demand.md) (section Overcommit, public cloud reference); [Health, risk and efficiency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/health-risk-efficiency.md) (section Efficiency, cost); [Business, application and IaaS layers](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/realms-and-layers.md); [Dashboards for IT leaders](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/it-leaders-dashboards.md) (overcommit ratio).
- Search 1: "Customers usually aim at half the public cloud price"
- Search 2: "Public cloud free tiers are smaller"
- Search 3: "Public cloud providers have no oversizing problem"
- Written as now: named competitor vendors and products are removed (2026-11-11: AWS, Azure, EC2, Nutanix, KVM). About 14 lines still name the public cloud as a category: as a price target for the IaaS business, as a reference for overcommit and free tier sizes, and as a statement about public cloud providers' motives. VMware offerings on a hyperscaler (VMware Cloud on AWS, Azure VMware Solution) stay: they are VCF.
- Question: the public cloud is a competitor of the private cloud. Do these lines stay? (a) keep the public cloud as a price and service benchmark for the IaaS business, and remove the lines on what public cloud providers sell or why (free tier sizes, CPU 1:1 reference, the oversizing motive); (b) keep all; (c) remove all.
- Proposed answer (expert call): (a). Pricing a private cloud against the public cloud is part of running IaaS as a business, which the SP5 Framework teaches; facts about a provider's offering go stale and invite comparison Agent E2 should not make.
- For you: (a), (b) or (c).
- Answer: Author (2026-11-11): (a). Applied: lines on public cloud free tier sizes, the CPU 1:1 reference, the oversizing motive, the free tier made slower on purpose, and the 40-vCPU instance removed; public cloud as a price and service benchmark kept.

### Q167 · MISSION.md, section 1 · Mission sentence and outcome metric

- Files: [MISSION.md](https://github.com/e1-rahabok/agent-e2/blob/main/MISSION.md), [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md) (Mission).
- What the knowledge base says now: scope worded four ways; target 99% in the headline; no user-outcome metric.
- Question: (a) one scope sentence; claim = beats frontier models used alone, stretch = matches frontier with the knowledge base; 99% moved to the 300-question plan; add one outcome metric (right root cause on real tickets in the live test); (b) keep.
- Proposed answer: (a).
- For you: the scope sentence.
- Answer: Author (2026-11-11): closed. MISSION.md edited directly by the author.

### Q164 · benchmark/design.md, sections 1 and 8 · What "frontier model" means in the claim

- Files: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), [benchmark/models.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/models.md) (section 5).
- What the knowledge base says now: one frontier reference, baseline mode, no web search, no extended thinking.
- Question: (a) best of 3 vendors, as shipped (web search and thinking on), plus frontier with the E2 knowledge base as the ceiling; (b) keep one reference; (c) other.
- Proposed answer: (a). One model without its product features invites the strawman charge.
- Answer: Author (2026-11-11): only Claude Opus 5.5 is tested, because the whole application is built with Claude. Web search on (Claude Opus has it). Effort capped at medium, for the cost of the subscription. Applied in benchmark/models.md, section 5. Closed.

### Q163 · Plan, Decisions 2026-11-06 · Benchmark before M1 and M2 are complete

- Files: [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md) (Not doing), [project/review-2026-11-11.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/review-2026-11-11.md) (section 5).
- What the knowledge base says now: no benchmark run until the 100 questions and the knowledge base are complete. Last run 2026-11-03, 17 questions.
- Question: (a) run the 70 scorable questions now as a development signal: 1 candidate and the frontier reference, 3 modes, 5 runs, about US$ 20-40; (b) keep the 2026-11-06 decision.
- Proposed answer: (a). Every change since 2026-11-03 is unmeasured.
- Answer: Author (2026-11-11): (b). Absolutely no benchmark until development is done. Closed.

### Q170 · KNOWLEDGE-ENGINEERING.md, section 5.1 · Home of the misreadings

- Files: [harness/misreadings.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/misreadings.md); [KNOWLEDGE-ENGINEERING.md](https://github.com/e1-rahabok/agent-e2/blob/main/KNOWLEDGE-ENGINEERING.md), section 5.1; [ARCHITECTURE.md](https://github.com/e1-rahabok/agent-e2/blob/main/ARCHITECTURE.md), section 8, Ingest.
- Search: not from the book.
- Written as now: the 12 misreadings are VMware knowledge, given to the agent up front, and live in `harness/` since 2026-11-07, so that search never returns the one-line summary in place of the file with the mechanism.
- Question: should the misreadings move into `knowledge/`, so all the domain knowledge you review has one home? (a) move to [knowledge/misreadings.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/misreadings.md), with ingest skipping that one file; (b) keep in `harness/`, documented as knowledge in section 5.1 (done).
- Proposed answer (expert call): (a). Your review scope is `knowledge/`; a misreading reaches every answer, so it needs that review more than any metric file. `knowledge/` already holds content that is not indexed as prose (the catalog), so "in `knowledge/`" does not have to mean "searched". Cost: one ingest exclusion in [harness/kb.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/kb.py), the primer path, lint, docs; retrieval check before and after (expected unchanged, since the file stays out of the index).
- For you: accept (a), or keep (b).
- Answer: Author (2026-11-11): yes, move into `knowledge/`. Applied: [knowledge/misreadings.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/misreadings.md), skipped by ingest ([harness/kb.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/kb.py), `NOT_INDEXED`).

### Q169 · KNOWLEDGE-ENGINEERING.md, sections 5 and 10 · Single-pillar flows filed as health checks

- Files: [Can this cluster take more VMs?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms.md), [Does this ESXi host have CPU headroom?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/decision-tree/host-cpu-capacity-headroom.md), [Downsizing a large, idle VM](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/decision-tree/oversized-vm-downsizing.md); rule: [KNOWLEDGE-ENGINEERING.md](https://github.com/e1-rahabok/agent-e2/blob/main/KNOWLEDGE-ENGINEERING.md), section 5 (Placement rules, Flows) and section 10; concept: [Health check](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/health-check.md).
- Search: not from the book. Follows your statement of 2026-11-11: a health check is done on a system or object, never on one pillar.
- Written as now: the repository rule (section 5, Flows) lets [Health check](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/health-check.md) hold single-pillar flows ("is it full, is it wasteful"). The three files above are capacity or efficiency only, so their folder calls them health checks. can-cluster-take-more-vms now says it is a capacity decision used by the cluster health check, not a health check. The Harness finds flows by the folder names [Health check](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/health-check.md) and `troubleshooting/` (harness/flows.py, primer flow index, lint flow map).
- Question: where do single-pillar flows go? (a) a third flow kind, folder `decision/` (for example `sp5-framework/capacity/decision/can-cluster-take-more-vms`), run by the flow tool like the other two; (b) keep them in [Health check](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/health-check.md) and accept the name; (c) fold each into its object health check as a step.
- Proposed answer (expert call): (a). The folder name is read by the Harness and shown to the model in the flow index: a capacity question labelled health check teaches the wrong concept. (c) loses the standalone question ("can this cluster take 20 more VMs?"), which users ask on its own. Cost of (a): 3 ids moved (moved.yaml), `decision` added to tags.yaml and the flow folders, a retrieval check before and after.
- For you: accept (a), or choose (b) or (c).
- Answer: Author (2026-11-11): "decision" is wrong: a decision records something done. Use decision-tree or operational-question. Can a cluster take more VMs is not a health check; many operational questions are not. A health check is always on an object type, never on a technology; a parent's health includes its children's unless a realm separates them (Guest OS slowness is not ESXi health). Applied: folder `decision-tree/` (not operational-question: every flow answers an operational question, health checks and troubleshooting included; decision tree names what this kind does, branch to a choice to act). can-cluster-take-more-vms moved to `vsphere/object-types/cluster/decision-tree/` (vSphere only, so not sp5-framework); host-cpu-capacity-headroom and oversized-vm-downsizing to `vsphere/technology/cpu/decision-tree/`. Health check concept, VM health check (Guest OS step removed: separate realm), KNOWLEDGE-ENGINEERING.md, harness, lint and REPOSITORY-MAP.md updated.

### Q059 · Agent · Core rules and confusable pairs given to the agent up front

- Files: [harness/misreadings.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/misreadings.md) (Level 300 misreadings; moved out of the knowledge base 2026-11-07); [Terminology](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md) (section Confusable pairs); design: [harness/AGENT.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/AGENT.md), section 3.
- Search: not from the book. Each rule and pair summarises the knowledge file it points to.
- Question:
  1. Are these the 12 rules an expert would give a new colleague first? Which would you drop, add or reword?
  2. Are the 8 confusable pairs right, and is any pair missing?
- Written as now: drafted by Claude 2026-11-06, status draft. The agent receives them only when the switches are on (all off by default).
- Proposed answer (expert call). Now 12 rules and 28 pairs (not 8). The five up-front blocks total 2,997 of 3,000 tokens: every addition needs a cut.
  - Rules: keep 1, 2, 5, 7, 10, 11.
  - Reword 3: "Utilization is not contention ...". "Saturation" already names a metric type (Cluster Consumption, availability step); one word, one meaning.
  - Reword 4: add "an ESXi Ready value is a sum or average of its VMs: read the worst VM".
  - Reword 8: "Memory is a cache: high Consumed is normal and is not demand; Active is not a capacity counter" (Q115 b, c).
  - Reword 9: "... convert with the interval and the vCPU count, and read Ready against Run". Broadcom KB 419238 and 386180 give a Ready bar of 5% or 10% without either.
  - Drop 6: it repeats the pair Run vs Used.
  - Drop 12: a flow heuristic; the flow carries it.
  - Add: "A vCPU runs on a thread: overcommit ratios are per thread; 4:1 per thread is 8:1 per core" (Q079, Q151).
  - Add: "Capacity is read against usable capacity; contention overrides utilization: a cluster at low utilization can be full."
  - Pairs, 28 to 20: drop those a rule covers (Reservation vs usage, VM vs Guest OS, VM CPU Ready vs Latency); merge Consumed vs Active with Guest OS In Use vs VM Consumed; merge Storage vs disk with Device vs disk vs LUN; move four rare pairs (Consistency vs compatibility, Health check operations vs Kubernetes, Metric vs property, Inventory vs configuration) to a new glossary section "Other distinctions" (still indexed; the primer reads only Confusable pairs). Add Core Utilization vs Thread Utilization. Add to the Latency row: "network: no VM latency counter; read dropped packets". Frees about 300 tokens (measure with lint).
  - Change if accepted: harness/misreadings.md; glossary (Confusable pairs, Other distinctions); harness/AGENT.md section 3.
  - For you: whether your own top 12 for a new colleague differs.
- Answer: Author (2026-11-11), in chat and by editing harness/misreadings.md: terminology is the overall structure; an entry may have synonyms and confusable pairs. Misreadings hold only Level 300 mistakes a frontier model makes, never a duplicate of the glossary, never Level 100. Review every pair: add, remove, correct. Author's misreadings edit kept (rule 12 dropped; ESXi CPU Utilization for capacity, memory as a cache, overcommit per thread added).
- Applied 2026-11-11: [Terminology](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md) is one entry per term (meaning; Also called; Not to confuse with; File), grouped by area; tables Synonyms, Defined terms and Confusable pairs merged into it; duplicate rows (KAI, KSI, Symptom, Consumed CPU) merged. Pairs 28 to 17 (counted, not row numbers): 13 removed (2 of them by the author on main, d791a29), 2 merges, 4 added; the list with reasons is in [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md), decision 2026-11-11, terminology. [harness/misreadings.md](https://github.com/e1-rahabok/agent-e2/blob/main/harness/misreadings.md): the two Consumed lines merged, the summation line dropped (Level 200; the catalog and calculate tools cover it), files added to the Utilization and overcommit lines, grammar. Rules: [KNOWLEDGE-ENGINEERING.md](https://github.com/e1-rahabok/agent-e2/blob/main/KNOWLEDGE-ENGINEERING.md), section 11.2. No section 'Other distinctions': it was a way to keep rare pairs out of the up-front block; the pair tests remove them instead.

### Q095 · Part 1 > Service Level Agreement > SLA Calculation · Pass scored as 0%, and partial VM scores

- Files: [IaaS SLAs: what each measures and how it is computed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/sla-metrics.md) (section SLA calculation); [Cluster SLA and SLI, archived 2026-11-11](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/knowledge/cluster-sla-sli.md) (section Cluster SLI).
- Search 1: "If VM CPU Ready > 2.5% then 100% else 0%"
- Search 2: "So, every 5 minutes, a VM gets a score of 100% or 75%"
- Search 3: "Since SLA is binary, this is simply counted as failure"
- Question:
  - (a) As written, a breach scores 100% and a pass 0%, so a good month averages near 0%, not 99.9%. Should all four lines read "If ... > threshold then 0% else 100%"?
  - (b) The VM SLI is the average of four pass/fail values (100, 75, 50, 25, 0). Penalty Quantification says there is no partial failure. Which holds for the VM: (A) partial, one counter breached = 75% for that interval; (B) binary, any counter breached = 0% for that interval?
  - (c) The Cluster SLI file says a VM must pass all four (option B), while its formula counts breaches divided by 4 (option A). Which should both files say?
- Written as now: pass = 100%; VM SLI = average of the four (option A); Cluster SLI file unchanged, flagged.
- Proposed answer (settled by the 2026-11-10 decision "SLI is binary: a fail is a fail"):
  - (a) Yes: "If X > threshold then 0% else 100%". sla-metrics already has it right.
  - (b) B, binary. Option A brings back, one level up, the partial failure that Penalty Quantification rules out. Arithmetic: Gold 99.9% in a 28-day month (8,064 intervals) allows 8 failed intervals. Under A, CPU alone could fail 32 times (32 × 25% = 8) and still pass. VM SLI = 100% if all four counters pass, else 0%.
  - (c) B in both files. Cluster SLI (%) = 100 × (running VMs and pods with no breach) / (running VMs and pods). The current formula counts breaches: 1 VM with 4 breaches equals 4 VMs with 1 breach each. Under B that is 1 failing VM against 4. This matches the Cluster SLA (share of VMs that fail).
  - Change if accepted: sla-metrics (SLA calculation), cluster-sla-sli (Cluster SLI formula; remove "Normalized by actual breaches"); delete both review notes.
  - For you: whether the shipped Cluster SLI metric in the pack changes to count VMs with zero breaches.
- Answer: closed 2026-11-11. The SLI and the Performance SLA are removed (author: the SLA is a business contract; the KPI is enough). Nothing left to fix.

### Q020 · Chapter 3 Memory > ESXi · Consumed and compressed

- Files: [ESXi Memory Consumed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/host/consumed.md)
- Search 1: "It only includes the resultant zipped, not the amount subjected to compression"
- Search 2: "Consumed does not include compressed"
- Question: does host Consumed include the compressed result in DIMM?
- Written as now: includes the result, flagged. Your diagram (physical view) also shows it inside Consumed.
- Proposed answer (expert call, from the vSphere 9.1 documentation):
  - Yes. ESXi Consumed includes the compressed result: the compression cache holding the zipped pages in DRAM. It excludes what compression freed.
  - Mechanism: host Consumed = total host memory − free host memory (vSphere Web Services API 9.1, `mem.consumed`). Cache pages are ESXi pages in use, not free. Each VM's cache is capped by Mem.MemZipMaxPct (default 10% of its memory).
  - The VM side agrees: esxtop CNSM excludes "the amount of memory saved if some of the VM memory is compressed". Only the saving leaves Consumed.
  - The two search strings conflict in wording only. Read Search 2 as "Consumed does not include the memory compression freed". The chart (Compressed and swap-out up about 200 GB while Consumed falls) shows the saving plus swap-out, not the cache outside Consumed.
  - Counter names per tool: esxtop CACHEUSD (per VM) = result held in DRAM; vCenter `mem.compressed` (VM and host), `mem.zipped` and `mem.zipSaved` (VM only). The 9.1 API summary of `mem.compressed` is a copy error ("Amount of memory reserved by userworlds").
  - Sources: vSphere 9.1 documentation (Memory Compression; esxtop Memory panel: CNSM, CACHESZ, CACHEUSD); https://developer.broadcom.com/xapis/vsphere-web-services-api/9.1/memory_counters.html
  - Change if accepted: host consumed (state as fact; "a Consumed drop while Compressed rises is the saving"); host compressed (counters per tool, API copy error). Side fix: virtual-motherboard consumed says a 4 KB page compressed to 1 KB frees "0.75 KB"; it frees 3 KB.
  - For you: nothing. Optional live check: on a host that is compressing, compare vCenter Compressed with the sum of esxtop CACHEUSD.
- Answer: agree with the proposed answer.
- Applied 2026-11-11: host consumed (Formula: compression cache inside Consumed, only the saving leaves; Behaviour: a Consumed drop while Compressed rises is the saving; trap); host compressed (Meaning: the result in DRAM, Mem.MemZipMaxPct cap; new section Counters per tool; API copy error; traps); virtual-motherboard consumed (a 4 KB page compressed to 1 KB frees 3 KB, not 0.75 KB). Live check of host Compressed against the sum of CACHEUSD kept in review_notes.

### Q053 · vCenter API counters · gpu.mem.reserved vs gpu.mem.used

- Files: [GPU monitoring](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/gpu/concepts/gpu-monitoring.md) (sections Counters, Reading the counters, vGPU capacity).
- Search: not from the book. Counters and vCenter 9.1.0 API summaries, on ClusterComputeResource and ResourcePool, level 1:
  - `gpu.mem.reserved` (latest, KB): "The amount of GPU memory consumed by virtual GPUs in kilobytes".
  - `gpu.mem.used` (average, KB): "The amount of GPU memory used by workloads in kilobytes".
  - `gpu.mem.total` (latest, KB): "The total amount of GPU memory in kilobytes".
  - `gpu.utilization` (average, %): "The compute utilization of a GPU in percentage".
- Context: the knowledge base says a vGPU profile fixes the frame buffer per VM, reserved at power-on, so host GPU memory can look high while VMs are idle. Per-device host counters (GPU Memory Usage) are level 4 in the chart tables.
- Question:
  1. Is `gpu.mem.reserved` the sum of the vGPU profile frame buffers of powered-on VMs?
  2. Is `gpu.mem.used` the frame buffer the workloads actually touch, so it is always at or below reserved?
  3. When reserved approaches total, can no further vGPU be placed even with low utilization? (Placement is per physical GPU, so the cluster total may hide fragmentation.)
- Written as now: reserved and used named, with your rule that reservation is a setting and used is activity, so reserved can exceed used. Points 1-3 not stated.
- Proposed answer (expert call; one live reading):
  - 1. Yes. NVIDIA allocates a vGPU's frame buffer from the physical GPU when the vGPU is created (VM power-on) and keeps it until it is destroyed. Broadcom KB 439680: GPU memory use equals what is assigned, "a partition that is created on PowerOn of the VM". So `gpu.mem.reserved` = sum of the profile frame buffers of powered-on vGPU VMs. Whether whole-GPU DirectPath VMs count is not documented.
  - 2. Yes, per vGPU. The configured profile is the upper bound of the frame buffer the VM uses (vSphere 9.1 documentation), so `gpu.mem.used` ≤ `gpu.mem.reserved`. Trap: the host per-device chart "Memory used" (level 4) shows the reserved frame buffer, not workload use. Same word, different meaning at host and cluster.
  - 3. Yes, and well before reserved approaches total. Frame buffer is not overcommitted; only compute is time-sliced, so low utilization frees nothing. Placement needs one physical GPU with room for the whole profile; in equal-size mode (the default) a GPU that already holds a vGPU accepts only the same size. A cluster with GB to spare can refuse a VM (Broadcom KB 312021). Read DirectPath Profiles Remaining per profile.
  - Sources: vSphere 9.1 documentation (Configuring vGPU Size; Capacity Visualization of DirectPath Profiles; GPU Memory charts); NVIDIA Virtual GPU Software User Guide, Release 21.0 (https://docs.nvidia.com/vgpu/latest/pdf/grid-vgpu-user-guide.pdf); https://knowledge.broadcom.com/external/article/439680
  - Change if accepted: gpu-monitoring (Reading the counters: points 1-3; the "Memory used" trap; trap "utilization is low, so another vGPU fits").
  - For you: one live reading: on a cluster with known profiles (for example 4 × 8 GB), does `gpu.mem.reserved` equal the sum, and do passthrough GPUs count?
- Answer (summary of the author's review):
  - 1. Partly correct. NVIDIA allocates the whole frame buffer at VM power-on, so `gpu.mem.reserved` is the sum of the assigned profiles. DirectPath I/O (PCI passthrough) VMs are excluded: the whole device is mapped into the VM and bypasses the NVIDIA vGPU Manager on ESXi, so the host cannot account for or monitor that memory.
  - 2. Correct for vSphere 9.0 and 9.1; not for vSphere 8.x.
  - 3. Frame buffer overcommit is not supported. Placement needs one contiguous frame buffer on one physical GPU; cluster capacity hides fragmentation (32 GB free across four GPUs rejects a 16 GB profile). "Only the same size on a GPU that holds a vGPU" applies to older architectures: Ampere, Ada Lovelace and Hopper support mixed profile sizes on one GPU (for example 8Q and 4Q). Fragmentation still decides placement; DirectPath Profiles Remaining is the metric for exhaustion.
- Review of the answer:
  - Accepted all three corrections.
  - Naming: nv-hostengine is NVIDIA's DCGM host engine, not the vGPU Manager. The knowledge base names the NVIDIA vGPU Manager (the host driver) as the component passthrough bypasses.
  - Added: MixedSize needs both a supporting GPU and the host set to MixedSize; each profile size has fixed placement positions on the GPU, so one GPU can be fragmented too.
  - Added trap: DirectPath Profiles charts count vGPU instances, not DirectPath I/O passthrough; the two names share a word.
  - Open: what `gpu.mem.used` counts on 8.x (Q168); whether passthrough GPUs are also outside `gpu.mem.total` (review_notes, live check).
- Applied 2026-11-11: gpu-monitoring (Counters: host Memory used is allocation; Reading the counters: reserved = sum of profiles at power-on, passthrough excluded, used ≤ reserved on 9.0 and 9.1 only, no frame buffer overcommit; vGPU capacity: one GPU, contiguous, fragmentation example, SameSize vs MixedSize by architecture; 5 traps).

### Q161 · KPI vs SLA · The daily KPI actual

- Files: [KPI vs SLA](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/kpi-vs-sla.md) (Two numbers each), [project/explainers/sla-vs-kpi.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/explainers/sla-vs-kpi.md) (KPI, daily).
- Search: not from the book.
- What the knowledge base says now: the KPI is a score every 5 minutes and is reviewed daily against its class target. It does not say how the 288 scores of a day become the daily actual.
- Question: which statistic? (a) the average of the 288 scores; (b) the lowest score; (c) a percentile, such as the 5th, as Close for Business uses; (d) other. In the worked example, (a) gives VM 01 98.84 on its bad day, (b) gives 33.33.
- Answer: For capacity, it is already part of the model. For performance, use the 95th percentile.
- Applied 2026-11-10: kpi-vs-sla (Two numbers each: the 95th percentile of the day's 288 scores, worst 14 intervals ignored); explainer recomputed (both VMs score 100 daily; the 25-minute episode is the alert's job). Revised 2026-11-10: the 99th percentile (worst 2 intervals ignored); 95th is too lenient for large organisations. The KPI is never per class of service.

### Q160 · KPI vs SLA · "75% is acceptable" and the class KPI targets

- Files: [KPI vs SLA](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/kpi-vs-sla.md) (Value; Traps), [Class of service in capacity planning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/class-of-service-planning.md) (Contention).
- Search 1: "75% is acceptable"
- Search 2: "Contention: minimum VM Performance"
- What the knowledge base says now: KPI "tends to be lower; 75% is acceptable", and a trap says a KPI of 75% is not a failure. The class KPI targets are Gold 99.5%, Silver 99%, Bronze 98%.
- Question: for a Gold VM, 75% misses the target by far. Is 75% the green edge of one 5-minute score (an interval at 75 or above is green), while the class target applies to the daily KPI? If yes, the Value line and the trap are rewritten that way.
- Answer: kpi-vs-sla says a KPI of 75% is acceptable for a given 5 minutes for a development VM, not for the whole day. The point: do not treat the KPI like a severe legal contract with a heavy penalty.
- Applied 2026-11-10: kpi-vs-sla (Value; trap).

### Q158 · Threshold design · Alert definitions in 1.0

- Files: [project/design-thresholds.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/design-thresholds.md) (section 5.4, block `alerts`).
- Search: not from the book.
- What the knowledge base says now: your brief says the alerts file holds symptoms only. The plan puts the alert definition catalog at 1.2, after the overhaul.
- Question: (a) a thin `alerts` block now: id, criticality, any or all, symptom ids, persona; only your ~20 book alerts; (b) symptoms only until 1.2.
- Recommendation: (a). Without it the `all` logic and the 1 GHz gate are lost, and "why did this alert fire" cannot be answered.
- Answer: Yes, the question cannot be answered. Add to the to do list.
- Applied 2026-11-10: design work list 15.1 item 9; plan open work.

### Q157 · Threshold design · VM CPU Net Run alert at KPI yellow

- Files: [knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml) (ids `alert-vm-cpu-net-run-red`, levels line CPU Net Run); [CPU alerts](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/configuration/cpu-alerts.md).
- Search: "VM CPU Net Run above 95%"
- What the knowledge base says now: red alert above 95% with Guest OS CPU Queue above 4 for 15 minutes; VM KPI CPU Net Run is yellow 95, orange 97, red 99.
- Question: an alert fires at the KPI yellow edge. (a) intended: the queue condition and 15 minutes make it urgent, and lint allows a lower value when a second issue symptom is required; (b) the alert value moves to 99 or above.
- Answer: KPI is independent of alert. The purpose is different.
- Applied 2026-11-10: design section 6 rewritten (KPI and alert: independent); the consistency rules and their lint check removed.

### Q156 · Threshold design · Alert rows in the capacity file

- Files: [knowledge/catalog/thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml) (ids `alert-esxi-cpu-thread-utilization-red`, `alert-esxi-memory-consumed-red`, `alert-datastore-used-space-red`); [Alert design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/alert-design.md) ("Capacity: red only, as a guard rail").
- Search: "Capacity: red only, as a guard rail"
- What the knowledge base says now: three consumption alerts sit in the capacity file; alert-design gives capacity a red guard-rail alert.
- Question: with your rule that capacity does not use alerts, (a) the two ESXi rows become performance consumption alerts (host saturated today) and the datastore row an availability alert (full datastore stops writes); the alert-design line "Capacity: red only" is rewritten; (b) they stay capacity.
- Recommendation: (a).
- Answer: Remove the rule that capacity does not use alerts; make it a principle. Capacity management takes a longer view; done properly, it raises no alert. A capacity alert means something is amiss: a software bug or a hardware availability issue.
- Applied 2026-11-10: alert-design (Capacity line), design premises and alerts file (capacity pillar allowed under the principle).

### Q155 · Threshold design · Cancel cycle values

- Files: [project/design-thresholds.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/design-thresholds.md) (section 5.4); [Alert definitions in VCF Operations](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/alerts/alert-definitions.md) (Wait cycle).
- Search: "Values in the author's set"
- What the knowledge base says now: wait cycle 5 minutes for contention, 10 where false positives are common, 15 for consumption. No cancel cycle anywhere.
- Question: (a) cancel cycle per type (contention, consumption)? (b) symptom-level wait and cancel with alert-level cycles at 1, as Broadcom advises? (c) does any of your alerts set an alert-level wait cycle?
- Answer: Cancel cycle needs an overall design; Claude to propose one. Example for review: project/alert_close_cycle_design_best_practices.md.
- Applied 2026-11-10: proposal in project/design-thresholds.md, section 9 (three states, rules R1-R6, incident layer, review of the example). Values wait for approval.

### Q154 · Threshold design · Symptom: two meanings

- Files: [project/design-thresholds.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/design-thresholds.md) (sections 5.4, 9); [Alert definitions in VCF Operations](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations/alerts/alert-definitions.md) (Conditions, not symptoms; Traps); [Alerts, symptoms and insights](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/alerts-and-insights.md).
- Search: "Build alerts from conditions, not from symptom definitions"
- What the knowledge base says now: a symptom is a minor issue for the daily check; your alerts are built from conditions, and "reuse symptom definitions to build alerts" is listed as a trap. Your brief says alerts.yaml holds symptoms with wait and cancel cycles.
- Question: (a) the file holds VCF Operations symptom definitions (tests); the glossary splits "symptom definition" (product object) from "symptom" (SP5 minor issue), and the trap is rewritten; (b) the file holds conditions, named `conditions`, and the knowledge file stays; (c) other.
- Recommendation: (a). Reuse across alert definitions needs a stored test; inline conditions cannot be reused. Also: are conditions in the 9.1 editor stored as symptom definitions internally?
- Answer: Condition and symptom are two terms used only in VCF Operations. Symptoms are reusable; a condition is embedded in the alert. Agent E2 needs to know they mean the same thing.
- Applied 2026-11-10: alert-definitions (section Symptom and condition: one test, two names; trap rewritten), glossary (Symptom row, Synonyms row), design.

### Q153 · Threshold design · KPI in availability and security files

- Files: [project/design-thresholds.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/design-thresholds.md) (section 5.5); [KPI vs SLA](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/kpi-vs-sla.md) (Traps); [glossary](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md) (KPI vs model).
- Search: not from the book.
- What the knowledge base says now: KPI is performance only; availability is KAI, compliance KCI. Your brief says availability.yaml and security.yaml hold "KPI and SLA". sla-metrics also says "the internal KPI is 100%" for compliance.
- Question: the `use` value for the internal target in the availability and security files. (a) `kai` and `kci`, keeping the rule; (b) `kpi` everywhere, and the rule changes; (c) `target`, a neutral word for all non-performance pillars.
- Recommendation: (a). One word per concept; a 32B model that sees `kpi` in the availability file will mix it with the performance KPI.
- Answer: KPI is an internal target, not a contract like SLA. KPI is strictly performance: automated, self-driving operations need unambiguous terms, and performance management is a big part of IT management, so the P in KPI means performance. Availability has KAI; security has KSI. Users say availability KPI, business KPI, marketing KPI in daily life: Agent E2 translates them to KAI and KSI.
- Applied 2026-11-10: glossary (Synonyms KAI, KSI; Defined terms KPI, KAI, KSI; KPI vs model), kpi-vs-sla trap, term map row kpi-other-pillar, design use values kai and ksi.

### Q152 · Thresholds > levels · Empty cells in the 9-value table

- Files: [knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml), section `levels`
- Search 1 (file): "levels:"
- What the knowledge base says now: 31 metrics, one line each. Every line has one interval filled from its band table (20s or 5m). The other two are null. No 2s value exists anywhere.
- Question: give yellow, orange, red for the null cells, or say which stay empty. Should 2s apply only to the 20s-peak metrics (CPU Ready, Co-stop, disk latency)? A 2s value for Guest OS free memory or balloon has no meaning.
- Written as now: null. The 4x rule is not used to fill cells.
- Answer: The 4x rule is not used. I asked for 9 values, so I can manually hardcode the values for 2 second, 20 second, and 5 minute. Each will have yellow, orange, and red.
- Applied 2026-11-10: `levels` is the one copy of the KPI levels; band rows and `from` removed; null cells wait for values entered by hand; no 4x rule (thresholds-performance.yaml, KNOWLEDGE-ENGINEERING.md section 9).

### Q159 · Repository rules · Who-said-it tags

- Files: [CLAUDE.md](https://github.com/e1-rahabok/agent-e2/blob/main/CLAUDE.md) (Facts and sources); [KNOWLEDGE-ENGINEERING.md](https://github.com/e1-rahabok/agent-e2/blob/main/KNOWLEDGE-ENGINEERING.md) (sections 8, 13); [knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml) (field `source`: book, author, vsphere-9.1-docs, ...); [project/plan.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/plan.md) (Decisions: "author, date").
- Search: not from the book.
- What the repository does now: tags who said a fact or made a decision ("author", "book", "Claude's knowledge"), in review notes, threshold `source` values, the plan's decisions and prose.
- Your point: the knowledge base is yours; Claude brings Internet knowledge and you choose. Who said it adds nothing.
- What Agent E2 does use: whether a fact comes from the knowledge base (mechanism, wins) or from a vendor document of a given version (can go stale; the newer official document wins), and whether a file is reviewed (`status: draft` is said in the answer).
- Question: (a) drop who-said-it tags everywhere; keep `source` only as knowledge base vs vendor document with version, and `status` for review; review notes keep only what is still to check, with its URL; (b) drop them in prose and project documents, keep them in review notes until a file is reviewed; (c) keep as is.
- Recommendation: (a). Applied already to the threshold design document.
- Answer: (a).
- Applied 2026-11-10: CLAUDE.md (Facts and sources), KNOWLEDGE-ENGINEERING.md (sections 8, 9, 10, 13, 14), threshold `source` values (book and author became knowledge-base; lint, test), who-said-it tags removed from knowledge text, metadata, catalogs, plan and project documents; review notes cut to what is still to check.

### Q126 · Part 1 > Rightsizing > Optimization vs The Big Picture · 100% or 40%

- Files: [Rightsizing VMs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/rightsizing.md) (sections What to optimize, Big picture).
- Search 1: "utilization should be 100% to minimize ping pong"
- Search 2: "You expect this number to hover around 40%"
- Question: per VM, CPU utilization should be near 100%; across hundreds of large right-sized VMs, the average is about 40% and the max about 80%. The knowledge base reads the first as the aim per VM at its busy time, the second as the fleet average over every 5 minutes. Correct?
- Written as now: as above.
- Answer: Two different things; the author rewrote rightsizing.md (Monster VMs Capacity Management).
- Applied 2026-11-09: typo fixed, monster VM definition linked, one bullet separating the per-VM aim from the monster VM group.

### Q123 · Part 1 > Capacity Management > Reclamation · Benefit table and scope

- Files: [Reclamation](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/reclamation.md) (sections When reclamation is the provider's job, What each area frees).
- Search 1: "Cluster RAM as idle RAM pages tend to occupy ESXi memory"
- Search 2: "It is only applicable when VMs are free"
- Question: (a) In the benefit table, cells seem shifted: Idle VM, Storage holds "Cluster RAM as idle RAM pages tend to occupy ESXi memory"; Oversized VM, Memory holds the context-switch text (a CPU benefit). Claude rewrote the table from the chapter text: unused VM frees real CPU and memory; oversized VM frees memory and performance, CPU in allocation only; idle VM frees memory, CPU in allocation only; storage only on delete. Correct? (b) The chapter starts with reclamation applying only when VMs are free, then applies the stocktake to internal IT with chargeback. Which scope is right?
- Written as now: the rewritten table; both scope statements.
- Answer: Answered by the author's edit of reclamation.md (2026-11-09): the benefit table (oversized VM also frees cluster capacity through a lower overcommit ratio) and the scope (free VMs: the infrastructure team may reclaim; charged VMs: the application team owns the cost; stocktake still applies).
- Applied: review notes updated; table cleaned of HTML line breaks.

### Q148 · Part 2 > Overall Design Approach > Design Consideration · Data points per month and the wastage colour

- Files: [Dashboard design in VCF Operations](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/dashboard-design.md) (section Conflicting requirements); [Colour and thresholds in dashboards](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/outputs/dashboard-colour.md).
- Search 1: "Can the dashboard be understood within 5 seconds?" (the picture after it)
- Search 2: "We use dark grey in Capacity as wastage"
- Question: (a) the picture says 1 month = 8650 data; 30 days of 5-minute data is 8,640. Typo? (b) the picture says black for wastage, the colour table says dark grey. Which colour do the shipped capacity dashboards use?
- Written as now: (a) 8,640; (b) dark grey.
- Answer: (a) Per month: use 365.25 days a year on average (leap years), so 288 × 365.25 / 12 = about 8,766 points. (b) Dark grey; black is wrong.
- Applied 2026-11-09: dashboard-design.

### Q151 · Cluster Risk (%) · CPU overcommit per core or per thread

- Files: [Cluster Risk (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md) (row CPU overcommit), [Class of service in capacity planning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/class-of-service-planning.md) (CPU per thread).
- Search: not from the book; your answer to Q115 (e).
- Question: you state that a CPU ratio is per thread, because the CPU executes per thread. The Cluster Risk CPU overcommit row (vCommunity pack) counts vCPUs of powered-on VMs per physical core (`hardware|cpuInfo|numCpuCores`), and its bands (red at 3-4) are set per core. With Hyper-Threading, 4:1 per thread is 8:1 per core. Should the row count per thread (and its bands change), or is per core intended for the risk score?
- Written as now: the row per core, the planning ratios per thread, the conflict in review notes.
- Answer: Per thread. Document that the vCommunity pack must be fixed.
- Applied 2026-11-09: cluster-risk (new section CPU overcommit: per thread, table row, trap); plan item to fix the pack.

### Q105 · Part 1 > Monitor | Troubleshoot; SP5 Framework: Process · Logs in monitoring and the length of the daily check

- Files: [Monitoring vs troubleshooting, root cause analysis and validating a log alert](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/monitoring-vs-troubleshooting.md); [Proactive operations: dual track, daily cadence, NOC screens and the VM life cycle](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/proactive-operations.md).
- Search 1: "Not required. Metrics, properties, and Event suffice."
- Search 2: "Should take just 5 minutes"
- Search 3: "The check must be quick, ~1 minute"
- Search 4: "There are 3 techniques we can apply"
- Image text (not searchable): "Daily Check (10 minutes)"; present health "Data is mostly coming from logs, not metrics".
- Question:
  - (a) Monitoring needs no logs, yet availability data comes mostly from logs and the daily SOP reads logs for soft errors. Is log analysis (daily, in the cadence image) part of monitoring?
  - (b) Monitoring 5 minutes, daily check about 1 minute, timeline 10 minutes. One number?
  - (c) 3 techniques announced, 4 listed (text) and 4 in the diagram with other names. Use the diagram names?
- Written as now: (a) and the interval applied 2026-11-08 (monitoring-vs-troubleshooting: Logs row required, 20-second peak within the 5-minute interval, 20-second visibility for mission-critical systems); (b) applied: about 5 minutes when there is no problem; (c) the diagram's four techniques.
- Answer: Monitoring needs log. Monitoring depends on what is being monitored. Log is streaming continuously not discrete every 5 minutes or 1 minute. Performance monitoring reports peak of 20 seconds within 5 minutes reporting interval. An exception is mission critical system where 20 seconds visibility is worth the cost of monitoring. I'll review item 105(c).
- Answer (b), 2026-11-08: A daily check, if there is no problem, it should take a few minutes. That's why I put 5 minutes. Now, if there is a problem, logically, it can take a lot longer than that, depending on the problem.
- Applied (b): proactive-operations (A 24-hour day, Dual track, Traps), monitoring-vs-troubleshooting (Duration row).
- Still open: (c).
- Restated (c), 2026-11-09: the book says "There are 3 techniques we can apply" for proactive operations, then lists 4 in the text; the dual-track diagram also has 4 but with other names (automated process, insight, modelling, monthly performance baselining). The knowledge base uses the diagram's 4 names. Correct, and is the "3" a typo for 4?
- Answer (c), 2026-11-09: diagram updated. Two processes. Reactive: down, slow, breached; the first two are troubleshooting, the security one is forensic investigation; performance troubleshooting uses the KPI, not the SLA. Proactive: the health check, daily, complemented by weekly and monthly; a superset of reactive.
- Applied 2026-11-09: proactive-operations (Dual track, diagram replaced), KNOWLEDGE-ENGINEERING.md section 10, glossary (Troubleshooting).

### Q101 · Part 1 > SP5 Framework: Pillars · Relationship lines and what is troubleshot

- Files: [SP5 framework and the five pillars of operations: scope, relationships, non-pillars](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/overview.md) (sections Relationships, Capacity); [Proactive operations: dual track, daily cadence, NOC screens and the VM life cycle](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/proactive-operations.md) (section Who does which day).
- Search 1: "Lines without arrowheads means there is relationship but not impact"
- Search 2: "Availability and Capacity should not overlap"
- Search 3: "Why isn’t there a line to Performance?"
- Search 4: "You troubleshoot availability, performance, and security"
- Question:
  - (a) The text puts Availability-Capacity among lines without arrowheads; the diagram draws an arrow from Availability to Capacity. Arrow or not?
  - (b) The detailed diagram that follows draws Availability → Performance; the text says there is no line. Remove it from the diagram?
  - (c) The detailed capacity diagram says a reservation becomes a share. What is the mechanism you mean?
  - (d) The Day 0-2 table marks compliance not applicable for troubleshooting; the Troubleshoot section troubleshoots security. Is security troubleshot and compliance not?
- Written as now: text version for (a) and (b); (c) written as the label; (d) both, flagged.
- Answer (2026-11-09): (a), (b) not clear, explanation sent in the session (see below). (c) Answered in the updated overview file: reservation in planning becomes share in running. (d) Only availability and performance are troubleshot; security is forensic investigation; compliance is finding the setting that differs from the desired configuration. Applied: proactive-operations, glossary.
- Restated (a): the book's text says Availability and Capacity have a line without an arrowhead (a relationship, no impact), but its pillar diagram draws an arrowhead from Availability to Capacity (impact). Which is right: does availability design (an HA host held back) impact capacity, or only relate to it?
- Restated (b): the text says there is no line from Availability to Performance (a planned host outage does not reduce performance). The detailed diagram after it draws Availability → Performance. Keep the arrow or remove it?
- Answer (a, b), 2026-11-09: (a) An availability problem can definitely impact available capacity. (b) Availability can impact performance, especially when it is intermittent: flapping between on and off, or between passive and active nodes. Diagram updated (attached).
- Applied 2026-11-09: overview (section Relationships, diagram replaced, two traps).

### Q106 · Part 1 > Service Level Agreement > Performance SLA · SLA counters vs the prevention window alerts

- Files: [IaaS SLAs: what each measures and how it is computed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/sla-metrics.md); [knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml) (rows vm-sli-*). Related: Q088 (a).
- Search: "Use the above threshold as they are."
- Question: the four SLI thresholds are now catalog rows at 5-minute VM level (CPU Ready 2.5%, Memory Contention 1%, Disk Latency 10 ms, Transmit Dropped 0%). Q088 (a) asks about the 5% Ready in the prevention window image. Confirm the rows, and that the SLA reading is the 5-minute VM average, never the 20-second peak?
- Written as now: four rows, interval 5m, instance aggregate.
- Answer: The Performance SLA is never 20 seconds: a very short window gives no room for error. The KPI uses 20 seconds as a leading indicator. The KPI should be higher than the SLA. Alerts are based on the KPI, not the SLA or SLI; a red alert may mean the SLI is breached.
- Applied 2026-11-09: sla-metrics (Traps); the vm-sli-* rows stay at 5 minutes.

### Q100 · Part 1 > Service Level Agreement > Size Limit · Socket or logical CPUs

- Files: [Class of service: price, overcommit, SLA numbers, size limit and cluster design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/class-of-service.md) (section Size limit per class); [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/noisy-neighbour.md) (section Maximum VM size).
- Search 1: "Capping the size at each tier"
- Search 2: "If you allow a single VM to be the same size as the ESXi host"
- Image text (not searchable): "Tier 1 ≤ 1 socket 32 vCPU, 512 GB RAM", "Tier 2 ≤ 50% of a socket", "Tier 3 ≤ 25% of a socket".
- Question: here the cap is per socket (Tier 1 one socket). Noisy Neighbour caps by host logical CPUs (1:1 up to all of them; 2:1 half; 4:1 a quarter). For a 2-socket, 48-core, 96-thread host, Tier 1 is 48 logical CPUs here and 96 there. Which rule should the agent give: (A) socket (NUMA) based; (B) logical-CPU based; (C) both, the smaller wins? Is 32 vCPU per socket meant as 32 cores or 32 threads?
- Written as now: both, each in its file, linked.
- Related: Q111 (VM size by physical cores) and Q125 (8-core block and VM size).
- Answer: The cap should not relate to the socket: many ESXi servers are single socket, and NUMA now happens within a socket, which consists of multiple CCDs (AMD EPYC) or compute tiles (Intel Xeon).
- Applied 2026-11-09: class-of-service (Size limit per class).

### Q098 · Part 1 > Service Level Agreement > Recommended SLA · Compliance 99.95% or 100%

- Files: [IaaS SLAs: what each measures and how it is computed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/sla-metrics.md) (section Compliance SLA); [Class of service: price, overcommit, SLA numbers, size limit and cluster design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/class-of-service.md) (sections Recommended SLA per class, Sample offering).
- Search 1: "I did not put 99.99% as that"
- Search 2: "You should maintain perfect compliance with your compliance requirements for all classes of service"
- Search 3: "you should guarantee to your customers that you will be perfectly (100%) compliant"
- Question: the recommended table gives Compliance 99.95% for every class; the sample offering, the Compliance SLA definition and the Compliance pillar give 100%. Which number goes in the contract? Is 99.95% the contract value, with perfect compliance as the promise outside the maintenance window?
- Written as now: both tables as the book gives them; the definition says perfect compliance outside an ad hoc window.
- Answer: The SLA is a formal contract between 2 entities; do not put 100%. The KPI is 100%, as a non-compliant setting could be a door for a security attack. The maintenance window is always excluded from the SLA, as it is an agreed period of change.
- Applied 2026-11-09: sla-metrics (Compliance SLA, Traps).

### Q097 · Part 1 > Service Level Agreement > Performance SLA · Co-stop exclusion and Memory Contention unit

- Files: [IaaS SLAs: what each measures and how it is computed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/sla-metrics.md) (sections Performance SLA, What the numbers mean); [VM Memory Latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/latency.md).
- Search 1: "exclude CPU Co-Stop and CPU Contention from the Performance SLA"
- Search 2: "Memory Contention is relative to the amount of memory being used"
- Search 3: "Unlike CPU, it is not measured across time"
- Question:
  - (a) The book gives the reason for excluding CPU Contention (up to 37.5% unnoticed) but not for Co-stop. What is the reason for Co-stop? Is the 37.5% the Hyper-Threading effect inside Contention?
  - (b) Your Q015 answer: Memory Latency (VCF Operations: Memory Contention) is a share of time a vCPU waits on page faults. This section says it is relative to memory used and not measured across time. Book correction to time?
- Written as now: Co-stop listed as excluded with no reason; Contention excluded for the Hyper-Threading effect (Claude's reading); Memory Contention written as time.
- Answer: (a) Co-stop is excluded in the SLA or SLI, not in the KPI, as Ready gives the best balance between cost of reporting and value of reporting. (b) Align it to the raw value. Less ideal for an SLA, simpler operationally.
- Applied 2026-11-09: sla-metrics (Performance SLA, review notes).

### Q122 · Part 1 > Cluster Closure vs Planning Phase · Performance (%) closure values

- Files: [Can this cluster take more VMs?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms.md) (step 4), [Class of service in capacity planning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/class-of-service-planning.md) (section Example implementation), [Cluster Performance (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md).
- Search: book table after "Implementing the above with actual threshold"
- Question: production closes when Performance (%) at the 95th percentile of 24 hours drops below 40% (red) or 60% (orange). The class minimum for VM Performance (%) is 98-99.5%. The knowledge base reads the first as the cluster KPI (Cluster Performance, worst VM and 90th percentile rows) and the second as the VM KPI. Correct? With the weighted scoring, one row a quarter into red already gives about 53%; is 40% the value you want?
- Written as now: both, as different metrics.
- Answer: Use the attached table (see Q121). The Cluster KPI is not related to the VM SLA. Many customers confuse SLA: when they say SLA they mean KPI, as they have no written agreement.
- Applied 2026-11-09: can-cluster-take-more-vms (step 4, review note, two traps).

### Q121 · Part 1 > Capacity Model > Cluster Closure > Logic · Non-production capacity and the orange case

- Files: [Can this cluster take more VMs?](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/decision-tree/can-cluster-take-more-vms.md) (steps 4 and 5), [thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml) (rows closure-*).
- Search 1: "If both capacity and performance are orange"
- Search 2: book table after "Implementing the above with actual threshold"
- Question: (a) Non-production closes on performance and risk later than production (red below 20% vs 40%; risk above 75% vs 50%), but on Capacity Remaining earlier (red below 15% vs 10%; orange below 30% vs 20%). Intended (smaller buffer in non-production), or swapped? (b) One orange and one green: open without a risk check? (c) The flow now follows your closure logic for steps 2-5; Q061 stays open for the full order (state, fit, balance).
- Written as now: as in the book table; (b) read as open.
- Answer: The book was wrong; use the attached table (all at the 95th percentile of the last 24 hours): Consumption (%) red above 80%, orange above 60%; Performance (%) red below 20%, orange below 40%; both for production and non-production. Risk (%): production orange above 60%, non-production red above 80%.
- Applied 2026-11-09: can-cluster-take-more-vms (steps 4 and 5, image replaced), thresholds-capacity.yaml (closure rows: 10 replaced by 6), glossary (Closed cluster).

### Q120 · Part 1 > Planning Phase vs Cluster Risk · Bronze plan scores red

- Files: [Class of service in capacity planning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/class-of-service-planning.md), [Cluster Risk (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md) (Allocation rows).
- Search: "Notice the consistent 2x gap"
- Question: Bronze CPU 4:1 per thread is 8 vCPUs per core with Hyper-Threading. Cluster Risk counts vCPUs per physical core and marks 3-4 as red; Silver 2:1 per thread (4 per core) is red too. Bronze memory 2:1 sits in the Cluster Risk red range 1.8-2.2. So a cluster built to your plan always shows red overcommit rows, and with the production closure limit (Risk above 50%) it may close. (a) Should the Cluster Risk overcommit bands depend on the class of service? (b) Or is Cluster Risk meant only for Gold and Silver clusters?
- Written as now: both files unchanged; the conflict is noted in review_notes.
- Answer: (a) and (b) together: planning phase vs running phase. Planning (no running VMs, maybe no cluster yet): use the overcommit ratio, tied to the VM price, not to the Cluster Risk (%) score. Running: reality overrides theory; Bronze clusters should have higher Cluster Risk (%) than Gold clusters.
- Applied 2026-11-09: class-of-service-planning (new section Planning phase vs running phase, Traps), cluster-risk (review note).

### Q119 · Part 1 > Capacity Model > Planning Phase · Is the gap 2x everywhere

- Files: [Class of service in capacity planning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/class-of-service-planning.md) (section Example implementation), [Noisy neighbour](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/noisy-neighbour.md) (section Avoiding it).
- Search: "Notice the consistent 2x gap"
- Question: the implementation table keeps 2x for reservation (50/25/12.5% CPU, 100/50/25% RAM), CPU allocation (1:1, 2:1, 4:1) and contention (0.5/1/2% unmet). Memory allocation is 1:1, 1.5:1, 2:1, and utilization (50/70/90% CPU) is not 2x. Is memory deliberately less than 2x (risk of swapping), and should the text say so?
- Written as now: the values as in the table, with a note that memory and utilization do not follow 2x.
- Answer: 2x consistency is a goal, not a rule.
- Applied 2026-11-09: class-of-service-planning (section Why a fixed gap, Traps).

### Q118 · Part 1 > 4 Dimensions of Capacity > Reservation | Share · Unit of CPU reservation

- Files: [Capacity dimensions](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/demand.md) (section Reservation and share).
- Search: "That’s why the unit is Hertz, milliseconds"
- Question: CPU reservation is set in MHz. What does "milliseconds" refer to? Share is the runtime one (time slices). Remove "milliseconds" from the reservation column?
- Written as now: reservation in Hz; share in time slices.
- Answer: The book contained a mistake: no milliseconds.
- Applied: the knowledge base already gives reservation in Hz only.

### Q117 · Part 1 > 4 Dimensions of Capacity > Allocation · Memory tiering version

- Files: [Capacity dimensions](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/demand.md) (section Allocation), [Memory tiering](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-tiering.md).
- Search: "a new feature in vSphere 8"
- Question: memory tiering was a tech preview in vSphere 8.0 Update 3 and is supported from vSphere 9.0. The knowledge base says introduced in 9.0. Change the book to vSphere 9?
- Written as now: no version in the capacity file; memory-tiering says 9.0.
- Answer: Update the knowledge base: memory tiering was a tech preview in vSphere 8.0 Update 3 and is supported from vSphere 9.0.
- Applied 2026-11-09: memory-tiering, capacity-dimensions (review note).

### Q115 · Part 1 > Capacity Management > "Good" Advice · Why each statement is wrong

- Files: [Capacity dimensions](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/demand.md) (section Traps), [Capacity management: demand, supply, phases and planning inputs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/README.md) (section Traps).
- Search 1: "Memory Active should not exceed 50-60%"
- Search 2: "Memory should be running at high state"
- Question: the book lists 9 statements as wrong but does not say why. Claude wrote one reason per statement as a trap. Confirm or correct each:
  - (a) 2:1 RAM overcommit is risky → a ratio ignores utilization, VM size and class; Bronze can run 2:1.
  - (b) 90% memory, aim for 80% because of HA → usable capacity already excludes the HA host; subtracting HA again counts it twice.
  - (c) Active below 50-60% → Active is a sampled estimate; capacity reads demand against usable capacity.
  - (d) Each host in the high memory state → High means much free memory: wastage.
  - (e) 5:1 CPU on an important cluster → important clusters take a lower ratio.
  - (f) 3:1 gives buffer for spikes and HA → allocation ignores utilization and VM size; buffer and HA belong in usable capacity.
  - (g) 4:1 for Tier 3 → not used as a trap; what is wrong with it?
  - (h) UAT at 70%, worry at 85% → utilization alone does not close a cluster; read contention and risk.
  - (i) 25% CPU is good, plenty left → below 40% of usable is wastage.
- Written as now: (a)-(f), (h), (i) as traps.
- Answer: (a) Confirm. (b) Wrong reason: Consumed is unaware of HA; do not worry about high Consumed, memory is a form of cache and has to be high, else the DIMM is wasted. (c) Active is not a capacity counter; it is for VMkernel memory management, of no use unless doing memory tiering. (d) Confirm. (e) Not wrong but misleading: it simplifies capacity management into the allocation model, and does not say physical core or thread; the CPU ratio is per thread, as execution is per thread. (f) (g) Not wrong but misleading, same reason. (h) Confirm; not wrong but misleading, same reason. (i) Confirm.
- Applied 2026-11-09: capacity-dimensions (Traps); new trap for (g). The Cluster Risk CPU overcommit row counts per core: Q151.

### Q114 · Part 1 > Capacity Management > Stages and Capacity Model · Book text fixes

- Files: [Capacity management: demand, supply, phases and planning inputs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/README.md), [Capacity dimensions](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/demand.md).
- Search 1: "e first place, by using progressive pricing"
- Search 2: "They need to be reviewed as complimentary"
- Search 3: "measured againsts usable"
- Question: (a) Search 1 is a sentence fragment after the four-phase table; text seems lost before it. What was meant? (b) "complimentary" should be "complementary". (c) "againsts" should be "against". Confirm (b) and (c) for your next edition.
- Written as now: fragment left out; the knowledge base uses the corrected words.
- Answer: (a) Solve the oversized VM in the first place, before the VM is provisioned. Use progressive pricing to encourage smaller size configuration. (b) and (c) fixed in the book's next update.
- Applied 2026-11-09: capacity-management-process (section Four phases).

### Q102 · Part 1 > SP5 Framework > Health · Where compliance and inventory sit

- Files: [Health: present health, risk and efficiency, not one score](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/health-risk-efficiency.md).
- Search 1: "There are 4 problems that create risk in operations"
- Image text (not searchable): present/future health image, "Is it safe? Security Compliance" under Present Health and "Inventory" under Future Health.
- Question: the table and the grouping image put compliance under risk (future health) and inventory outside health (environment). The present/future health image puts compliance with security in present health and inventory in future health. Which grouping should the agent use?
- Written as now: table and grouping image; the other image's details used as text only.
- Answer: "Is it secure?" implies both security and compliance. A security issue is more urgent: the non-compliant setting is being exploited already or is on a public network. Not all non-compliant settings trigger a security alert, as that would cause excessive noise. Security management: operational, proactive, dynamic; CIA triad of hosts, storage fabrics and workloads against zero-day exploits, unauthorized access and runtime threats. Compliance management: structural, declarative, governance-driven; verifiable baselines against internal policy, industry benchmarks (CIS, VMware security configuration guides) and regulation (PCI-DSS, MAS TRM, ISO 27001).
- Applied 2026-11-09: sp5-framework/concepts/overview (section Security and compliance), health-risk-efficiency (definition vs check, analogies condensed), glossary pair Security vs compliance. Grouping kept: security incidents in present health; compliance in risk.

### Q133 · Health check · Decisions still open from the 2026-11-08 review

- Files: [KNOWLEDGE-ENGINEERING.md](https://github.com/e1-rahabok/agent-e2/blob/main/KNOWLEDGE-ENGINEERING.md) (section 10); the three health checks.
- Search: not from the book.
- Question: (a) Without VCF Operations (vCenter only), should a health check fall back to the raw counters of each KPI sub-metric? Answered (author, 2026-11-08): the question is invalid; there is no vCenter without VCF Operations. The fallback line was removed from the ESXi health check. (b) Order: answered by Q104 (2026-11-08): availability, performance, security, with configuration as the drill-down under each; every performance flow checks configuration. Still open: does risk (capacity, compliance) and efficiency follow, as in health-risk-efficiency? (c) Keep the word triage for the first troubleshooting step after a complaint (vm-slow-triage), or drop it? Answered (author, 2026-11-09): drop it; it is a flow. Renamed sp5-framework/performance/troubleshooting/vm-slow.
- Written as now: (a) resolved, no fallback; (b) as stated; (c) triage kept.
- Answer: (a) The SP5 health check requires VCF Operations, not vSphere alone; other health check tools are outside the scope of Agent E2, so the fallback is invalid. (b) Health check flow: availability, performance, security, capacity; configuration is checked during the check, as a setting can affect all four. (c) Drop triage: one English word per purpose; synonyms are kept in knowledge/glossary.md.
- Applied 2026-11-09: the three health checks, the template and KNOWLEDGE-ENGINEERING.md sections 5 and 10; glossary (triage as an alias of troubleshooting, duplicate rows merged); vm-slow-triage renamed vm-slow.

### Q103 · Part 1 > SP5 Framework > Basic Terminology · Alert: urgent or important; symptom

- Files: [Alerts, symptoms and insights: why alert-driven operations stay reactive](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/alerts-and-insights.md) (sections Symptom, alert, insight; Finding, issue, alert, notification). Related: Q089.
- Search 1: "It’s an urgent Issue with Symptom crossing threshold"
- Search 2: "An issue is identified by its 1 or more Symptom"
- Image text (not searchable): "Important issues" (Issue → Alert), "Urgent issue" (Alert → Notification), "Non-important issue" (Alert → Daily Check).
- Question:
  - (a) The table defines an alert as an urgent issue; the diagram routes important issues to alerts, then urgent ones to notification and non-important ones to the daily check. Is an alert defined by urgency, by importance, or by a symptom crossing a threshold (either)?
  - (b) Symptom: here part of an issue (an issue has 1 or more symptoms); in Observability, a minor non-urgent issue that becomes an alert if it persists. One definition?
- Written as now: both, flagged.
- Answer: (a) See the corrected diagram: alert = urgent; only the important one is pushed to the VMware admin's mobile phone. (b) An issue is a negative finding: something found bad. It can have 1 or more symptoms; untreated, they can degenerate and become urgent.
- Applied 2026-11-09: sp5-framework/outputs/alerts-and-insights (section Finding, issue, alert, notification; diagram replaced).

### Q092 · Part 1 > Begin with The End in Mind > The Crown Jewel · Health across tiers

- Files: [Purpose-driven architecture: Day 2 first, business context, automation last, two sides of VCF](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/purpose-driven-architecture.md) (section Health of an application tier).
- Search: "The health of a tier is the average health of its members."
- Question:
  - (a) Inside a tier, the average. Across tiers (web → application → database) work runs in sequence, like a convoy. Is the application's health the minimum of its tiers?
  - (b) A database tier with active and passive nodes: the passive node serves no requests. Average both, or count the active node only for performance?
- Written as now: tier = average of members; nothing on across tiers or active/passive.
- Answer: (a) Yes. (b) Only count the active one. Note this is not yet implemented in VCF Operations as it does not know how to figure out active/passive. Where do you document under knowledge/ about business applications KPI? A Level 300 mistake is thinking that measurement of business application is not necessary at infrastructure layer (see realms-and-layers: 3 main layers). Critical business applications are sometimes called the Crown Jewels as they are strategic to the core business.
- Applied 2026-11-09: new file sp5-framework/performance/business-application-kpi (why the infrastructure layer measures it, crown jewels, tier average, worst tier across tiers, active node only, not yet in VCF Operations); crown jewels and tier rules moved there from purpose-driven-architecture.

### Q090 · Part 1 > Observability > Input | Output · Property types, the second Event row, DRS automation level

- Files: [Input types: metric, property, event, log, trace, NetFlow](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/observability/input-types.md) (sections Property, Event).
- Search 1: "There are 3 types of properties:"
- Search 2: "It can be a setting change, a state change, or a label change."
- Search 3: "Cluster 007 DRS automation level was changed from 2 to 5."
- Search 4: "That’s why state is a metric, not a property."
- Question:
  - (a) The three property types are announced but not listed. Which are they?
  - (b) The table has two rows named Event. Is the second (setting, state, label change) meant as Property? If so, state is listed both as a metric and as a property type.
  - (c) DRS automation level is Manual, Partially Automated or Fully Automated; the 1-5 scale is the migration threshold. Change the example to migration threshold?
- Written as now: setting, state and label change as change events; the example written as migration threshold, flagged.
- Answer: (a), (b) In the attached document: three property types (label or tag; setting; non-setting); the second Event row is an event (setting, state or label change), in a nested table the extraction missed. (c) Yes. Applied 2026-11-08: sp5-framework/observability/input-types.

### Q086 · Part 1 > Your Private Cloud > Overview > Key Metrics · Operational Availability and green zone

- Files: [IaaS as a service: variants, class of service and what each layer checks](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/iaas-business.md) (section Metrics per pillar).
- Search: "Relative Availability, against your availability architecture and green zone."
- Question: what is the green zone here? (a) the planned availability band of the architecture (for example the HA design target), or (b) something else. The formula comes later, in the Service Level Agreement section; this asks only for the term.
- Written as now: Operational Availability is relative to the availability architecture; green zone left out.
- Answer: Neither. Green zone = change window (maintenance window, authorized execution window): the predefined time when approved changes, deployments, patches and infrastructure changes may enter production. Applied 2026-11-08: sla-metrics, iaas-business, glossary.

### Q072 · Part 1 > The Layers in IT Systems · Apdex

- Files: [Business, application and IaaS: layers, lost context and metric types](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/realms-and-layers.md) (image troubleshooting-layers-loss-of-context-example-table.png).
- Search 1: "Johnny’s transaction was the worst at 20.1 seconds"
- Search 2: "I like the principle behind apdex, but not its implementation"
- Question: (a) and (b), book typos, closed 2026-11-08 (book edition does not matter to Agent E2, author on Q107). (c) The book offers an improved Apdex formula. Give it to the knowledge base, or leave it out, since it is not IaaS?
- Written as now: no number from the image in the text; no Apdex.
- Answer: Author note on Apdex flaws (2026-11-08); close, as the focus is not business transaction monitoring. Applied: realms-and-layers, section Apdex: not used; the book's improved formula left out.

### Q063 · Sources · Book Part 1 and the VCF Operations chapters

- Files: [sp5-framework/](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework) (4 files and 2 new flows); [vcf-operations/](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vcf-operations) (1 concept, 12 metrics, 5 KPIs). Review: [project/review-2026-11-06.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/review-2026-11-06.md), section 3.3.
- Search: not applicable.
- Question: please upload Part 1 of the book (capacity and performance management) and your VCF Operations chapters to [project/sources](https://github.com/e1-rahabok/agent-e2/blob/main/project/sources). Today 159 of 206 files come from Part 3, and operators work in VCF Operations, which a third of the screenshot questions show. Claude will fetch the VCF Operations 9.1 metric reference from TechDocs for the catalog.
- Written as now: Part 3 extracted; operations-management and vcf-operations hold only what Part 3 and the vCommunity adapter documentation give.
- Answer: Uploaded and digested already (author, 2026-11-08). Part 1 is extracted; the VCF Operations knowledge now sits with the objects it describes (pull request 164).

### Q094 · Repository · Where cross-pillar operations files go

- Files: [IaaS as a service: variants, class of service and what each layer checks](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/iaas-business.md); [Purpose-driven architecture: Day 2 first, business context, automation last, two sides of VCF](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/purpose-driven-architecture.md); [Alerts, symptoms and insights: why alert-driven operations stay reactive](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/alerts-and-insights.md).
- Search: not applicable. Rule: [project/tools/lint.py](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/lint.py) allows only pillar folders (performance, capacity) under [knowledge/operations-management](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework).
- Also (2026-11-07, Service Level Agreement to SP5 Framework: Process): [IaaS SLAs: what each measures and how it is computed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/sla-metrics.md), [Class of service: price, overcommit, SLA numbers, size limit and cluster design](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/class-of-service.md), [SP5 framework and the five pillars of operations: scope, relationships, non-pillars](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/overview.md), [Health: present health, risk and efficiency, not one score](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/health-risk-efficiency.md), [Monitoring vs troubleshooting, root cause analysis and validating a log alert](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/monitoring-vs-troubleshooting.md), [Proactive operations: dual track, daily cadence, NOC screens and the VM life cycle](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/proactive-operations.md): same placement, same question.
- Also (2026-11-07, Configuration Management): [Configuration management: standards, review dimensions and the four types of check](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/configuration-management.md). There is no configuration pillar; it sits in performance/ for now.
- Question: these three files cover several pillars (availability, performance, capacity, security) and the platform itself. They are in `sp5-framework/performance/` to pass lint. Options: (A) keep them in performance/; (B) allow files at the root of `sp5-framework/`; (C) a new folder such as `sp5-framework/service/`.
- Written as now: option A, pillars in the tags.
- Answer: (B). C is wrong as the jargon service is incorrect here. Applied 2026-11-08: 12 cross-pillar files and their images moved to [knowledge/operations-management](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework); lint allows files at its root; every reference updated.

### Q091 · Part 1 > Purpose-Driven Architecture > The 2 Sides of VCF · Workload and the pillar list

- Files: [Purpose-driven architecture: Day 2 first, business context, automation last, two sides of VCF](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/purpose-driven-architecture.md) (section Two sides of VCF); [Three perspectives on metrics](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/observability/metric-perspectives.md); [project/tools/tags.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/project/tools/tags.yaml) (pillar).
- Search 1: "Workload means the customers VM, not your infrastructure software."
- Search 2: diagram label "IT (VCF & Non-VCF Appliances )"
- Question:
  - (a) The text excludes infrastructure software from workload; the diagram lists IT appliances under Workloads. Are VCF appliances (vCenter, NSX Edge) workloads?
  - (b) Pillars differ across the book: this diagram has seven (availability, performance, security, compliance, capacity, configuration, inventory); Key Metrics has availability, performance, capacity, compliance; the `pillar` tag has availability, performance, security, capacity, value. Options: (A) keep the tag list; (B) add compliance, configuration and inventory to the tag; (C) another list.
- Written as now: workload = customer VMs, appliances also run as VMs; pillar tag unchanged.
- Answer: (a) Yes and No. They are technically workload, as they are VM that runs on vSphere Cluster. Operationally they are not owned by the business users. They are yours, so they are internal and hence have 0 SLA. They only have KPI. SLA is always between 2 parties.
  (b) Pillars follow the SP5 Framework diagram in Part 1 of the book.
  Applied 2026-11-08: purpose-driven-architecture (Two sides of VCF); pillar tag now availability, performance, compliance, capacity, cost (tags.yaml, 44 files); pillars-of-operations renamed sp5-framework. (a) Yes and No. They are technically workload, as they are VM that runs on vSphere Cluster. Operationally they are not owned by the business users. They are yours, so they are internal and hence have 0 SLA. They only have KPI. SLA is always between 2 parties.
  (b) Pillars follow the SP5 Framework diagram in Part 1 of the book.
  Applied 2026-11-08: purpose-driven-architecture (Two sides of VCF); pillar tag now availability, performance, compliance, capacity, cost (tags.yaml, 44 files); pillars-of-operations renamed sp5-framework.

### Q089 · Part 1 > Observability > Alert · Importance of alerts and the colours

- Files: [Alerts, symptoms and insights: why alert-driven operations stay reactive](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/alerts-and-insights.md) (sections Alert vs insight, Criticality).
- Search 1: "Hopefully not important issue"
- Search 2: "Urgent and important. However, it does not always mean you must drop everything you do and start firefighting in seconds."
- Search 3: "Symptom. Non urgent. Leading Indicators. Symptoms. Could be important, could also be false positive"
- Question:
  - (a) The alert vs insight table says alerts are hopefully not important and insights are important. The colour table says red alerts are urgent and important, and the diagram calls yellow low importance while the table says it could be important. Which wording should the knowledge base keep?
  - (b) Red: attend within 1-2 hours (table) vs review it today, the sooner the better (legend image). Keep 1-2 hours?
  - (c) Do the KPI colour bands (green, yellow, orange, red in the VCF Operations KPIs) carry the same response times: yellow next business day, orange today, red within 1-2 hours?
- Written as now: alerts urgent; red urgent and important, 1-2 hours; yellow possibly important or a false positive; (c) not stated.
- Answer: (a) Alerts should be minimized to issues that you cannot avoid, as each alert is reactive. When you react, you lose as time has started. So you hope that the alerts are not important. It's common for Enterprise IT to experience alerts storm and alerts fatigue. The root cause is the alerts are never defined properly. Red = urgent + important. Orange = urgent + not important. Yellow = not urgent, hence removed from the alerts definition and dealt as insights as part of proactive Health Check. Do this at the start of the day, or the start of your shift.
  (b) Red = ASAP, max within 1-2 hours. Orange = by end of day, do not differ until tomorrow. Any issue that can be deferred until tomorrow is not urgent. They are best dealt as a group as insight, so you can see the big picture.
  (c) No. The color in alert has a timeline as alert is reactive by nature. Time has started. The color in KPI is for proactive. They are not related.
  Applied 2026-11-08: alerts-and-insights (Alert vs insight, Criticality, Traps). (a) Alerts should be minimized to issues that you cannot avoid, as each alert is reactive. When you react, you lose as time has started. So you hope that the alerts are not important. It's common for Enterprise IT to experience alerts storm and alerts fatigue. The root cause is the alerts are never defined properly. Red = urgent + important. Orange = urgent + not important. Yellow = not urgent, hence removed from the alerts definition and dealt as insights as part of proactive Health Check. Do this at the start of the day, or the start of your shift.
  (b) Red = ASAP, max within 1-2 hours. Orange = by end of day, do not differ until tomorrow. Any issue that can be deferred until tomorrow is not urgent. They are best dealt as a group as insight, so you can see the big picture.
  (c) No. The color in alert has a timeline as alert is reactive by nature. Time has started. The color in KPI is for proactive. They are not related.
  Applied 2026-11-08: alerts-and-insights (Alert vs insight, Criticality, Traps).

### Q112 · Part 1 > Configuration Management > Review List · Facts to update for VCF 9.1

- Files: [Cluster configuration review: HA, DRS, DPM and cluster variants](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/configuration/cluster-configuration-review.md) (section DRS); [Storage configuration review: datastores, LUNs, NFS, arrays, queue depth](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/configuration/storage-configuration-review.md); [VM configuration review: VMware Tools, hardware, compute and storage settings](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/configuration/vm-configuration-review.md) (sections Storage, VMware Tools).
- Search 1: "Since DRS calculates every five minutes" (DRS runs every minute since vSphere 7; [DRS migration levels](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/configuration/drs-migration-levels.md)).
- Search 2: "Is the usage following design best practice?" (vVols; deprecated in VCF 9.0, Broadcom KB 401070; Protection and Recovery 9.1 is its last release with vVols).
- Search 3: "Ensure that the snapshot is removed within one day" (the SP5 Process daily SOP says older than about 3 days).
- Search 4: "refer to KB 340" (VMware Tools benefits; KB number under Broadcom to confirm).
- Question: confirm (1) every minute; (2) keep vVol checks for existing estates, with the deprecation stated; (3) one day or three days; (4) the KB number.
- Written as now: every minute; vVols deprecated; one day in the VM review; KB 340 as cited.
- Answer: 1. Every minute 2. Yes 3. One day 4. Article 315382
- Applied 2026-11-08: vm-configuration-review (KB 315382, snapshot one day), proactive-operations (daily SOP: one day), review notes in the cluster and storage reviews.

### Q093 · Part 1 > Your Private Cloud · Book corrections for the next edition

- Files: none; the knowledge base already uses current names.
- Search 1: "something you can implement with the current version of Aria products" (now VCF Operations).
- Search 2: "Salesforce, VMware Skyline, Microsoft Office 365" (Skyline status under Broadcom to check).
- Search 3: "Typically, Windows 10 + End-User applications" (Windows 10 support ended October 2025).
- Search 4: "VMware Horizon Cloud, Microsoft Windows Cloud are cloud examples" (Horizon is now Omnissa; Microsoft's product is Windows 365).
- Search 5: "This is not so obvious as it’s the only product in this category." (Nutanix Cloud Platform and Azure Local are in the same category.)
- Search 6: "The creates a bigger problem" (typo: This).
- Question: confirm each for the next edition; (5) is a claim the knowledge base does not repeat.
- Written as now: not in the knowledge base.
- Answer (author, 2026-11-08, on Q107): the book edition does not matter to Agent E2; what matters is the knowledge. Closed without review: the knowledge base already holds the corrected facts and current names.

### Q107 · Part 1 > Your Private Cloud (Service Level Agreement to SP5 Framework: Process) · Book corrections for the next edition

- Files: none beyond those named; the knowledge base already uses the corrected wording.
- Search 1: "because it is charged at 200% more" (2x price is 100% more).
- Search 2: "It looks operationally visible" (viable).
- Search 3: "It took me years to vrealize the mistake"; "you vrealize that there are 3 sides of health" (realize, twice).
- Search 4: "Your ticket is also directly answered by Level 3" vs "Gold bypasses the first level help desk" (Level 2 in the service table).
- Search 5: "We covered both in-depth in Part 1 of the book" (this is Part 1).
- Search 6: "There are 3 techniques we can apply" (4 listed).
- Search 7: "Happy to discuss my documented analysis ." (stray space; the link target is missing).
- Search 8: "Buying 64 cores maximizes your vSphere license" (per-core licensing, Q099 d).
- Image text: "Aria Operations for Logs" in the Not Healthy diagram (now VCF Operations for logs); the RCA screenshot is VMware Log Insight from 2016.
- Search 9: "Since storage IO control configuration is not based on latency" (Storage I/O Control deprecated in VCF 9, Q080).
- Question: confirm each for the next edition.
- Written as now: corrected wording in the knowledge base.

### Q113 · Part 1 > Configuration Management · Book corrections for the next edition

- Files: none beyond those named; the knowledge base uses the corrected wording.
- Search 1: "You can categorizes check into 4" (two bullets follow; the four are value, consistency, compatibility, variance).
- Search 2: "You have 1 ESXi host while providing higher redundancy" (you save 1 host: 21 vs 20).
- Search 3: "Is the HBA configured for high availability?" under Network Related (NIC, not HBA).
- Search 4: "both NSX Controller and Manager" (the controller is part of the NSX Manager cluster since NSX-T).
- Search 5: "Use Log Insight to parse Windows events" (now VCF Operations for logs).
- Search 6: "addiitonal", "combile", "issueing", "imaging both VMs" (typos).
- Question: confirm each for the next edition.
- Written as now: corrected wording.
- Answer (author, 2026-11-08, on Q107): the book edition does not matter to Agent E2; what matters is the knowledge. Closed without review: the knowledge base already holds the corrected facts and current names.

### Q104 · Part 1 > SP5 Framework > Troubleshoot; SP5 Framework: Process · Three orders of checks

- Files: [Monitoring vs troubleshooting, root cause analysis and validating a log alert](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/monitoring-vs-troubleshooting.md) (section Troubleshooting); [Proactive operations: dual track, daily cadence, NOC screens and the VM life cycle](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/proactive-operations.md) (section Dual track); [Users say the VM is slow: triage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/troubleshooting/vm-slow.md). Related: Q060.
- Search: image text only (not searchable): "4 possible areas. Check in this order: Contention, Configuration, Availability, Utilization"; reactive track "Configuration Issue? Availability Issue? Known Bugs? Consumption Issue?".
- Question: the Not Healthy diagram starts with contention; the reactive track starts with configuration and adds known bugs; the VM slow triage flow (draft) has no configuration or known-bug step. (a) Is the reactive track the order after a complaint, and Not Healthy the order after a health check? (b) Should vm-slow-triage add configuration (version incompatibility) and known bugs after contention?
- Written as now: each order in its file; vm-slow-triage unchanged.
- Answer: There is an overall daily health check runs each morning so VMware Admin can review. It should start with Availability then performance then security. Configuration issue can cause these 3 so they are checked as a drill down. Known bugs are typically caused by configuration issue, such as older version or incompatible settings. Contention is part of performance as it's the primary metric type for performance management. Performance flow such as VM slow triage should always check configuration.
  Reactive is after an alert, an incident (outage, breached), or human complain. Proactive focuses on insight, as system has not detected a known problem. Typically it's anomaly detection. While a monitoring system can detect anomaly mathematically it results in false positives as it lacks real world business context. What is abnormal can mean normal and vice versa.
- Applied 2026-11-08: monitoring-vs-troubleshooting (section Troubleshooting), proactive-operations (Dual track, Day-to-day order), vm-slow-triage (new step 5, Configuration), the three health checks (configuration step as drill-down), KNOWLEDGE-ENGINEERING.md section 10, both flow templates.

### Q083 · Part 1 > Noisy Neighbour > Network · Author's network limit and reservation

- Files: [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/noisy-neighbour.md) (section Network).
- Search 1: "I think it should be 8 Gb/s."
- Search 2: "consider setting 100 Mb/s per VM"
- Question: these are the only network numbers per VM. 8 Gb/s × 25 VMs = 200 Gb on a 40 Gb host: the limit stops one villain, not many at once. Is 8 Gb/s a cap for one VM's peak and 100 Mb/s a floor? Should they go in the capacity threshold file as rules?
- Written as now: in the text, not in the threshold files.
- Answer: book was wrong. I do not encourage both VM limit and VM reservation as it complicates operations, especially in dynamic and large scale environment.

### Q084 · Knowledge base · ESXi CPU Demand: sum of VMs or not

- Files: [knowledge/vsphere/foundations/provider-consumer.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/provider-consumer.md) (sections ESXi CPU Demand, Provider metric types); [knowledge/glossary.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/glossary.md) (Confusable pairs, ESXi CPU Demand vs Usage).
- Search (Part 3): "Not the sum of all VM worlds + VMkernel worlds"
- Question: found while checking this chapter. One file says ESXi CPU Demand is not a sum of consumers, with a trap. The same file, in Provider metric types, gives it as a sum-of-consumer example. The glossary says it is the sum over the VMs. Which is right? Claude will make the three agree.
- Written as now: contradictory.
- Answer: In my Part 1 book, it stated that "If a host has no VM, Demand will likely show flat 0. Usage will not show 0 as it includes the kernel" . It was followed by a screenshot. I can't figure out the image in the images directory so I added one called esxi-cpu-demand-usage-without-vm.png. If you have the same thing, ignore it.

### Q085 · Follow-up to Q070 · Does the hypervisor count a full VMXNET3 receive ring

- Files: [VM Network Packets Dropped](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/metrics/virtual-motherboard/packets-dropped.md) (sections Known causes, Traps).
- Search: not from the book. Broadcom KB 1010071 (Claude's own knowledge, not fetched): esxtop shows dropped receive packets at the virtual switch port when the guest does not empty its receive ring fast enough; the fix is a larger ring in the Guest OS.
- Question: your answer says the ring-buffer drop is not visible to the hypervisor. As Claude reads it, the guest never receives the packet, so the drop is counted at the VM's port: VM Network Receive Packets Dropped in vCenter, %DRPRX in esxtop. Visible to the hypervisor, but caused and fixed in the guest. Your conclusion holds either way: outside the IaaS SLA, and receive drops are already left out of it. Which is right for the reason: (a) not visible, or (b) visible but not controllable?
- Written as now: guest-os layer, outside the IaaS SLA; the visibility claim left out.
- Answer: (b), visible but not controllable. The author's document Packet Lifecycle and Metric Accounting in Virtualized Networks (2026-11-07): ESXi counts the drop at the dvPort and the VM (%DRPRX, net.droppedRx); VMXNET3 also shares it with the guest. Applied in [Packet drop accounting: which layer counts a dropped packet](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/concepts/packet-drop-accounting.md).

### Q081 · Part 1 > Noisy Neighbour > Network · Host pool or uplink pool

- Files: [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/noisy-neighbour.md) (section Network).
- Search 1: "Now, a single villain VM can hit 10 Gb."
- Search 2: "sustaining 5 Gb over 300 seconds period"
- Search 3: "The share should be larger for production VM network and development VM network."
- Question: (a) The calculation pools 2 × 25 Gb per host. With the default teaming (route based on originating virtual port) each vNIC uses one uplink. A 10 Gb villain fills 10 of one 25 Gb uplink and hurts only the VMs on that uplink. Compute per uplink? (b) The villain is 10 Gb in the calculation, 5 Gb sustained in the example: the 5-minute average hides the 10 Gb 20-second peak (the Interval rule)? (c) Read the share sentence as "larger for production VM traffic than development"?
- Written as now: per host, both figures, (c) as read.
- Answer: (a) Not per uplink, per group of uplinks assigned to the switch. With Load Based Teaming, the distributed switch tests the uplinks every 30 seconds, and if their load exceeds 75 percent of usage, the port ID of the virtual machine or vmkernel port with the highest I/O is moved to a different uplink. (b) my book was wrong. It should be sustaining 10 Gbps over 300 seconds period. (c) No. The main issue is the VM traffic is given a default share of 100 as a group, but each VMkernel traffic is given their own share. So the VM traffic is outnumbered. See the shares in this image https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/images/distributed-switch-network-share-allocation-by-traffic-type.png showing VM is 100 while VMkernel is up to 475 shares.

### Q082 · Part 1 > Noisy Neighbour > Memory and Solution · Gold 1:1 with memory tiering

- Files: [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/noisy-neighbour.md) (sections Memory, Avoiding it); [knowledge/vsphere/technology/memory/concepts/memory-tiering.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-tiering.md).
- Search 1: "Per-VM reservation becomes irrelevant when the entire cluster does not overcommit."
- Search 2: the table row Gold, overcommit "1 : 1", under "the following shows the SLA for memory"
- Question: vSphere 9 memory tiering adds NVMe memory beyond DRAM. For Gold 1:1: (a) is the ratio against DRAM only, so a Gold host has no tier, or against DRAM plus tier? (b) Does VM memory contention count time on pages in the NVMe tier? If not, Gold can read 0% while pages are in NVMe.
- Written as now: the book's table; no tiering note.
- Answer: (a) overcommit ratio for memory is only against DRAM portion only, because the whole point of adding an NVMe disk is to avoid overcommit. (b) I'm unsure if the memory latency or memory contention metric is modified to ignore it. I hope it should as NVMe is around 1000x slower, but logically the code that increments LAT_M may not be aware. I cannot confirm if the LAT_M polling logic was explicitly rewritten to inject tiering page faults into the latency aggregate. As a comparison, Linux and KVM do not explicitly report when a VM reads a page from NVMe instead of DIMM. No new KVM-specific counter was added, and existing KVM counters were not modified. vSphere introduces new counters in the vCenter UI for the NVMe tier:
  •	Memory type read bandwidth
  •	Memory type read latency
  •	Memory type write bandwidth
  •	Memory type write latency
  The consumed metric reflects the combined usage of both the DRAM and NVMe tiers. Because the VMkernel tiering algorithm explicitly tracks physical DRAM (Tier 0) and initiates migration to Tier 1 when Tier 0 consumption crosses the 80% threshold, total consumed memory can exceed the physical DRAM capacity once cold pages are migrated.

### Q065 · Part 1 > Performance Management > Utilization vs Demand · Absolute or relative performance

- Files: [Performance vs capacity: two readings of the same utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/performance-vs-capacity.md) (section Absolute vs relative); [KPI vs SLA: from complaint-based operations to a contract](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/kpi-vs-sla.md) (section KPI vs SLA, Reference).
- Search 1: "Performance will be absolute (real value), Capacity will be relative"
- Search 2: "It tends to be absolute, as it’s reporting raw metrics"
- Question: the book says performance is absolute. In chat you said relative cluster performance is more meaningful than absolute, because no perfect formula exists. Relative to what: (a) other clusters and the same cluster last week, (b) the class-of-service threshold (a score in %), (c) the share of VMs served well (a count, not milliseconds)? Which sentence should the knowledge base hold?
- Written as now: performance absolute, against total capacity; capacity relative, against usable capacity. The paradigm in your chat message is not written yet.
- Answer:
  (a). Performance is relative to other clusters, and relative to itself over time. Think of your stock market index like Nasdaq. The actual amount is basically irrelevant as it's just a combination of number. What you care is the relative movement.
  (b) Gold Class Cluster should relatively high higher performance (%) score , lower consumption (%) score, and lower risk (%) score versus Bronze Class Cluster.

Capacity is relative because it's relative to Usable Capacity, not Total Capacity. The real, actual, cluster utilization is lower in reality. But since it's divided over Usable Capacity instead of Total Capacity, the score becomes artificially higher.

### Q067 · Part 1 > Contention vs Consumption · Points A and B: 100% and queues

- Files: [Performance vs capacity: two readings of the same utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/performance-vs-capacity.md) (sections Contention vs consumption, Four points on the utilization scale).
- Search 1: "rarely happens here as utilization rarely exceeds 100% in real world"
- Search 2: "High utilization does not compromise performance, so long as there is no queue or contention"
- Question: (a) Point A: utilization cannot pass 100% of physical capacity; demand can. Write A as "demand above physical capacity", and add "utilization above physical capacity" to the Words to avoid table? (b) Point B: demand arrives in bursts. At 20-second resolution, a host at 100% CPU Usage almost always shows some VM Ready. Is 100% with 0 contention the best point for throughput (provider view), and acceptable for the VMs only while measured contention stays in the KPI? Or do you hold it as a target?
- Written as now: A worded as demand above physical capacity; B as the most work done.
- Answer:
  (a) Point A is above the physical capacity. Utilization cannot pass 100% of physical capacity as utilization measures reality; demand can exceed, as demand includes unmet demand. So there is no such thing as utilization above physical capacity as that's not possible.
  (b) The English word "target" implies something you have yet to achieve. You aim at a target before you hit it. Once the arrow hits the mark, you have achieved or hit the target. KPI is closer to Baseline / Standard Expectation: What you currently or consistently maintain as standard performance, albeit with great effort. In the ideal world, which is not realistic, your ESXi reaches 100% utilization while non VM experience contention. Provider and Consumer have their own KPI metrics.

### Q074 · Part 1 > KPIs in IaaS · How many SLAs per service; is there a Guest OS SLA

- Files: [KPI vs SLA: from complaint-based operations to a contract](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/kpi-vs-sla.md) (section KPIs in VM as a Service).
- Search 1: "There is only 1 SLA per service."
- Search 2: "What happens inside the Guest OS is not even relevant to the VM SLA."
- Search 3: heading "The 4 SLAs of IaaS"
- Question: (a) One SLA per service, while the earlier section gives 4 SLAs of IaaS and the layer table gives availability, performance and compliance per SLA. Read as one SLA contract per service, holding several SLA metrics? (b) The VM as a Service diagram shows a Guest OS SLA. The table says Guest OS metrics stay out of the IaaS SLA. Does a Guest OS SLA exist only when IT owns Guest OS sizing, and then as a separate SLA?
- Written as now: one SLA per service; Guest OS outside the IaaS SLA.
- Answer:
- (a): Read as one SLA contract per service, holding several SLA metrics
- (b): When central IT Department owns Guest OS, they should provide Guest OS SLA. It should have its own Availability SLA, Performance SLA and Security SLA. These values can be combined with the VM SLA to ease reporting and aggregation.
- Use the word Security SLA, not Compliance SLA. Security is more than Compliance. Compliance management is mostly about comparing settings against secured configuration. Security management covers activity, such as undesirable activity which is potentially a security risk.

### Q075 · Part 1 > KPI | SLA > Differences · KPI timing words

- Files: [KPI vs SLA: from complaint-based operations to a contract](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/kpi-vs-sla.md) (sections Three steps of maturity, KPI vs SLA).
- Search 1: "5-minute window. They are used as the starting point to troubleshoot"
- Search 2: "Based on day (e.g. last 1 hour), which is moving as time passes."
- Search 3: "Customers can track the SLA via self-service portal."
- Question: (a) The KPI is a 5-minute window with 20-second accuracy: computed every 5 minutes from 20-second peaks (Q048)? (b) "Based on day" means a moving window and "based on date" a calendar period? (c) The portal line is in the KPI step, where no SLA exists yet. Is it the KPI the customers track?
- Written as now: (a) and (b) as read; (c) written as "follow the numbers".
- Answer:
- (a) The KPI is a 5-minute window with 20-second accuracy: computed every 5 minutes from 20-second peaks? Yes.
- (b) KPI is based on day, not date. It's rolling continuously, like live operations. SLA is based on calendar date.
- (c) In the absence of SLA, yes, both application team and infrastructure team tracks KPI. SLA requires far more advanced cloud maturity model.

### Q076 · Part 1 > KPI step and Noisy Neighbour > Solution · How the SLA is computed; 99.99% at 5 minutes

- Files: [KPI vs SLA: from complaint-based operations to a contract](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/kpi-vs-sla.md); [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/noisy-neighbour.md) (memory class table); [knowledge/vcf-operations/kpis/cluster-sla-sli.md](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/knowledge/cluster-sla-sli.md).
- Search 1: "SLA = 1 month average of SLI of that specific month."
- Search 2: "VM contention is <1% for 99.99% of the time in the entire month"
- Question: (a) Is the SLA the mean of the SLI values, or the share of 5-minute intervals that pass the threshold? They differ: one bad hour at 50% contention averages out in a mean, but fails 12 intervals. (b) A 30-day month has 8,640 five-minute intervals. One failed interval gives 99.988%. So 99.99% allows 0 failures, the same count as Gold's 100%; only the threshold differs (0% vs below 1%). Did you mean 99.9% (8 intervals, 40 minutes)? (c) Bronze has no threshold. Give one?
- Written as now: the table as the book gives it.
- Answer:
- (a) the mean value. The SLI itself is already computed based on pass or fail. So each 5 minute a micro SLA is computed, leading to the final SLA number at the end of the calendar month. SLI = SLA Leading Indicator. It is not Service Level Indicator. That's a trap as people think SLI and SLA are peers as they sound similar.
- (b) the table was wrong. 100% is unrealistic practically. Cost will escalate.
- (c) Recommended threshold for Performance SLA: 99.9% gold, 99.8% silver and 99.6% bronze

### Q077 · Part 1 > Noisy Neighbour > CPU · Shares of a busy vCPU beside an idle one

- Files: [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/noisy-neighbour.md) (section CPU, Share); [knowledge/vsphere/foundations/resource-controls.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/resource-controls.md) (section Default CPU shares).
- Search: "the vCPU 1 of VM 2 does get 2x the share as it does not benefit from idleness of vCPU 2 of VM 2"
- Question: the sentence says both "does get 2x" and "does not benefit". As Claude reads the scheduler: default shares are set per vCPU (1,000 per vCPU at Normal; your screenshot shows 2,000 for a 2-vCPU VM). Under contention each vCPU is charged against its own part, and an idle sibling's part is not handed to the busy vCPU. So vCPU 1 of VM 2 gets the same as vCPU 1 of VM 1, not 2x. Is "does get" a typo for "does not get"? And "shares are per VM, not per vCPU": per VM in configuration, per vCPU in effect?
- Written as now: "the busy vCPU of a 2-vCPU VM does not gain from its idle sibling".
- Answer: that's a Level 400 trap. I think even VMware VCDX will fail for it. A larger VM has more overall CPU shares, the share is shareable among its vCPU. In the following example, the vCPU 1 of VM 2 does get 2x the share as it benefits from idleness of vCPU 2 of VM 2.

### Q078 · Part 1 > Noisy Neighbour > CPU and Disk · Two calculations

- Files: [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/noisy-neighbour.md) (sections CPU, Reservation; Disk, Limit).
- Search 1: "At 8:1 overcommit against physical thread, you cannot guarantee more than 0.25 CPU thread worth of resource"
- Search 2: "then it only takes 5% of the VM population (40 VM in this case) to saturate your storage"
- Question: (a) 8 vCPU per thread gives 0.125 thread per vCPU. 0.25 is right for 8:1 per core (4:1 per thread). Which basis? (b) 5% of 2,000 VMs is 100, not 40; at 1% each, 100 VMs reach 100% of the array. Was it meant as 40 VMs at 2.5% each, or 100?
- Written as now: (a) left out; (b) 100 VMs.
- Answer:
- (a) a core typically has dual threads due to Hyper Threading. I meant to say a 4:1 overcommit against physical thread.
- (b) 2.5% limit per VM, not 1%.

### Q079 · Part 1 > Solution > Maximum VM Size · Core or thread as the basis

- Files: [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/noisy-neighbour.md) (section Maximum VM size).
- Search 1: "Maximum size = ESXi logical CPU."
- Search 2: "if your ESXi has 48 cores total, then avoid doing 12 vCPU VM"
- Question: the example states overcommit per core ("1 core is assigned to 4 vCPU"); the size table per logical CPU (thread). Mixed: (a) 1:1 allows 96 vCPU on 48 cores and 96 threads, which alone is 2:1 per core; (b) 8:1 gives 0.125 × 96 = 12 vCPU, and the same row says avoid 12 on 48 cores, keep 4-6; (c) 4:1 gives 24 vCPU, called a whole socket, which is one socket's cores, not its threads. Should the table state overcommit and size per physical core? Then 1:1 → 48, 2:1 → 24 (19 with headroom), 4:1 → 12, 8:1 → 6.
- Written as now: the table as the book gives it, flagged.
- Answer: the book is wrong as the overcommit was based on core, not thread. It should be based on CPU physical thread. So 8:1 on a thread means 4:1 on the core if the core has dual threads.

### Q080 · Part 1 > Noisy Neighbour > Storage I/O Control · Deprecated in VCF 9

- Files: [Noisy neighbour: limit, reservation and share per resource](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/noisy-neighbour.md) (sections Disk, Storage I/O Control).
- Search: "SIOC provides 2 choices for congestion threshold"
- Source: vSphere 9.1 documentation, Manage Storage I/O Resources with vSphere (p. 1886): "With VCF 9.0, vSphere Storage I/O Control Components are deprecated." The datastore performance charts still list SIOC Normalized Latency and Aggregate IOPs.
- Question: (a) In 9.1, should the knowledge base mark SIOC as deprecated and keep only the per-disk limit and shares? Or does your field practice still enable it? (b) "There is no reservation for VM Disk." From vSphere 6.5, SIOC policy components also had an IOPS reservation, now deprecated with them (Claude's own knowledge). Keep the sentence as "none in the VM disk settings"?
- Written as now: SIOC as the book gives it; the deprecation in review notes only.
- Answer:
- (a) for product deprecation, follows the official manual as the book gets outdated. We can't practice what is officially deprecated.
- (b) Yes, keep as none. Do not include deprecated feature.

### Q066 · Part 1 > Contention vs Consumption · Point C: worst performance at 0% utilization

- Files: [Performance vs capacity: two readings of the same utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/performance-vs-capacity.md) (section Four points on the utilization scale).
- Search: "Worst performance actually happens when utilization = 0% as nothing gets done"
- Question: 0% utilization with 0 demand is an idle VM: no contention, nothing to serve. Only 0% with demand above 0 is bad: a VM frozen by a storage pause, as in your antivirus story. Is the rule "performance = demand served / demand", so that utilization alone cannot tell good from bad at either end?
- Written as now: "C, 0% while there is demand" (Claude's wording).
- Answer: Yes, utilization alone does not mean anything. 0% can be bad, 100% can be good. Hence my book said utilization is not something you manage. It's just an input, and one of the inputs to 2 things you care, which is performance and capacity. Utilization is used differently in capacity and performance.

### Q068 · Part 1 > Utilization vs Demand · Highest host utilization in cluster performance

- Files: [Performance vs capacity: two readings of the same utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/performance-vs-capacity.md) (section Cluster: performance vs capacity); [knowledge/vcf-operations/kpis/cluster-performance.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md).
- Search 1: "you want to take the highest among the host as your primary counter for cluster utilization"
- Search 2: "Utilization is for troubleshooting, not monitoring." (table image, Cluster Performance column)
- Question: for cluster performance, the same chapter says utilization is for troubleshooting only, and the cluster KPI holds only the contention of running VMs. Where does the highest-host utilization belong: (a) a performance monitoring metric, (b) the first troubleshooting drill-down after the cluster KPI drops, (c) a capacity-risk early warning?
- Written as now: both statements, unreconciled.
- Answer: highest-host utilization belong cluster risk score. See https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-risk.md and https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/formula/cluster-risk.png. I thought I gave you these 2 already?
- BTW, typically risk hits both capacity and performance, as capacity and performance are 2 sides of the same coin.
- I think you hallucinated here. I'm not able to find anything around "you want to take the highest among the host as your primary counter for cluster utilization" in the 2 files you refer. In future, cite something I can search.

On the file https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md. Why does vCommunity have to be part of the page title? What's the relevant to the local LLM?

### Q069 · Part 1 > Pattern Difference · Where the cliff starts

- Files: [Performance vs capacity: two readings of the same utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/performance-vs-capacity.md) (section Pattern difference).
- Search: "You can’t forecast performance using capacity"
- Question: the chart marks the drop at "Overcommit >1". The noisy-neighbour example runs 4:1 vCPU to core with no cliff. Is the cliff where demand passes supply on a host (demand overcommit), not where the allocation ratio passes 1? And since each host is its own pool, does it start on the hottest host, before the cluster average reaches 100%?
- Written as now: "falls steeply once demand passes what the hosts supply".
- Answer: Is the cliff where the allocation ratio passes 1. And since each host is its own pool, does it start on the hottest host, before the cluster average reaches 100%? Yes, although in theory DRS is supposed to balance all the hosts. There is no such thing demand overcommit as you can only overcommit the allocation. Demand, Usage, Utilization, are not something you can control.

### Q070 · Part 1 > IaaS Metric Types · Layer of the driver metrics

- Files: [Business, application and IaaS: layers, lost context and metric types](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/realms-and-layers.md) (section Consumer and provider metric types); [knowledge/vsphere/technology/network/metrics/virtual-motherboard/packets-dropped.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/metrics/virtual-motherboard/packets-dropped.md) (VMXNET3 buffer drops).
- Search: "One at the Windows/Linux layer, and one at the driver layer (e.g. PVSCSI, vmxnet)"
- Question: the book puts PVSCSI and vmxnet metrics in the Guest OS. The repository rule places a metric by the layer that produces it. The driver runs in the guest kernel, but it is VMware's virtual device. Is a VMXNET3 ring-buffer drop (a) guest-os layer, outside the IaaS SLA, or (b) virtual-motherboard layer, inside it? This decides the folder and who fixes it.
- Written as now: VMXNET3 drops sit in the VM (virtual-motherboard) file.
- Answer: VMXNET3 ring-buffer drop is a guest-os layer, outside the IaaS SLA as it's not visible to the hypervisor. You don't put SLA on something you cannot see, let alone control. The one covered by SLA is the vNIC as seen by the hypervisor.

### Q071 · Part 1 > The 3 Realms · One word, two meanings: realm

- Files: [Business, application and IaaS: layers, lost context and metric types](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/concepts/realms-and-layers.md); [knowledge/vsphere/foundations/vm-vs-guest-os.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/vm-vs-guest-os.md) (VM vs Guest OS: two realms); [knowledge/sp5-framework/performance/performance-kpi-design.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/performance-kpi-design.md) ("one per realm").
- Search: "In the big picture, there are 3 realms of IT in business"
- Question: Part 1 uses realm for business, application and IaaS. Part 3 and the knowledge base use realm for VM and Guest OS. One word per concept. Keep realm for the 3 of Part 1 and call VM and Guest OS layers? Or the reverse?
- Written as now: both meanings.
- Answer: realm in this case means world with a boundary. It's not an IT operations management jargon. So use for both.

### Q073 · Part 1 > KPI | SLA > Differences · One KPI or two for VM and Guest OS

- Files: [KPI vs SLA: from complaint-based operations to a contract](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/kpi-vs-sla.md) (section KPI vs SLA, Scope); [knowledge/sp5-framework/performance/performance-kpi-design.md](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/performance-kpi-design.md) (section Two KPIs, not one).
- Search 1: "they are 1 logical entity due to 1:1 permanent relationship, hence they are combined in 1 KPI number"
- Search 2 (Part 3): "VM Performance (%) and Guest OS Performance (%)"
- Question: Part 1 combines VM and Guest OS in one KPI. Part 3, the KPIs in VCF Operations and the Part 1 diagram (Guest OS KPI, VM KPI) keep two. Is Part 1's sentence older? The knowledge base would then state: two KPIs, one logical entity, read together.
- Written as now: both, flagged.
- Answer: Yes, Part 1 is outdated. In operations, we may refer to it at VM GOS KPI, using average of the 2 as from the perspective of application team, these 2 objects are the same thing.

### Q045 · Chapter 3 Memory > VM · Swapped formula in the vSphere 9.1 documentation

- Files: [VM Memory Swapped](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/swapped.md)
- Search: "This is why Swapped is not Swapped In – Swapped Out"
- Question: the vSphere 9.1 documentation (Virtual Machines > Memory (MB), p. 2103) defines VM Swapped = swapout – swapin, and adds that vMotion can make Swapped larger than swapout – swapin. Is the documentation wrong, or does its formula hold for cumulative counters (total swapped out minus total swapped in) while the book means the rates?
- Written as now: Swapped is not Swap in - Swap out: both run in parallel on different pages. Related to Q019 (host Swap Consumed).
- Answer: The vSphere 9.1 documentation is wrong. My book is correct. However, add  that vMotion can make Swapped larger than swapout – swapin if the VM comes with its memory already swapped.
  BTW, the page is 2105, not 2103.
- Done 2026-11-06: VM Memory Swapped: vMotion line added; documentation formula recorded as wrong.

### Q046 · Provider Objects > esxtop · HTQ and DTYP still in the 9.1 documentation

- Files: [esxtop CPU, power and interrupt counters](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/tools/esxtop/cpu.md), [esxtop network counters](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/tools/esxtop/network.md)
- Search 1: "The column HTQ is no longer shown in ESXi 7.0"
- Search 2: "does not seem to be available anymore"
- Question: the vSphere 9.1 documentation still lists HTQ (CPU panel) and DTYP (network panel). Do they show on an ESXi 9.1 host?
- Written as now: both described as no longer shown, per the book.
- Answer: both no longer shown. My book is correct. Add this as a mistake in the manual.
- Done 2026-11-06: esxtop CPU and network files state HTQ and DTYP are not shown on ESXi 9.1 and the documentation is out of date.

### Q047 · The World of Metrics > Resource management · Untouched memory reservation

- Files: [Resource controls: reservation, limit, shares, entitlement](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/resource-controls.md)
- Search: "since ESXi has reserved the space, it is not available to other VMs"
- Question: the vSphere 9.1 documentation (vSphere Resource Management > Virtual Machine Memory, pp. 1833-1834) says that until a VM has touched all memory within its reservation, the VMkernel can allocate the untouched part to other VMs; only touched reserved memory is kept, even when idle. Does the book statement mean admission control (the reservation cannot be promised to another VM), while the physical pages can still be used by others until touched?
- Written as now: Consumed jumps to the reservation at power-on; the reserved space is not available to other VMs. The existing correction says RAM is backed on first use, then stays locked.
- Answer: Consumed does not jump to the reservation at power-on. Until a VM has touched all memory within its reservation, the VMkernel can allocate the untouched part to other VMs; only touched reserved memory is kept, even when idle. Correct my book.
- Done 2026-11-06: Resource controls (table and corrections) and VM Memory Consumed: Consumed does not jump to the reservation; untouched reserved memory can go to other VMs.

### Q048 · Thresholds · Interval and instance reading of every band

- Files: band tables in [VM Performance (%) (VCF Operations KPI)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/kpis/vm-performance.md), [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md), [Cluster Consumption (%) (VCF Operations KPI)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-consumption.md), [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md), [Cluster SLA and SLI, archived 2026-11-11](https://github.com/e1-rahabok/agent-e2/blob/main/project/archive/knowledge/cluster-sla-sli.md), [Guest OS Performance (%) (VCF Operations KPI)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/metrics/guest-os-performance.md); rows in [knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml) and [thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml) (fields `interval`, `instance`).
- Search: not from the book. Follows the rule added to [Thresholds and interpretation](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/observability/thresholds.md) (Interval rule, Instance rule).
- Question: for each band row, which sample interval was it set on (20-second peak, 5-minute, 1-day), and which reading (worst instance, object aggregate, percentile of objects)? Most rows say "peak" or "worst" but not the interval; utilization rows say neither.
- Written as now: interval and instance stated only where the row name says it (for example "Peak CPU Ready among any vCPU"); Compressed + Swapped at 5 minutes and Memory Contention at 20 seconds (Q026).
- Answer: In VCF Operations, when the metric name has the word peak, that means it's reporting the highest 20-second-average within the 300-second reporting period. There are 15 data points within each 5 minute, each is a 20-second average. It's taking the highest among these 15 instance. The metrics at VM level are:
  Peak CPU Queue within collection cycle
  Peak CPU Context Switch within collection cycle
  Peak Guest OS Page-out Rate within collection cycle
  Peak Disk Queue within collection cycle
  Peak vCPU Ready within collection cycle
  Peak vCPU Co-Stop within collection cycle
  Peak Memory Contention within collection cycle
  Peak Latency within collection cycle
  Peak Usage Rate within collection cycle
  Peak Network Packets/sec within collection cycle
  Peak Transmitted Packet Dropped within collection cycle
  All the KPI and SLI are always by 5 minute. SLA is a lagging indicator, reported at the end of the month for the whole month. KPI, SLA, SLI are covered in Part 1 of my book. These are not vSphere metrics. They are VCF Operations metrics.
- Done 2026-11-06: intervals set in both threshold files (peak metrics 20s, other KPI and SLI rows 5m); peak and reporting periods added to the 20-second peak metrics file.

### Q049 · vCenter API counters · clusterServices.cpufairness and memfairness (low priority)

- Files: [knowledge/catalog/vcenter-api-counters.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/vcenter-api-counters.yaml) (HostSystem rows); no knowledge file yet.
- Search: not from the book. vCenter 9.1.0 API summaries: cpufairness "Fairness of distributed CPU resource allocation"; memfairness "Aggregate available memory resources of all the hosts within a cluster" (looks copied from another counter).
- Question: what do the two host counters measure, and are they worth documenting for operations?
- Written as now: listed in the catalog only, no knowledge file.
- Answer: not worth documenting. They are internal counter. The Cluster Risk (%) metric in https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/c1c954d0fb284bb813fded0aeb4ebd299897edd2/docs/reference/metrics/cluster-risk.md is more applicable to VMware admin.
- Closed 2026-11-06: not documented (internal counters).

### Q050 · vCenter API counters · clusterServices.effectivecpu and effectivemem vs totalmhz and totalmb (low priority)

- Files: [knowledge/catalog/vcenter-api-counters.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/vcenter-api-counters.yaml) (ClusterComputeResource rows); candidate: [Capacity model: total, usable, buffer, projection](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/supply.md).
- Search: not from the book. vCenter 9.1.0 API summaries: effectivecpu "Total available CPU resources of all hosts within a cluster"; effectivemem "Total amount of machine memory of all hosts in the cluster that is available for use for virtual machine memory and overhead".
- Question: Claude's own knowledge (the API's cluster summary) says effective capacity excludes hosts in maintenance mode or not responding, and virtualization overhead. Is that right, and should the knowledge base prefer it over totalmhz and totalmb for usable capacity?
- Written as now: listed in the catalog only.
- Answer: This is a good example of why jargon confuses people. In capacity, we have Total and Usable. Total is the raw and physical capacity. It typically does not change and remain static. Usable capacity  = Total - availability buffer - capacity buffer - overhead. I'm unsure if effective maps to total or usable. Anyway, this is low priority as there is no such word as Effective in the vCenter UI. The API is not fully documented, so focus on what the UI shows.
- Closed 2026-11-06: not documented (API only, not in the UI); Total vs Usable stays in the capacity model.

### Q051 · vCenter API counters · clusterServices.failover

- Files: [Admission control, expandable reservations and cluster state](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/admission-control-and-cluster-state.md).
- Search: not from the book. vCenter 9.1.0 API summary: "vSphere HA number of failures that can be tolerated".
- Question: how does the value behave under each HA admission control policy (slot, percentage of cluster resources, dedicated failover hosts, disabled)? Any trap in reading it?
- Written as now: the counter, its level and its summary; behaviour per policy left open.
- Answer: The trap comes when the hosts in the cluster is not identical. Regarding the counter, ignore it for now as it's low priority item.
- Done 2026-11-06: trap of non-identical hosts added to the admission control file; the counter itself left as low priority.

### Q052 · vCenter API counters · vmop counters: cumulative or per interval (low priority)

- Files: [Cluster VM operations event counts](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/metrics/vm-operations.md).
- Search: "Cumulative since the cluster was created"
- Question: vCenter stores the 20 vmop counters with rollup latest and stat type absolute, on the cluster and the datacenter. Your hypothesis: vCenter accumulates them while VCF Operations shows a rate. Confirm? Do the vCenter counts ever reset (vCenter restart, cluster re-creation)?
- Written as now: cumulative since cluster creation (book); VCF Operations converts them to rates (book).
- Answer: the counter is cumulative since the object creation. vCenter reset does not impact it. I'm unsure of re-creation but ignore it as we don't re-create cluster.
- Done 2026-11-06: VM operations counts are cumulative since object creation, not reset by a vCenter restart.

### Q057 · Benchmark · [Memory reservation vs CPU reservation](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-07-reservation-cpu-vs-memory.md): check with a vCenter CPU screenshot

- Files: [Memory reservation vs CPU reservation](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-07-reservation-cpu-vs-memory.md) (section Expected key points, CPU bullet); [Resource controls: reservation, limit, shares, entitlement](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/resource-controls.md) (section Reservation: CPU vs memory).
- Search: not from the book. The question comes from the book section The World of Metrics > Resource management (`source_path` of the question).
- Question: please validate the CPU key point with a screenshot of the vCenter UI: a VM with a 4 GHz CPU reservation, powered on and sitting at the BIOS screen. Do Run, Used, Demand and Usage stay at or near 0? The screenshot can then become the question's attachment (input type screenshot).
- Written as now: CPU reservation is on demand; the CPU counters stay at or near 0 while the VM sits at the BIOS screen.
- Answer: I was wrong. Memory is also on demand. So both are. I verified on a live vCenter.
- Done 2026-11-06: question L3-07 key and the resource controls file: memory reservation is also on demand.

### Q058 · Benchmark · Synthetic share and review of L4-14 to L4-49

- Files: https://github.com/e1-rahabok/agent-e2/tree/main/benchmark/questions (L4-14 to L4-49); [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md) (section 10, synthetic cap; section 12, status).
- Search: not from the book.
- Context: the Level 400 allocation (37 questions) is now drafted by Claude from the knowledge base. Synthetic questions are 63 of 90 (70%), against the cap of about 30% in section 10.
- Question:
  1. Keep the cap? If yes, which synthetic questions should be replaced by book, quiz or real-ticket questions, or should the cap rise?
  2. Review the 37: answer letters and key points per question (each `## Expected key points`), and the `## Input to supply` of the 24 awaiting-input questions (0066 to 0089).
  3. [Which VMs to reclaim memory from](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-39-memory-reclaim-from-300-vms.md), [Which datastores run out of space first](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-40-datastores-running-out-of-space.md), [Bad network packets: find the host and the cause](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-47-bad-packets-which-host.md), [Disk latency peak 40 times the average](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-48-disk-latency-peak-vs-average.md): the key names rows of the table you supply. Record the names in each question's Notes.
- Written as now: all 37 are `origin: synthetic`, status draft or awaiting-input; none counts until approved.
- Answer: no need to keep cap as I'm reviewing every question one by one. What is important is the allocation and distribution. The source (book versus Claude) is less important.
- Done 2026-11-06: synthetic cap removed from benchmark/design.md (sections 10 and 12).

### Q023 · Chapter 4 Storage > VM · Disk metric scope

- Files: [VM Disk (device level)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/virtual-motherboard/disk.md)
- Search: "if the value is per VM or per disk"
- Question: is the VM Disk (device-level) metric value for this VM only, or for the whole device shared by many VMs?
- Written as now: associated with the VM, flagged as unsure.
- Answer: it is for the VM, not the whole device or datastore.
- Done 2026-11-06: [VM Disk (device level)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/virtual-motherboard/disk.md), section Meaning, states the value is for the VM only.

### Q042 · Quiz > CPU > Q11 Reclamation · Option D, power off frees memory

- Files: [Reclaiming vCPUs from an idle VM](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-06-reclaiming-vcpus-from-an-idle-vm.md); [Why rightsizing matters for VMs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/rightsizing.md), [Unused and idle vCPUs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/idle-and-unused-vcpus.md), [Large VM with low utilization: build the case to downsize](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/decision-tree/oversized-vm-downsizing.md)
- Search (quiz): "Power off the VM, as this also frees the VM memory"
- Question: key is C,D. Frontier baseline chose C,D in 5 of 5; frontier classic chose C only in 5 of 5, citing that the knowledge base does not make the claim. Should the knowledge base state that powering off an idle VM frees its memory, as part of reclamation?
- Written as now: no file states that powering off an idle VM frees its memory. idle-and-unused-vcpus covers the CPU cost of idle vCPUs only.
- Answer: Yes, the knowledge base should state that powering off an idle VM frees its memory, as the consumed page tends to linger long after the VM has gone idle. The main reason is Windows and Linux tends to hold on to the memory. Powering off is a good best practice to claim this unused memory.
- Done 2026-11-06: [Why rightsizing matters for VMs](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/rightsizing.md), new section Idle VM: power it off, and a trap.

### Q043 · Quiz > Memory > Q2 VM vs Guest OS · Options A and D

- Files: [Relationship between VM and Guest OS memory metrics](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-13-relationship-between-vm-and-guest-os-memory-metrics.md); [Guest OS memory vs VM memory](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/guest-os-vs-vm-memory.md), [Ballooning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/ballooning.md), [VM Memory Usage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/usage.md)
- Search 1 (quiz): "Neither layer considers the other"
- Search 2 (quiz): "the hypervisor cannot balloon the VM"
- Question: key is A,B,D,E. Frontier dropped A or D in every run (baseline and agentic B,D,E; classic A,B,E). Are A and D both correct? If yes, which statements should the knowledge base add?
- Written as now: guest-os-vs-vm-memory says neither the VMkernel nor the Guest OS has full visibility into the other (close to A, but not "managed independently"). No file states that ballooning requires VMware Tools running (D).
- Answer: Yes, A and D are correct. The architecture of virtualization in ESXi means Guest OS cannot see the underlying memory. As a result, Windows and Linux completely operate its given memory as if they are on physical server hardware. Unlike a Type 2 hypervisor, which executes as software applications on top of a conventional host operating system, ESXi access the Guest OS via VMware Tools. This is the only channel for ESXi to issue a malloc() request to Windows or Linux. Without this request, ESXi is blind and can swap used memory.
- Done 2026-11-06: [Guest OS memory vs VM memory](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/guest-os-vs-vm-memory.md), section No mapping (A); [Ballooning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/ballooning.md), section Trigger and requirement and a trap (D).

### Q044 · Chapter 4 Storage > ESXi · Latency thresholds vs vSphere 9.1 documentation

- Files: [ESXi storage latency is high](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/troubleshooting/host-storage-latency.md), [vSphere documentation performance guidance](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/tools/vsphere-client/performance-guidance.md)
- Search 1: "the value should be within 0.5 ms"
- Search 2: "In a healthy environment, it should be well within 5 ms"
- Question: the vSphere 9.1 documentation (vSphere Monitoring and Performance > Solutions for Disk Performance Problems, p. 2121) says kernelLatency best 0-1 ms and a problem above 4 ms; deviceLatency above 15 ms indicates an array problem; queueLatency must be 0. Keep the book values as the knowledge-base thresholds, and the documentation values only as the vendor's published guidance?
- Written as now: diagnosis file uses the book values (KAVG 0.5 ms, DAVG well within 5 ms). The guidance file lists the documentation values, says the 15 ms value comes from spinning-disk arrays, and points to the book values.
- Answer: move all these threshold guidance from scattered over many files into a single small database, so it's quick for the Agent or Harness to check, and easy for human expert to review. You did create the database before. Where is it?
- Done 2026-11-06: all thresholds in one place, [knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml) and `thresholds-capacity.yaml` (YAML source, loaded into the harness catalog). The book values (KAVG 0.5 ms, DAVG within 5 ms) and the documentation values (kernelLatency above 4 ms, deviceLatency above 15 ms, queueLatency 0) are separate rows, each with its source.

### Q056 · Benchmark · Level of each existing question

- Files: the 28 files in https://github.com/e1-rahabok/agent-e2/tree/main/benchmark/questions (metadata `level`).
- Search: not from the book.
- Question: Claude assigned a draft level to each question (definitions: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 3.2). Which are wrong? None is at Level 100 or 200.
- Written as now:
  - [High CPU Wait](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-01-cpu-wait-includes-idle.md) (judged, text): 300
  - [CPU Latency without contention](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-01-cpu-latency-frequency.md) (judged, text): 400
  - [Hyper-Threading and two vantage points](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-02-hyperthreading-vm-vs-esxi.md) (judged, text): 400
  - [ESXi true utilization from Usage, Core Utilization and Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-03-esxi-true-utilization-from-usage-core-utilization-and-utilization.md) (deterministic, screenshot): 400
  - [Likely vCPU speed on a busy Hyper-Threaded cluster](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-04-likely-vcpu-speed-on-a-busy-hyper-threaded-cluster.md) (deterministic, text): 400
  - [ESXi CPU capacity: threads, not hertz](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-05-esxi-cpu-capacity-threads-not-hertz.md) (judged, screenshot): 400
  - [Reading an Intel Xeon specification: base, all-core Turbo, TDP](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-02-reading-an-intel-xeon-specification-base-all-core-turbo-tdp.md) (deterministic, screenshot): 300
  - [Which counter to size VM CPU](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-06-which-counter-to-size-vm-cpu.md) (deterministic, text): 400
  - [Counters where a vCPU cannot run at all](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-03-counters-where-a-vcpu-cannot-run-at-all.md) (deterministic, text): 300
  - [Guest OS run queue, context switch, Windows thread states](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-04-guest-os-run-queue-context-switch-windows-thread-states.md) (deterministic, text): 300
  - [CPU reservation behaviour](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-05-cpu-reservation-behaviour.md) (deterministic, text): 300
  - [Utilization 50% and Core Utilization 50%](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-07-utilization-50-and-core-utilization-50.md) (deterministic, text): 400
  - [Reclaiming vCPUs from an idle VM](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-06-reclaiming-vcpus-from-an-idle-vm.md) (deterministic, text): 300
  - [Memory reservation vs CPU reservation](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-07-reservation-cpu-vs-memory.md) (judged, text): 300
  - [VM availability](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-08-vm-availability.md) (judged, text): 300
  - [Provider vs consumer metrics](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-09-provider-consumer-ready-demand.md) (judged, text): 300
  - [What counts as overhead](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-10-overhead-classification.md) (judged, text): 300
  - [VM (virtual motherboard) vs Guest OS metrics](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-08-vm-is-a-virtual-motherboard.md) (deterministic, text): 400
  - [Performance vs capacity view of utilization](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-11-performance-vs-capacity-view-of-utilization.md) (deterministic, text): 300
  - [Memory usage: VM vs ESXi](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-09-usage-vm-vs-esxi.md) (judged, text): 400
  - [Which counter to size VM memory](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-12-which-counter-to-size-vm-memory.md) (deterministic, text): 300
  - [Relationship between VM and Guest OS memory metrics](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-13-relationship-between-vm-and-guest-os-memory-metrics.md) (deterministic, text): 300
  - [Actual vs potential memory contention](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-10-actual-vs-potential-memory-contention.md) (deterministic, text): 400
  - [Memory reservation behaviour](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-11-memory-reservation-behaviour.md) (deterministic, text): 300
  - [Balloon 0 while Swapped and Compressed are not 0](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-12-balloon-0-while-swapped-and-compressed-are-not-0.md) (deterministic, text): 400
  - [Guest queue invisible to the hypervisor](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-13-guest-queue-invisible.md) (judged, text): 400
  - [Setting a disk latency threshold](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-14-disk-latency-threshold.md) (judged, text): 400
  - [Latency and outstanding IO](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-15-latency-and-outstanding-io.md) (deterministic, text): 300
- Answer: Author (2026-11-05): reviewed all. [Memory reservation behaviour](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-11-memory-reservation-behaviour.md) is Level 400, not 300; [Setting a disk latency threshold](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-14-disk-latency-threshold.md) is Level 300, not 400. The others stand.
- Done 2026-11-05: both levels changed; the draft marks removed from all 28 questions.

### Q054 · Benchmark · Allocation of the 100 questions

- Files: https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md, sections 3.1 (tasks), 3.2 (levels), 3.3 (answer types), 3.4 (input types), 3.6 (allocation), 3.7 (coverage).
- Search: not from the book.
- Question: the blueprint is now top down. Are these shares right?
  - Tasks: read a metric 30, troubleshoot 25, decide capacity 20, explain a mechanism 15, judge a setting 10.
  - Levels: 100: 10, 200: 15, 300: 25, 400: 50.
  - Answer types: deterministic 70, judged 30.
  - Input types (questions that include them): text only 60, table at least 15, screenshot at least 25; at least 5 Level 400 questions with a table and a screenshot.
- Written as now: the shares above, as a proposal. Replaces the earlier 60 multiple choice, 20 screenshot, 20 conversation.
- Answer: Author (2026-11-05): agreed; replaces the old proposal.
- Done 2026-11-05: [benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), section 3.6 marked decided.

### Q041 · Quiz > CPU > Q8 Reservation · Options A and B

- Files: [CPU reservation behaviour](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-05-cpu-reservation-behaviour.md); [Resource controls: reservation, limit, shares, entitlement](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/resource-controls.md), [ESXi CPU Reserved Capacity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/reserved-capacity.md), [Overhead: classification, hypervisor overhead and CPU virtualization overhead](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/overhead.md)
- Search 1 (quiz): "Total reservation at ESXi level is capped at the base nominal clock speed"
- Search 2 (quiz): "CPU reservation only comes into play during contention"
- Question: key is A,B,C,D. Frontier classic chose C,D in 5 of 5 runs and rejected A and B. Are A and B correct? If yes, which statements should the knowledge base add?
- Written as now: reservation in MHz/Hertz (supports D); CPU reservation not sticky, memory reservation sticky (supports C). No file states the cap at base nominal clock speed (A) or that the reservation only matters under contention (B).
- Note (2026-11-05): the text written here was about case [ESXi true utilization from Usage, Core Utilization and Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-03-esxi-true-utilization-from-usage-core-utilization-and-utilization.md) (image links missing). Done: the case and the other two cases with attachments now have an `## Attachments` section with image links. Options A and B are still open.
- Answer: A and B are correct.
- The justification for A was already in the key itself. ESXi CPU has 3 frequency (base or nominal, all core turbo, and single core turbo). Only the base frequency is used by ESXi logic to guarantee a reservation. This is a conservative design.
- The justification for A was already in the key itself. It's written "if there is enough for everyone, reservation is irrelevant. Think of a restaurant. If there is enough seat, does your reservation matter if you do not reserve a specific table?"
- Done 2026-11-05: [Resource controls: reservation, limit, shares, entitlement](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/resource-controls.md) (section Reservation: CPU vs memory) and [ESXi CPU Reserved Capacity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/reserved-capacity.md) (Meaning, Traps). The second justification line is read as being about B.

### Q033 · MS Windows > CPU > Usage | Utilization | Time · VM CPU Run and Hyper-Threading

- Files: [Windows CPU scheduling and thread states](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/cpu/concepts/windows-cpu-scheduling.md), [VM CPU Run](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/run.md)
- Search 1 (MS Windows table): "Which VM counters can be used when you have no visibility into the Guest"
- Search 2 (Chapter 2, Run | Net Run): "counter not affected by CPU frequency scaling and hyper threading"
- Question: the MS Windows table marks VM CPU Run as Yes in the Hyperthreading column. Chapter 2 says Run is not affected by Hyper-Threading. Which is right?
- Written as now: the table as in the book, marked with the conflict; `run` keeps the Chapter 2 statement.
- Answer: Run and Net Run not affected by hyper threading
- Done 2026-11-05: [Windows CPU scheduling and thread states](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/cpu/concepts/windows-cpu-scheduling.md) table: Run and Net Run marked not affected by Hyper-Threading; Demand marked affected (Q035).

### Q038 · Auto Test > Prompt design · ONLY the knowledge base, or knowledge base first

- Files: [harness/modes.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/modes.py) (SYSTEM_KB, SYSTEM_AGENT); evidence in [benchmark/results/20261103-093742/report.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/results/20261103-093742/report.md), section Analysis.
- Search: not from the book. Finding from the frontier reference run 20261103-093742.
- Question: should the AI answer from the knowledge base only, or use the knowledge base first and its own knowledge where the knowledge base is silent?
- Written as now: prompt says answer using ONLY the knowledge base; if not covered, choose "Not covered by the knowledge base".
- Finding:
  - Frontier model: baseline (no knowledge base) 75%, classic 67%, agentic 67%.
  - The ONLY rule cost 3 questions where the knowledge base is silent: vendor-neutral-general-001 (5 of 5 to 0 of 5), [Reclaiming vCPUs from an idle VM](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-06-reclaiming-vcpus-from-an-idle-vm.md) (5 to 0), [Performance vs capacity view of utilization](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-11-performance-vs-capacity-view-of-utilization.md) (5 to 2).
  - The knowledge base cut the trap rate: 16% to 6-9%.
- Options:
  - Keep ONLY: fewer invented answers; no credit where the knowledge base is silent; every gap must be filled in the knowledge base.
  - Knowledge base first: knowledge base wins on conflict; own knowledge fills gaps; more coverage; more risk of invented answers.
  - Test both in one run and compare.
- Answer: In the auto test, we're testing 3 components as 1 expert (harness + model + knowledge base). So use the knowledge base first and its own knowledge where the knowledge base is silent.
- Done 2026-11-05: [harness/modes.py](https://github.com/e1-rahabok/agent-e2/blob/main/harness/modes.py) prompts: knowledge base first, it wins on conflict, own knowledge where it is silent and marked in the reason. The Not covered option is removed from the benchmark; docs updated ([benchmark/design.md](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/design.md), both benchmark READMEs, `ARCHITECTURE.md`).

### Q040 · Quiz > CPU > Q1 ESXi CPU Utilisation · Which counter is ESXi true utilization

- Files: [ESXi true utilization from Usage, Core Utilization and Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-03-esxi-true-utilization-from-usage-core-utilization-and-utilization.md); [ESXi CPU Core Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/core-utilization.md), [ESXi CPU Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/utilization.md), [ESXi CPU Usage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/usage.md)
- Search 1 (quiz): "It is a balanced reporting"
- Search 2 (quiz): "Plenty of physical threads are idle"
- Question: key is C (Utilization, 40%). All models, frontier included, chose B (Core Utilization, 70%), with and without the knowledge base. Is C right? If yes, which statement should the knowledge base add?
- Written as now: core-utilization says Core Utilization is a capacity metric (ignores frequency). utilization says Utilization suits capacity management. No file says which one is the ESXi true utilization, or why Core Utilization overstates it.
- Answer: I think you got triggered with the word "true". Change it to "Three metrics show three values. What is the ESXi utilization, from capacity management perspective? Hint: capacity is about space, while performance is about speed. Capacity is about quantity, performance is about quality". Review https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/utilization.md and https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/core-utilization.md and update accordingly.
- Done 2026-11-05: case [ESXi true utilization from Usage, Core Utilization and Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-03-esxi-true-utilization-from-usage-core-utilization-and-utilization.md) prompt and hint reworded as given; [ESXi CPU Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/utilization.md) (section The capacity reading, traps) and [ESXi CPU Core Utilization](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/core-utilization.md) (not the capacity reading; traps) updated.

### Q055 · Follow-ups to Q027 and Q029

- Files: [VM footprint sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/vm-footprint-sizing.md) (section CPU), [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/concepts/guest-os-sizing.md) (section Memory).
- Search: not from the book; from your answers to Q027 and Q029.
- Question 1 (Q027): the formula ends with "/ 20000 * vCPU". The sum over all vCPUs divided by 20,000 already gives the footprint in vCPUs (2 vCPUs each fully busy: 40,000 / 20,000 = 2). Is the result meant in vCPUs, so "× vCPU" is not needed, or in % of the VM, so the division is by (20,000 × vCPU)?
- Question 2 (Q029): option 2 has four ranges, 0-75, 75-85, 85-95, 95-100%. The image shows grey, green, yellow, orange and red. Is it grey (waste) below 75, green 75-85, yellow 85-95, red 95-100?
- Written as now: Q027 formula as you wrote it, with this question in review_notes. Q029 boundaries only, no colours.
- Answer to Q1: From my book, which you missed: "The System counter is not available per vCPU. Reason is the underlying physical core that does the IO work on behalf of the VM may be doing it for more than 1 vCPU. There is no way to break it down for each vCPU.". Because of this, I need to sum all the per-vCPU counters one by one, then add CPU System. After that, we divide by 20000 x vCPU. Is it clear?
- Answer to Q2: Grey is the 5th region. Only applicable to Capacity. It's not applicable to Performance as there is no such thing as wastage performance. Grey symbolizes wastage. It's placed below green. For Guest OS Memory, the range is 0 - 75 - 85 - 90 - 95 - 100. Yes, green is 10 point wide. Add in to do to upload Part 1 of my book to complete the capacity and performance management knowledge.
- Done 2026-11-05: [VM footprint sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/vm-footprint-sizing.md) (divisor 20,000 × vCPU, System reason, example); [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/concepts/guest-os-sizing.md) (ranges 75-85-90-95-100, grey below 75 for capacity only). To-do added: upload Part 1 of the book.

### Q027 · Consumer Objects > Capacity · VM CPU Needed formula

- Files: [VM footprint sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/vm-footprint-sizing.md)
- Search: "VM CPU Needed = (Used + Overlap + Co-stop + Ready + Other Wait) + System"
- Question: is the whole sum divided by 20,000, or only System? VM-level Used already includes System (Chapter 2 VM, Used formula). Is System counted twice?
- Written as now: formula copied as is, flagged.
- Answer: VM CPU Needed = (Sum of all vCPU (Used + Overlap + Co-stop + Ready + Other Wait) + System ) / 20000 * vCPU
  Emphasize that this is a narrow use case, as it's about the footprint of the VM on the underlying ESXi. This is only useful in VM migration to a different ESXi. What's more relevant in the Guest OS (Windows or Linux) capacity sizing.
- Done 2026-11-05: [VM footprint sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/capacity/vm-footprint-sizing.md) (formula grouping, narrow use case, pointer to Guest OS sizing). Follow-up on the unit of the result: Q055.

### Q028 · Consumer Objects > Capacity · Balloon in Guest OS memory sizing

- Files: [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/concepts/guest-os-sizing.md)
- Search: "Exclude balloon"
- Question: the text excludes balloon, but the sizing table marks Ballooned in blue (include) with "The memory was taken by Tools". Include or exclude?
- Written as now: exclude, flagged.
- Answer: include. It is hard to know if the page used by balloon was a free page or not.
  If it’s from free page, then exclude.
  If it’s from non-free page, then include.
  To be conservative, I recommend include.
- Done 2026-11-05: [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/concepts/guest-os-sizing.md), rule changed to Include balloon, with the reason.

### Q029 · Consumer Objects > Capacity · Memory utilization ranges

- Files: [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/concepts/guest-os-sizing.md)
- Search: "The company is wasting money if the utilization falls below 50%"
- Question: the text gives waste below 50% and risk above 75%, which matches bar 1. You recommend bar 2, where green starts near 75%. What are the ranges for bar 2?
- Written as now: bar 2 recommended, no numbers stated.
- Answer: I’d recommend 0 - 75% - 85% – 95% - 100% as Windows and Linux tend to cache memory.
- Done 2026-11-05: [Guest OS sizing](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/guest-os/system/concepts/guest-os-sizing.md), option 2 boundaries added. Follow-up on the colour of each range: Q055.

### Q030 · Provider Objects > Performance · vMotion in Cluster Performance (%)

- Files: [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md)
- Search 1: "vMotion is not included as it only becomes an issue"
- Search 2: "vMotion is included as it does impact the VM performance"
- Question: is vMotion part of the cluster KPI or not? The threshold table has no vMotion row.
- Written as now: vMotion described as a leading indicator, flagged.
- Answer: vMotion should not be included in actual performance as the metric counts the number of vmotion, not the length of the actual downtime. In a healthy environment, each vMotion down time is below 0.2 second and does not impact the Guest OS. Broadbase infrastructure capabilities like vMotion, NSX Edge, vSAN resync and general infrastructure (e.g. network) should be monitored separately. For example, track the maximum downtime for all vMotion across entire environment as a high downtime is a leading indicator of performance degradation.
- Done 2026-11-05: [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md), section vMotion is not part of the KPI; [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md), section Not used.

### Q031 · Provider Objects > Performance · Cluster KPI table vs text

- Files: [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md)
- Search 1: "Storage troubleshooting differs to compute troubleshooting" (disk latency listed as not used)
- Search 2: "That’s why it’s given 4x the threshold of zipped + swapped" (balloon thresholds)
- Search 3: "I did not set green = 0"
- Question: the table includes disk latency rows, has no balloon or swapped rows, and sets packet green to 0%. Is the table or the text current?
- Written as now: the table, with text reasons listed and the conflict flagged.
- Answer: both are outdated. The updated information is here https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/formula/cluster-performance.png and https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-performance.md Update the knowledge accordingly.
  Also, update Cluster Risk in the knowledge base from https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/formula/cluster-risk.png and https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-risk.md
- Done 2026-11-05: [Cluster Performance (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/kpis/cluster-performance.md) and [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md) rewritten from the adapter documentation (thresholds, calculation, DRAM-only memory, scoring, Excluded rows, known limitation, missing data); both threshold images replaced with the current tables; shared scoring rule updated in [Performance KPI design: VM Performance (%) and Guest OS Performance (%)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/sp5-framework/performance/performance-kpi-design.md).

### Q032 · Provider Objects > Other Metrics · Monster VM threshold

- Files: [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md), [vSphere cluster: operations complexity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/cluster-operations.md)
- Search 1 (Overview): "If a VM vCPU > 45% of the ESXi count of threads"
- Search 2 (Monster VM): "if a VM vCPU size is > 40% of the ESXi count of threads"
- Search 3 (Cluster Risk): "the VM size needs to be at least half the ESXi"
- Search 4 (recommendation): "Monster VM > 50% of physical core, not thread"
- Question: which CPU threshold defines a monster VM?
- Written as now: the recommendation (above 50% of physical cores); the others flagged.
- Answer: The final and up to date answer at https://github.com/e1-rahabok/VCF-vCommunity-Adapter/blob/main/docs/reference/metrics/cluster-risk.md#when-a-vm-is-a-monster  Update the
- Done 2026-11-05: [Cluster Risk (%) (vCommunity management pack KPI for VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/models/cluster-risk.md), section Monster VM; [vSphere cluster: operations complexity](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/cluster/concepts/cluster-operations.md) Monster VM row; [knowledge/catalog/thresholds-performance.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-performance.yaml) and [thresholds-capacity.yaml](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/catalog/thresholds-capacity.yaml) rows monster-vm-cpu and monster-vm-memory.

### Q024 · Chapter 5 Network > Architecture · VM and ingress

- Files: [Network layers and observability](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/concepts/network-observability.md)
- Search: "That’s why a VM does not have ingress traffic"
- Question: if moving further inside is ingress, traffic arriving at a VM looks like ingress. What does "a VM does not have ingress traffic" mean? That VM metrics use receive/transmit instead?
- Written as now: definitions only; the VM statement is flagged.
- Answer: Diagram is wrong. Correct answer is RX / TX (Receive / Transmit): L1/L2 hardware and driver domain. Used by physical interface cards (NICs), hypervisor VMkernel drivers, and DMA ring buffers. RX measures frame processing at the lowest stack layer regardless of protocol payload.
  Ingress / Egress: L3–L7 policy and control plane domain. Used by routing engines, distributed firewalls, and microsegmentation policies. Ingress evaluates stateful rule processing upon crossing a defined logical security or administrative boundary.
  Incoming / Outgoing: Operational telemetry domain. Used in application dashboards, capacity planning, and generalized monitoring to describe directional bandwidth utilization without mapping to a specific hardware driver or firewall rule.
  Here is a simple mermaid diagram. If you can add to the diagram, that's good.
  flowchart LR
  Traffic["Network → VM Interface<br/><b>(100 Packets / 150 KB)</b>"]

  subgraph AbstractionLayers ["Operational Abstraction Layers"]
  direction TB
  L1["<b>L1/L2 Driver Layer</b><br/>RX Count: 100<br/><i>(DMA Ring Buffer)</i>"]
  L2["<b>L3/L7 Policy Layer</b><br/>Ingress Count: 100<br/><i>(Stateful Firewall Rule)</i>"]
  L3["<b>Telemetry Layer</b><br/>Incoming Count: 100<br/><i>(Monitoring Dashboard)</i>"]
  end

  Traffic --> L1
  L1 --> L2
  L2 --> L3

### Q025 · Chapter 5 Network > VM · Dropped packet volume

- Files: [VM Network Packets Dropped](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/network/metrics/virtual-motherboard/packets-dropped.md)
- Search: "1 thousand packets dropped = 1500 MB worth of packets within 300 seconds"
- Question: 1,000 × 1.5 KB = 1.5 MB. Should it be 1 million packets = 1,500 MB, or 1,000 packets = 1.5 MB?
- Written as now: flagged, no number stated.
- Answer: 1.5 MB. Book was wrong.

### Q026 · Consumer Objects > Performance · Compressed + Swapped threshold

- Files: [VM Performance (%) (VCF Operations KPI)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/object-types/vm/kpis/vm-performance.md)
- Search: "their threshold is 2x of memory contention"
- Question: the table gives Compressed + Swapped green at 0-0.25%, half of Memory Contention (0-0.5%), not 2x. Which is intended?
- Written as now: the table values, with the conflict flagged.
- Answer: Swapped and Compressed are combined as they are the result of the same action. Together they tell the complete picture. As they may not indicate actual problem, their threshold is higher. However, since we measure at 5 minute sample, while memory contention is measured at 20 second, I adjust the threshold.

### Q019 · Chapter 3 Memory > ESXi · Swap Consumed formula

- Files: [ESXi Memory Swap Used](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/host/swap-used.md)
- Search 1 (ESXi): "I think this is swapped out – swapped in"
- Search 2 (VM): "This is why Swapped is not Swapped In – Swapped Out"
- Question: is host Swap Consumed equal to swapped out minus swapped in?
- Written as now: both statements, flagged.
- Answer: Search 1 is wrong. Search 2 is correct.

### Q021 · Chapter 3 Memory > ESXi · Utilization formula

- Files: [ESXi Memory Utilization (VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/host/utilization.md)
- Search 1: "the sum of running VM Utilization metrics + the kernel reservation"
- Search 2: "Utilization. Machine Demand + ESX System Usage"
- Question: is the kernel part the kernel reservation or ESX System Usage? Are they the same thing?
- Written as now: both forms, flagged. Note: Provider Objects > Capacity says "Memory \\ ESX System Usage (KB)" is the kernel reservation (legacy name). If so, the two forms agree; please confirm.
- Answer: They are the same thing. See my book for Reservation. The metric name is Memory \ ESX System Usage (KB). It is a raw counter from vCenter. Just in case you’re wondering, the name ESX System Usage is a legacy name.

### Q022 · Chapter 4 Storage > Architecture · IP storage read and network direction

- Files: [VM Disk Latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/metrics/virtual-motherboard/disk-latency.md)
- Search: "Read and Write are both mapped to Transmit counter"
- Question: for a read, the data returns to ESXi as received traffic. Do reads show mostly as Receive (data) with only the command on Transmit?
- Written as now: both map to Transmit, as in the book.
- Answer: book was wrong. Answer is If you are using IP storage, take note that Read and Write in storage do not map 1:1 to Transmit (Tx) and Receive (Rx) in Networking metrics. This depends on the storage block size (normally 4K or 8K), network packet size (ideally 9000 MTU), and TCP/IP handshakes packets. Get detail from https://docs.google.com/document/d/1E7Or6rsJZ_P1MUZZfL1X3RSXPxhR2lW2fSp3wcaqnGo/edit?usp=sharing and add it accordingly.
- Done 2026-11-04: [IP storage: storage counters vs network counters](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/storage/concepts/ip-storage-network-accounting.md) (from the linked note); disk-latency corrected, with a `corrections` entry until the book is updated.

### Q039 · Auto Test > Golden case vendor-neutral-general-001 · Hyperscaler cost not in the knowledge base

- Files: `benchmark/questions/vendor-neutral/general/general-001-hyperscaler-cost-of-1000-vms.md`
- Search: not from the book.
- Question: add hyperscaler cost content to the knowledge base, or score this case in baseline mode only?
- Written as now: the knowledge base has no cost content. In knowledge-base modes every model chose "Not covered" (frontier: 10 of 10 runs). Baseline frontier: correct 5 of 5.
- Answer: remove the case. Cost and price management is out of scope: the knowledge base is about performance troubleshooting (author, 2026-11-04). Case deleted; its id is not reused.

### Q001 · Chapter 2 CPU > VM · Linux Steal Time

- Files: [VM CPU Overlap](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/overlap.md), [VM CPU Latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/latency.md)
- Search 1 (Chapter 1): "Steal Time in Linux only includes CPU Ready"
- Search 2 (CPU > VM > Overlap): "Linux Guest OS tracks this as Stolen time"
- Question: does Linux Steal Time include Ready only, Overlap only, or both?
- Written as now: both statements, flagged.
- Answer: CPU Ready only. Because ESXi accounts for Overlap as active CPU Run time rather than wait time, it bypasses the hypervisor steal-time accumulator. The hypervisor does not report this interrupted time to the guest OS as stolen. The Linux OS Steal Time metric remains completely blind to vCPU Overlap. This ESXi accounting behavior necessitates the VCF Operations Net Run = Run - Overlap metric to determine actual execution time.

### Q002 · Chapter 2 CPU > VM · System charged to vCPU 0

- Files: [VM CPU System](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/system.md), [VM CPU Used](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/used.md)
- Search 1: "this is charged to the VM CPU 0"
- Search 2 (diagram text): "Charged at VM level, not at vCPU 1"
- Question: is System charged to vCPU 0 or to the VM level only? Chapter 1 says per-vCPU Used excludes System.
- Written as now: charged to vCPU 0, flagged.
- Answer: Charged at VM level, not vCPU 0 or 1. This results in Total VM cost > sum of all vCPU. This is not a problem for CPU scheduling. It’s just the way the kernel does the CPU accounting.

### Q003 · Chapter 2 CPU > VM · Run for sizing

- Files: [VM CPU Run](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/run.md), [Controlled test: VM and ESXi CPU metrics under Hyper-Threading](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/comparisons/vm-vs-esxi-ht-ramp-test.md)
- Search 1: "suitable as input to size the Guest OS and not the VM"
- Search 2: "This counter is suitable for VM Capacity sizing"
- Question: is Run for Guest OS sizing, VM sizing, or both?
- Written as now: both statements, flagged.
- Answer: Guest OS. I've updated my document.

### Q004 · Chapter 2 CPU > VM · Contention formula condition

- Files: [VM CPU Contention (VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/contention.md)
- Search: "Other Wait (if less than 1%)"
- Question: what does the condition mean?
- Written as now: formula copied as is.
- Answer: The condition of < 1% is added to ensure no false positive. See https://knowledge.broadcom.com/external/article/338438/increased-vmwait-for-idle-vms-after-upgr.html

### Q005 · Chapter 2 CPU > VM · Contention and limit

- Files: [VM CPU Contention (VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/contention.md), [VM CPU Latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/latency.md)
- Search 1: "Unlike CPU Ready, it does not account for Limit"
- Search 2: "Why does the counter include Ready by Limit?"
- Question: is the first statement about the pre-July-2024 Contention, which mapped to Latency?
- Written as now: yes, pre-July-2024 Contention excludes limit; current Contention includes it.
- Answer: This is VCF Operations counter, not vSphere. vSphere does not have counter. vSphere has CPU Latency, also known as %LAT_C in esxtop. The formula for CPU Contention changed in VCF Operations 8.18

### Q006 · Chapter 2 CPU > VM · Used above Run

- Files: [VM CPU Run and Used differ](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/troubleshooting/run-vs-used-gap.md)
- Search: "Why is Used consistently 41% higher than Run?"
- Question: how does Ready make Used higher than Run?
- Written as now: the book's answer (Ready), without explanation.
- Answer: Book was wrong. Answer is CPU frequency. The VM run at a higher clock speed due to turbo boost.

### Q007 · Chapter 2 CPU > VM · Ready and VM size

- Files: [VM CPU Ready](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/ready.md), [States of a VM vCPU](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/vcpu-states.md)
- Search 1 (VM): "CPU Ready tends to be higher, ceteris paribus, in larger VMs"
- Search 2 (Architecture): "You can reduce Co-stop by reducing the VM size"
- Question: does downsizing reduce Ready too, or only Co-stop?
- Written as now: both statements, flagged.
- Answer: It should reduce both, as the VM can be slot more easily. On the other than, having smaller share can increase CPU Ready.

### Q008 · Chapter 2 CPU > VM · Ramp test

- Files: [Controlled test: VM and ESXi CPU metrics under Hyper-Threading](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/comparisons/vm-vs-esxi-ht-ramp-test.md)
- Search: "ESXi CPU Core Utilization (%) matches VM Run. Both went 2x."
- Question: Core Utilization stayed at 100%. Should this read Utilization (%)?
- Written as now: Utilization (%).
- Answer: Correct. Make it clearer by using Thread Utilization instead of just Utilization.

### Q009 · Chapter 2 CPU > ESXi · Demand: provider or consumer

- Files: [ESXi CPU Demand](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/demand.md)
- Search 1: "Demand is consumer-view, while Usage is provider view"
- Search 2: "The value you see at ESXi is the summation of all the VMs"
- Question: your correction (2026-11-02) says ESXi Demand is a provider metric. Which holds?
- Written as now: both, flagged.
- Answer: The providers have 2 types of counters:
  •	Provider metric. This metric does not exist at consumer. For example, the physical network in ESXi.
  •	Sum of Consumer metric. This metric aggregates the metric of consumers. For example, the sum of VM network in the ESXi.

### Q010 · Chapter 2 CPU > ESXi · Usage cap

- Files: [ESXi CPU Usage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/usage.md)
- Search: "Usage no longer capped at 100% of total capacity at the nominal frequency"
- Question: your correction says capped at 100% (KB pending). Is the cap only in vCenter, removed in VCF Operations since Aria Operations 8.18?
- Written as now: vCenter capped; VCF Operations not capped since 8.18.
- Answer: Cap have been removed in both. Add the KBs https://knowledge.broadcom.com/external/article/417702/esxi-host-reporting-over-100-cpu-usage.html and https://knowledge.broadcom.com/external/article/431027/esxi-host-cpu-usage-appears-high-in-vcen.html

### Q011 · Chapter 2 CPU > ESXi · CPU Imbalance

- Files: [ESXi CPU Imbalance](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/host/imbalance.md)
- Search: "ESXi CPU Imbalance = Count of Running Threads / Count of Running Cores"
- Question: built-in VCF Operations metric, or your own?
- Written as now: product tagged vsphere and vcf-operations, flagged.
- Answer: my own metric, not built-in. Add reference to https://github.com/e1-rahabok/VCF-vCommunity-Adapter/tree/main/docs/reference/metrics

### Q012 · Chapter 3 Memory > Architecture · 3 levels

- Files: [Memory layers and page mapping](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-layers.md)
- Search: "ESXi uses 3 levels to manage memory"
- Question: the list after it has 4 items (TPS, Tiered Memory, Balloon, Compress/Swap). Which are the 3 levels?
- Written as now: 4 mechanisms listed, no level count.
- Answer: 4 level. Book corrected.

### Q013 · Chapter 3 Memory > Architecture · Balloon and unmet demand

- Files: [Memory layers and page mapping](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-layers.md), [VM Memory Ballooned](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/ballooned.md)
- Search: "The first sign of unmet demand"
- Question: the next sentences say ballooning does not mean ESXi is unable to meet demand. Is balloon a sign of memory pressure rather than unmet demand?
- Written as now: proactive, not unmet demand.
- Answer: The first sign of memory pressure, not unmet demand. It's a grey matter as memory management has gradient as ESXi applies 4 different layers.
- Applied 2026-11-03.

### Q014 · Chapter 3 Memory > VM · Limit and balloon

- Files: [VM Memory Ballooned](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/ballooned.md), [Ballooning](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/ballooning.md)
- Search 1: "Does limit result in Balloon?" (the book answers no)
- Search 2: "heavily ballooned as limit was imposed on it"
- Search 3: "Since the VM needed more, it experienced heavy ballooning"
- Search 4 (Memory > ESXi): "If you actually see balloon, that means there is limit imposed"
- Search 5 (Memory > ESXi): "It takes longer to realize, and is not affected by limit"
- Question: does a limit cause ballooning?
- Written as now: both, flagged.
- Answer: The answer is not directly. Why an in-between answer? Go back to the 4 layers of memory. They are at different level on memory management. Limit results in swapped or compressed is Consumed tries to grow beyond. Consumed grows because Guest OS uses more. These uses can come from balloon driver or other processes.

### Q015 · Chapter 3 Memory > VM · Memory Latency: space or time

- Files: [VM Memory Latency](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/latency.md), [Memory as storage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-as-storage.md)
- Search 1 (Architecture): "percentage of memory space"
- Search 2 (VM): "the amount of time a vCPU spends waiting on the completion of a page fault"
- Question: is Memory Latency a share of space or a share of time?
- Written as now: both definitions, flagged. vCenter description says time.
- Answer: Search 1 is wrong. Book updated. The correct answer is Search 2. Memory Latency, aka "Page-fault latency" is tracking the amount of time a vCPU spends waiting on the completion of a page fault. Its value is mostly swap wait, with a bit of page decompression / copy-on-write-break. The counter is called %LAT_M in esxtop. The latency metric is highly corelated with the swap-in rate.

### Q016 · Chapter 3 Memory > VM · Meaning of Compressed and Swapped

- Files: [VM Memory Swapped](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/swapped.md), [Memory layers and page mapping](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/concepts/memory-layers.md)
- Search 1 (VM): "indicates that the host is unable to satisfy the VM memory requirement"
- Search 2 (Architecture): "It does not mean VMs were contending for RAM"
- Question: which holds?
- Written as now: Architecture statement in the concept file; VM statement flagged.
- Answer: VM compressed happens when ESXi Consumed is very high or a particular VM hit its limit. That Consumed page of a VM can contain a lot of cache, so it does not always translate to VM hitting latency.

### Q017 · Chapter 3 Memory > VM · Sharing savings

- Files: [VM Memory Shared](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/shared.md), [VM Memory Consumed](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/consumed.md)
- Search: "Savings = 29.83 TB"
- Question: Consumed = Granted - Savings gives 23.7 TB of savings, not 6.13 TB. Which is right?
- Written as now: the book's calculation, flagged.
- Answer:

### Q018 · Chapter 3 Memory > VM · Utilization 5%

- Files: [VM Memory Utilization (VCF Operations)](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/memory/metrics/virtual-motherboard/utilization.md)
- Search: "We add 5% of Total, not Used"
- Question: where does the 5% enter the formula?
- Written as now: formula and the 5% statement, flagged.
- Answer:

### Q034 · Quiz > CPU > Q2 VM CPU Speed · 80% vs 62.5% Hyper-Threading charge

- Files: [Likely vCPU speed on a busy Hyper-Threaded cluster](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L4-04-likely-vcpu-speed-on-a-busy-hyper-threaded-cluster.md), [VM CPU Usage](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/usage.md), [VM CPU Used](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/used.md)
- Search 1 (quiz key): "3.0 (All Cores Turbo) x 80% (as HT delivers 1.25x total)"
- Search 2 (book): "37.5%"
- Question: the quiz key gives 3.0 GHz x 80% = 2.4 GHz. The knowledge base charges each thread 62.5% when both threads run, which gives 1.875 GHz. Which factor does VM CPU Usage apply?
- Written as now: case uses the key (2.4 GHz), flagged in Notes. KB unchanged.
- Answer: Author (2026-11-03): the key is correct (2.4 GHz). Added All-Core Turbo knowledge to [CPU frequency, Turbo and their impact on a VM](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/cpu-frequency.md).

### Q035 · Quiz > CPU > Q6 VM CPU Contention · Demand and Hyper-Threading

- Files: [Counters where a vCPU cannot run at all](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-03-counters-where-a-vcpu-cannot-run-at-all.md), [VM CPU Demand](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/demand.md)
- Search 1 (quiz key): "G is wrong as Demand is affected by hyper threading"
- Search 2 (book, MS Windows table): "| VM CPU Demand   | Yes               | No             | Yes           |"
- Question: the key says Demand is affected by Hyper-Threading. The MS Windows table marks Demand as not affected. Which is right?
- Written as now: case keeps the key's answer (G wrong); reason flagged.
- Answer: Author (2026-11-03): the key is correct. Guest OS and VM are 2 realms; the Guest OS does not see physical threads. Added to [VM vs Guest OS: two realms and their visibility layers](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/architecture/vm-vs-guest-os.md), [VM CPU Demand](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/metrics/virtual-motherboard/demand.md), [Guest OS CPU vs VM CPU](https://github.com/e1-rahabok/agent-e2/blob/main/knowledge/vsphere/technology/cpu/concepts/guest-os-vs-vm-cpu.md).

### Q036 · Quiz > CPU > Q7 Guest OS CPU · Is F correct?

- Files: [Guest OS run queue, context switch, Windows thread states](https://github.com/e1-rahabok/agent-e2/blob/main/benchmark/questions/L3-04-guest-os-run-queue-context-switch-windows-thread-states.md)
- Search 1 (quiz key): "F is correct. Windows has 8 states."
- Question: the answer column says D, E. The explanation says F is correct. Is the answer D, E, F?
- Written as now: scored as D, E, F until answered.
- Answer: Author (2026-11-03): F is correct. Answer D, E, F.

### Q037 · Quiz > Cost and Price > Q1 VM Cost · Missing explanations

- Files: `benchmark/questions/vendor-neutral/general/general-001-...`
- Search 1 (quiz key): "C is correct. The VM costs around US$ 2000 per year."
- Question: the key has empty explanations for A, B and D. What is the reason each is wrong? Which pricing date and source should the case record?
- Written as now: answer C only; no reasons for the others.
- Answer: Author (2026-11-03): tracked as a to-do in project/todo.md. Closed 2026-11-04: case removed (see Q039).
- None yet. Earlier resolved questions are recorded in each file's `review_notes`.
